"""Sphinx configuration."""
project = "EditorConfig Python Validator"
author = "Trey Hunner"
copyright = "2022, Trey Hunner"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
]
autodoc_typehints = "description"
html_theme = "furo"
