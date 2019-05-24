# systems.py - build feature set lattice from FCA concept lattice

"""Lattice of possible feature sets."""

import concepts

from ._compat import string_types, zip, map, with_metaclass

from . import meta, bases, parsers, visualize

__all__ = ['FeatureSystem']


class FeatureSystem(with_metaclass(meta.FeatureSystemMeta, object)):
    """Feature set lattice defined by config instance.

    Usage:

    >>> fs = FeatureSystem('plural')

    >>> FeatureSystem(fs) is fs
    True

    >>> print(fs)  # doctest: +NORMALIZE_WHITESPACE
    <FeatureSystem('plural') of 6 atoms 22 featuresets>
    '1st, 2nd, and 3rd person & singular and plural number'
        [+1 -1 +2 -2 +3 -3 +sg +pl -sg -pl] ->
                 -> [+1 +sg] [+1 +pl] [+2 +sg] [+2 +pl] [+3 +sg] [+3 +pl]
        [+1 +sg] -> [+1] [-3 +sg] [-2 +sg]
        [+1 +pl] -> [+1] [-3 +pl] [-2 +pl]
        [+2 +sg] -> [-3 +sg] [+2] [-1 +sg]
        [+2 +pl] -> [-3 +pl] [+2] [-1 +pl]
        [+3 +sg] -> [-2 +sg] [-1 +sg] [+3]
        [+3 +pl] -> [-2 +pl] [-1 +pl] [+3]
        [+1]     -> [-3] [-2]
        [-3 +sg] -> [+sg] [-3]
        [-2 +sg] -> [+sg] [-2]
        [-3 +pl] -> [+pl] [-3]
        [-2 +pl] -> [+pl] [-2]
        [+2]     -> [-3] [-1]
        [-1 +sg] -> [+sg] [-1]
        [-1 +pl] -> [+pl] [-1]
        [+3]     -> [-2] [-1]
        [+sg]    -> []
        [+pl]    -> []
        [-3]     -> []
        [-2]     -> []
        [-1]     -> []
        []       ->


    >>> fs.FeatureSet
    <class 'FeatureSet' of <FeatureSystem('plural') of 6 atoms 22 featuresets>>

    >>> fs.FeatureSet.__base__
    <class 'features.bases.FeatureSet'>


    >>> fs.infimum
    FeatureSet('+1 -1 +2 -2 +3 -3 +sg +pl -sg -pl')

    >>> fs.supremum
    FeatureSet('')

    >>> fs[0] is fs.infimum and fs[-1] is fs.supremum
    True

    >>> len(fs)
    22

    >>> fs('+1') in fs
    True

    >>> fs.atoms  # doctest: +NORMALIZE_WHITESPACE
    [FeatureSet('+1 +sg'), FeatureSet('+1 +pl'),
     FeatureSet('+2 +sg'), FeatureSet('+2 +pl'),
     FeatureSet('+3 +sg'), FeatureSet('+3 +pl')]

    >>> fs('+1 -1')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: '+1 -1' (['+1', '-1']) is not a valid feature set in ...


    >>> fs.join([fs('1sg'), fs('1pl'), fs('3sg')])
    FeatureSet('-2')

    >>> fs.meet([fs('-1'), fs('-2'), fs('-pl')])
    FeatureSet('+3 +sg')
    """

    FeatureSet = bases.FeatureSet

    def __init__(self, config):
        self._config = config

        context = concepts.Context.fromstring(config.context, frmat=config.format)
        if (len(context.objects) != len(context.lattice.atoms)
            or any((o,) != a.extent
                   for o, a in zip(context.objects, context.lattice.atoms))):
            raise ValueError('context does not allow to refer'
                             ' to each individual object: %r' % context)

        self.key = config.key  #: The unique name of the feature system.
        self.description = config.description  #: A description of the feature system.
        self.context = context  #: The FCA context defining the feature system.
        self.lattice = context.lattice  #: The corresponding FCA lattice of the feature system.
        self.parse = parsers.Parser(context.properties)

        base = self.FeatureSet
        cls = type(base.__name__, (base,), {'system': self})
        if config.str_maximal:
            cls.__str__ = cls.__strmax__

        create = super(cls.__class__, cls).__call__
        self._featuresets = featuresets = list(map(create, self.lattice))
        cls._sibling = featuresets.__getitem__

        self.FeatureSet = cls
        self.infimum = featuresets[0]  #: The systems most specific feature set.
        self.supremum = featuresets[-1]  #: The systems most general feature set.

    def __call__(self, string='', allow_invalid=False):
        """Idempotently return featureset from parsed feature ``string``."""
        if isinstance(string, string_types):
            features = self.parse(string)
        elif isinstance(string, self.FeatureSet):
            return string
        else:
            features = string

        concept = self.lattice(features)
        result = self._featuresets[concept.index]

        if result is self.infimum and not allow_invalid:
            raise ValueError('%r (%s) is not a valid feature set in'
                             ' %r.' % (string, features, self))
        return result

    def __getitem__(self, index):
        """Return the feature set with the given ``index``."""
        return self._featuresets[index]

    def __iter__(self):
        """Yield all feature sets."""
        return iter(self._featuresets)

    def __len__(self):
        """Return the number of feature sets."""
        return len(self._featuresets)

    def __contains__(self, other):
        """Test for feature set membership."""
        return other in self._featuresets

    def __str__(self):
        description = '\n%r' % self.description if self.description else ''
        tmpl = '    %%-%ds -> %%s' % max(len(str(f))for f in self._featuresets[1:])
        return '%r%s\n%s\n%s\n%s' % (self, description, tmpl % (self.infimum, ''),
            tmpl % ('', ' '.join(str(c) for c in self.infimum.upper_neighbors)),
            '\n'.join(tmpl % (f, ' '.join(str(c) for c in f.upper_neighbors))
                for f in self._featuresets[1:]))

    def __repr__(self):
        if self.key is None:
            return ('<%s object of %d atoms %d featuresets'
                    ' at %#x>') % (self.__class__.__name__,
                                   len(self.atoms), len(self._featuresets),
                                   id(self))
        return '<%s(%r) of %d atoms %d featuresets>' % (self.__class__.__name__,
                                                        self.key,
                                                        len(self.atoms),
                                                        len(self._featuresets))

    def __reduce__(self):
        if self.key is None:
            return self.__class__, (self._config,)
        return self.__class__, (self.key,)

    @property
    def atoms(self):
        """The systems Minimal non-infimum feature sets."""
        return self.infimum.upper_neighbors

    def join(self, featuresets):
        """Return the nearest featureset that subsumes all given ones."""
        concepts = (f.concept for f in featuresets)
        join = self.lattice.join(concepts)
        return self._featuresets[join.index]

    def meet(self, featuresets):
        """Return the nearest featureset that implies all given ones."""
        concepts = (f.concept for f in featuresets)
        meet = self.lattice.meet(concepts)
        return self._featuresets[meet.index]

    def upset_union(self, featuresets):
        """Yield all featuresets that subsume any of the given ones."""
        concepts = (f.concept for f in featuresets)
        indexes = (c.index for c in self.lattice.upset_union(concepts))
        return map(self._featuresets.__getitem__, indexes)

    def downset_union(self, featuresets):
        """Yield all featuresets that imply any of the given ones."""
        concepts = (f.concept for f in featuresets)
        indexes = (c.index for c in self.lattice.downset_union(concepts))
        return map(self._featuresets.__getitem__, indexes)

    def graphviz(self, highlight=None, maximal_label=None, topdown=None,
                 filename=None, directory=None, render=False, view=False,
                 **kwargs):
        """Return the system lattice visualization as graphviz source."""
        return visualize.featuresystem(self, highlight, maximal_label,
                                       topdown, filename, directory,
                                       render, view, **kwargs)
