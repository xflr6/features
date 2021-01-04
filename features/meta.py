# meta.py - retrieve feature system from config file section

import copyreg

import fileconfig

__all__ = ['Config', 'FeatureSystemMeta', 'FeatureSetMeta']

DEFAULT = 'default'


def register_reduce(mcls):
    """Register __reduce__ as reduction function for mcls instances."""
    copyreg.pickle(mcls, mcls.__reduce__)
    return mcls


class Config(fileconfig.Stacked):
    """Define possible feature combinations and their minimal specification."""

    filename = 'config.ini'

    _encoding = 'utf-8-sig'

    def __init__(self, key, context, format='table', aliases=None,
                 inherits=None, str_maximal=False, description=None):
        self.key = key
        self.context = context.strip()
        self.format = format
        self.aliases = aliases if aliases is not None else []
        self.inherits = inherits
        self.str_maximal = (False if not str_maximal
                            else True if str_maximal is True
                            else str_maximal.lower() in ('1', 'yes', 'true', 'on'))
        self.description = description.strip() if description is not None else ''


class FeatureSystemMeta(type):
    """Idempotently cache and return feature system instances by config."""

    __map = {}

    def __call__(self, config=DEFAULT, string=None):  # noqa: N804
        if isinstance(config, self):
            return config

        if isinstance(config, str):
            config = Config(config)

        if config.key is not None and config.key in self.__map:
            inst = self.__map[config.key]
        else:
            inst = super().__call__(config)
            self.__map.update(dict.fromkeys(inst._config.names, inst))

        if string is not None:
            if string == -1:  # unpickle set class
                return inst.FeatureSet
            return inst(string)
        return inst


@register_reduce
class FeatureSetMeta(type):

    system = None

    def __call__(self, string=''):  # noqa: N804
        return self.system(string)

    def __repr__(self):  # noqa: N804
        if self.system is None:
            return type.__repr__(self)
        return f'<class {self.__name__!r} of {self.system!r}>'

    def __reduce__(self):  # noqa: N804
        if self.system is None:
            return self.__name__
        elif self.system.key is None:
            return self.system.__class__, (self.system._config, -1)
        return self.system.__class__, (self.system.key, -1)
