"""
registry.py

Registry contains the Registry class,
which is the base class for registered classes
and functions available to the application.
"""

__author__ = 'Alan Barber'

#python

class Registry(object):

    def __init__(self, name):
        self._registry = {}
        if '.' in name:
            raise ValueError(
                "Registry name cannot contain" +\
                "the namespace character '.'"
            )
        self._name = name

    def add(self, name,  func):
        self._registry[name] = func

    def get(self, name):
        return self._registry[name]

    def call(self, name, *args, **kwargs):
        return self._registry[name](
            *args, **kwargs
            )
