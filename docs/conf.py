# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# -- Path setup --------------------------------------------------------------

project = "NC3 E-Learning Platform"
copyright = "2024, NC3 Team <info@nc3.lu>"
author = "NC3 Team <info@nc3.lu>"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom

extensions = [
    "sphinx.ext.autodoc",
    "sphinxcontrib.openapi",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

numfig = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"
html_static_path = ["_static"]

html_title = "E-learning"
html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/NC3-LU/eLearning",
    # "repository_branch": "gh-pages",  # For testing
    "launch_buttons": {
        "binderhub_url": "https://github.com/NC3-LU/eLearning",
    },
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "use_download_button": True,
    "home_page_in_toc": True,
    "navigation_with_keys": True,
    # For testing
    # "use_fullscreen_button": False,
    # "single_page": True,
    # "extra_footer": "<a href='https://google.com'>Test</a>",  # DEPRECATED KEY
    # "extra_navbar": "<a href='https://google.com'>Test</a>",
    # "show_navbar_depth": 2,
}

# -- Options for LaTeX output --------------------------------------------------

latex_engine = "pdflatex"

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    ("index", "E-Learning.tex", "NC3 E-Learning Platform", "NC3-LU", "howto"),
]

latex_show_urls = "footnote"
latex_show_pagerefs = True

ADDITIONAL_PREAMBLE = r"""
\setcounter{tocdepth}{3}
"""
