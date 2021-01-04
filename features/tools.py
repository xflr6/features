# tools.py

import string

__all__ = ['uniqued', 'butlast', 'generic_translate']


def uniqued(iterable):
    """Return unique list of items preserving order.

    >>> uniqued([3, 2, 1, 3, 2, 1, 0])
    [3, 2, 1, 0]
    """
    seen = set()
    add = seen.add
    return [i for i in iterable if i not in seen and not add(i)]


def butlast(iterable):
    """Yield all items from ``iterable`` except the last one.

    >>> list(butlast(['spam', 'eggs', 'ham']))
    ['spam', 'eggs']

    >>> list(butlast(['spam']))
    []

    >>> list(butlast([]))
    []
    """
    iterable = iter(iterable)
    try:
        first = next(iterable)
    except StopIteration:
        return
    for second in iterable:
        yield first
        first = second


def generic_translate(frm=None, to=None, delete=''):
    """Return a translate function for strings and unicode.

    >>> translate = generic_translate('Hoy', 'Bad', 'r')

    >>> translate('Holy grail')
    'Bald gail'
    """
    string_trans = str.maketrans(frm or '', to or '', delete or '')

    def translate(basestr):
        return basestr.translate(string_trans)

    return translate
