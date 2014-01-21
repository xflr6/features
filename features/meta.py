# meta.py - retrieve feature system from config file section

import fileconfig

__all__ = ['Config', 'FeatureSystemMeta']

DEFAULT = 'default'


class Config(fileconfig.Stacked):
    """Define possible feature combinations and their minimal specification."""

    filename = 'config.ini'
    _encoding = 'utf_8_sig'

    def __init__(self, key, context, format='table', aliases=None, inherits=None, str_maximal=False, description=''):
        self.key = key
        self.context = context.strip()
        self.format = format
        self.aliases = [] if aliases is None else aliases
        self.inherits = inherits
        self.str_maximal = (False if not str_maximal
            else str_maximal.lower() in ('1', 'yes', 'true', 'on'))
        self.description = description.strip()

    def __str__(self):
        return '%r\n%s' % (self, self.context)


class FeatureSystemMeta(type):
    """Idempotently cache and return feature system instances by config."""

    __map = {}

    def __call__(self, config=DEFAULT, string=None):
        if isinstance(config, self):
            return config

        if isinstance(config, basestring):
            config = Config(config)

        if config.key in self.__map:
            inst = self.__map[config.key]
        else:
            inst = super(FeatureSystemMeta, self).__call__(config)
            self.__map.update(dict.fromkeys(inst._config.names, inst))

        if string is not None:
            if string == -1:  # unpickle set class
                return inst.FeatureSet
            return inst(string)
        return inst

    def __iter__(self):
        return (self(config) for config in Config)
