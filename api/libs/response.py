def api_response(status="success", message=None, data=None, status_code=200, headers=None):
    """
    生成统一的 API 响应

    :param headers: 响应头
    :param status: 响应状态，默认为 "success"
    :param message: 响应消息
    :param data: 响应数据
    :param status_code: HTTP 状态码，默认为 200
    :return: Flask Response 对象
    """
    response = {
        "status": status,
        "message": message,
        "data": data,
        "code": status_code
    }
    return response, status_code, headers
