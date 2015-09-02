import unittest
import pandas
import math
import pymongo
from pandas.util.testing import assert_frame_equal
import settings
from models.project import Project
from models.proto import Proto
from models.registry import Registry

def doPivot(pivot_config):

    # Shorthand
    filter = pivot_config['filter']
    pivot = pivot_config['pivot']

    # Active Database Connection
    session = get_database()

    # Load project
    project = Project(session, search_by= { 'name' : filter['project'] })

    # Load project data
    project_data = project.getData(filter['query'])

    # Convert to data frame using specified function
    toDataframe = Registry.r[pivot_config['toDataframe']]['f']
    project_data_to_dataframe = toDataframe(project_data)

    ## apply pivot functions
    for f in pivot:
        function_name = f['function']
        arguments = f['kwargs']
        project_data_to_dataframe = Registry.r[function_name]['f'](project_data_to_dataframe, arguments)

    return project_data_to_dataframe

@Registry.register("Similarity")
def similarityFunc(data):
    """
    This function would create a panda from data from mongo.
    """
    to_panda, sources = [], set([])

    for item in data:
        sources.add(item['hash'])

    for item in data:
        annots = item['annotations']['similarity']
        for annot in annots:
            if annot in sources:
                to_panda.append({
                    'source': item['hash'],
                    'target': annot,
                    'weight': annots[annot]
                })
    return pandas.DataFrame(to_panda)

@Registry.register("RegisteredOne")
def registeredFunc(df, transform=False, **kwargs):
    """
    This is an example pivot/transforming function.
    """
    if transform:
        df['weight'] = df['weight'].apply(lambda x: math.log(x, 10))
    return df

class TestPivotServiceScaffold(unittest.TestCase):

    def setUp(self):

        self.data_fixtures = [
            {
                "type": "proteinSequence",
                "data": "MAEEEEPPPLLKDDD",
                "hash": "c24b3e4ba6e94a3ebc79e4506b0cabac",
                "keywords": {
                    "id": 1,
                    "subgroup": 0
                },
                "annotations": {
                    "similarity": {
                        "60c8a6f0d2a940fdbe3d6860659d045e": 1E50,
                        "f3c4bcd9fa2ad699e6c739834a0b9639": 1E4,
                        "f82d75f5ea1efd02f033a40bee4bf631": 1E3
                    }
                }
            },
            {
                "type": "proteinSequence",
                "data": "MTTYPLPMKLHNNNG",
                "hash": "60c8a6f0d2a940fdbe3d6860659d045e",
                "keywords": {
                    "id": 2,
                    "subgroup": 0
                },
                "annotations": {
                    "similarity": {
                        "c24b3e4ba6e94a3ebc79e4506b0cabac": 1E50,
                        "f3c4bcd9fa2ad699e6c739834a0b9639": 1E5,
                        "f82d75f5ea1efd02f033a40bee4bf631": 1E4
                    }
                }
            },
            {
                "type": "proteinSequence",
                "data": "MYGYFWAAAGGGLPS",
                "hash": "f3c4bcd9fa2ad699e6c739834a0b9639",
                "keywords": {
                    "id": 3,
                    "subgroup": 1
                },
                "annotations": {
                    "similarity": {
                        "c24b3e4ba6e94a3ebc79e4506b0cabac": 1E4,
                        "60c8a6f0d2a940fdbe3d6860659d045e": 1E5,
                        "f82d75f5ea1efd02f033a40bee4bf631": 1E7
                    }
                }
            },
            {
                "type": "proteinSequence",
                "data": "MKKRRKRRKWEDEDES",
                "hash": "f82d75f5ea1efd02f033a40bee4bf631",
                "keywords": {
                    "id": 4,
                    "subgroup": 2
                },
                "annotations": {
                    "similarity": {
                        "c24b3e4ba6e94a3ebc79e4506b0cabac": 1E3,
                        "60c8a6f0d2a940fdbe3d6860659d045e": 1E4,
                        "f3c4bcd9fa2ad699e6c739834a0b9639": 1E7
                    }
                }
            }
        ]

        #
        # Moved to Registry
        #
        #These would be in a registry, but here are just put into
        #a dictionary.
        # self.functions = {
        #     "Similarity": similarityFunc,
        #     "RegisteredOne": registeredFunc
        # }

        #This is an imagined pivot configuration object.
        self.pivot_config = {
            #This filter would query the project collection
            #for test_project and then pull the first three
            # data objects.
            "filter": {
                "project": "Test Project One",
                "query": {"keywords.subgroup": {"$in": [0, 1]}}
            },
            #This will call the registered function called similarity
            #to transform the output data objects into a dataframe.
            "toDataframe": "Similarity",
            #This pivot would pass the data to the pivoting
            #service and then call a series of registered
            #functions to transform the output data
            "pivot": [
                {
                    "function": "RegisteredOne",
                    "kwargs": {
                        "transform": True
                    }
                }
            ]
        }

    def testCallFunctions(self):
        #This is the correct output data.
        correct_data = [
            {
                'source':"c24b3e4ba6e94a3ebc79e4506b0cabac",
                'target':"60c8a6f0d2a940fdbe3d6860659d045e",
                'weight':50.0
            },
            {
                'source':"c24b3e4ba6e94a3ebc79e4506b0cabac",
                'target':"f3c4bcd9fa2ad699e6c739834a0b9639",
                'weight':4.0
            },
            {
                'source':"60c8a6f0d2a940fdbe3d6860659d045e",
                'target':"c24b3e4ba6e94a3ebc79e4506b0cabac",
                'weight':50.0
            },
            {
                'source':"60c8a6f0d2a940fdbe3d6860659d045e",
                'target':"f3c4bcd9fa2ad699e6c739834a0b9639",
                'weight':5.0
            },
            {
                'source':"f3c4bcd9fa2ad699e6c739834a0b9639",
                'target':"c24b3e4ba6e94a3ebc79e4506b0cabac",
                'weight':4.0
            },
            {
                'source':"f3c4bcd9fa2ad699e6c739834a0b9639",
                'target':"60c8a6f0d2a940fdbe3d6860659d045e",
                'weight':5.0
            },
        ]
        correct_df = pandas.DataFrame(correct_data)

        #This test should pass once all the steps
        #are in place.
        df = doPivot(self.pivot_config)

        #This won't actually work. We will need to
        #build a custom test function to assert
        #equality on two pandas data frames.
        print("\n\nCORRECT:\n")
        correct_df = correct_df.sort(['source', 'target'])
        correct_df = correct_df.reset_index(drop=True)
        print(correct_df)
        print("\n\nTEST:\n")
        df = df.sort(['source', 'target'])
        df = df.reset_index(drop=True)
        print(df)
        print("\n\n")
        assert_frame_equal(correct_df, df)
        #self.assertEqual(correct_df, df)

""" Get a connection to our database """
def get_database():
    return connectToMongoDb()

""" Connect to mongodb """
def connectToMongoDb():
    try:
        mongo_connection = pymongo.MongoClient(settings.TestingSettings.MONGO_CONNECTION_URI)
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to mongodb, is it running?\n\t%s" % str(e))
        abort(500)

    db = mongo_connection[settings.TestingSettings.MONGO_DATABASE]

    return db

if __name__ == '__main__':
    unittest.main()
