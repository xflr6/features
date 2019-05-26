# _compat.py - Python 2/3 compatibility

import sys

PY2 = (sys.version_info.major == 2)


if PY2:
    string_types = basestring

    from itertools import (imap as map,
                           izip as zip)

    def py2_bool_to_nonzero(cls):
        cls.__nonzero__ = cls.__bool__
        del cls.__bool__
        return cls

    import copy_reg as copyreg


else:
    string_types = str

    map, zip = map, zip

    def py2_bool_to_nonzero(cls):
        return cls

    import copyreg


def register_reduce(mcls):
    """Register __reduce__ as reduction function for mcls instances."""
    copyreg.pickle(mcls, mcls.__reduce__)
    return mcls


def with_metaclass(meta, *bases):
    """From Jinja2 (BSD licensed).

    https://github.com/mitsuhiko/jinja2/blob/master/jinja2/_compat.py
    """
    class metaclass(meta):  # noqa: N801
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})
