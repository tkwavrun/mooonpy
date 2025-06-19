# mooonpy documentation generation
## Automatic documentation generation
The GitHub pages documentation should be auto-generated everytime "https://github.com/jdkemppa" commits to the repository. At this point in time no others have the ability to automatically re-generate the sphinx documentation. There are notes below in-case the docs folder needs to be 
rebuilt from scratch, but these are mainly for Josh Kempppainen. Users and developers of mooonpy currently are not given the ability to effect the documentation.


## Notes for rebuilding docs folder from scratch
1. In mooonpy/
   * mkdir docs
   
2. In mooonpy/docs/
   * sphinx-quickstart
   
3. In mooonpy/
   * sphinx-apidoc -o docs mooonpy

4. In mooonpy/docs/
   * Add this to top of conf.py
     - import sys
     - import os
     - sys.path.insert(0, os.path.abspath('../mooonpy'))

   * Change these in conf.py
     - change "extensions" to extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc']
     - change "html_theme" to html_theme = 'sphinx_rtd_theme'

   * In index.rst 
     - add the "modules" keyword near bottom
   
5. In mooonpy/docs/
   * make html

6. In mooonpy/docs/
   * add requirements.txt for GitHub workflow to use adding:
     - sphinx
     - sphinx_rtd_theme
     - ghp-import
   * To allow for the .github/workflows/sphinx.yml file to install dependencies on a container
