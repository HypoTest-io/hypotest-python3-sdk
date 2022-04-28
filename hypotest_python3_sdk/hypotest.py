import atexit
from typing import Dict, Union
from datetime import datetime
from threading import Thread
from .config import ht_config
from .logger import logger
from .utils import convert_user_visitor_to_str, put_event, datetime_format
from .send_events import events_sender_thread, flush_events_in_queue
from .retrieve_experiments import retrieve_experiments_thread


def start_threads():
    if ht_config.async_mode:
        for thread_func in [events_sender_thread, retrieve_experiments_thread]:
            _thread = Thread(target=thread_func)
            _thread.daemon = True
            _thread.start()
        atexit.register(flush_events_in_queue)


start_threads()


def kpi_event(event_name: str, user_id=None, visitor_id=None, value=1.0,
              tags: Dict[str, Union[str, int, float, bool, None]] = None):

    user_id, visitor_id = convert_user_visitor_to_str(user_id, visitor_id)

    event = {'user_id': user_id,
             'visitor_id': visitor_id,
             'time': datetime.strftime(datetime.utcnow(), datetime_format),
             'event_type': 'goal',
             'goal_name': event_name,
             'goal_value': value}
    if tags:
        event['tags_name_value'] = tags
    if not user_id and not visitor_id:
        err_msg = 'goal was sent without user_id and visitor_id'
        logger.warning({'msg': err_msg})
        event['ht_sdk_error'] = 'goal was sent without user_id and visitor_id'
    put_event(event)


def match_user_visitor(user_id: str, visitor_id: str, context: str = None,
                       tags: Dict[str, Union[str, int, float, bool, None]] = None):
    user_id, visitor_id = convert_user_visitor_to_str(user_id, visitor_id)
    event = {'user_id': user_id,
             'visitor_id': visitor_id,
             'time': datetime.strftime(datetime.utcnow(), datetime_format),
             'event_type': 'match_user_visitor'}
    if context:
        event['context'] = context
    if tags:
        event['tags_name_value'] = tags
    put_event(event)
