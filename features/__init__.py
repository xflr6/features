# features - implement feature algebra

"""Feature set algebra for linguistics."""

__title__ = 'features'
__version__ = '0.5.2'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE'
__copyright__ = 'Copyright (c) 2014 Sebastian Bank'

from .meta import Config
from .systems import FeatureSystem

__all__ = ['Config', 'FeatureSystem', 'add_config', 'make_features']


def add_config(filename):
    """Add feature system definition file on top of the stack."""
    Config.add(filename, caller_steps=2)


def make_features(context, frmat='table', str_maximal=False):
    """Return a new feature system from context string in the given format.

    >>> fs = make_features('''
    ...      |+male|-male|+adult|-adult|
    ... man  |  X  |     |   X  |      |
    ... woman|     |  X  |   X  |      |
    ... boy  |  X  |     |      |   X  |
    ... girl |     |  X  |      |   X  |
    ... ''')

    >>> fs  # doctest: +ELLIPSIS
    <FeatureSystem object of 4 atoms 10 featuresets at 0x...>
    """
    config = Config.create(context=context, format=frmat, str_maximal=str_maximal)
    return FeatureSystem(config)
