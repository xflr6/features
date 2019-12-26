# features - implement feature algebra

"""Feature set algebra for linguistics."""

from .meta import Config
from .systems import FeatureSystem

__all__ = ['Config', 'FeatureSystem', 'add_config', 'make_features']

__title__ = 'features'
__version__ = '0.5.12'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE.txt'
__copyright__ = 'Copyright (c) 2014-2019 Sebastian Bank'


def add_config(filename):
    """Add feature system definition file on top of the stack of config files.

    Args:
        filename: Path to the INI-file with feature system definitions.

    Note:
        If ``filename`` is a relative path, it is resolved relative to the
        directory of the caller (which may be different from the current working
        dicrectry).
    """
    Config.add(filename, caller_steps=2)


def make_features(context, frmat='table', str_maximal=False):
    """Return a new feature system from context string in the given format.

    Args:
        context (str): Formal context table as plain-text string.
        frmat: Format of the context string (``'table'``, ``'cxt'``, ``'csv'``).
        str_maximal (bool):

    Example:
        >>> make_features('''
        ...      |+male|-male|+adult|-adult|
        ... man  |  X  |     |   X  |      |
        ... woman|     |  X  |   X  |      |
        ... boy  |  X  |     |      |   X  |
        ... girl |     |  X  |      |   X  |
        ... ''')  # doctest: +ELLIPSIS
        <FeatureSystem object of 4 atoms 10 featuresets at 0x...>
    """
    config = Config.create(context=context, format=frmat,
                           str_maximal=str_maximal)
    return FeatureSystem(config)
