from flask import request
from flask_restful import Resource

from controllers.web import api


class AppHello(Resource):
    def get(self):
        """Get app meta"""
        return {
            'hello': "world"
        }


api.add_resource(AppHello, '/hello')
