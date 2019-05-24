# test_systems.py

import pickle

import pytest

from features.meta import Config
from features.systems import FeatureSystem


def test_init_inatomic():
    context = '''
        |catholic|protestant|
    spam|    X   |          |
    eggs|    X   |          |
    ham |        |     X    |
    '''
    config = Config.create(context=context)
    with pytest.raises(ValueError, match=r'individual'):
        FeatureSystem(config)


def test_init_substrings():
    context = '''
        |egg|eggs|
    spam| X |    |
    ham |   | X  |
    '''
    config = Config.create(context=context)
    with pytest.raises(ValueError, match=r'substring'):
        FeatureSystem(config)


def test_pickle_instance(fs):
    inst = pickle.loads(pickle.dumps(fs))
    assert inst is fs


def test_pickle_instance_noname(fs_noname):
    inst = pickle.loads(pickle.dumps(fs_noname))
    assert isinstance(inst, FeatureSystem)


@pytest.mark.parametrize('features, expected', [
    (['1sg', '+1', '+sg'], ['+sg', '+1',
                            '-3 +sg', '-2 +sg', '-1 +sg',
                            '+1 +sg', '+1 +pl',
                            '+2 +sg', '+3 +sg',
                            '+1 -1 +2 -2 +3 -3 +sg +pl -sg -pl']),
])
def test_downset_union(fs, features, expected):
    features = [fs(f) for f in features]
    expected = [fs(e, allow_invalid=True) for e in expected]
    assert list(fs.downset_union(features)) == expected
