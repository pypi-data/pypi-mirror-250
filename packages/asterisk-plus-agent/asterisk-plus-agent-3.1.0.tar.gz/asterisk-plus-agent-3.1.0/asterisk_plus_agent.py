# TODO: Receive sentry SDK from billing. Re-activate Sentry on sentry_reload method

import asyncio
import base64
import subprocess
import functools
import json
import hashlib
import inspect
import ipaddress
import logging
import io
import os
import re
import time
import sys
from urllib.parse import urljoin
import uuid
import yaml
import aioboto3
from aio_odoorpc import AsyncOdooRPC
import httpx
from ipsetpy import ipset_list, ipset_create_set, ipset_add_entry
from ipsetpy import ipset_del_entry, ipset_test_entry, ipset_flush_set
from panoramisk import Manager, Message
import wave
import lameenc

__version__ = '3.1.0'

PRIVATE_NETWORKS = [
    ipaddress.ip_network('127.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('10.0.0.0/8')]

RE_IPSET_ENTRY = re.compile(
    r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?) '
    'timeout ([0-9]+) packets ([0-9]+) bytes ([0-9]+)( comment "(.+)")?$')


if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        traces_sample_rate=1.0)    


logger = logging.getLogger(__name__)


class AsteriskPlusAgent:
    manager = None
    odoo = None
    odoo_connected_event = asyncio.Event()
    ami_connected_event = asyncio.Event()
    # Dictionary to store channels for accounting
    current_channels = {}
    config = {}
    rpc_message_count = 0


