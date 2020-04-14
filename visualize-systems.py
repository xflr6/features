#!/usr/bin/env python
# visualize-systems.py

import features.visualize

DIRECTORY = 'visualize-output'
FORMAT = 'pdf'

features.visualize.render_all(directory=DIRECTORY, format=FORMAT)
