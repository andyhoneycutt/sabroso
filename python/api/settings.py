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
    PORT = 5000
    """
    Configure the below for current api version as
    all requests must be directed to app_endpoint/<whatever>
    e.g. '/api/v1.0/projects/abcd1234', this handles the
    /api/v1.0 part of uri access
    """
    base_endpoint = '/api'
    version = 'v1.0'
    url = '/'
    APP_ENDPOINT = url.join([base_endpoint, version])

class DebugSettings(DefaultSettings):
    DEBUG = True

class TestingSettings(DefaultSettings):
    MONGO_DATABASE = 'sabroso_testing'
    TESTING = True
    DEBUG = True
    PORT = 8271
