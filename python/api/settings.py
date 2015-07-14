"""
settings.py

Configuration for the API package
  - mongo connection settings
  - mongo default database
"""
__author__ = 'Andy Honeycutt'

class DefaultSettings(object):
    MONGO_HOST = 'localhost'
    MONGO_DATABASE = 'sabroso'
    MONGO_CONNECTION_URI = 'mongodb://localhost'
    TESTING = False
    DEBUG = False

class TestingSettings(DefaultSettings):
    MONGO_DATABASE = 'sabroso_testing'
    TESTING = True
    DEBUG = True
