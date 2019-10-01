from flask import Flask, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Student(Resource):
    def get(self, name):
        response = {
            'student': name
        }
        return jsonify(response)


api.add_resource(Student, '/student/<string:name>')

app.run(port=5000)
