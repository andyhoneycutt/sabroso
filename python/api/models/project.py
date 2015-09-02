from models.proto import Proto
import pymongo

class Project(Proto):

    def __init__(self, session = None, **kwargs):
        super(Project, self).__init__(session, **kwargs)

    def getData(self, query=None):
        results = []
        data_collection = "project_data_" + self.getId()
        if type(self.session) is pymongo.database.Database:
            results = [data for data in self.session[data_collection].find(query)]

        return results
