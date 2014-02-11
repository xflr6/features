# systems.py - build feature set lattice from FCA concept lattice

"""Lattice of possible feature sets."""

from itertools import izip, imap, combinations

import concepts

import meta
import bases
import parsers
import tools
import visualize

__all__ = ['FeatureSystem']


class FeatureSystem(object):
    """Feature set lattice defined by config instance.

    >>> fs = FeatureSystem('plural')

    >>> print fs  
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


    >>> fs.infimum
    FeatureSet('+1 -1 +2 -2 +3 -3 +sg +pl -sg -pl')

    >>> fs.supremum
    FeatureSet('')

    >>> fs.atoms  # doctest: +NORMALIZE_WHITESPACE
    [FeatureSet('+1 +sg'), FeatureSet('+1 +pl'),
     FeatureSet('+2 +sg'), FeatureSet('+2 +pl'),
     FeatureSet('+3 +sg'), FeatureSet('+3 +pl')]


    >>> fs.join([fs('1sg'), fs('1pl'), fs('3sg')])
    FeatureSet('-2')

    >>> fs.meet([fs('-1'), fs('-2'), fs('-pl')])
    FeatureSet('+3 +sg')
    """

    __metaclass__ = meta.FeatureSystemMeta

    FeatureSet = bases.FeatureSet

    def __init__(self, config):
        self._config = config

        context = concepts.Context.fromstring(config.context, frmat=config.format)

        if (len(context.objects) != len(context.lattice.atoms) or
            any((o,) != a.extent for o, a in
                izip(context.objects, context.lattice.atoms))):
            raise ValueError('Context does not allow to refer '
                'to each individual object: %r' % context)

        names = tools.uniqued(parsers.remove_sign(p) for p in context.properties)
        if any(l in r or r in l for l, r in combinations(names, 2)):
            raise ValueError('%r %r: some feature names %r are in '
                'substring relation' % (self.__class__, config.key, names))

        self.key = config.key
        self.description = config.description
        self.context = context
        self.lattice = context.lattice
        self.parse = parsers.Parser(context.properties)

        cls = type('FeatureSet', (self.FeatureSet,), {'system': self})
        if config.str_maximal:
            cls.__str__ = cls.__strmax__

        create = super(cls.__class__, cls).__call__
        self._featuresets = featuresets = map(create, self.lattice)
        cls._sibling = featuresets.__getitem__

        self.FeatureSet = cls
        self.infimum = featuresets[0]
        self.supremum = featuresets[-1]

    def __call__(self, string=''):
        """Idempotently return featureset from parsed feature string."""
        if isinstance(string, basestring):
            features = self.parse(string)
        elif isinstance(string, self.FeatureSet):
            return string
        else:
            features = string

        concept = self.lattice(features)
        result = self._featuresets[concept.index]

        if result is self.infimum:
            raise ValueError('%r (%s) is not a valid feature set in %r.' % (string, features, self))
        return result

    def __getitem__(self, index):
        return self._featuresets[index]

    def __iter__(self):
        return iter(self._featuresets)

    def __len__(self):
        return len(self._featuresets)

    def __contains__(self, featureset):
        return featureset in self._featuresets

    def __str__(self):
        description = '\n%r' % self.description if self.description else ''
        tmpl = '    %%-%ds -> %%s ' % max(len(str(f))for f in self._featuresets[1:])
        return '%r%s\n%s\n%s\n%s' % (self, description, tmpl % (self.infimum, ''),
            tmpl % ('', ' '.join(str(c) for c in self.infimum.upper_neighbors)),
            '\n'.join(tmpl % (f, ' '.join(str(c) for c in f.upper_neighbors))
                for f in self._featuresets[1:]))

    def __repr__(self):
        if self.key is None:
            return '<%s object of %d atoms %d featuresets at %#x>' % (self.__class__.__name__,
                len(self.atoms), len(self._featuresets), id(self))
        return '<%s(%r) of %d atoms %d featuresets>' % (self.__class__.__name__,
            self.key, len(self.atoms), len(self._featuresets))

    def __reduce__(self):
        if self.key is None:
            return self.__class__, (self._config,)
        return self.__class__, (self.key,)

    @property
    def atoms(self):
        """Minimal non-infimum feature sets."""
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
        return imap(self._featuresets.__getitem__, indexes)

    def downset_union(self, featuresets):
        """Yield all featuresets that imply any of the given ones."""
        concepts = (f.concept for f in featuresets)
        indexes = (c.index for c in self.lattice.downset_union(concepts))
        return imap(self._featuresets.__getitem__, indexes)

    def graphviz(self, highlight=None, maximal_label=None, topdown=None,
            filename=None, directory=None, render=False, view=False):
        """Return the system lattice visualization as graphviz source."""
        return visualize.featuresystem(self, highlight, maximal_label,
            topdown, filename, directory, render, view)
