Features
========

|PyPI version| |License| |Downloads|

Features is a simple implementation of **feature set algebra** in Python.

Linguistic analyses commonly use sets of **binary or privative features** to
refer to different groups of linguistic objects: for example a group of
*phonemes* that share some phonological features like ``[-consonantal, +high]``
or a set of *morphemes* that occur in context of a specific person/number
combination like ``[-participant, GROUP]``. Usually, the features are applied in
a way such that only **some of their combinations are valid**, while others are
impossible (i.e. refer to no object) |--| for example ``[+high, +low]``, or
``[-participant, +speaker]``.

With this package, such feature systems can be created with a simple contingency
**table definition** (feature matrix) and saved under a section in a
**configuration file**. Each feature system can then be **loaded** and provides
its own ``FeatureSet`` subclass that implements all **comparisons and
operations** between its feature sets according to the given definition
(compatibility, entailment, intersection, unification, etc.).

Features creates the **complete lattice** structure between the possible feature
sets of each feature system and lets you navigate and **visualize their
relations** using the Graphviz_ graph layout library.


Installation
------------

.. code:: bash

    $ pip install features

This will also install the concepts_ package from PyPI providing the `Formal
Concept Analysis`_ (FCA) algorithms which are the base of this package.

Features is essentially a convenience wrapper around the FCA-functionality of
concepts.


Systems
-------

Features includes some **predefined feature systems** you can try immediately.
To load a feature system, pass its **name** to ``features.FeatureSystem``:

.. code:: python

    >>> import features

    >>> fs = features.FeatureSystem('plural')

    >>> fs
    <FeatureSystem('plural') of 6 atoms 22 featuresets>

The built-in feature systems are found in the ``config.ini`` file in the package
directory (usually ``Lib/site-packages/concepts`` in your Python directory).

The definition of a feature system is stored in its ``context`` object:

.. code:: python

    >>> print fs.context  # doctest: +ELLIPSIS
    <Context object mapping 6 objects to 10 properties at 0x...>
          |+1|-1|+2|-2|+3|-3|+sg|+pl|-sg|-pl|
        1s|X |  |  |X |  |X |X  |   |   |X  |
        1p|X |  |  |X |  |X |   |X  |X  |   |
        2s|  |X |X |  |  |X |X  |   |   |X  |
        2p|  |X |X |  |  |X |   |X  |X  |   |
        3s|  |X |  |X |X |  |X  |   |   |X  |
        3p|  |X |  |X |X |  |   |X  |X  |   |

Check the documentation of concepts_ for further information on its full
functionality.

.. code:: python

    >>> fs.context.objects
    ('1s', '1p', '2s', '2p', '3s', '3p')

    >>> fs.context.properties
    ('+1', '-1', '+2', '-2', '+3', '-3', '+sg', '+pl', '-sg', '-pl')


Feature sets
------------

All feature system contain a **contradicting feature set** with all features
referring to no object:

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
    ...     print f, f.concept.extent
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

Set inclusion (*subsumption*):

.. code:: python

    >>> fs('') < fs('-3') <= fs('-3') < fs('+1') < fs('1sg')
    True


Operations
----------

Intersection (*join*, closest feature set that subsumes the given ones):

.. code:: python

    >>> fs('1sg') % fs('2sg')
    FeatureSet('-3 +sg')

Intersect an iterable of feature sets:

.. code:: python

    >>> fs.join([fs('+1'), fs('+2'), fs('1sg')])
    FeatureSet('-3')

Unification (*meet*, closest feature set that implies the given ones):

.. code:: python

    >>> fs('-1') ^ fs('-2')
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

    >>> fs('+1').upset
    [FeatureSet('+1'), FeatureSet('-3'), FeatureSet('-2'), FeatureSet('')]

    >>> fs('+1').downset  # doctest: +NORMALIZE_WHITESPACE
    [FeatureSet('+1 -1 +2 -2 +3 -3 +sg +pl -sg -pl'),
     FeatureSet('+1 +sg'), FeatureSet('+1 +pl'), FeatureSet('+1')]


Visualization
-------------

Create a graph of the feature system lattice.

