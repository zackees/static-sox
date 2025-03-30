"""
Setup file.
"""

import os
import re

from setuptools import setup

URL = "https://github.com/zackees/static-sox"
KEYWORDS = "sox static binaries pysox"
HERE = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    setup(
        maintainer="Zachary Vorhies",
        keywords=KEYWORDS,
        url=URL,
        include_package_data=True)
