"""
test_common_model.py

This module contains tests for the data layer
common model.

"""

__author__ = 'Alan Barber'

#python
import unittest

#app
from application.data_layer.models.project import (
    Project)

class TestCommonPersistence(unittest.TestCase):

    def setUp(self):
        """
        Set up tests.
        """
        self.name = "Project"
        self.created_on = "date_created"
        self.modified_on = "data_modified"
        self.test_model = Project(
            name=self.name,
            created_on=self.created_on,
            modified_on=self.modified_on)

    def test_create_model(self):
        """
        Test that model is created correctly.
        """
        self.assertEqual(
            self.test_model.name,
            self.name)
        self.assertEqual(
            self.test_model.created_on,
            self.created_on)
        self.assertEqual(
            self.test_model.modified_on,
            self.modified_on
        )
if __name__ == '__main__':
    unittest.main()
