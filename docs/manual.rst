.. _manual:

User Guide
==========


Installation
------------

:mod:`features` is a pure-python package implementing **feature set algebra**
as commonly used in linguistics. It runs under both Python 3.7+ and is
`available from PyPI`_. To install it using pip_, run the following command:

.. code:: bash

    $ pip install features

For a system-wide install, this typically requires administrator access. For an
isolated installation, you can run the same inside a :mod:`py3:venv` or a
virtualenv_.

The pip-command will automatically download and install the (pure-python)
fileconfig_ and concepts_ packages (plus dependencies) from PyPI. The latter
provides the lower level `Formal Concept Analysis`_ (FCA) algorithms on which
:mod:`features` is based.

Features is essentially a convenience wrapper around the FCA-functionality of
``concepts``.


Feature systems
---------------

Features includes some **predefined feature systems** that you can try out
immediately and will be used as example in this documentation. See below on
how to define, persist, and load you own feature systems/definitions.
To load a feature system, pass its **name** to :class:`features.FeatureSystem`:

.. code:: python

    >>> import features

    >>> fs = features.FeatureSystem('plural')

    >>> fs
    <FeatureSystem('plural') of 6 atoms 22 featuresets>

The built-in feature systems are defined in the ``config.ini`` file in the
package directory (usually, this will be ``Lib/site-packages/concepts/`` in your
Python directory). You can either directly define new systems within a Python
script or create your own INI-file(s) with definitions so that you can load 
and reuse feature systems in different scripts.

The definition of a feature system is stored in its
:attr:`~.FeatureSystem.context` object. It is basically a cross-table giving
the features (properties) for each thing to be described (object):

.. code:: python

    >>> print(fs.context)  # doctest: +ELLIPSIS
    <Context object mapping 6 objects to 10 properties [3011c283] at 0x...>
          |+1|-1|+2|-2|+3|-3|+sg|+pl|-sg|-pl|
        1s|X |  |  |X |  |X |X  |   |   |X  |
        1p|X |  |  |X |  |X |   |X  |X  |   |
        2s|  |X |X |  |  |X |X  |   |   |X  |
        2p|  |X |X |  |  |X |   |X  |X  |   |
        3s|  |X |  |X |X |  |X  |   |   |X  |
        3p|  |X |  |X |X |  |   |X  |X  |   |

    >>> fs.context.objects
    ('1s', '1p', '2s', '2p', '3s', '3p')

    >>> fs.context.properties
    ('+1', '-1', '+2', '-2', '+3', '-3', '+sg', '+pl', '-sg', '-pl')

    >>> fs.context.bools  # doctest: +NORMALIZE_WHITESPACE
    [(True, False, False, True, False, True, True, False, False, True),
     (True, False, False, True, False, True, False, True, True, False),
     (False, True, True, False, False, True, True, False, False, True),
     (False, True, True, False, False, True, False, True, True, False),
     (False, True, False, True, True, False, True, False, False, True),
     (False, True, False, True, True, False, False, True, True, False)]

In other words, it provides a mapping from objects to features and vice versa.
Check the `documentation <concepts docs_>`_ of the concepts_ package for
further information on its full functionality.

.. code:: python

    >>> fs.context.intension(['1s', '1p'])  # common features?
    ('+1', '-2', '-3')

    >>> fs.context.extension(['-3', '+sg'])  # common objects?
    ('1s', '2s')


Feature sets
------------

All feature system contain a **contradicting feature set** with all features
that refers to no object:

.. code:: python

    >>> fs.infimum
    FeatureSet('+1 -1 +2 -2 +3 -3 +sg +pl -sg -pl')

    >>> fs.infimum.concept.extent
    ()

As well as a maximally general **tautological feature set** with no features
referring to all objects:

.. code:: python

    >>> fs.supremum
    FeatureSet('')

    >>> fs.supremum.concept.extent
    ('1s', '1p', '2s', '2p', '3s', '3p')

Use the feature system to iterate over **all defined feature sets** in shortlex
extent order:

