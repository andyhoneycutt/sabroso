import bson
from bson.objectid import ObjectId
import pymongo

class Proto(object):

    def __init__(self, session = None, *args, **kwargs):
        self.session = session
        id = kwargs.get('id', None)
        search_by = kwargs.get('search_by', None)

        self._id = id
        self.search_by = search_by

        if id is not None:
            if bson.objectid.ObjectId.is_valid(id):
                self._id = ObjectId(id)

        self.data = self.Get()

    def _typeName(self):
        return self.__class__.__name__

    def _documentName(self):
        return str.lower(self._typeName())

    def getSession(self):
        return self.session

    def getId(self):
        if type(self._id) is bson.objectid.ObjectId:
            return str(self._id)
        return self._id

    def Get(self):
        data = []

        if self.session is None:
            print(self._documentName() + " has no session")
            return data

        if type(self.session) is pymongo.database.Database:
            db = self.session
            do_search = {}

            if self.getId() is not None:
                do_search = {"_id" : ObjectId(self.getId())}
            elif self.search_by is not None:
                do_search = self.search_by
            else:
                print("No way to search for " + self._documentName())
                return data

            try:
                data = db[self._documentName()].find_one(do_search)
                if data is not None and self._id is None:
                    self._id = ObjectId(data['_id'])

            except bson.errors.InvalidId:
                print(self.getId() + " is not a valid ObjectId")

        return data
