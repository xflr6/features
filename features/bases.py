# bases.py - relations, comparisons, operations

from itertools import imap
import copy_reg

import tools

__all__ = ['FeatureSet']


class FeatureSetMeta(type):

    system = None

    def __call__(self, string=''):
        return self.system(string)

    def __repr__(self):
        if self.system is None:
            return type.__repr__(self)
        return '<class %r of %r>' % (self.__name__, self.system)

    def __reduce__(self):
        if self.system is None:
            return self.__name__
        return self.system.__class__, (self.system.key, -1)


copy_reg.pickle(FeatureSetMeta, FeatureSetMeta.__reduce__)


class FeatureSet(object):
    """Formal concept intent as ordered set of features.

    >>> fs('1sg')
    FeatureSet('+1 +sg')
    """

    __metaclass__ = FeatureSetMeta

    def __init__(self, concept):
        self.concept = concept
        self.index = concept.index
        self.string = ' '.join(concept.minimal())
        self.string_maximal = ' '.join(concept.intent)

    def __nonzero__(self):
        """Return True iff the set has features.

        >>> fs('1sg') and fs('1') and not fs('')
        True
        """
        return self is not self.system.supremum

    @property
    def upper_neighbors(self):
        """Immediate implied neighbors.

        >>> fs('1').upper_neighbors
        [FeatureSet('-3'), FeatureSet('-2')]
        """
        indexes = (c.index for c in self.concept.upper_neighbors)
        return map(self._sibling, indexes)

    @property
    def lower_neighbors(self):
        """Immediate subsumed neighbors.

        >>> fs('1').lower_neighbors
        [FeatureSet('+1 +sg'), FeatureSet('+1 +pl')]
        """
        indexes = (c.index for c in self.concept.lower_neighbors)
        return map(self._sibling, indexes)

    @property
    def atoms(self):
        """Subsumed atoms.

        >>> fs('1').atoms
        [FeatureSet('+1 +sg'), FeatureSet('+1 +pl')]
        """
        indexes = (c.index for c in self.concept.atoms)
        return map(self._sibling, indexes)

    def upset(self):
        """Implied neighbors.

        >>> list(fs('1').upset())  # doctest: +NORMALIZE_WHITESPACE
        [FeatureSet('+1'),
         FeatureSet('-3'), FeatureSet('-2'),
         FeatureSet('')]
        """
        indexes = (c.index for c in self.concept.upset())
        return map(self._sibling, indexes)

    def downset(self):
        """Subsumed neighbors.

        >>> list(fs('1').downset())  # doctest: +NORMALIZE_WHITESPACE
        [FeatureSet('+1'),
         FeatureSet('+1 +sg'), FeatureSet('+1 +pl'),
         FeatureSet('+1 -1 +2 -2 +3 -3 +sg +pl -sg -pl')]
        """
        indexes = (c.index for c in self.concept.downset())
        return map(self._sibling, indexes)

    def subsumes(self, other):
        """Submsumption.

        >>> fs('-3') <= fs('-3') <= fs('1') <= fs('1sg')
        True
        """
        return self.concept.subsumes(other.concept)

    def implies(self, other):
        """Implication.

        >>> fs('1sg') >= fs('1sg') >= fs('1') >= fs('-3')
        True
        """
        return self.concept.implies(other.concept)

    __le__ = subsumes
    __ge__ = implies

    def properly_subsumes(self, other):
        """Proper subsumption.

        >>> fs('-3') < fs('1') < fs('1sg')
        True
        """
        return self.concept.properly_subsumes(other.concept)

    def properly_implies(self, other):
        """Proper implication.

        >>> fs('1sg') > fs('1') > fs('-3')
        True
        """
        return self.concept.properly_implies(other.concept)

    __lt__ = properly_subsumes
    __gt__ = properly_implies

    def incompatible_with(self, other):
        """Empty common extent.

        >>> fs('1').incompatible_with(fs('3'))
        True
        >>> fs('1').incompatible_with(fs('sg'))
        False
        """
        return self.concept.incompatible_with(other.concept)

    def complement_of(self, other):
        """Empty common extent and universal extent union.

        >>> fs('1').complement_of(fs('-1'))
        True
        >>> fs('1').complement_of(fs('3'))
        False
        """
        return self.concept.complement_of(other.concept)

    def subcontrary_with(self, other):
        """Nonempty common extent and uiversal extent union.

        >>> fs('-1').subcontrary_with(fs('-2'))
        True
        >>> fs('-1').subcontrary_with(fs('sg'))
        False
        """
        return self.concept.subcontrary_with(other.concept)

    def intersection(self, other):
        """Closest implied neighbor.

        >>> fs('1sg') % fs('2sg')
        FeatureSet('-3 +sg')
        """
        join = self.concept.join(other.concept)
        return self._sibling(join.index)

    def unification(self, other):
        """Closest subsumed neighbor.

        >>> fs('1') ^ fs('sg')
        FeatureSet('+1 +sg')
        """
        meet = self.concept.meet(other.concept)
        return self._sibling(meet.index)

    __mod__ = intersection
    __xor__ = unification

    def __str__(self):
        """Concise string representation.

        >>> print fs('1sg')
        [+1 +sg]
        """
        return '[%s]' % self.string

    def __strmax__(self):
        """Verbose string representation.

        >>> print fs('1sg').__strmax__()
        [+1 -2 -3 +sg -pl]
        """
        return '[%s]' % self.string_maximal

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.string)

    def __reduce__(self):
        return self.system.__class__, (self.system.key, self.string)

    # internal interface used by cases
    def _upper_neighbors_nonsup(self):
        indexes = (c.index for c in self.concept.upper_neighbors if c.upper_neighbors)
        return map(self._sibling, indexes)

    def _upper_neighbors_union_nonsup(self, other):
        if other.properly_subsumes(self):
            return iter(self.upper_neighbors)
        elif self.properly_subsumes(other):
            return iter(other.upper_neighbors)
        indexes = set(c.index for c in
            self.concept.upper_neighbors + other.concept.upper_neighbors
            if c.upper_neighbors)
        return imap(self._sibling, indexes)

    def _upset_nonsup(self):
        indexes = (c.index for c in tools.butlast(self.concept.upset()))
        return imap(self._sibling, indexes)

    def _upset_union_nonsup(self, other):
        return tools.butlast(self.system.upset_union([self, other]))


def _test(verbose=False):
    from systems import FeatureSystem
    global fs
    fs = FeatureSystem('plural')

    import doctest
    doctest.testmod(verbose=verbose, extraglobs=locals())

if __name__ == '__main__':
    _test()
