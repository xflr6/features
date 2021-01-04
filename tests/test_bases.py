# test_bases.py

import pickle

import pytest

from features.bases import FeatureSet


def test_pickle_base(fs):
    base = pickle.loads(pickle.dumps(fs.FeatureSet.__base__))
    assert base is fs.FeatureSet.__base__


def test_pickle_class(fs):
    cls = pickle.loads(pickle.dumps(fs.FeatureSet))
    assert cls is fs.FeatureSet


def test_pickle_class_noname(fs_noname):
    cls = pickle.loads(pickle.dumps(fs_noname.FeatureSet))
    assert issubclass(cls, FeatureSet)
    pytest.xfail(reason='TODO')
    assert isinstance(cls, FeatureSet)
    assert cls is fs_noname.FeatureSet


def test_pickle_instance(fs):
    assert fs('1') is fs('1')
    assert pickle.loads(pickle.dumps(fs('1'))) is fs('1')


def test_pickle_instance_noname(fs_noname):
    assert fs_noname('1') is fs_noname('1')
    inst = pickle.loads(pickle.dumps(fs_noname('1')))
    assert isinstance(inst, FeatureSet)


@pytest.mark.parametrize('features, expected', [
    ('1sg', ['+1', '-3 +sg', '-2 +sg']),
])
def test_upper_neighbors_nonsup(fs, features, expected):
    features = fs(features)
    expected = [fs(e) for e in expected]
    assert features._upper_neighbors_nonsup() == expected


@pytest.mark.parametrize('features, other, expected', [
    pytest.param('1sg', '1sg', ['+1', '-3 +sg', '-2 +sg'],
                 marks=pytest.mark.xfail(reason='TODO: fix order')),
    ('1sg', '1', ['+1', '-3 +sg', '-2 +sg']),
    ('1', '1sg', ['+1', '-3 +sg', '-2 +sg']),
    pytest.param('1sg', '1pl', ['-3 +sg', '-2 +sg', '-3 +pl', '-2 +pl', '+1'],
                 marks=pytest.mark.xfail(reason='TODO: fix order')),
])
def test_upper_neighbors_union_nonsup(fs, features, other, expected):
    features, other = (fs(f) for f in (features, other))
    expected = [fs(e) for e in expected]
    assert list(features._upper_neighbors_union_nonsup(other)) == expected


@pytest.mark.parametrize('features, expected', [
    ('1sg', ['+1 +sg',
             '+1', '-3 +sg', '-2 +sg',
             '+sg', '-3', '-2']),
])
def test_upset_nonsup(fs, features, expected):
    features = fs(features)
    expected = [fs(e) for e in expected]
    assert list(features._upset_nonsup()) == expected


@pytest.mark.parametrize('features, other, expected', [
    ('1sg', '1pl', ['+1 +sg', '+1 +pl',
                    '+1',
                    '-3 +sg', '-2 +sg',
                    '-3 +pl', '-2 +pl',
                    '+sg', '+pl',
                    '-3', '-2']),
])
def test_upset_union_nonsup(fs, features, other, expected):
    features, other = (fs(f) for f in (features, other))
    expected = [fs(e) for e in expected]
    assert list(features._upset_union_nonsup(other)) == expected
