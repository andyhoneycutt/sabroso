"""
project.py

This module contains the model for project
management.
"""

__author__ = 'Alan Barber'

#python
from collections import namedtuple

Project = namedtuple(
    'Project',
    [
        "name",
        "created_on",
        "modified_on"
    ])
