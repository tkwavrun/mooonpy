#!/bin/bash
#
# This bash script is meant to manually build the html docs for quick
# testing and deployment, before letting the GitHub actions build and
# publish the online versions.
#
# SCRIPT/PYTHON SETUP:
#   This script requires the packages found in .requirements.txt. To add them 
#   to your Python enviroment run this in the /docs directory:
#     Windows PowerShell:
#       python -m pip install -r requirements.txt
#     Linux commandline:
#       chmod 755 build_manually.sh
#       pip install -r requirements.txt
#
# SCRIPT/BASH RUN:
#     Windows PowerShell (EXPEIRMENTAL):
#     ./build_manually.sh
#
#   Linux commandline:
#     bash build_manually.sh


# Remove old *.rst files except for:
# * index.rst
# * installing.rst
# * examples.rst
echo "Removing old *.rst files"
find . -type f -name "*.rst" \
! -name "index.rst" \
! -name "installing.rst" \
! -name "examples.rst" -delete

cd ../
sphinx-apidoc --force --no-toc --separate --module-first -o docs src
cd docs/

make clean
make html
