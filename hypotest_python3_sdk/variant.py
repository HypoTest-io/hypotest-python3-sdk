import json
from .logger import logger


class Variant:
    def __init__(self, variant):
        self.variant = variant
        self.is_control = variant == 'control'

    def __getattr__(self, item):
        if 'control' in item:
            return self.is_control
        try:
            item = item.split('is_')[1]
            return item == self.variant
        except Exception as e:
            logger.warning({'error': e, 'error_description': 'failed to parse variant', 'item': item})
            return False

    def __str__(self):
        return str(self.variant)

    def __repr__(self):
        return "<Variant: {}>".format(self.variant)

    def to_json(self):
        return json.dumps({'variant': self.variant, 'is_control': self.is_control})
