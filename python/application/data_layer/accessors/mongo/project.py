"""
project.py

This module contains the accessor to save the
project models into MongoDB.
"""

__author__ = 'Alan Barber'

#python


class ProjectAccessor(object):

    def __init__(
            self, session,
            project_collection="_project"):
        """
        Create new project accessor.
        """
        self._session = session
        self._collection = self._session[project_collection]
        if not 'name_index' in self._collection.index_information():
            self._session[self._collection].create_index(
                'name', name='name_index', unique=True)

    def create(self, project):
        self._collection.insert_one(project._asdict())

    def query(self, name):
        pass

    def update(self, project):
        pass

    def delete(self, project):
        pass
