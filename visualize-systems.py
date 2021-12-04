#!/usr/bin/env python3

import features.visualize

DIRECTORY = 'visualize-output'

FORMAT = 'pdf'


features.visualize.render_all(directory=DIRECTORY, format=FORMAT)
