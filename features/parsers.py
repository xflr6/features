# parsers.py - extract kown features from string

import re
from itertools import permutations

from ._compat import map

from . import tools

__all__ = ['Parser']


remove_sign = tools.generic_translate(delete='+-')

remove_sign_sp = tools.generic_translate(delete='+- ')


def make_regex(string):
    """Regex string for optionally signed binary or privative feature.

    >>> [make_regex(s) for s in '+spam -spam spam'.split()]
    ['([+]?spam)', '(-spam)', '(spam)']

    >>> make_regex('+eggs-spam')
    Traceback (most recent call last):
        ...
    ValueError: inappropriate feature name: '+eggs-spam'

    >>> make_regex('')
    Traceback (most recent call last):
        ...
    ValueError: inappropriate feature name: ''
    """
    if string and string[0] in '+-':
        sign, name = string[0], string[1:]
        if not name or '+' in name or '-' in name:
            raise ValueError('inappropriate feature name: %r' % string)

        tmpl = r'([+]?%s)' if sign == '+' else r'(-%s)'
        return tmpl % name

    if not string or '+' in string or '-' in string:
        raise ValueError('inappropriate feature name: %r' % string)

    return r'(%s)' % string


def substring_names(features):
    """Yield all feature name pairs in substring relation.

    >>> list(substring_names(['+spam', '-ham', '+pam']))
    [('pam', 'spam')]
    """
    names = tools.uniqued(map(remove_sign, features))
    for l, r in permutations(names, 2):
        if l in r:
            yield (l, r)


class Parser(object):
    """Extract known features from a string.

    >>> Parser(['+masc', '-ma'])
    Traceback (most recent call last):
        ...
    ValueError: feature names in substring relation: [('ma', 'masc')]

    >>> parse = Parser(['+1', '-1', 'sg', 'pl'])

    >>> parse('+sg 1')
    ['sg', '+1']

    >>> parse('1PL')
    ['+1', 'pl']

    >>> parse('spam')
    Traceback (most recent call last):
        ...
    ValueError: unmatched feature splitting 'spam', known features: ['+1', '-1', 'sg', 'pl']
    """

    make_regex = staticmethod(make_regex)

    def __init__(self, features):
        ambiguous = list(substring_names(features))
        if ambiguous:
            raise ValueError('feature names in substring relation:'
                             ' %r' % ambiguous)

        regexes = map(self.make_regex, features)
        pattern = r'(?i)(?:%s)' % '|'.join(regexes)
        self.features = features
        self.regex = re.compile(pattern)

    def __call__(self, string):
        indexes = (ma.lastindex - 1 for ma in self.regex.finditer(string))
        features = list(map(self.features.__getitem__, indexes))

        if (len(remove_sign_sp(string))
            != len(remove_sign_sp(''.join(features)))):
            raise ValueError('unmatched feature splitting %r,'
                             ' known features: %r' % (string, self.features))

        return features
