#!/usr/bin/env bash
# Remove dist folder as it will be generated again in the next step with a new build.
if [ -d "dist" ]
then
echo "Deleting dist directory"
rm -r dist
fi
# Install/update needed tools
python -m pip install --upgrade twine setuptools wheel
# Create new build
python setup.py sdist
# Upload new build to pypi using twine
python -m twine upload dist/*