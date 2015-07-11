#!flask/bin/python
from flask import Flask, jsonify, abort

app = Flask(__name__)

projects = [
    {
        '_id' : 1,
        'name' : 'Project 1',
        'created_on' : '2015-07-11 12:00:00',
        'modified_on' : '2015-07-11 12:00:00'
    },
    {
        '_id' : 2,
        'name' : 'Project 2',
        'created_on' : '2015-07-11 13:00:00',
        'modified_on' : '2015-07-11 13:30:00'
    },
]

@app.route('/api/v1.0/projects', methods=['GET'])
def get_projects():
    return jsonify({'projects' : projects})

@app.route('/api/v1.0/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = [project for project in projects if project['_id'] == project_id]

    if len(project) == 0 or not project:
        abort(404)

    return jsonify({'project' : project[0]})

if __name__ == '__main__':
    app.run(debug=True)
