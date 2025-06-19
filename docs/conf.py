# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os
sys.path.insert(0, os.path.abspath('../'))

project = 'mooonpy'
copyright = '2025, Kemppainen-Muzzy'
author = 'Josh Kemppainen, Tristan Muzzy'
release = '0.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc']
todo_include_todos = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# https://sphinx-themes.org/

html_theme = 'sphinx_rtd_theme'
#import sphinx_pdj_theme
#html_theme = 'sphinx_pdj_theme'
#html_theme_path = [sphinx_pdj_theme.get_html_theme_path()]
html_static_path = ['_static']
