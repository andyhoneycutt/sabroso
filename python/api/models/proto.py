import bson
from bson.objectid import ObjectId
import pymongo

class Proto(object):

    def __init__(self, session, id = None):
        self.session = session
        self._id = id

        if id is not None:
            if bson.objectid.ObjectId.is_valid(id):
                self._id = ObjectId(id)
            else:
                self._id = id

    def _typeName(self):
        return self.__class__.__name__

    def _documentName(self):
        return str.lower(self._typeName())

    def getId(self):
        if type(self._id) is bson.objectid.ObjectId:
            return str(self._id)
        return self._id

    def Get(self):
        data = None
        if self.session is None:
            return data

        if self._id is None:
            return data

        if type(self.session) is pymongo.database.Database:
            db = self.session
            data = db[self._documentName()].find_one({"_id" : ObjectId(self.getId())})

        return data
