# bases.py - relations, comparisons, operations

from ._compat import map, py2_bool_to_nonzero, with_metaclass

from . import meta, tools

__all__ = ['FeatureSet']


@py2_bool_to_nonzero
class FeatureSet(with_metaclass(meta.FeatureSetMeta, object)):
    """Formal concept intent as ordered set of features.

    Usage:

    >>> from features.systems import FeatureSystem

    >>> fs = FeatureSystem('plural')

    >>> fs
    <FeatureSystem('plural') of 6 atoms 22 featuresets>


    >>> fs('1sg')
    FeatureSet('+1 +sg')

    >>> fs.FeatureSet('1sg')
    FeatureSet('+1 +sg')

    >>> print(fs('1sg'))
    [+1 +sg]

    >>> print(fs('1sg').__strmax__())
    [+1 -2 -3 +sg -pl]

    >>> fs('1sg') and fs('1') and not fs('')
    True


    >>> fs('1').atoms
    [FeatureSet('+1 +sg'), FeatureSet('+1 +pl')]

    >>> fs('1').upper_neighbors
    [FeatureSet('-3'), FeatureSet('-2')]

    >>> fs('1').lower_neighbors
    [FeatureSet('+1 +sg'), FeatureSet('+1 +pl')]

    >>> list(fs('1').upset())  # doctest: +NORMALIZE_WHITESPACE
    [FeatureSet('+1'),
     FeatureSet('-3'), FeatureSet('-2'),
     FeatureSet('')]

    >>> list(fs('1').downset())  # doctest: +NORMALIZE_WHITESPACE
    [FeatureSet('+1'),
     FeatureSet('+1 +sg'), FeatureSet('+1 +pl'),
     FeatureSet('+1 -1 +2 -2 +3 -3 +sg +pl -sg -pl')]


    >>> fs('-3') <= fs('-3') <= fs('1') <= fs('1sg')
    True

    >>> fs('1sg') >= fs('1sg') >= fs('1') >= fs('-3')
    True

    >>> fs('-3') < fs('1') < fs('1sg')
    True

    >>> fs('1sg') > fs('1') > fs('-3')
    True


    >>> fs('1sg') % fs('2sg')
    FeatureSet('-3 +sg')

    >>> fs('1') ^ fs('sg')
    FeatureSet('+1 +sg')


    >>> fs('1').incompatible_with(fs('3'))
    True

    >>> fs('1').incompatible_with(fs('sg'))
    False

    >>> fs('1').complement_of(fs('-1'))
    True

    >>> fs('1').complement_of(fs('3'))
    False

    >>> fs('-1').subcontrary_with(fs('-2'))
    True

    >>> fs('-1').subcontrary_with(fs('sg'))
    False

    >>> fs('1').orthogonal_to(fs('sg'))
    True

    >>> fs('-1').orthogonal_to(fs('-3'))
    False
    """

    def __init__(self, concept):
        self.concept = concept  #: The corresponding FCA concept.
        self.index = concept.index  #: The position of the feature set with its system.
        self.string = ' '.join(concept.minimal())  #: Space-concatenated minimal features.
        self.string_maximal = ' '.join(concept.intent)  #: All features space-concatenated.
        self.string_extent = ' '.join(concept.extent)  #: Space-concatenated extent labels.

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.string)

    def __reduce__(self):
        if self.system.key is None:
            return self.system.__class__, (self.system._config, self.string)
        return self.system.__class__, (self.system.key, self.string)

    def __str__(self):
        """Return the concise string representation."""
        return '[%s]' % self.string

    def __strmax__(self):
        """Return the verbose string representation."""
        return '[%s]' % self.string_maximal

    def __bool__(self):
        """Return ``True`` iff the set has features."""
        return self is not self.system.supremum

    @property
    def atoms(self):
        """The subsumed atoms."""
        indexes = (c.index for c in self.concept.atoms)
        return list(map(self._sibling, indexes))

    @property
    def upper_neighbors(self):
        """The directly implied neighbors."""
        indexes = (c.index for c in self.concept.upper_neighbors)
        return list(map(self._sibling, indexes))

    @property
    def lower_neighbors(self):
        """The directly subsumed neighbors."""
        indexes = (c.index for c in self.concept.lower_neighbors)
        return list(map(self._sibling, indexes))

    def upset(self):
        """Return the list of implied neighbors (including self)."""
        indexes = (c.index for c in self.concept.upset())
        return list(map(self._sibling, indexes))

    def downset(self):
        """Return the list of subsumed neighbors (including self)."""
        indexes = (c.index for c in self.concept.downset())
        return list(map(self._sibling, indexes))

    def subsumes(self, other):
        """Submsumption comparison."""
        return self.concept.subsumes(other.concept)

    def implies(self, other):
        """Implication comparison."""
        return self.concept.implies(other.concept)

    __le__ = subsumes
    __ge__ = implies

    def properly_subsumes(self, other):
        """Proper subsumption comparison."""
        return self.concept.properly_subsumes(other.concept)

    def properly_implies(self, other):
        """Proper implication comparison."""
        return self.concept.properly_implies(other.concept)

    __lt__ = properly_subsumes
    __gt__ = properly_implies

    def intersection(self, other):
        """Return the closest implied neighbor (generalization, join)."""
        join = self.concept.join(other.concept)
        return self._sibling(join.index)

    def union(self, other):
        """Return the closest subsumed neighbor (unification, meet)."""
        meet = self.concept.meet(other.concept)
        return self._sibling(meet.index)

    __mod__ = intersection
    __xor__ = union

    def incompatible_with(self, other):
        """Empty common extent comparison."""
        return self.concept.incompatible_with(other.concept)

    def complement_of(self, other):
        """Empty common extent and universal extent union comparison."""
        return self.concept.complement_of(other.concept)

    def subcontrary_with(self, other):
        """Nonempty common extent and universal extent union comparison."""
        return self.concept.subcontrary_with(other.concept)

    def orthogonal_to(self, other):
        """Nonempty common extent, incomparable, nonempty extent union comparison."""
        return self.concept.orthogonal_to(other.concept)

    # internal interface used by cases
    def _upper_neighbors_nonsup(self):
        indexes = (c.index for c in self.concept.upper_neighbors
                   if c.upper_neighbors)
        return list(map(self._sibling, indexes))

    def _upper_neighbors_union_nonsup(self, other):
        if other.properly_subsumes(self):
            return iter(self.upper_neighbors)
        elif self.properly_subsumes(other):
            return iter(other.upper_neighbors)

        union = self.concept.upper_neighbors + other.concept.upper_neighbors
        indexes = {c.index for c in union if c.upper_neighbors}
        return map(self._sibling, indexes)

    def _upset_nonsup(self):
        indexes = (c.index for c in tools.butlast(self.concept.upset()))
        return map(self._sibling, indexes)

    def _upset_union_nonsup(self, other):
        return tools.butlast(self.system.upset_union([self, other]))
