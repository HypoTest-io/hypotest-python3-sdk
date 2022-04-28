from typing import Dict, Union
from datetime import datetime
import math
from . import pymmh3
from .config import ht_config
from .logger import logger
from .variant import Variant
from .utils import convert_user_visitor_to_str, put_event, datetime_format
from .retrieve_experiments import experiments, failed_retrieve_settings, retrieve_experiments

CONTROL = 'control'


def _get_variant(_experiment, user_id=None, visitor_id=None, override=None):
    err = None
    if override:
        return override, err, "local_override_"+override

    if user_id in _experiment.override_control or visitor_id in _experiment.override_control:
        return CONTROL, err, "remote_override_" + CONTROL
    if 'b' in list(_experiment.variants_distribution.keys()) and (user_id in _experiment.override_b or visitor_id in _experiment.override_b):
        return 'b', err, "remote_override_" + 'b'

    _MAGIC = 9300000028840
    _id = user_id
    if user_id and visitor_id:
        err = 'both user_id and visitor_id where sent'
    elif not _experiment.experiment_active:
        err = 'experiment is inactive'
    if visitor_id:
        _id = visitor_id
    _id += str(_MAGIC + _experiment.experiment_id)
    variant = (math.floor(((float(pymmh3.hash(_id, 1) & 0xFFFFFFFF)) / math.pow(2, 32)) * 10000)) / 10000
    total = 0

    variants_distribution = _experiment.variants_distribution
    if _experiment.experiment_state == 'calibration':
        variants_distribution = {CONTROL: 0.5, 'a': 0.5}

    for key, value in variants_distribution.items():
        total += value
        if variant <= total:
            return key, err, None

    return CONTROL, 'this code should be unreachable', None


def _send_visit_event_and_return_variant(chosen_variant, experiment_name=None, experiment_state=None, user_id=None,
                                         visitor_id=None, tags=None, override=None, err=None, report_event=True):
    event = {'time': datetime.strftime(datetime.utcnow(), datetime_format),
             'event_type': 'visit',
             'user_id': user_id,
             'visitor_id': visitor_id,
             'variant': chosen_variant}
    if experiment_name:
        event['test_name'] = experiment_name
    if tags:
        event['tags_name_value'] = tags
    if err:
        event['ht_sdk_error'] = err
    if report_event:
        put_event(event)

    result = Variant(chosen_variant)
    test_completed = err is not None and 'inactive' in err
    if experiment_state == 'calibration' and not override and not test_completed:
        result = Variant(CONTROL)
    if not ht_config.connect_to_server and override:
        result = Variant(override)

    return result


def _merge_tags(og_tags, new_tags):
    # safely merge to tags dicts
    og_tags = og_tags if og_tags else {}
    og_tags.update(new_tags)
    return og_tags


def experiment(experiment_name: str, user_id: str = None, visitor_id: str = None,
               tags: Dict[str, Union[str, int, float, bool, None]] = None, override: str = None, report_event=True):

    user_id, visitor_id = convert_user_visitor_to_str(user_id, visitor_id)

    if not ht_config.async_mode:
        retrieve_experiments()

    logger.debug({'msg': 'entering ab_experiment', 'user_id': user_id, 'visitor_id': visitor_id, 'tags': str(tags)})
    if not user_id and not visitor_id:
        logger.warning({'error': 'user_id or visitor_id must be sent'})
        return _send_visit_event_and_return_variant(CONTROL, experiment_name=experiment_name, tags=tags,
                                                    err='user_id or visitor_id must be sent', override=override,
                                                    report_event=report_event)
    _experiment = experiments.get(experiment_name)
    if not _experiment:
        if failed_retrieve_settings is None:
            error = 'did not retrieved the settings in time'
        elif not failed_retrieve_settings:
            error = '_xperiment not defined - fallback to control'
        else:
            error = 'retrieving the settings from server failed'
        logger.warning({'error': error})
        return _send_visit_event_and_return_variant(CONTROL, experiment_name=experiment_name,
                                                    user_id=user_id, visitor_id=visitor_id, tags=tags,
                                                    err=error, override=override, report_event=report_event)
    try:
        enter_experiment = eval(_experiment.condition_to_enter_experiment)
        if not isinstance(enter_experiment, bool):
            logger.warning({'error': 'condition_to_enter_experiment is invalid',
                            'condition': _experiment.condition_to_enter_experiment})
            return _send_visit_event_and_return_variant(CONTROL, experiment_name=experiment_name,
                                                        experiment_state=_experiment.experiment_state,
                                                        user_id=user_id, visitor_id=visitor_id, tags=tags,
                                                        err='condition_to_enter_experiment is invalid', override=override,
                                                        report_event=report_event)
        if not enter_experiment:
            logger.debug({'user will not enter experiment'})
            return Variant(CONTROL)

        selected_variant, err, override_reason = _get_variant(_experiment, user_id, visitor_id, override)
        if override_reason:
            tags = _merge_tags(tags, {'override_reason': override_reason})
        return _send_visit_event_and_return_variant(selected_variant, experiment_name=experiment_name,
                                                    experiment_state=_experiment.experiment_state,
                                                    user_id=user_id, visitor_id=visitor_id, tags=tags, err=err,
                                                    override=override, report_event=report_event)
    except Exception as e:
        logger.warning({"error": repr(e)})
        return _send_visit_event_and_return_variant(CONTROL, experiment_name=experiment_name, user_id=user_id,
                                                    experiment_state=_experiment.experiment_state,
                                                    visitor_id=visitor_id, tags=tags, err=str(e), override=override,
                                                    report_event=report_event)
