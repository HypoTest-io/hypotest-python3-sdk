import logging

from .config import ht_config


def create_logger():
    log = logging.getLogger("HypoTest")
    log.setLevel(ht_config.log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
    log.addHandler(stream_handler)

    return log


logger = create_logger()
