#!flask/bin/python
from flask import Flask, abort, make_response
from pymongo import MongoClient
import json
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

""" Try to get a connection to MongoDB, or fail out """
try:
    db = MongoClient('localhost')
except pymongo.errors.ConnectionFailure:
    exit("Could not connect to MongoDB is it running?")

""" Get a list of projects """
@app.route('/api/v1.0/projects', methods=['GET'])
def get_projects():
    projects = [project for project in db.sabroso.projects.find()]
    return toJson(projects)

""" Get a single project by _id """
@app.route('/api/v1.0/projects/<_id>', methods=['GET'])
def get_project(_id):
    if not _id:
        abort(404)

    project = db.sabroso.projects.find_one({"_id" : ObjectId(_id)})
    return toJson(project)

""" Put a project """
""" TODO: Use the ProjectAccessor for this task """
@app.route('/api/v1.0/projects', methods=['POST'])
def put_project():
    if not 'name' in request.json:
        abort(400)

""" Make the 404 handler spit out JSON instead of html """
@app.errorhandler(404)
def not_found(error):
    return make_response(toJson({'error': 'Not found'}), 404)

""" Handle 400 Bad Requests """
@app.errorhandler(400)
def bad_request(error):
    return make_response(toJson({'error': 'Bad Request'}), 400)

""" Convert data into json format for api presentation """
def toJson(data):
    return json.dumps(cursor_data, default=json_util.default)

if __name__ == '__main__':
    app.run(debug=True)
