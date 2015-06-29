"""
test_common_mongo_accessor.py

This module contains tests for the mongo
accessor for the common data model.

"""

__author__ = 'Alan Barber'

#python
import unittest

#3rd party
import pymongo

#app
from application.data_layer.models.common import (
    Common)
from application.data_layer.accessors.mongo.common import (
    CommonMongoAccessor
)

class TestCommonMongoAccessor(unittest.TestCase):

    def setUp(self):
        """
        Set up tests.
        """
        self.project_name = "TestProject"
        self.client = pymongo.MongoClient('localhost')
        self.db = self.client['TestDatabase']
        self.collection = self.db[self.project_name]
        self.accessor = CommonMongoAccessor(self.db)

    def tearDown(self):
        """
        Tear down after tests.
        """

        self.client.drop_database('TestDatabase')

    def test_create_object(self):
        """
        Test that model is created correctly.
        """
        cType, cData, cHash, cTags, cLinked = (
            "type", "data", "hash", "tags",
            "linked"
        )
        to_add = Common(
            type=cType, data=cData,
            hash=cHash, tags = cTags,
            linked=cLinked
        )
        self.accessor.create(
            self.project_name, to_add
        )
        rslts = self.collection.find({
            "hash":cHash
        })
        self.assertEqual(
            len(list(rslts)), 1
        )


if __name__ == '__main__':
    unittest.main()
