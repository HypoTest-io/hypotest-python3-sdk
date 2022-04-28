from queue import Queue, Empty
from .config import ht_config
from .logger import logger
from . import ht_connector

_q = Queue()


def events_sender_thread():
    while ht_config.async_mode:
        try:
            events = _q.get(timeout=ht_config.queue_timeout)
            if events == ['DONE']:
                break
            logger.debug({'msg': 'receiving events in thread', 'len': len(events)})
            ht_connector.report_events(events=events)
            _q.task_done()
        except Empty as e:
            # Queue is empty, we continue
            continue
        except Exception as e:
            pass
            logger.warning({'error': str(e), 'error_type': type(e), 'queue': _q})


def flush_events_in_queue():
    if ht_config.flush_events:
        # no logger at atexit
        _q.join()


def put_event_in_queue(event: dict):
    if ht_config.async_mode:
        _q.put([event])
    else:
        ht_connector.report_events(events=[event])
