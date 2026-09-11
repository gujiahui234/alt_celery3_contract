"""Sphinx configuration for the alt_celery3_contract documentation."""

project = "alt_celery3_contract"
copyright = "2026, alt_celery3 contract maintainers"
author = "alt_celery3 contract maintainers"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

napoleon_google_docstring = True
napoleon_numpy_docstring = False

autodoc_member_order = "bysource"
autodoc_typehints = "description"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build"]

html_theme = "sphinx_rtd_theme"
