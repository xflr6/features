Changelog
=========


Version 0.6 (in development)
----------------------------

Switch to pyproject.toml.

Drop Python 2 support.

Drop Python 3.5, 3.6, and 3.7 support and tag Python 3.9, 3.10, and 3.11 support.


Version 0.5.12
--------------

Tag Python 3.8 support.


Version 0.5.11
--------------

Drop Python 3.4 support.


Version 0.5.10
--------------

Tag Python 3.7 support, add simple tox config.


Version 0.5.9
-------------

Increase API docs coverage.

Use compatible release version specifiers (bump ``graphviz`` to ~=0.7).


Version 0.5.8
-------------

Drop Python 3.3 support.

Add LICENCE file to wheel.


Version 0.5.7
-------------

Fix pep-0479 ``StopIteration`` ``DeprecationWarning`` under Python 3.5+


Version 0.5.6
-------------

Port tests from nose/unittest to pytest, add Travis CI and coveralls.

Update meta data, tag Python 3.6 support.


Version 0.5.5
-------------

Simplified feature set string parsing.

Relaxed ``fileconfig``, ``concepts``, and ``graphviz`` dependencies to < 1.0.

Improved documentation.


Version 0.5.4
-------------

Added extended Sphinx-based documentation.

Fixed Python 3.5 compatibility.


Version 0.5.3
-------------

Fixed broken manual install due to ``setuptools`` automatic zip_safe analysis not
working as expected.


Version 0.5.2
-------------

Added ``string_extent`` attribute to feature sets.

Added simple example to README.

Moved feature name sanity checks to parser.


Version 0.5.1
-------------

Added wheel.


Version 0.5
-----------

Added Python 3.3+ support.


Version 0.4.2
-------------

Switch ``setup.py`` dependencies to version ranges.


Version 0.4.1
-------------

Easier customization.

Improved documentation.


Version 0.4
-----------

Added ``add_config()``.

Added ``make_features()``.


Version 0.3
-----------

Added ``orthogonal_to()``.

Rename ``unifcation`()`` to ``union()``.

Improved doctests.


Version 0.2
-----------

Update ``concepts`` dependency to 0.5 and improve separation of concerns.

Changed ``upset`` and ``downset`` from properties to methods (backwards incompatible).

Order downsets longlex instead of shortlex.


Version 0.1.3
-------------

Update ``concepts`` dependency to 0.4.


Version 0.1.2
-------------

Fixed ineffective filename parameter in visualization.


Version 0.1.1
-------------

Fixed missing ``config.ini`` in package with non-source installation.


Version 0.1
-----------

First public release.