.. code:: python

    >>> dot = fs.graphviz()

    >>> print dot.source  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    // <FeatureSystem('plural') of 6 atoms 22 featuresets>
    digraph plural {
    graph [margin=0]
    edge [arrowtail=none dir=back penwidth=.5]
    	f0 [label="+1 &minus;1 +2 &minus;2 +3 &minus;3 +sg +pl &minus;sg &minus;pl"]
    	f1 [label="+1 +sg"]
    		f1 -> f0
    	f2 [label="+1 +pl"]
    		f2 -> f0
    ...

.. image:: https://raw.github.com/xflr6/features/master/docs/fs-plural.png
    :width: 720px
    :align: center

Check the documentation of `this package`__ for details on the resulting object.

.. __: http://pypi.python.org/pypi/graphviz


Definition
----------

Create an INI-file with your configurations, for example:

.. code:: ini

    # phonemes.ini - define distinctive features

    [vowels]
    description = Distinctive vowel place features
    str_maximal = true
    context = 
       |+high|-high|+low|-low|+back|-back|+round|-round|
      i|  X  |     |    |  X |     |  X  |      |  X   |
      y|  X  |     |    |  X |     |  X  |  X   |      |
      ɨ|  X  |     |    |  X |  X  |     |      |  X   |
      u|  X  |     |    |  X |  X  |     |  X   |      |
      e|     |  X  |    |  X |     |  X  |      |  X   |
      ø|     |  X  |    |  X |     |  X  |  X   |      |
      ʌ|     |  X  |    |  X |  X  |     |      |  X   |
      o|     |  X  |    |  X |  X  |     |  X   |      |
      æ|     |  X  |  X |    |     |  X  |      |  X   |
      œ|     |  X  |  X |    |     |  X  |  X   |      |
      ɑ|     |  X  |  X |    |  X  |     |      |  X   |
      ɒ|     |  X  |  X |    |  X  |     |  X   |      |

Add your config file, overriding existing sections with the same name:

.. code:: python

    >>> features.Config.add('docs/phonemes.ini')

If the filename is relative, it is resolved relative to the file where the
``add`` method was called. Check the documentation of the fileconfig_ package
for details.

Load your feature system:

.. code:: python

    >>> fs = features.FeatureSystem('vowels')

    >>> fs
    <FeatureSystem('vowels') of 12 atoms 55 featuresets>

Retrieve feature sets, extents and intents:

.. code:: python

    >>> print fs('+high')
    [+high -low]

    >>> fs('high round').concept.extent
    (u'y', u'u')

    >>> fs.lattice[('i', 'e', 'o')].intent
    (u'-low',)

Logical relations between feature pairs:

.. code:: python

    >>> fs.context.relations()  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    [<u'+high' Complement u'-high'>, <u'+low' Complement u'-low'>,
     <u'+back' Complement u'-back'>, <u'+round' Complement u'-round'>,
     <u'+high' Incompatible u'+low'>,
     <u'+high' Implication u'-low'>, <u'+low' Implication u'-high'>,
     <u'-high' Subcontrary u'-low'>,
     <u'+high' Orthogonal u'+back'>, <u'+high' Orthogonal u'-back'>,
     ...


Further reading
---------------

- http://www.upriss.org.uk/fca/


See also
--------

- concepts_ |--| Formal Concept Analysis with Python
- fileconfig_ |--| Config file sections as objects
- graphviz__ |--| Simple Python interface for Graphviz

.. __: http://pypi.python.org/pypi/graphviz


License
-------

Features is distributed under the `MIT license`_.


.. _Graphviz: http://www.graphviz.org
.. _Formal Concept Analysis: http://en.wikipedia.org/wiki/Formal_concept_analysis

.. _concepts: http://pypi.python.org/pypi/concepts
.. _fileconfig: http://pypi.python.org/pypi/fileconfig

.. _MIT license: http://opensource.org/licenses/MIT


.. |--| unicode:: U+2013


.. |PyPI version| image:: https://pypip.in/v/features/badge.png
    :target: https://pypi.python.org/pypi/features
    :alt: Latest PyPI Version
.. |License| image:: https://pypip.in/license/features/badge.png
    :target: https://pypi.python.org/pypi/features
    :alt: License
.. |Downloads| image:: https://pypip.in/d/features/badge.png
    :target: https://pypi.python.org/pypi/features
    :alt: Downloads
