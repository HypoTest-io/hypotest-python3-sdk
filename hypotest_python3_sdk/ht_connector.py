import json
from urllib3.util.retry import Retry
from urllib3.util import Timeout
from urllib3 import PoolManager

from .config import ht_config
from .logger import logger


class HypoJSONEncoder(json.JSONEncoder):
    # Your custom JSONEncoder subclass will override the default() method to serialize additional types.
    # https://pynative.com/make-python-class-json-serializable/
    def default(self, obj):
        try:
            return str(obj)
        except:
            return str(None)


retries = Retry(total=ht_config.max_retries, status=ht_config.max_retries, status_forcelist=[408, 504],
                backoff_factor=1, allowed_methods=False)
timeout = Timeout(total=ht_config.connection_timeout)

dummy_experiment = {'test_id': 1000000,
                    'test_name': 'dummy_test_name',
                    'experiment_hypothesis': 'dummy hypothesis',
                    'tag_names': ['user_id'],
                    'condition_to_enter_test': 'True',
                    'variants_distribution': {'control': 1.0},
                    'goal_names': [],
                    'test_state': 'calibration',
                    'test_active': True,
                    'override_control': [],
                    'override_b': []}
dummy_all_experiments = {'tests': {dummy_experiment['test_name']: dummy_experiment}}

http_pool = None


def _http_call(method, data_type, url, body=None):
    global http_pool
    if not ht_config.connect_to_server:
        return None

    if ht_config.token is None:
        logger.warning({'error': 'token is None'})
        return None

    if http_pool is None:
        http_pool = PoolManager(headers={'Authorization': "Bearer " + ht_config.token}, timeout=timeout)

    try:
        if not body:
            body = {}
        body = json.dumps(body, skipkeys=True, cls=HypoJSONEncoder).encode('utf-8')
        response = http_pool.request(method=method, url=url, body=body, retries=retries)
    except Exception as e:
        logger.warning({'error': e, 'error_description': ' general exception for ' + data_type, 'body': body})
        return None
    try:
        result = json.loads(response.data)
    except Exception as e:
        logger.warning({'error': str(e),
                        'error_description': 'failed to parse ' + data_type + ' response to valid json'})
        return None
    if response.status == 200:
        return result
    logger.warning({'error': result, 'error_description': 'failed for ' + data_type,
                    'status_code': response.status})
    return None


def get_all_experiments():
    url = ht_config.address + ':' + str(ht_config.port) + '/v1/all_series_tests'
    if ht_config.connect_to_server:
        all_experiments = _http_call(method='GET', data_type='settings', url=url)
    else:
        all_experiments = dummy_all_experiments
    if all_experiments is None:
        logger.warning({"error": "failed to get all series and tests, giving up"})
    else:
        all_experiments = all_experiments.get('tests')
    return all_experiments


def report_events(events):
    url = ht_config.address + ':' + str(ht_config.port) + '/v1/events'
    body = {'events': events}

    if ht_config.connect_to_server:
        response = _http_call(method='POST', data_type='events', url=url, body=body)
    else:
        response = 'not_None'
    if response is not None:
        logger.info({"msg": "sending events to server success", "len": str(len(events))})
    else:
        logger.warning({"error": "failed to send events, giving up", "len": str(len(events))})
    return response
