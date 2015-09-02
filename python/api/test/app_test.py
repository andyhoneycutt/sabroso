import app
from app import get_database
import os
import json
from bson.objectid import ObjectId
import unittest
import settings
import datetime
from models.proto import Proto
from models.project import Project

"""
TODO: better fixtures
"""
test_data_get_projects = {
    "name" : "Test Project List",
    "created_on" : str(datetime.datetime.now())
}

test_data_get_project = {
    "name" : "Test Project Single",
    "created_on" : str(datetime.datetime.now())
}

test_data_put_project = {
    "name" : "Test Put Project",
    "created_on" : str(datetime.datetime.now())
}

test_data_post_project = {
    "name" : "Test Post Project",
    "created_on" : str(datetime.datetime.now())
}

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app
        self.app.config.from_object('settings.TestingSettings')
        self.test_client = self.app.test_client(self)

        # clear out testing database, make sure we start anew
        with app.app.app_context():
            get_database().project.delete_many({})

    def tearDown(self):
        # clear out testing database
        with app.app.app_context():
            get_database().project.delete_many({})

    """
    Make sure we get a json list of projects back
    """
    def test_get_projects(self):
        # insert a project into testing database
        project_data = test_data_get_projects

        with app.app.app_context():
            project = Project(get_database())
            project.Create(name=project_data['name'], created_on=project_data['created_on'])

        response = self.test_client.get(self.app.config['APP_ENDPOINT'] + '/projects/', content_type='application/json')
        data = json.loads(response.data.decode())

        # We have to convert the json oid to an actual ObjectId to match Project class
        for d in data:
            d['_id'] = ObjectId(d['_id']['$oid'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [project.Get()])

    """
    GET a single project
    """
    def test_get_project(self):
        # insert a project into testing database
        project_data = test_data_get_project

        with app.app.app_context():
            project = Project(get_database())
            project.Create(name=project_data['name'], created_on=project_data['created_on'])

        response = self.test_client.get(self.app.config['APP_ENDPOINT'] + '/projects/' + project.getId() + '/', content_type='application/json')
        data = json.loads(response.data.decode())

        # We have to convert the json oid to an actual ObjectId to match Project class
        data['_id'] = ObjectId(data['_id']['$oid'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, project.Get())

    """
    POST a project
    """
    def test_post_project(self):
        response = self.test_client.post(self.app.config['APP_ENDPOINT'] + '/projects/', data=json.dumps(test_data_post_project), content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], test_data_post_project['name'])
        self.assertEqual(data['created_on'], test_data_post_project['created_on'])
        self.assertIsNotNone(data['_id'])
        self.assertIsValidObjectId(data['_id']['$oid'])

    """
    POST a project with invalid data
    """
    def test_post_project_invalid_json(self):
        response = self.test_client.post(self.app.config['APP_ENDPOINT'] + '/projects/', data="this is not json", content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)

    """
    PUT a project
    """
    def test_put_project(self):
        response = self.test_client.put(self.app.config['APP_ENDPOINT'] + '/projects/', data=json.dumps(test_data_put_project), content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], test_data_put_project['name'])
        self.assertEqual(data['created_on'], test_data_put_project['created_on'])
        self.assertIsNotNone(data['_id'])
        self.assertIsValidObjectId(data['_id']['$oid'])

    """
    PUT a project with invalid data
    """
    def test_put_project_invalid_json(self):
        response = self.test_client.put(self.app.config['APP_ENDPOINT'] + '/projects/', data="this is not json", content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)

    def assertIsNotNone(self, value):
        assert value is not None

    def assertIsValidObjectId(self, value):
        assert ObjectId.is_valid(value)

if __name__ == '__main__':
    unittest.main()
