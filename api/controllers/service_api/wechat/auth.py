from flask import request
from flask_restful import Resource

from controllers.service_api import api
from extensions.ext_weixin import weixin
from libs.response import api_response


class WechatAuthApi(Resource):
    def post(self):
        """Handle WeChat authentication and return openid and session_key"""
        code = request.json.get('code')
        if not code:
            return api_response(message="Missing code parameter", status_code=400)

        try:
            auth_info = weixin.jscode2session(code)
            return api_response(message="Authentication successful", data=auth_info)
        except Exception as e:
            return api_response(message=f"Authentication failed: {str(e)}", status_code=500)


api.add_resource(WechatAuthApi, '/wechat/auth')
