.. _examples:

Examples
========


Common features from tokens
---------------------------

In this example, we will crate a paradigm for the present and past tense forms
of the English copula *to be* (tokens) and compute the common features for all
different word forms (types).

Define a feature system with the **meanings** for the paradigm cells.

.. code:: python

    >>> import features

    >>> context = '''
    ...         |+1|-1|+2|-2|+3|-3|+sg|+pl|+pst|-pst|
    ... 1sg.pres| X|  |  | X|  | X|  X|   |    |   X|
    ... 1pl.pres| X|  |  | X|  | X|   |  X|    |   X|
    ... 2sg.pres|  | X| X|  |  | X|  X|   |    |   X|
    ... 2pl.pres|  | X| X|  |  | X|   |  X|    |   X|
    ... 3sg.pres|  | X|  | X| X|  |  X|   |    |   X|
    ... 3pl.pres|  | X|  | X| X|  |   |  X|    |   X|
    ... 1sg.past| X|  |  | X|  | X|  X|   |   X|    |
    ... 1pl.past| X|  |  | X|  | X|   |  X|   X|    |
    ... 2sg.past|  | X| X|  |  | X|  X|   |   X|    |
    ... 2pl.past|  | X| X|  |  | X|   |  X|   X|    |
    ... 3sg.past|  | X|  | X| X|  |  X|   |   X|    |
    ... 3pl.past|  | X|  | X| X|  |   |  X|   X|    |'''

    >>> fs = features.make_features(context)

    >>> cellmeanings = fs.atoms

Enter the word **forms** for each cell.

.. code:: python

    >>> cellforms = [
    ...     'am', 'are',
    ...     'are', 'are',
    ...     'is', 'are',
    ... 
    ...     'was', 'were',
    ...     'were', 'were',
    ...     'was', 'were']

Create the **paradigm** as ordered mapping
(:class:`py:collections.OrderedDict`) from meaning to form.

.. code:: python

    >>> from collections import OrderedDict

    >>> paradigm = OrderedDict(zip(cellmeanings, cellforms))

Pretty-print the meaning -> word form mapping.

.. code:: python

    >>> for meaning, form in paradigm.items():
    ...     print('%s | %s' % (meaning.string_extent, form))
    1sg.pres | am
    1pl.pres | are
    2sg.pres | are
    2pl.pres | are
    3sg.pres | is
    3pl.pres | are
    1sg.past | was
    1pl.past | were
    2sg.past | were
    2pl.past | were
    3sg.past | was
    3pl.past | were

Create a **correspondence** from each word form to the list of cell meanings
where it occurs.

.. code:: python

    >>> occurrences = OrderedDict()

    >>> for meaning in paradigm:
    ...     form = paradigm[meaning]
    ...     occurrences.setdefault(form, []).append(meaning)

Pretty-print the form -> occurrences mapping.

.. code:: python

    >>> for form in occurrences:
    ...     meanings = occurrences[form]
    ...     labels = ', '.join(m.string_extent for m in meanings)
    ...     print('%4s | %s' % (form, labels))
      am | 1sg.pres
     are | 1pl.pres, 2sg.pres, 2pl.pres, 3pl.pres
      is | 3sg.pres
     was | 1sg.past, 3sg.past
    were | 1pl.past, 2sg.past, 2pl.past, 3pl.past

Show the **common features** for all word forms, computed with the
:meth:`~.FeatureSystem.join`-method (generalization, `least upper bound`_).

.. code:: python

    >>> for form in occurrences:
    ...     meanings = occurrences[form]
    ...     common = fs.join(meanings)
    ...     print('%4s | %s' % (form, common))
      am | [+1 +sg -pst]
     are | [-pst]
      is | [+3 +sg -pst]
     was | [-2 +sg +pst]
    were | [+pst]

Their **necessary conditions** (common features).


.. _least upper bound: https://en.wikipedia.org/wiki/Join_and_meet
