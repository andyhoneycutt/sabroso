"""
test_persistence_models.py

This module contains tests for models.persistence.

"""

__author__ = 'Alan Barber'

#python
import unittest

#app
from application.models.persistence import (
    CommonPersistence)

class TestCommonPersistence(unittest.TestCase):

    def setUp(self):
        """
        Set up tests.
        """
        self.type = "type"
        self.data = "data"
        self.hash = "AAAA!!!!"
        self.tags = {
            "tag1": "value1",
            "tag2": "value2"
            }
        self.linked = [
            "link1",
            "link2"
        ]
        self.test_model = CommonPersistence(
            type = self.type,
            data = self.data,
            hash = self.hash,
            tags = self.tags,
            linked = self.linked)


    def test_create_model(self):
        """
        Test that model is created correctly.
        """
        self.assertEqual(
            self.test_model.type,
            self.type)
        self.assertEqual(
            self.test_model.hash,
            self.hash)
        self.assertEqual(
            self.test_model.data,
            self.data
        )
        self.assertEqual(
            self.test_model.tags,
            self.tags
        )
        self.assertEqual(
            self.test_model.linked,
            self.linked
        )

if __name__ == '__main__':
    unittest.main()
