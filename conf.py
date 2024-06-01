import os
import sys
import django

sys.path.insert(0, os.path.abspath("."))

# Nom de la configuration Django que Sphinx doit utiliser
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

# Configuration de l'environnement Django
django.setup()


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


project = "Django-community-forum"
copyright = "2024, ISSAKA HAMA Barhamou"
author = "ISSAKA HAMA Barhamou"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".env_work/*"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
