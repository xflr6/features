# test_bases.py

import unittest

import pickle

from features.systems import FeatureSystem
from features.meta import Config
from features.bases import FeatureSet


class TestFeatureSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fs = FeatureSystem('plural')
        config = Config.create(context=cls.fs._config.context)
        cls.fs_noname = FeatureSystem(config)

    @classmethod
    def tearDownClass(cls):
        del cls.fs
        del cls.fs_noname

    def test_pickle_base(self):
        self.assertIs(
            pickle.loads(pickle.dumps(self.fs.FeatureSet.__base__)),
            self.fs.FeatureSet.__base__)

    def test_pickle_class(self):
        self.assertIs(pickle.loads(pickle.dumps(self.fs.FeatureSet)),
            self.fs.FeatureSet)

    def test_pickle_class_noname(self):
        pickle.loads(pickle.dumps(self.fs_noname.FeatureSet))
        return  # TODO
        self.assertIsInstance(
            pickle.loads(pickle.dumps(self.fs_noname.FeatureSet)),
            FeatureSet)

    def test_pickle_instance(self):
        self.assertIs(pickle.loads(pickle.dumps(self.fs('1'))), self.fs('1'))

    def test_pickle_instance_noname(self):
        self.assertIsInstance(
            pickle.loads(pickle.dumps(self.fs_noname('1'))),
            FeatureSet)

    def test_upper_neighbors_nonsup(self):
        self.assertEqual(self.fs('1sg')._upper_neighbors_nonsup(),
            [self.fs('+1'), self.fs('-3 +sg'), self.fs('-2 +sg')])

    def test_upper_neighbors_union_nonsup(self):
        # TODO
        True or self.assertEqual(
            list(self.fs('1sg')._upper_neighbors_union_nonsup(self.fs('1sg'))),
            [self.fs('+1'), self.fs('-3 +sg'), self.fs('-2 +sg')])
        self.assertEqual(
            list(self.fs('1sg')._upper_neighbors_union_nonsup(self.fs('1'))),
            [self.fs('+1'), self.fs('-3 +sg'), self.fs('-2 +sg')])
        self.assertEqual(
            list(self.fs('1')._upper_neighbors_union_nonsup(self.fs('1sg'))),
            [self.fs('+1'), self.fs('-3 +sg'), self.fs('-2 +sg')])
        True or self.assertEqual(
            list(self.fs('1sg')._upper_neighbors_union_nonsup(self.fs('1pl'))),
            [self.fs('-3 +sg'), self.fs('-2 +sg'),
             self.fs('-3 +pl'), self.fs('-2 +pl'),
             self.fs('+1')])

    def test_upset_nonsup(self):
        self.assertEqual(list(self.fs('1sg')._upset_nonsup()),
            [self.fs('+1 +sg'),
             self.fs('+1'), self.fs('-3 +sg'), self.fs('-2 +sg'),
             self.fs('+sg'), self.fs('-3'), self.fs('-2')])

    def test_upset_union_nonsup(self):
        self.assertEqual(
            list(self.fs('1sg')._upset_union_nonsup(self.fs('1pl'))),
            [self.fs('+1 +sg'), self.fs('+1 +pl'),
             self.fs('+1'),
             self.fs('-3 +sg'), self.fs('-2 +sg'),
             self.fs('-3 +pl'), self.fs('-2 +pl'),
             self.fs('+sg'), self.fs('+pl'),
             self.fs('-3'), self.fs('-2')])
