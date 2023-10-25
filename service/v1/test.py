from flask_restx import Namespace, Resource, fields
from service.custom_exceptions import CustomException

api = Namespace('test', description='test the application')


class Hello(Resource):

    def get(self):

        return {"message": "My Service!"}


api.add_resource(Hello, '/test')
