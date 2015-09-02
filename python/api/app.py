#!flask/bin/python
"""
app.py

TODO: We need to abstract database handling and record
stuff away from being mongo centric. Right now we have specific
mongo errors being handled all over the place. Need to come up
with a common data handler. Please, sweet baby jesus, do this
soon.
"""
from flask import Flask, abort, make_response, g, request
from bson import json_util, errors
from bson.objectid import ObjectId
import pymongo
import json
import bson
from models.proto import Proto
from models.project import Project

app = Flask(__name__)
#app.config.from_object('settings.DefaultSettings')
app.config.from_object('settings.DebugSettings')
app_endpoint = app.config['APP_ENDPOINT']

""" Get a list of projects """
@app.route(app_endpoint + '/projects/', methods=['GET'])
def get_projects():
    try:
        projects = [project for project in get_database().project.find()]
    except (
        pymongo.errors.ServerSelectionTimeoutError,
        pymongo.errors.NetworkTimeout,
        pymongo.errors.ConnectionFailure
    ):
        abort(500)
    except pymongo.errors.AutoReconnect:
        print("Had to reconnect, we can keep working")
    return toJson(projects)

""" Get a single project by _id """
@app.route(app_endpoint + '/projects/<path:_id>/', methods=['GET'])
def get_project(_id):
    if not _id:
        abort(404)
    try:
        project = Project(get_database(), id = _id)
    except bson.errors.InvalidId:
        abort(400)
    except pymongo.errors.ServerSelectionTimeoutError:
        abort(500)
    except pymongo.errors.AutoReconnect:
        print("Had to reconnect, we can keep working")

    return toJson(project.Get())

""" Put a project """
""" TODO: Use the ProjectAccessor for this task """
@app.route(app_endpoint + '/projects/', methods=['POST','PUT'])
def put_project():
    if not 'name' in request.json:
        abort(400)
    return make_response(toJson(request.json), 201)

""" Make the 404 handler spit out JSON instead of html """
@app.errorhandler(404)
def not_found(error):
    return make_response(toJson({'error': 'Not found'}), 404)

""" Handle 400 Bad Requests """
@app.errorhandler(400)
def bad_request(error):
    return make_response(toJson({'error': 'Bad Request'}), 400)

""" Handle 500 Internal Server Error """
@app.errorhandler(500)
def internal_server_error(error):
    return make_response(toJson({'error': 'Internal Server Error'}), 500)

""" Close stuff out """
@app.teardown_appcontext
def do_teardown(error):
    close_database_connections(error)

""" Close Database Connections """
def close_database_connections(error):
    if hasattr(g, 'mongodb'):
        try:
            g.mongodb.client.close()
        except TypeError as e:
            print ("It looks like we lost mongodb before clean connection close, did it die?\n\t%s" % str(e))

""" Convert data into json format for api presentation """
def toJson(data):
    return json.dumps(data, default=json_util.default)

""" Get a connection to our database """
def get_database():
    if not hasattr(g, 'mongodb'):
        g.mongodb = connectToMongoDb()

    return g.mongodb

""" Connect to mongodb """
def connectToMongoDb():
    try:
        mongo_connection = pymongo.MongoClient(app.config['MONGO_CONNECTION_URI'])
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to mongodb, is it running?\n\t%s" % str(e))
        abort(500)

    db = mongo_connection[app.config['MONGO_DATABASE']]

    return db

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
