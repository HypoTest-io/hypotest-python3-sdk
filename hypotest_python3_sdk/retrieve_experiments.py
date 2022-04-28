import time
import random
from .experiment_settings import ExperimentSettings
from .config import ht_config
from .logger import logger
from . import ht_connector

failed_retrieve_settings = None
experiments = {}


def _fix_condition(condition, tag_names):
    for tag in tag_names:
        if tag in ['user_id', 'visitor_id']:
            continue
        condition = condition.replace(tag, "tags['" + tag + "']")
    return condition


def retrieve_experiments():
    global failed_retrieve_settings
    _experiments = ht_connector.get_all_experiments()
    if _experiments is None:
        failed_retrieve_settings = True
    else:
        failed_retrieve_settings = False
        for experiment_name, experiment in _experiments.items():
            settings = ExperimentSettings(experiment_id=experiment['test_id'], experiment_name=experiment['test_name'],
                                          experiment_hypothesis=experiment['experiment_hypothesis'],
                                          tag_names=experiment['tag_names'],
                                          condition_to_enter_experiment=experiment['condition_to_enter_test'],
                                          variants_distribution=experiment['variants_distribution'],
                                          goal_names=experiment['goal_names'],
                                          experiment_state=experiment['test_state'],
                                          experiment_active=experiment['test_active'],
                                          override_control=experiment['override_control'],
                                          override_b=experiment['override_b'])
            settings.condition_to_enter_experiment = _fix_condition(settings.condition_to_enter_experiment,
                                                                    settings.tag_names)
            experiments[experiment_name] = settings
        logger.debug({"msg": "retrieving all experiments from server success"})


def retrieve_experiments_thread():
    while ht_config.async_mode:
        retrieve_experiments()
        time.sleep(random.randint(ht_config.pull_interval, ht_config.pull_interval + ht_config.pull_jitter))
