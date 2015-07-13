"""
settings.py

Configuration for the API package
  - mongo connection settings
  - mongo default database
"""
__author__ = 'Andy Honeycutt'

import pymongo

mongo_settings = {
  'host' : 'localhost',
  'database' : 'sabroso',
  'username' : '',
  'password' : '',
  'port' : ''
}

""" Try to get a connection to MongoDB, or fail out """
try:
    connection_string = 'mongodb://'
    if mongo_settings['username'] != '' and mongo_settings['password'] != '':
        connection_string = connection_string + mongo_settings['username'] + ':' + mongo_settings['password'] + '@'
    connection_string = connection_string + mongo_settings['host']
    if mongo_settings['port'] != '':
        connection_string = connection_string + ':' + mongo_settings['port']
    connection_string = connection_string + '/'
    mongo_connection = pymongo.MongoClient(connection_string)
    
    db = mongo_connection[mongo_settings['database']]
except pymongo.errors.ConnectionFailure:
    exit("Could not connect to MongoDB is it running?")
