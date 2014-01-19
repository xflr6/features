# systems.py - build feature set lattice from FCA concept lattice

"""Lattice of possible feature sets."""

from itertools import izip, combinations

import concepts

import meta
import bases
import parsers
import tools
import visualize

__all__ = ['FeatureSystem']


class FeatureSystem(object):
    """Feature set lattice defined by config instance."""

    __metaclass__ = meta.FeatureSystemMeta

    _base = bases.FeatureSet

    def __init__(self, config):
        self._config = config

        context = concepts.Context.from_string(config.context)

        if (len(context.objects) != len(context.lattice.atoms) or
            any((o,) != a.extent for o, a in
                izip(context.objects, context.lattice.atoms))):
            raise ValueError('Context does not allow to refer '
                'to each individual object: %r' % context)

        names = tools.uniqued(parsers.remove_sign(p) for p in context.properties)
        if any(l in r or r in l for l, r in combinations(names, 2)):
            raise ValueError('Some %r feature names %r are in '
                'substring relation' % (self, names))

        self.key = config.key
        self.description = config.description
        self.context = context
        self.lattice = context.lattice
        self.parse = parsers.Parser(context.properties)

        cls = type('FeatureSet', (self._base,), {'system': self,
            '_indexes': staticmethod(self.lattice._Concepts._indexes.__func__),
             '_nonsup': (self.lattice._Concepts.supremum
                ^ self.lattice._Concepts._atoms[-1])})
        if config.str_maximal:
            cls.__str__ = cls.__strmax__

        create = super(cls.__class__, cls).__call__
        self._featuresets = featuresets = map(create, self.lattice)
        cls._sibling = featuresets.__getitem__

        self.FeatureSet = cls
        self.infimum = featuresets[0]
        self.supremum = featuresets[-1]

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
        union = 0
        for f in featuresets:
            union |= f.concept._upset
        indexes = self.FeatureSet._indexes(union)
        return map(self._featuresets.__getitem__, indexes)

    def downset_union(self, featuresets):
        union = 0
        for f in featuresets:
            union |= f.concept._downset
        indexes = self.FeatureSet._indexes(union)
        return map(self._featuresets.__getitem__, indexes)

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

    def __iter__(self):
        return iter(self._featuresets)

    def __len__(self):
        return len(self._featuresets)

    def __contains__(self, featureset):
        return featureset in self._featuresets

    def __getitem__(self, index):
        return self._featuresets[index]

    def __repr__(self):
        return '<%s(%r) of %d atoms %d featuresets>' % (self.__class__.__name__,
            self.key, len(self.atoms), len(self._featuresets))

    def __reduce__(self):
        return self.__class__, (self.key,)

    def __str__(self):
        description = '\n%r' % self.description if self.description else ''
        tmpl = '    %%-%ds -> %%s ' % max(len(str(f))for f in self._featuresets[1:])
        return '%r%s\n%s\n%s\n%s' % (self, description, tmpl % (self.infimum, ''),
            tmpl % ('', ' '.join(str(c) for c in self.infimum.upper_neighbors)),
            '\n'.join(tmpl % (f, ' '.join(str(c) for c in f.upper_neighbors))
                for f in self._featuresets[1:]))

    def graphviz(self, highlight=None, maximal_label=None, topdown=None,
            filename=None, directory=None, render=False, view=False):
        """Return the system lattice visualization as graphviz source."""
        return visualize.featuresystem(self, highlight, maximal_label,
            topdown, filename, directory, render, view)
