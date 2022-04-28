import os
from copy import copy


class HtConfig:
    def __init__(self):
        self.address = 'https://sdk.hypotest.io'
        self.port = 443
        self.version = '1.0.0'
        self.sdk_type = 'python3'
        self.pull_interval = int(os.environ.get('HT_PULL_INTERVAL', 30))
        self.pull_jitter = int(os.environ.get('HT_PULL_JITTER', 5))
        # self.NUM_OF_EVENTS = 10
        self.max_retries = int(os.environ.get('HT_MAX_RETRIES', 3))
        self.connection_timeout = int(os.environ.get('HT_CONNECTION_TIMEOUT', 2))
        self.queue_timeout = int(os.environ.get('HT_QUEUE_TIMEOUT', 1))
        self.token = os.environ.get('HT_TOKEN', None)
        self.log_level = (os.environ.get('HT_LOG_LEVEL', 'INFO')).upper()
        self.flush_events = os.environ.get('HT_FLUSH_EVENTS', 'false').lower() == 'true'
        self.connect_to_server = (os.environ.get('HT_CONNECT_TO_SERVER', 'true')).lower() == 'true'
        self.async_mode = os.environ.get('HT_ASYNC_MODE', 'true').lower() == 'true'


ht_config = HtConfig()


def config(token: str = None, pull_interval: int = None, pull_jitter: int = None, max_retries: int = None,
           connection_timeout: int = None, queue_timeout: int = None, log_level: str = None, flush_events: bool = None,
           connect_to_server: bool = None):
    kwargs = copy(locals())
    for name, value in kwargs.items():
        if value is None:
            continue
        setattr(ht_config, name, value)