.. code:: python

    >>> for f in fs:
    ...     print(f, f.concept.extent)
    [+1 -1 +2 -2 +3 -3 +sg +pl -sg -pl] ()
    [+1 +sg] ('1s',)
    [+1 +pl] ('1p',)
    [+2 +sg] ('2s',)
    [+2 +pl] ('2p',)
    [+3 +sg] ('3s',)
    [+3 +pl] ('3p',)
    [+1] ('1s', '1p')
    [-3 +sg] ('1s', '2s')
    [-2 +sg] ('1s', '3s')
    [-3 +pl] ('1p', '2p')
    [-2 +pl] ('1p', '3p')
    [+2] ('2s', '2p')
    [-1 +sg] ('2s', '3s')
    [-1 +pl] ('2p', '3p')
    [+3] ('3s', '3p')
    [+sg] ('1s', '2s', '3s')
    [+pl] ('1p', '2p', '3p')
    [-3] ('1s', '1p', '2s', '2p')
    [-2] ('1s', '1p', '3s', '3p')
    [-1] ('2s', '2p', '3s', '3p')
    [] ('1s', '1p', '2s', '2p', '3s', '3p')

The **string representations** will show the smallest possible notation for
each feature set by default (shortlex minimum). The full representation is also
available (and an extent-based representation):

.. code:: python

    >>> fs('1sg').string
    '+1 +sg'

    >>> fs('1sg').string_maximal
    '+1 -2 -3 +sg -pl'

    >>> fs('1sg').string_extent
    '1s'

To use the maximal representation for :meth:`~.FeatureSet.__str__`, put
``str_maximal = true`` into the configuration file section (see
`below <Definition_>`_).


Retrieval
---------

You can call the feature system with an iterable of features to retrieve one of
its feature sets:

.. code:: python

    >>> fs(['+1', '+sg'])
    FeatureSet('+1 +sg')

Usually, it is more convenient to let the system extract the features from a
string:

.. code:: python

    >>> fs('+1 +sg')
    FeatureSet('+1 +sg')

Leading plusses can be omitted. Spaces are optional. Case, order, and
duplication of features are ignored.

.. code:: python

    >>> fs('2 pl')
    FeatureSet('+2 +pl')

    >>> fs('SG3sg')
    FeatureSet('+3 +sg')

Note that commas are not allowed inside the string.


Uniqueness
----------

Feature sets are *singletons*. The constructor is also *idempotent*:

.. code:: python

    >>> fs('1sg') is fs('1sg')
    True

    >>> fs(fs('1sg')) is fs('1sg')
    True

All different possible ways to notate a feature set map to the *same* instance:

.. code:: python

    >>> fs('+1 -2 -3 -sg +pl') is fs('1pl')
    True

    >>> fs('+sg') is fs('-pl')
    True

Notations are equivalent, when they refer to the **same set of objects** (have
the same *extent*).


Comparisons
-----------

Compatibility tests:

.. code:: python

    >>> fs('+1').incompatible_with(fs('+3'))
    True

    >>> fs('sg').complement_of(fs('pl'))
    True

    >>> fs('-1').subcontrary_with(fs('-2'))
    True

    >>> fs('+1').orthogonal_to(fs('+sg'))
    True

Set inclusion (*subsumption*):

.. code:: python

    >>> fs('') < fs('-3') <= fs('-3') < fs('+1') < fs('1sg')
    True


Operations
----------

Intersection (*join*, generalization, closest feature set that subsumes the
given ones):

.. code:: python

    >>> fs('1sg') % fs('2sg')  # common features, or?
    FeatureSet('-3 +sg')

Intersect an iterable of feature sets:

.. code:: python

    >>> fs.join([fs('+1'), fs('+2'), fs('1sg')])
    FeatureSet('-3')

Union (*meet*, unification, closest feature set that implies the given ones):

.. code:: python

    >>> fs('-1') ^ fs('-2')  # commbined features, and?
    FeatureSet('+3')

Unify an iterable of feature sets:

.. code:: python

    >>> fs.meet([fs('+1'), fs('+sg'), fs('-3')])
    FeatureSet('+1 +sg')

Relations
---------

Immediately implied/subsumed neighbors.

.. code:: python

    >>> fs('+1').upper_neighbors
    [FeatureSet('-3'), FeatureSet('-2')]

    >>> fs('+1').lower_neighbors
    [FeatureSet('+1 +sg'), FeatureSet('+1 +pl')]

Complete set of implied/subsumed neighbors.