############### SYSTEM #################################

    def __init__(self, config_path):
        self.config_path = config_path

    def get_source(self):
        script_path = inspect.getfile(inspect.currentframe())
        source_code = open(script_path, 'rb').read()
        data = base64.b64encode(source_code).decode()
        return data

    async def load_config(self):
        if not os.path.exists(self.config_path):
            raise Exception('Config file %s does not exist!' % self.config_path)
        with open(self.config_path) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
            if not self.config:
                raise Exception('Config file %s is empty or broken!' % self.config_path)
        r = None
        try:
            # Next load config from the billing            
            async with httpx.AsyncClient() as client:                
                r = await client.post(
                    urljoin(self.config['api_url'], 'app/asterisk_plus/config'),
                    json={
                        'source_code': self.get_source(),
                    },
                    headers={
                        'x-api-key': self.config['api_key'],
                        'x-instance-uid': self.config['instance_uid']})
                r.raise_for_status()
                agent_config = r.json()
                # Check versions
                major_version = float('.'.join(__version__.split('.')[:2]))
                if float(agent_config['asterisk_plus_version']) != major_version:
                    logger.error('Asterisk Plus module version is %s, but your Agent version is %s, upgrade the Agent!',
                        agent_config['asterisk_plus_version'], __version__)
                    sys.exit(1)
                # Finally overwrite with local values                
                self.config.update(agent_config)
                logger.debug(json.dumps(self.config, indent=2))
                logger.info('Config loaded.')
        except Exception as e:
            logger.error('Init config: %s', r and r.text or e)
            sys.exit(0)

    def install_security(self):
        # Create lists
        logger.info('Installing security...')
        config = {
            'security_banned_timeout': self.config.get('security_banned_timeout', '86400'),
            'security_authenticated_timeout': self.config.get('security_authenticated_timeout', '604800'),
            'security_expire_short_timeout': self.config.get('security_expire_short_timeout', '30'),
            'security_expire_long_timeout': self.config.get('security_expire_long_timeout', '86400'),
            'security_ports_tcp': self.config.get('security_ports_tcp', '5060,5061,5062,65060,65061,8088,8089,48088,48089'),
            'security_ports_udp': self.config.get('security_ports_udp', '5060,5061,5062,65060,65061,65062'),
            'iptables': self.config.get('security_iptables', 'iptables')
        }
        commands = """
            # Create ipsets
            ipset create -exist whitelist hash:net family inet hashsize 1024 maxelem 65536 counters comment
            ipset create -exist blacklist hash:net family inet hashsize 1024 maxelem 65536 counters comment
            ipset create -exist authenticated hash:ip family inet hashsize 1024 maxelem 65536 counters comment timeout "{security_authenticated_timeout}"
            ipset create -exist banned hash:ip family inet hashsize 1024 maxelem 65536 counters comment timeout "{security_banned_timeout}"
            ipset create -exist expire_short hash:ip family inet hashsize 1024 maxelem 65536 counters comment timeout "{security_expire_short_timeout}"
            ipset create -exist expire_long hash:ip family inet hashsize 1024 maxelem 65536 counters comment timeout "{security_expire_long_timeout}"
            # Clean existing rules
            {iptables} -D INPUT -p tcp -m multiport --dports "{security_ports_tcp}" -j voip 2> /dev/null
            {iptables} -D INPUT -p udp -m multiport --dports "{security_ports_udp}" -j voip 2> /dev/null
            {iptables} -F voip 2>/dev/null || {iptables} -N voip
            # Fill iptables with working rules
            {iptables} -I INPUT -p tcp -m multiport --dports "{security_ports_tcp}" -j voip
            {iptables} -I INPUT -p udp -m multiport --dports "{security_ports_udp}" -j voip
            {iptables} -A voip -m set --match-set whitelist src -j ACCEPT
            {iptables} -A voip -m set --match-set blacklist src -j DROP
            {iptables} -A voip -m set --match-set authenticated src -j ACCEPT
            {iptables} -A voip -m set --match-set banned src -j DROP
            {iptables} -A voip -m set --match-set expire_short src -j ACCEPT
            {iptables} -A voip -m set --match-set expire_long src -j DROP
            {iptables} -A voip -m string --string "VaxSIPUserAgent" --algo bm --to 65535 -j DROP
            {iptables} -A voip -m string --string "friendly-scanner" --algo bm --to 65535 -j DROP
            {iptables} -A voip -m string --string "sipvicious" --algo bm --to 65535 -j DROP
            {iptables} -A voip -m string --string "sipcli" --algo bm --to 65535 -j DROP
            {iptables} -A voip -j ACCEPT
        """.format(**config)
        result = subprocess.run(commands, shell=True, text=True, capture_output=True)
        if len(result.stdout) > 0:
            print(result.stdout)
        if len(result.stderr) > 0:        
            print(result.stderr)

    async def start(self):        
        # Install signal handlers
        try:
            await self.load_config()
        except Exception as e:
            logger.error(e)
            sys.exit(1)
        # Initialize security if enabled
        if self.config.get('security_enabled'):
            try:
                self.install_security()
            except Exception:
                logger.exception('Install security error')
        # Connect to Odoo.
        retry = 0
        while True:
            if await self.connect_odoo():
                # Start failed queries worker.
                # asyncio.ensure_future(self.failed_request_worker())
                break
            else:
                retry += 1
                if retry > 30:
                    retry = 1
                logger.info('Retry in %s seconds...', retry * 2)
                await asyncio.sleep(retry * 2)
        
    async def rpc_message_loop(self):
        try:
            await self.odoo_connected_event.wait()
            await self.ami_connected_event.wait()
            # Register event handlers
            self.register_event_map()
            # Initialize SQS
            session = aioboto3.Session(
                aws_access_key_id=self.config['aws_access_key'],
                aws_secret_access_key=self.config['aws_secret_access_key'])
            async with session.client('sqs', region_name='eu-central-1') as sqs_client:
                # Purge the Q
                try:
                    await sqs_client.purge_queue(QueueUrl=self.config['event_queue_url'])
                except Exception as e:
                    # Silently ignore.
                    pass
                while True:
                    logger.debug('Checking RPC queue...')
                    response = await sqs_client.receive_message(
                        QueueUrl=self.config['event_queue_url'],
                        MaxNumberOfMessages=1,
                        WaitTimeSeconds=20
                    )
                    messages = response.get('Messages', [])
                    if messages:
                        message = messages[0]
                        receipt_handle = message['ReceiptHandle']
                        await sqs_client.delete_message(
                            QueueUrl=self.config['event_queue_url'],
                            ReceiptHandle=receipt_handle
                        )
                        asyncio.ensure_future(self.rpc_message(message))
        except Exception as e:
            logger.exception('RPC Message error:')

    async def rpc_message(self, message):
        data = {}
        try:
            self.rpc_message_count += 1
            logger.debug('RPC message[%s]: %s', self.rpc_message_count, message['Body'])
            data = json.loads(message['Body'])
            # Replace . with _ and find the method
            method = getattr(self, data['fun'].replace('.', '_'), False)
            if not method:                
                raise Exception('Method %s not found' % data['fun'])
            args = data.get('args', [])
            if not isinstance(args, list):
                args = [args]
            kwargs = data.get('kwargs', {})
            if args and args != [None]:
                res = await method(*args, **kwargs)
            else:
                res = await method()
            # Deliver result
            if data.get('res_model') and data.get('res_method'):
                if data.get('pass_back'):
                    await self.odoo_execute(data['res_model'], data['res_method'], res, data['pass_back'])
                else:
                    await self.odoo_execute(data['res_model'], data['res_method'], res)
            # Notify with result
            if data.get('res_notify_uid'):
                await self.notify_user(str(res), data['res_notify_uid'],
                    data.get('res_notify_title'))
        except Exception as e:
            logger.exception('RPC Message error: %s', e)


    async def agent_reload_config(self):
        await self.load_config()
        await self.connect_odoo()

