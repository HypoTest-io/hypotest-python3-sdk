from .logger import logger
from .config import ht_config
from .send_events import put_event_in_queue


datetime_format = '%Y-%m-%d %H:%M:%S.%f'
_constant_tags = {'sdk_version': ht_config.version, 'sdk_type': ht_config.sdk_type}


def convert_user_visitor_to_str(user_id: str = None, visitor_id: str = None):
    try:
        if user_id is not None:
            user_id = str(user_id)
    except Exception as e:
        user_id = None
        logger.warning({"error": repr(e),
                        'error_description': 'an error occurred while converting user_id to str'})
    try:
        if visitor_id is not None:
            visitor_id = str(visitor_id)
    except Exception as e:
        visitor_id = None
        logger.warning({"error": repr(e),
                        'error_description': 'an error occurred while converting visitor_id to str'})
    return user_id, visitor_id


def put_event(event):
    # add constant tags
    tags_name_value = event.get('tags_name_value', {})
    tags_name_value.update(_constant_tags)
    if tags_name_value:
        event['tags_name_value'] = tags_name_value

    # clear null tags
    new_tags = {}
    for key, value in event.get('tags_name_value', {}).items():
        if value is not None:
            if not isinstance(value, str) or (isinstance(value, str) and 'null' != value.lower()):
                new_tags[key] = value
    if new_tags:
        event['tags_name_value'] = new_tags

    logger.debug({'msg': 'adding ' + event['event_type'] + ' event to thread queue', 'event': event})
    put_event_in_queue(event)

