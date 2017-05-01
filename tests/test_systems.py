# test_systems.py

import pickle

import pytest

from features.meta import Config
from features.systems import FeatureSystem


def test_init_inatomic():
    config = Config.create(context='''
        |catholic|protestant|
    spam|    X   |          |
    eggs|    X   |          |
    ham |        |     X    |
    ''')
    with pytest.raises(ValueError) as e:
        FeatureSystem(config)
    e.match(r'individual')


def test_init_substrings():
    config = Config.create(context='''
        |egg|eggs|
    spam| X |    |
    ham |   | X  |
    ''')
    with pytest.raises(ValueError) as e:
        FeatureSystem(config)
    e.match('substring')


def test_pickle_instance(fs):
    assert pickle.loads(pickle.dumps(fs)) is fs


def test_pickle_instance_noname(fs_noname):
    assert isinstance(pickle.loads(pickle.dumps(fs_noname)), FeatureSystem)


def test_downset_union(fs):
    assert list(fs.downset_union([fs('1sg'), fs('+1'), fs('+sg')])) == \
        [fs('+sg'), fs('+1'),
         fs('-3 +sg'), fs('-2 +sg'), fs('-1 +sg'),
         fs('+1 +sg'), fs('+1 +pl'),
         fs('+2 +sg'), fs('+3 +sg'),
         fs.infimum]
