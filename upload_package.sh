#!/bin/bash
set -e
rm -rf build dist
. ./activate.sh
pip install wheel twine
echo "Building Source and Wheel (universal) distribution…"
python3 setup.py bdist_wheel --universal
echo "Uploading the package to PyPI via Twine…"
twine upload dist/* --verbose
# echo Pushing git tags…
