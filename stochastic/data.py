import os.path
import tempfile
import base64
import numpy as np

## Problème du message caché

import pyximport
pyximport.install()

__file = tempfile.mktemp(suffix=".pyx")

with open(__file, 'w') as f:
    f.write('''
def score(candidate, solution="Grab your towel and DON'T PANIC!"):
    """Evaluates a string.

    Usage: score(candidate, solution)
    Coded as: sum(c1 == c2 for c1, c2 in zip(candidate, solution))

    The objective is to find the default string for solution.
    >>> score("poo", solution="foo")
    2

    """
    return sum(c1 == c2 for c1, c2 in zip(candidate, solution))
''')

__data = pyximport.load_module("data", __file, os.path.dirname(__file))

score = __data.score


## Problème des villes

cities = """
Amsterdam Athens    Barcelona Berlin   Bucarest  Budapest Brussels Copenhagen
Dublin    Edinburgh Gibraltar Helsinki Istanbul  Kiev     Lisbon   London
Madrid    Milan     Moscow    Munich   Nantes    Oslo     Paris    Prague
Reykjavik Riga      Rome      Sofia    Stockholm Toulouse Vilnius  Warsaw
"""

cities = cities.split()

distances_base64 = \
"""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
AAAAAAAAAA=="""

__file = tempfile.mktemp(suffix=".npy")

with open(__file, 'wb') as f:
    f.write(base64.decodebytes(distances_base64.encode()))

distances = np.load(__file)
