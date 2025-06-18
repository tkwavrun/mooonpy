# mooonpy

## Notes on making docs
https://redandgreen.co.uk/sphinx-to-github-pages-via-github-actions/
https://github.com/RGGH/jubilant-lamp/tree/master
https://www.youtube.com/watch?v=bjUkCCn2VoU&t=291s

## Start docs build process
sphinx-quickstart
make html

## Update docs by running in mooonpy
sphinx-apidoc -o docs src/mooonpy


## Learning Sphinx
1. In docs directory:
   * sphinx-quickstart
   
2. In highesht level directory:
   * sphinx-apidoc -o docs mooonpy
   
3. In docs directory:
   * make html
