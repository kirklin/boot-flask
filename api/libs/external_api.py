import re
import sys

from flask import current_app, got_request_exception
from flask_restful import Api, http_status_message
from werkzeug.datastructures import Headers
from werkzeug.exceptions import HTTPException

from core.errors.error import AppInvokeQuotaExceededError


class ExternalApi(Api):
    """
    扩展的Flask-RESTful Api类，提供自定义的错误处理机制。

    Extended Flask-RESTful Api class that provides custom error handling.
    """
    def handle_error(self, e):
        """
        API的错误处理器，将引发的异常转换为适当的HTTP状态码和响应体的Flask响应。

        Error handler for the API that transforms a raised exception into a Flask
        response with the appropriate HTTP status code and body.

        主要功能：
        1. 处理不同类型的异常（HTTPException, ValueError, AppInvokeQuotaExceededError等）
        2. 生成包含错误代码、消息和状态的响应数据
        3. 处理特殊情况，如406 Not Acceptable和401 Unauthorized
        4. 记录服务器错误（状态码>=500）

        Main features:
        1. Handles different types of exceptions (HTTPException, ValueError, AppInvokeQuotaExceededError, etc.)
        2. Generates response data containing error code, message, and status
        3. Handles special cases like 406 Not Acceptable and 401 Unauthorized
        4. Logs server errors (status code >= 500)

        :param e: 引发的异常对象
        :type e: Exception
        :return: 包含错误信息的Flask响应
        :rtype: flask.Response
        """
        got_request_exception.send(current_app, exception=e)

        headers = Headers()
        if isinstance(e, HTTPException):
            if e.response is not None:
                resp = e.get_response()
                return resp

            status_code = e.code
            default_data = {
                'code': re.sub(r'(?<!^)(?=[A-Z])', '_', type(e).__name__).lower(),
                'message': getattr(e, 'description', http_status_message(status_code)),
                'status': status_code
            }

            if default_data['message'] and default_data['message'] == 'Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)':
                default_data['message'] = 'Invalid JSON payload received or JSON payload is empty.'

            headers = e.get_response().headers
        elif isinstance(e, ValueError):
            status_code = 400
            default_data = {
                'code': 'invalid_param',
                'message': str(e),
                'status': status_code
            }
        elif isinstance(e, AppInvokeQuotaExceededError):
            status_code = 429
            default_data = {
                'code': 'too_many_requests',
                'message': str(e),
                'status': status_code
            }
        else:
            status_code = 500
            default_data = {
                'message': http_status_message(status_code),
            }

        # Werkzeug exceptions generate a content-length header which is added
        # to the response in addition to the actual content-length header
        # https://github.com/flask-restful/flask-restful/issues/534
        remove_headers = ('Content-Length',)

        for header in remove_headers:
            headers.pop(header, None)

        data = getattr(e, 'data', default_data)

        error_cls_name = type(e).__name__
        if error_cls_name in self.errors:
            custom_data = self.errors.get(error_cls_name, {})
            custom_data = custom_data.copy()
            status_code = custom_data.get('status', 500)

            if 'message' in custom_data:
                custom_data['message'] = custom_data['message'].format(
                    message=str(e.description if hasattr(e, 'description') else e)
                )
            data.update(custom_data)

        # record the exception in the logs when we have a server error of status code: 500
        if status_code and status_code >= 500:
            exc_info = sys.exc_info()
            if exc_info[1] is None:
                exc_info = None
            current_app.log_exception(exc_info)

        if status_code == 406 and self.default_mediatype is None:
            # if we are handling NotAcceptable (406), make sure that
            # make_response uses a representation we support as the
            # default mediatype (so that make_response doesn't throw
            # another NotAcceptable error).
            supported_mediatypes = list(self.representations.keys())  # only supported application/json
            fallback_mediatype = supported_mediatypes[0] if supported_mediatypes else "text/plain"
            data = {
                'code': 'not_acceptable',
                'message': data.get('message')
            }
            resp = self.make_response(
                data,
                status_code,
                headers,
                fallback_mediatype = fallback_mediatype
            )
        elif status_code == 400:
            if isinstance(data.get('message'), dict):
                param_key, param_value = list(data.get('message').items())[0]
                data = {
                    'code': 'invalid_param',
                    'message': param_value,
                    'params': param_key
                }
            else:
                if 'code' not in data:
                    data['code'] = 'unknown'

            resp = self.make_response(data, status_code, headers)
        else:
            if 'code' not in data:
                data['code'] = 'unknown'

            resp = self.make_response(data, status_code, headers)

        if status_code == 401:
            resp = self.unauthorized(resp)
        return resp