################### AMI ################################

    async def ami_start(self):
        try:
            manager = Manager(
                host=self.config['ami_host'],
                port=self.config['ami_port'],
                username=self.config['ami_user'],
                secret=self.config['ami_password'],
                ping_delay=10,  # Delay after start
                ping_interval=10,  # Periodically ping AMI (dead or alive)
                reconnect_timeout=2,  # Timeout reconnect if connection lost
            )
            manager.on_login = self.on_login
            manager.on_disconnect = self.on_disconnect
            self.manager = manager
            logger.info('Connecting to AMI at %s@%s:%s',
                self.config['ami_host'],
                self.config['ami_user'],
                self.config['ami_port']
            )
            return manager.connect(run_forever=False, on_shutdown=self.on_shutdown)
        except Exception:
            logger.exception('AMI start error: ')

    def on_login(self, mngr):        
        if not self.ami_connected_event.is_set():
            logger.info('AMI connected.')
            self.ami_connected_event.set()
        else:
            logger.info('AMI reconnected.')

    def register_event_map(self):
        # Odoo events
        evmap = set([k['name'] for k in self.config['events_map']])        
        for event in evmap:
            logger.info('Register AMI event: %s', event)
            self.manager.register_event(event, self.send_ami_event)
        # Security events
        if self.config.get('security_enabled'):
            self.manager.register_event('SuccessfulAuth', self.safe_handle_security_event)
            self.manager.register_event('ChallengeSent', self.safe_handle_security_event)
            self.manager.register_event('InvalidPassword', self.safe_handle_security_event)
            self.manager.register_event('InvalidAccountID', self.safe_handle_security_event)
            self.manager.register_event('ChallengeResponseFailed', self.safe_handle_security_event)
            logger.info('Register AMI event: SuccessfulAuth, ChallengeSent, InvalidPassword, InvalidAccountID, ChallengeResponseFailed')

    def safe_handle_security_event(self, manager, event):
        try:
            self.handle_security_event(manager, event)
        except subprocess.CalledProcessError as e:
            # Error will come from stdout.
            logger.error(e)
        except Exception:
            logger.exception('Handle security event error:')

    def handle_security_event(self, manager, event):
        try:
            addr = ipaddress.ip_address(event['RemoteAddress'].split('/')[2])
        except:
            logger.warning('Failed to get remote IP from {}'.format(event))
            return
        for net in PRIVATE_NETWORKS:
            if addr in net:
                if not event['Event'] == 'SuccessfulAuth':
                    # Skip successful local AMI connections.
                    logger.info('Ignore %s from %s: private network.', event['Event'], addr)
                return
        addr = str(addr)
        comm = ' '.join([event['Service'], event['Event'], event['AccountID']])
        if event['Event'] == 'SuccessfulAuth':
            logger.debug('Adding %s to authenticated & expire_long.', addr)
            subprocess.check_call(
                ['ipset', 'add', '-exist', 'authenticated', addr, 'comment',comm])
            subprocess.check_call(['ipset', 'del', '-exist', 'expire_long', addr])
        elif event['Event'] == 'ChallengeSent':
            logger.debug('Adding %s to expire_short & expire_long.', addr)
            subprocess.check_call(
                ['ipset', 'add', '-exist', 'expire_short', addr, 'comment', comm])
            subprocess.check_call(
                ['ipset', 'add', '-exist', 'expire_long', addr, 'comment', comm])
        elif event['Event'] in [
                'InvalidPassword', 'InvalidAccountID',
                'ChallengeResponseFailed']:
            logger.debug('Adding %s to banned & removing from expire_long.', addr)
            subprocess.check_call(
                ['ipset', 'add', '-exist', 'banned', addr, 'comment', comm])
            subprocess.check_call(
                ['ipset', 'del', '-exist', 'expire_long', addr])
            logger.info('Ban IP {} "{}"'.format(addr, comm))
        return True
        
    def on_disconnect(self, mngr, exc):
        logger.info(
            'AMI disconnect, error: %s', exc)

    async def on_shutdown(self, mngr):
        logger.info(
            'Shutdown AMI connection on %s:%s' % (mngr.config['host'], mngr.config['port'])
        )

    async def asterisk_manager_action(self, action, as_list=None):        
        logger.info('Received AMI action: %s', action['Action'])
        if not self.manager or not self.manager._connected:
            logger.error('AMI not connected. Dropping action.')
            return {}
        res = await self.manager.send_action(action, as_list=as_list)
        logger.debug('AMI reply: %s', res)
        if self.config.get('action_result_always_dict'):
            # Remove after all upgrade to 3.1.
            dict(res.items())
        elif isinstance(res, list):
            # Convert to dict
            return [dict(k.items()) for k in res]
        else:
            return dict(res.items())

    async def send_ami_event(self, manager, event):
        event = dict(event)
        if not event.get('Event'):
            return        
        handlers = [k for k in self.config['events_map'] if k['name'] == event.get('Event')]
        logger.debug('Handlers: %s', handlers)
        # Call handlers.
        for handler in handlers:
            try:                
                if handler.get('condition'):
                    # Handler has a condition so evaluate it first.
                    try:
                        # TODO: Create a more secure eval context?
                        res = eval(handler['condition'],
                                None, {'event': event})
                        if not res:
                            # The confition evaluated to False so do not send.                        
                            logger.debug('Handler %s evaluated to False', handler['id'])
                            continue
                    except Exception:
                        logger.exception(
                            'Error evaluating condition: %s, event: %s',
                            handler['condition'], event)
                        # The confition evaluated to error so do not send.
                        continue                
                # Sometimes it's required to send event to Odoo with a delay.
                if handler.get('delay'):
                    logger.debug('Handler %s sleep %s before send...', handler['id'], handler['delay'])
                    await asyncio.sleep(float(handler['delay']))
                else:
                    logger.debug('Delay for handler %s not set', handler['id'])
                await self.send_event(handler, event)
                logger.debug('Handler %s-%s has been published', handler['id'], handler['name'])
            except Exception:
                logger.exception('Handler %s-%s not handle event:', handler['id'], handler['name'])

    async def send_event(self, handler, event):
        if self.config['subscription_enabled'] != '1':
            logger.error('Ignoring event, subscription is not enabled.')
        try:
            logger.info('ID %s, event: %s, exten: %s', event.get('Uniqueid'), event.get('Event'), event.get('Exten'))
            res = await self.odoo_execute(handler['model'], handler['method'], event)
            logger.info('ID %s, Odoo response: %s', event.get('Uniqueid'), res)
        except Exception as e:
            if 'Access Denied' in str(e):
                logger.error('Odoo access error, please do not change billing password manually!')
            elif 'Expecting value: line 1 column 1 (char 0)' in str(e):
                logger.error('Cannot connect to Odoo, check if it is running.')
            else:
                logger.error('Send event error: %s', e)

    async def check_event(self, event):
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    urljoin(self.config['api_url'], 'app/asterisk_plus/event'),
                    headers={
                        'x-api-key': self.config['api_key'],
                        'x-instance-uid': self.config['instance_uid']
                    },
                    json={
                        'event': event['Event'],
                        'unique_id': event['Uniqueid']
                    }
                )
                r.raise_for_status()
                return True
        except Exception as e:
            logger.error(r.text)

    ###########################  ODOO CONNECTION ##############################
        
    async def connect_odoo(self):
        try:
            odoo_user = str(self.config['odoo_user'])
            password = str(self.config['odoo_password'])
            url = self.config['odoo_url']
            logger.info('Connecting to Odoo at %s', url)
            session = httpx.AsyncClient(base_url=url + '/jsonrpc', follow_redirects=True)
            self.odoo = AsyncOdooRPC(database=self.config['odoo_db'], username_or_uid=odoo_user ,
                                password=password, http_client=session)
            logged = await self.odoo.login()
            if not logged:
                logger.error('Cannot login. Check user and password.')
                return False
            logger.info('Connected to Odoo.')
            self.odoo_connected_event.set()
            return True
        except Exception as e:
            if 'Somehow the response id differs from the request id' in str(e):
                logger.error('HTTPS redirection issue, use 308 Permanent Redirect.')
            elif 'FATAL:  database' in str(e):
                logger.error('Database %s does not exist.', db)
            elif 'Expecting value: line 1 column 1 (char 0)' in str(e):
                logger.error('Cannot connect to Odoo, check if it is running.')
            else:
                logger.error('Odoo connect error: %s', e)

    async def odoo_execute(self, model, method, args, kwargs={}):
        logger.debug('Odoo Execute %s.%s(%s, %s)', model, method, args, kwargs)
        start = time.time()
        res = await self.odoo.execute_kw(
            model_name=model,
            method=method,
            args=args,
            kwargs=kwargs
        )
        req_time = time.time() - start
        if os.environ.get('ODOO_TRACE_RPC'):
            logger.info('Execute %s.%s took %.2f seconds.', model, method, req_time)
        return res
        
    async def failed_request_worker(self):
        REQUESTS_INTERVAL = 0.2 # Pause between sending failed requests.
        SLEEP_INTERVAL = 3 # Pause when Odoo is still down.
        MAX_FAILED_REQUESTS = 500 # Maximum requests in the deque.
        FAILED_REQUEST_EXPIRE = 300 # 5 minutes.
        self.failed_requests = deque(maxlen=MAX_FAILED_REQUESTS) # 100 requests maximum.
        while True:
            if len(self.failed_requests) == 0:
                await asyncio.sleep(1)
                continue
            # Take the oldest job.
            logger.info('%s requests in queue, processing...', len(self.failed_requests))
            data = self.failed_requests.popleft()
            failed_time = data.pop('failed_time')
            if time.time() - failed_time > FAILED_REQUEST_EXPIRE:
                # Remove outdated jobs and continue
                logger.info('Discarding expired request %s.%s', data['model'], data['method'])
                await asyncio.sleep(REQUESTS_INTERVAL)
                continue
            try:
                res = await self._odoo_execute(data)
                # Sleep a bit before the next request
                await asyncio.sleep(REQUESTS_INTERVAL)
            except Exception:
                # Move task back in the deck head.
                data['failed_time'] = failed_time
                self.failed_requests.insert(0, data)
                logger.info('Retry request %s.%s error, sleeping...', data['model'], data['method'])
                await asyncio.sleep(SLEEP_INTERVAL)

    async def notify_user(self, message, uid, title='PBX'):
        await self.odoo_execute(
            method='odoopbx_notify',
            model='asterisk_plus.settings',
            args=[message],
            kwargs={
                'title': title,
                'notify_uid': uid
            })

    async def test_ping(self):
        logger.info('Test ping received.')
        return True

    async def recording_get_file(self, file_path, file_format='wav', mp3_bitrate=96, mp3_quality=4):
        file_name = os.path.basename(file_path)
        try:
            res = {}
            mp3_conversion_done = False
            # Get Asterisk config
            if file_format == 'mp3':
                loop = asyncio.get_running_loop()
                mp3_data = await loop.run_in_executor(None, functools.partial(self.convert_to_mp3,
                    file_path,
                    mp3_bitrate,
                    mp3_quality))
                if mp3_data:
                    res['file_name'] = file_name.replace('.wav', '.mp3')
                    res['file_data'] = base64.b64encode(mp3_data).decode()
                    mp3_conversion_done = True
            if file_format == 'wav' or not mp3_conversion_done:
                # If we failed to get MP3 send wav anyway
                res['file_name'] = file_name
                res['file_data'] = base64.b64encode(open(file_path, 'rb').read()).decode()
            return res
        except Exception as e:
            logger.exception('Cannot get recording for %s:', file_path)
            return {'error': str(e)}

    def convert_to_mp3(self, file_path, bit_rate, quality):
        try:
            # Reduce priority.
            try:
                nice_level = int(os.environ.get('MP3_ENCODER_NICE', 10))
            except ValueError:
                logger.warning('Wrong MP3_ENCODER_NICE, defaulting to 10.')
                nice_level = 10
            os.nice(nice_level)
            file_data = open(file_path, 'rb')
            #io_data = io.BytesIO(file_data)
            started = time.time()
            wav_data = wave.open(file_data)
            num_channels = wav_data.getnchannels()
            sample_rate = wav_data.getframerate()
            num_frames = wav_data.getnframes()
            pcm_data = wav_data.readframes(num_frames)
            logger.debug(
                'Encoding Wave file. Number of channels: '
                '{}. Sample rate: {}, Number of frames: {}'.format(
                num_channels, sample_rate, num_frames))
            wav_data.close()
            encoder = lameenc.Encoder()
            encoder.set_bit_rate(bit_rate)
            encoder.set_in_sample_rate(sample_rate)
            encoder.set_channels(num_channels)
            encoder.set_quality(quality)  # 2-highest, 7-fastest
            mp3_data = encoder.encode(pcm_data)
            mp3_data += encoder.flush()
            file_name = os.path.basename(file_path)
            logger.info('Encoding of %s took %.2f seconds.', file_name, time.time() - started)
            return mp3_data
        except Exception as e:
            logger.exception('Convert MP3 error:')
            return ''
