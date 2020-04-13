#!/usr/bin/env python

import platform
import sys

import pytest

ARGS = [
    #'--pdb',
    #'--exitfirst',
]

if platform.system() == 'Windows':
    if 'idlelib' in sys.modules:
        ARGS.extend(['--capture=sys', '--color=no'])
    elif sys.version_info.major == 2 and 'win_unicode_console' in sys.modules:
        ARGS.append('--capture=sys')

sys.exit(pytest.main(ARGS + sys.argv[1:]))
