Features
========

|PyPI version| |License| |Supported Python| |Format|

|Build| |Codecov| |Readthedocs-stable| |Readthedocs-latest|

Features is a simple implementation of **feature set algebra** in Python.

Linguistic analyses commonly use sets of **binary or privative features** to
refer to different groups of linguistic objects: for example a group of
*phonemes* that share some phonological features like ``[-consonantal, +high]``
or a set of *morphemes* that occur in context of a specific person/number
combination like ``[-participant, GROUP]``. Usually, the features are applied in
a way such that only **some of their combinations are valid**, while others are
impossible (i.e. refer to no object) |--| for example ``[+high, +low]``, or
``[-participant, +speaker]``.

With this package, such feature systems can be defined with a simple contingency
**table definition** (feature matrix) and stored under a section name in a
simple clear-text **configuration file**. Each feature system can then be
**loaded** by its name and provides its own ``FeatureSet`` subclass that
implements all **comparisons and operations** between its feature sets according
to the given definition (compatibility, entailment, intersection, unification,
etc.).

Features creates the **complete lattice** structure between the possible feature
sets of each feature system and lets you navigate and **visualize their
relations** using the `Graphviz graph layout software`_.


Links
-----

- GitHub: https://github.com/xflr6/features
- PyPI: https://pypi.org/project/features/
- Documentation: https://features.readthedocs.io
- Changelog: https://features.readthedocs.io/en/latest/changelog.html
- Issue Tracker: https://github.com/xflr6/features/issues
- Download: https://pypi.org/project/features/#files


Installation
------------

This package runs under Python 3.6+, use pip_ to install:

.. code:: bash

    $ pip install features

This will also install the concepts_ package from PyPI providing the `Formal
Concept Analysis`_ (FCA) algorithms on which this package is based.


Quickstart
----------

Load a **predefined feature system** by name (in this case features for a
six-way person/number distinction, cf. the definitions in the bundled
``config.ini`` in the `source repository`_). 

.. code:: python

    >>> import features

    >>> fs = features.FeatureSystem('plural')

    >>> print(fs.context)  # doctest: +ELLIPSIS
    <Context object mapping 6 objects to 10 properties [3011c283] at 0x...>
          |+1|-1|+2|-2|+3|-3|+sg|+pl|-sg|-pl|
        1s|X |  |  |X |  |X |X  |   |   |X  |
        1p|X |  |  |X |  |X |   |X  |X  |   |
        2s|  |X |X |  |  |X |X  |   |   |X  |
        2p|  |X |X |  |  |X |   |X  |X  |   |
        3s|  |X |  |X |X |  |X  |   |   |X  |
        3p|  |X |  |X |X |  |   |X  |X  |   |


Create **feature sets** from strings or string sequences. Use **feature string
parsing**, get back string sequences and feature or extent strings in
their canonical order (definition order):

.. code:: python

    >>> fs('+1 +sg'), fs(['+2', '+2', '+sg']), fs(['+sg', '+3'])
    (FeatureSet('+1 +sg'), FeatureSet('+2 +sg'), FeatureSet('+3 +sg'))

    >>> fs('SG1').concept.intent
    ('+1', '-2', '-3', '+sg', '-pl')

    >>> fs('1').string, fs('1').string_maximal, fs('1').string_extent
    ('+1', '+1 -2 -3', '1s 1p')


Use **feature algebra**: intersection (`join`) , union/unification (`meet`),
set inclusion (`extension/subsumption`). Do feature set comparisons
(`logical connectives`_).

.. code:: python

    >>> fs('+1 +sg') % fs('+2 +sg')
    FeatureSet('-3 +sg')

    >>> fs('-3') ^ fs('+1') ^ fs('-pl')
    FeatureSet('+1 +sg')

    >>> fs('+3') > fs('-1') and fs('+pl') < fs('+2 -sg')
    True

    >>> fs('+1').incompatible_with(fs('+3')) and fs('+sg').complement_of(fs('+pl'))
    True


Navigate the created subsumption lattice_ (`Hasse graph`_) of **all valid
feature sets**:

.. code:: python

    >>> fs('+1').upper_neighbors, fs('+1').lower_neighbors
    ([FeatureSet('-3'), FeatureSet('-2')], [FeatureSet('+1 +sg'), FeatureSet('+1 +pl')])

    >>> fs('+1').upset()
    [FeatureSet('+1'), FeatureSet('-3'), FeatureSet('-2'), FeatureSet('')]

    >>> for f in fs:  # doctest: +ELLIPSIS
    ...     print(f'[{f.string_maximal}] <-> {{{f.string_extent}}}')
    [+1 -1 +2 -2 +3 -3 +sg +pl -sg -pl] <-> {}
    [+1 -2 -3 +sg -pl] <-> {1s}
    ...
    [-1] <-> {2s 2p 3s 3p}
    [] <-> {1s 1p 2s 2p 3s 3p}


See `the docs`_ on how to define, load, and use **your own feature systems**.


Further reading
---------------

- https://en.wikipedia.org/wiki/Join_and_meet
- https://en.wikipedia.org/wiki/Formal_concept_analysis
- http://www.upriss.org.uk/fca/


See also
--------

- concepts_ |--| Formal Concept Analysis with Python
- fileconfig_ |--| Config file sections as objects
- graphviz_ |--| Simple Python interface for Graphviz


License
-------

Features is distributed under the `MIT license`_.


.. _pip: https://pip.readthedocs.io

.. _Graphviz graph layout software: http://www.graphviz.org
.. _Formal Concept Analysis: https://en.wikipedia.org/wiki/Formal_concept_analysis
.. _source repository: https://github.com/xflr6/features/blob/master/features/config.ini
.. _logical connectives: https://en.wikipedia.org/wiki/Template:Logical_connectives_table_and_Hasse_diagram
.. _lattice: https://en.wikipedia.org/wiki/Lattice_(order)
.. _Hasse graph: https://en.wikipedia.org/wiki/Hasse_diagram
.. _the docs: https://features.readthedocs.io/en/stable/manual.html

.. _concepts: https://pypi.org/project/concepts/
.. _fileconfig: https://pypi.org/project/fileconfig/
.. _graphviz: https://pypi.org/project/graphviz/

.. _MIT license: https://opensource.org/licenses/MIT


.. |--| unicode:: U+2013


.. |PyPI version| image:: https://img.shields.io/pypi/v/features.svg
    :target: https://pypi.org/project/features/
    :alt: Latest PyPI Version
.. |License| image:: https://img.shields.io/pypi/l/features.svg
    :target: https://pypi.org/project/features/
    :alt: License
.. |Supported Python| image:: https://img.shields.io/pypi/pyversions/features.svg
    :target: https://pypi.org/project/features/
    :alt: Supported Python Versions
.. |Format| image:: https://img.shields.io/pypi/format/features.svg
    :target: https://pypi.org/project/features/
    :alt: Format

.. |Build| image:: https://github.com/xflr6/features/actions/workflows/build.yaml/badge.svg
    :target: https://github.com/xflr6/features/actions/workflows/build.yaml?query=branch%3Amaster
    :alt: Build
.. |Codecov| image:: https://codecov.io/gh/xflr6/features/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/xflr6/features
    :alt: Codecov
.. |Readthedocs-stable| image:: https://readthedocs.org/projects/features/badge/?version=stable
    :target: https://features.readthedocs.io/en/stable/?badge=stable
    :alt: Readthedocs stable
.. |Readthedocs-latest| image:: https://readthedocs.org/projects/features/badge/?version=latest
    :target: https://features.readthedocs.io/en/latest/?badge=latest
    :alt: Readthedocs latest
