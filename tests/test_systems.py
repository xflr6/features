# test_systems.py

import unittest

import pickle

from features.systems import FeatureSystem
from features.meta import Config


class TestFeatureSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fs = FeatureSystem('plural')
        config = Config.create(context=cls.fs._config.context)
        cls.fs_noname = FeatureSystem(config)

    @classmethod
    def tearDownClass(cls):
        del cls.fs
        del cls.fs_noname

    def test_init_inatomic(self):
        config = Config.create(context='''
            |catholic|protestant|
        spam|    X   |          |
        eggs|    X   |          |
        ham |        |     X    |
        ''')
        with self.assertRaisesRegexp(ValueError, 'individual'):
            FeatureSystem(config)

    def test_init_substrings(self):
        config = Config.create(context='''
            |egg|eggs|
        spam| X |    |
        ham |   | X  |
        ''')
        with self.assertRaisesRegexp(ValueError, 'substring'):
            FeatureSystem(config)

    def test_pickle_instance(self):
        self.assertIs(pickle.loads(pickle.dumps(self.fs)), self.fs)

    def test_pickle_instance_noname(self):
        self.assertIsInstance(pickle.loads(pickle.dumps(self.fs_noname)),
            FeatureSystem)

    def test_downset_union(self):
        self.assertEqual(list(self.fs.downset_union(
            [self.fs('1sg'), self.fs('+1'), self.fs('+sg')])),
            [self.fs('+sg'), self.fs('+1'),
             self.fs('-3 +sg'), self.fs('-2 +sg'), self.fs('-1 +sg'),
             self.fs('+1 +sg'), self.fs('+1 +pl'),
             self.fs('+2 +sg'), self.fs('+3 +sg'),
             self.fs.infimum])
