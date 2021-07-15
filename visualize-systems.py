#!/usr/bin/env python3
# visualize-systems.py

import features.visualize

DIRECTORY = 'visualize-output'

FORMAT = 'pdf'

features.visualize.render_all(directory=DIRECTORY, format=FORMAT)
