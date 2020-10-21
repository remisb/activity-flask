from flask import request
from flask_restful import Resource, Api, reqparse

projects = {}
parser = reqparse.RequestParser()


class ProjectListApi(Resource):
    def get(self):
        return projects

    def post(self):
        args = parser.parse_arfs()
        project_id = int(max(projects.keys()).lstrip('project')) + 1
        project_id = 'project%i' % project_id
        restaurants[project_id] = {'project': args['project']}
        return projects[project_id], 201


class ProjectApi(Resource):
    def get(self, project_id):
        return {project_id: projects[project_id]}

    def put(self, project_id):
        projects[project_id] = request.form['data']
        return {project_id: projects[project_id]}
