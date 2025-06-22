# This script is meant for quick Git pushes for Josh's development purposes
cd docs/
make clean
cd ../

git pull
git add .
git commit -m "gpush.sh quick - JDK"
git push origin main
