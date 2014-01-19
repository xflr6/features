# parsers.py - extract kown features from string

from itertools import imap
import re

import tools

__all__ = ['Parser']


remove_sign = tools.generic_translate(delete='+-')

remove_sign_sp = tools.generic_translate(delete='+- ')


def make_regex(string):
    if string[0] in '+-':
        sign, name = string[0], string[1:]
        if not name or '+' in name or '-' in name:
            raise ValueError('Inappropriate feature name: %r' % string)

        tmpl = r'([+]?%s)' if sign == '+' else r'(-%s)'
        return tmpl % name

    if '+' in string or '-' in string:
        raise ValueError('Inappropriate feature name: %r' % string)

    return r'(%s)' % string


class Parser(object):
    """Extract known features from a string.

    >>> parse = Parser(['+1', '-1', 'sg', 'pl'])

    >>> parse('+sg 1')
    ['sg', '+1']

    >>> parse('1PL')
    ['+1', 'pl']
    """

    make_regex = staticmethod(make_regex)

    def __init__(self, features):
        regexes = imap(make_regex, features)
        pattern = r'(?i)(?:%s)' % '|'.join(regexes)
        self.features = features
        self.regex = re.compile(pattern)

    def __call__(self, string):
        indexes = (next(i for i, m in enumerate(ma.groups()) if m)
            for ma in self.regex.finditer(string))

        features = map(self.features.__getitem__, indexes)

        if (len(remove_sign_sp(string)) !=
            len(remove_sign_sp(''.join(features)))):
            raise ValueError('Unmatched feature splitting %r, '
                'known features: %r' % (string, self.features))

        return features


def _test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    _test()
