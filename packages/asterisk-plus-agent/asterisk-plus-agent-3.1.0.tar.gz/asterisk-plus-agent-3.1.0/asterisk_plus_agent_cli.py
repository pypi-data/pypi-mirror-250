# TODO: Receive sentry SDK from billing. Re-activate Sentry on sentry_reload method

import asyncio
import base64
import subprocess
import click
import functools
import json
import inspect
import io
import logging
import logging.config
import os
import re
import time
import sys
from urllib.parse import urljoin
import uuid
import yaml
import aiorun
import httpx

if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        traces_sample_rate=1.0)    

LOG_CONFIG = """version: 1
formatters:
    default:
        format: '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'

handlers:
    console:
        class: logging.StreamHandler
        formatter: default
root:
    level: {}
    handlers: [console]    
""".format(os.environ.get('LOG_LEVEL', 'INFO').upper())

log_config = yaml.safe_load(LOG_CONFIG)
logging.config.dictConfig(log_config)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# Import agents after logger init.
try:
    from asterisk_plus_local_agent import AsteriskPlusLocalAgent as AsteriskPlusAgent
except ImportError:
    from asterisk_plus_agent import AsteriskPlusAgent


async def start(config):
    agent = AsteriskPlusAgent(config)
    asyncio.gather(        
        agent.start(),
        agent.rpc_message_loop(),
        agent.ami_start())
    

@click.group()
def main():
    pass


@main.command(help='Run the Agent')
@click.option('--config', default='/etc/asterisk_plus_agent.yaml', show_default=True)
def run(config):
    logging.info("Starting the application.")
    aiorun.run(start(config))


@main.command(help='Call a command.')
@click.argument('odoo_url')
@click.option('--config', default='/etc/asterisk_plus_agent.yaml', show_default=True)
@click.option('--skip-ami-setup', is_flag=True)
@click.option('--asterisk', default='/usr/sbin/asterisk', show_default=True)
def init(odoo_url, skip_ami_setup, asterisk, config):
    # First create AMI config
    agent_config = {}
    if not skip_ami_setup:
        agent_config.update(create_ami_config(asterisk))
    agent_config.update(load_config_from_odoo(odoo_url))
    # Save config
    open(config, 'w').write(yaml.dump(agent_config))
    logger.info('Agent configuration is placed at %s', config)    
    logger.info('Initialization complete. You can start the Agent now.')


def load_config_from_odoo(odoo_url):
    logger.info('Connecting to %s...', odoo_url)
    r = None
    try:
        r = httpx.get(urljoin(odoo_url, '/asterisk_plus/agent'))
        r.raise_for_status()
        data = json.loads(r.text)
        return data
    except Exception as e:
        logger.error('Initialize error: %s', r and r.text or e)
        sys.exit(1)

def create_ami_config(asterisk_executable):
    # Check if for manager.conf contains includes.
    if not os.path.exists('/etc/asterisk/manager.conf'):
        logger.error('/etc/asterisk/manager.conf not found. Do a manual setup and init with --skip-ami-setup option.')
        sys.exit(1)
    # Check for Asterisk executable    
    if not os.path.exists(asterisk_executable):
        logger.error('Asterisk executable %s not found, specify full path with --asterisk option.', asterisk_executable)
        sys.exit(0)
    # Check for include dirs
    if not os.path.isdir('/etc/asterisk/manager.conf.d'):
        logger.error('Directory /etc/asterisk/manager.conf.d not found, Do a manual setup and init with --skip-ami-setup option.')
    # Check AMI port
    re_ami_port = re.compile('^port = ([0-9]+)', re.MULTILINE)
    port_found = re_ami_port.search(open('/etc/asterisk/manager.conf').read())
    if not port_found:
        logger.warning('Cannot get port option from manager.conf, using default 5038!')
        ami_port = 5038
    else:
        ami_port = int(port_found.group(1))
    # Create a configuration and place it there.
    ami_password = str(uuid.uuid4())
    ami_config = """
[asterisk_plus_agent]
secret={}
timestampevents = yes
displayconnects = yes
read=call,dialplan
write=originate
deny=0.0.0.0/0.0.0.0
permit=127.0.0.0/255.0.0.0
allowmultiplelogin=no
""".format(ami_password)
    open('/etc/asterisk/manager.conf.d/asterisk_plus_agent.conf', 'w').write(ami_config)
    # Connect to Asterisk and apply
    try:
        res = subprocess.check_call('{} -rx "manager reload"'.format(asterisk_executable),
            shell=True)
    except Exception:
        logger.error('Cannot apply AMI configuration.')
        sys.exit(1)
    # Check that config is applied.
    try:
        res = subprocess.check_output('{} -rx "manager show user asterisk_plus_agent"'.format(asterisk_executable),
            shell=True, universal_newlines=True)
        if 'username: asterisk_plus_agent' not in str(res):
            logger.error('Asterisk does not see [asterisk_plus_agent] AMI account. Check that /etc/asterisk/manager.conf.d is included from /etc/asterisk/manager.conf!')
            sys.exit(0)
    except Exception:
        logger.error('Cannot apply AMI configuration.')
        sys.exit(1)
    # All is fine!
    logger.info('Asterisk Plus Agent AMI config placed in /etc/asterisk/manager.conf.d/asterisk_plus_agent.conf.')
    logger.info('Asterisk has been reloaded to apply this AMI account.')
    return {
        'ami_user': 'asterisk_plus_agent',
        'ami_password': ami_password,
        'ami_host': 'localhost',
        'ami_port': ami_port,
    }

if __name__ == '__main__':
    main()

