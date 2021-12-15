"""pytest fixtures."""

import pytest

from features.meta import Config
from features.systems import FeatureSystem


@pytest.fixture(scope='session')
def fs(name='plural'):
    return FeatureSystem(name)


@pytest.fixture(scope='session')
def fs_noname(fs):
    config = Config.create(context=fs._config.context)
    return FeatureSystem(config)
