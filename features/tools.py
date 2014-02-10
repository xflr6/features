# tools.py

from itertools import izip
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
    """Yield all items from iterable except the last one.

    >>> list(butlast(['spam', 'eggs', 'ham']))
    ['spam', 'eggs']

    >>> list(butlast(['spam']))
    []

    >>> list(butlast([]))
    []
    """
    iterable = iter(iterable)
    first = next(iterable)
    for second in iterable:
        yield first
        first = second


def generic_translate(frm=None, to=None, delete=''):
    """Return a translate function for strings and unicode.

    >>> translate = generic_translate('Hoy', 'Bad', 'r')

    >>> translate('Holy grail')
    'Bald gail'

    >>> translate(u'Holy grail')
    u'Bald gail'
    """
    delete_dict = dict.fromkeys(ord(unicode(d)) for d in delete)

    if frm is None and to is None:
        string_trans = None
        unicode_table = delete_dict
    else:
        string_trans = string.maketrans(frm, to)
        unicode_table = dict((ord(unicode(f)), unicode(t))
            for f, t in izip(frm, to), **delete_dict)

    string_args = (string_trans, delete) if delete else (string_trans,)

    translate_args = [string_args, (unicode_table,)]

    def translate(basestr):
        args = translate_args[isinstance(basestr, unicode)]
        return basestr.translate(*args)

    return translate
