# -*- coding: utf-8 -*-
"""
This module shows a few doc string examples for how
to write doc strings for automatic Sphinx documentation.

This module will eventually be deleted once all developers
understand doc strings and the syntax for sphinx.

The following is a good resource:
    https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html
"""



def greeter_msg(*, greeter: str) -> str:
    """
    Custom greeting

    :param greeter: name of a person who message will be from
    :type greeter: str
    :return: a greeting from the greeter
    :rtype: str
    """
    return f"Hello to you from {greeter}"