"""
test_registry.py

This module contains tests for utils.registry.

"""

__author__ = 'Alan Barber'

#python
import unittest

#app
from application.utils.registry import (
    Registry)

class TestCommonPersistence(unittest.TestCase):

    def setUp(self):
        """
        Set up tests.
        """
        self.registry = Registry("Registry1")


    def test_create_registry_error(self):
        with self.assertRaises(ValueError):
            Registry("bad.registry")

    def test_registry_add_and_call_function(self):
        self.registry.add("new", lambda x: x+x)
        self.assertEqual(
            self.registry.call("new", 1),
            2
        )

    def test_registry_add_and_get_function(self):
        self.registry.add("new", lambda x: x+x)
        self.assertEqual(
            self.registry.get("new")(1),
            2
        )


if __name__ == '__main__':
    unittest.main()
