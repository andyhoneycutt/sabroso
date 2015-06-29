"""
common.py

This module contains the accessor to save the
common data type into MongoDB.
"""

__author__ = 'Alan Barber'

#python


class CommonMongoAccessor(object):

    def __init__(self, session):
        self._session = session

    def create(self, project, common):
        self._session[project].insert_one(common._asdict())

    def query(self, project, data_type, tag_query):
        pass

    def update(self, project, common):
        pass

    def delete(self, project, data_type, tag_query):
        pass
