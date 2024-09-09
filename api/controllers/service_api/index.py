from flask_restful import Resource

from configs import app_config
from controllers.service_api import api
from libs.response import api_response


class IndexApi(Resource):
    def get(self):
        """
        获取 API 的基本信息
        """
        data = {
            "welcome": "Welcome to MVP API",
            "api_version": "v1",
            "server_version": app_config.CURRENT_VERSION,
        }
        return api_response(message="API is operational", data=data)

    def post(self):
        """
        示例 POST 方法 - 在 MVP 中可以用于创建资源
        """
        # 这里应该有创建资源的逻辑
        return api_response(message="Resource created successfully", status_code=201)

    def options(self):
        """
        处理 OPTIONS 请求，用于 CORS 预检请求
        """
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return api_response(message="CORS preflight request successful", status_code=204, headers=headers)


api.add_resource(IndexApi, '/')
