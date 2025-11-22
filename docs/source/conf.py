# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../../"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "adf-core-python"
copyright = "2024, Haruki Uehara, Yuki Shimada"
author = "Haruki Uehara, Yuki Shimada"
release = "0.2.2"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "myst_parser",
    "sphinxcontrib.mermaid",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"

html_sidebars = {
    "**": ["navbar-logo.html", "versions.html", "search-button-field.html", "sbt-sidebar-nav.html"]
}

html_static_path = ["_static"]

locale_dirs = ["locale"]
language = "en"

# get the environment variable build_all_docs and pages_root
build_all_docs = os.environ.get("build_all_docs")
pages_root = os.environ.get("pages_root", "")

# if not there, we dont call this
if build_all_docs is not None:
    current_language = os.environ.get("current_language")

    html_context = {
        'current_language' : current_language,
        'languages' : [],
    }

    html_context['languages'].append(['en', pages_root])
    html_context['languages'].append(['ja', pages_root+'/ja'])