.. code:: python

    >>> list(fs('+1').upset())
    [FeatureSet('+1'), FeatureSet('-3'), FeatureSet('-2'), FeatureSet('')]

    >>> list(fs('+1').downset())  # doctest: +NORMALIZE_WHITESPACE
    [FeatureSet('+1'),
     FeatureSet('+1 +sg'), FeatureSet('+1 +pl'),
     FeatureSet('+1 -1 +2 -2 +3 -3 +sg +pl -sg -pl')]


Definition
----------

If you do not need to save your definition, you can directly create a system
from an ASCII-art style table:

.. code:: python

    >>> fs = features.make_features('''
    ...      |+male|-male|+adult|-adult|
    ... man  |  X  |     |   X  |      |
    ... woman|     |  X  |   X  |      |
    ... boy  |  X  |     |      |   X  |
    ... girl |     |  X  |      |   X  |
    ... ''', str_maximal=False)

    >>> fs  # doctest: +ELLIPSIS
    <FeatureSystem object of 4 atoms 10 featuresets at 0x...>

    >>> for f in fs:
    ...     print(f, f.concept.extent)
    [+male -male +adult -adult] ()
    [+male +adult] ('man',)
    [-male +adult] ('woman',)
    [+male -adult] ('boy',)
    [-male -adult] ('girl',)
    [+adult] ('man', 'woman')
    [+male] ('man', 'boy')
    [-male] ('woman', 'girl')
    [-adult] ('boy', 'girl')
    [] ('man', 'woman', 'boy', 'girl')

Note that the strings representing the objects and features need to be disjoint
and features cannot be in substring relation.

To load feature systems by name, create an INI-file with your configurations,
for example:

.. code:: ini

    # phonemes.ini - define distinctive features

    [vowels]
    description = Distinctive vowel place features
    str_maximal = true
    context = 
       |+high|-high|+low|-low|+back|-back|+round|-round|
      i|  X  |     |    |  X |     |  X  |      |   X  |
      y|  X  |     |    |  X |     |  X  |   X  |      |
      ?|  X  |     |    |  X |  X  |     |      |   X  |
      u|  X  |     |    |  X |  X  |     |   X  |      |
      e|     |  X  |    |  X |     |  X  |      |   X  |
      ø|     |  X  |    |  X |     |  X  |   X  |      |
      ?|     |  X  |    |  X |  X  |     |      |   X  |
      o|     |  X  |    |  X |  X  |     |   X  |      |
      æ|     |  X  |  X |    |     |  X  |      |   X  |
      œ|     |  X  |  X |    |     |  X  |   X  |      |
      ?|     |  X  |  X |    |  X  |     |      |   X  |
      ?|     |  X  |  X |    |  X  |     |   X  |      |

Add your config file, overriding existing sections with the same name:

.. code:: python

    >>> features.add_config('examples/phonemes.ini')

If the filename is relative, it is resolved relative to the file where the
:func:`.add_config` function was called. Check the documentation of the
fileconfig_ package for details.

Load your feature system:

.. code:: python

    >>> fs = features.FeatureSystem('vowels')

    >>> fs
    <FeatureSystem('vowels') of 12 atoms 55 featuresets>

Retrieve feature sets, extents and intents:

.. code:: python

    >>> print(fs('+high'))
    [+high -low]

    >>> print('high round = {}, {}'.format(*fs('high round').concept.extent))
    high round = y, u

    >>> print('i, e, o = {}'.format(*fs.lattice[('i', 'e', 'o')].intent))
    i, e, o = -low


Logical relations between feature pairs (excluding orthogonal pairs):

.. code:: python

    >>> print(fs.context.relations())  # doctest: +NORMALIZE_WHITESPACE
    +high  complement   -high
    +low   complement   -low
    +back  complement   -back
    +round complement   -round
    +high  incompatible +low
    +high  implication  -low
    +low   implication  -high
    -high  subcontrary  -low


.. _available from PyPI: https://pypi.org/project/features/

.. _pip: https://pip.readthedocs.io
.. _virtualenv: https://virtualenv.pypa.io

.. _Graphviz graph layout software: http://www.graphviz.org
.. _Formal Concept Analysis: https://en.wikipedia.org/wiki/Formal_concept_analysis

.. _concepts: https://pypi.org/project/concepts/
.. _concepts docs: https://concepts.readthedocs.io
.. _fileconfig: https://pypi.org/project/fileconfig/
.. _graphviz: https://pypi.org/project/graphviz/
