import app
from app import get_database
import os
import json
from bson.objectid import ObjectId
import unittest
import settings
import datetime

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

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app
        self.app.config.from_object('settings.TestingSettings')
        self.test_client = self.app.test_client(self)

        # clear out testing database, make sure we start anew
        with app.app.app_context():
            get_database().projects.remove()

    def tearDown(self):
        # clear out testing database
        with app.app.app_context():
            get_database().projects.remove()

    """
    Make sure we get a json list of projects back
    """
    def test_get_projects(self):
        # insert a project into testing database
        project = test_data_get_projects

        with app.app.app_context():
            project_id = get_database().projects.insert_one(project)

        project['_id'] = {'$oid': str(ObjectId(project_id.inserted_id))}

        response = self.test_client.get(self.app.config['APP_ENDPOINT'] + '/projects/', content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [project])

    """
    GET a single project
    """
    def test_get_project(self):
        # insert a project into testing database
        project = test_data_get_project

        with app.app.app_context():
            project_id = get_database().projects.insert_one(project)

        project_id_str = str(ObjectId(project_id.inserted_id))
        project['_id'] = {'$oid': project_id_str}

        response = self.test_client.get(self.app.config['APP_ENDPOINT'] + '/projects/' + project_id_str + '/', content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, project)

    """
    POST a project
    """
    def test_post_project(self):
        response = self.test_client.post(self.app.config['APP_ENDPOINT'] + '/projects/', data=json.dumps(test_data_put_project), content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, test_data_put_project)

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
        self.assertEqual(data, test_data_put_project)

    """
    PUT a project with invalid data
    """
    def test_put_project_invalid_json(self):
        response = self.test_client.put(self.app.config['APP_ENDPOINT'] + '/projects/', data="this is not json", content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
