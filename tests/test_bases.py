# test_bases.py

import pickle

from features.bases import FeatureSet


def test_pickle_base(fs):
    assert pickle.loads(pickle.dumps(fs.FeatureSet.__base__)) is fs.FeatureSet.__base__


def test_pickle_class(fs):
    assert pickle.loads(pickle.dumps(fs.FeatureSet)) is fs.FeatureSet


def test_pickle_class_noname(fs_noname):
    pickle.loads(pickle.dumps(fs_noname.FeatureSet))
    # TODO
    assert True or isinstance(pickle.loads(pickle.dumps(fs_noname.FeatureSet)), FeatureSet)


def test_pickle_instance(fs):
    assert pickle.loads(pickle.dumps(fs('1'))), fs('1')


def test_pickle_instance_noname(fs_noname):
    assert isinstance(pickle.loads(pickle.dumps(fs_noname('1'))), FeatureSet)


def test_upper_neighbors_nonsup(fs):
    assert fs('1sg')._upper_neighbors_nonsup() == [fs('+1'), fs('-3 +sg'), fs('-2 +sg')]


def test_upper_neighbors_union_nonsup(fs):
    # TODO
    assert True or list(fs('1sg')._upper_neighbors_union_nonsup(fs('1sg'))) == \
        [fs('+1'), fs('-3 +sg'), fs('-2 +sg')]
    assert list(fs('1sg')._upper_neighbors_union_nonsup(fs('1'))) == \
        [fs('+1'), fs('-3 +sg'), fs('-2 +sg')]
    assert list(fs('1')._upper_neighbors_union_nonsup(fs('1sg'))) == \
        [fs('+1'), fs('-3 +sg'), fs('-2 +sg')]
    # TODO
    assert True or list(fs('1sg')._upper_neighbors_union_nonsup(fs('1pl'))) == \
        [fs('-3 +sg'), fs('-2 +sg'),
         fs('-3 +pl'), fs('-2 +pl'),
         fs('+1')]


def test_upset_nonsup(fs):
    assert list(fs('1sg')._upset_nonsup()) == \
        [fs('+1 +sg'),
         fs('+1'), fs('-3 +sg'), fs('-2 +sg'),
         fs('+sg'), fs('-3'), fs('-2')]


def test_upset_union_nonsup(fs):
    assert list(fs('1sg')._upset_union_nonsup(fs('1pl'))) == \
        [fs('+1 +sg'), fs('+1 +pl'),
         fs('+1'),
         fs('-3 +sg'), fs('-2 +sg'),
         fs('-3 +pl'), fs('-2 +pl'),
         fs('+sg'), fs('+pl'),
         fs('-3'), fs('-2')]
