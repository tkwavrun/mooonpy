# This bash script is meant to manually build the html docs for quick
# testing and deployment, before letting the GitHub actions build and
# publish the online versions.
cd ../
sphinx-apidoc -o docs .
cd docs/

make clean
make html
