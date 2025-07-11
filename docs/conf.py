# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os
sys.path.insert(0, os.path.abspath('../src/'))

project = 'mooonpy'
copyright = '2025, Kemppainen-Muzzy'
author = 'Josh Kemppainen, Tristan Muzzy'
release = '0.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo',
              'sphinx.ext.viewcode',
              'sphinx.ext.autodoc',
              'matplotlib.sphinxext.plot_directive'
]

todo_include_todos = True
add_module_names = True

# Control how Sphinx documents class docstrings
#  'class' -> Only documents top of class and methods
#  'init'  -> Only documents __init__
#  'both'  -> Documents top of class, methods, and __init__
autoclass_content = 'both'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# https://sphinx-themes.org/

#html_theme = 'sphinx_book_theme'
html_theme = 'sphinx_rtd_theme'
#html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
