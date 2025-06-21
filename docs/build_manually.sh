# This bash script is meant to manually build the html docs for quick
# testing and deployment, before letting the GitHub actions build and
# publish the online versions.

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
sphinx-apidoc -o docs .
cd docs/

make clean
make html
