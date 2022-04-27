import os


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

        # local
        self.address = os.environ.get('HT_DNS', 'http://0.0.0.0')
        self.port = int(os.environ.get('HT_PORT', 8001))
        self.log_level = (os.environ.get('HT_LOG_LEVEL', 'DEBUG')).upper()
        # self.connect_to_server = False
        # self.async_mode = False
        self.token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb21wYW55Ijoic21vcmUuY29tIiwiZXhwIjoxOTYwODIwOTI3LjMwOTg1NCwiZW52IjoicHJvZCJ9.C1YfyPDkKgJeajlrQbhjrrIIx1ZoRPJ1zumCndR7K_c'
        # self.token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb21wYW55Ijoic21vcmUuY29tIiwiZXhwIjoxOTYwODIxMDE0Ljk0MDU1ODIsImVudiI6InN0YWcifQ.yry8_QSRTrzz2-yeYhFS5Mwb6DDHr9JCSEcQgmclqfg'


ht_config = HtConfig()


def config(token: str = None, pull_interval: int = None, pull_jitter: int = None, max_retries: int = None,
           queue_timeout: int = None, flush_events: bool = None, connect_to_server: bool = None):
    kwargs = locals()
    for name, value in kwargs:
        if value is None:
            continue
        setattr(ht_config, name, value)
