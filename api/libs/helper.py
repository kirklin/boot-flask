"""
这个模块包含了一系列用于数据验证、处理和工具函数的实用程序。
它提供了电子邮件验证、UUID处理、时间戳转换、字符串生成等功能。

This module contains a series of utility functions for data validation, processing, and general tools.
It provides functionalities such as email validation, UUID handling, timestamp conversion, string generation, etc.
"""

import random
import re
import string
import subprocess
import uuid
from datetime import datetime
from hashlib import sha256

from flask_restful import fields
from zoneinfo import available_timezones


def run(script):
    """
    执行给定的shell脚本并返回其状态和输出。

    Execute the given shell script and return its status and output.
    """
    return subprocess.getstatusoutput('source /root/.bashrc && ' + script)


class TimestampField(fields.Raw):
    """
    用于将datetime对象转换为时间戳的自定义字段类。

    A custom field class for converting datetime objects to timestamps.
    """
    def format(self, value) -> int:
        """
        将datetime对象转换为Unix时间戳。

        Convert a datetime object to a Unix timestamp.
        """
        return int(value.timestamp())


def email(email):
    """
    验证给定的字符串是否为有效的电子邮件地址。

    Validate if the given string is a valid email address.
    """
    pattern = r"^[\w\.!#$%&'*+\-/=?^_`{|}~]+@([\w-]+\.)+[\w-]{2,}$"
    if re.match(pattern, email) is not None:
        return email

    error = ('{email} is not a valid email.'
             .format(email=email))
    raise ValueError(error)


def uuid_value(value):
    """
    验证并转换给定的字符串为有效的UUID。

    Validate and convert the given string to a valid UUID.
    """
    if value == '':
        return str(value)

    try:
        uuid_obj = uuid.UUID(value)
        return str(uuid_obj)
    except ValueError:
        error = ('{value} is not a valid uuid.'
                 .format(value=value))
        raise ValueError(error)


def alphanumeric(value: str):
    """
    验证给定的字符串是否只包含字母、数字和下划线。

    Validate if the given string contains only alphanumeric characters and underscores.
    """
    if re.match(r'^[a-zA-Z0-9_]+$', value):
        return value

    raise ValueError(f'{value} is not a valid alphanumeric value')


def timestamp_value(timestamp):
    """
    验证并转换给定的值为有效的时间戳。

    Validate and convert the given value to a valid timestamp.
    """
    try:
        int_timestamp = int(timestamp)
        if int_timestamp < 0:
            raise ValueError
        return int_timestamp
    except ValueError:
        error = ('{timestamp} is not a valid timestamp.'
                 .format(timestamp=timestamp))
        raise ValueError(error)


class str_len:
    """
    用于限制字符串长度的验证器类。

    A validator class for restricting string length.
    """

    def __init__(self, max_length, argument='argument'):
        self.max_length = max_length
        self.argument = argument

    def __call__(self, value):
        """
        验证给定字符串的长度是否在指定范围内。

        Validate if the length of the given string is within the specified range.
        """
        length = len(value)
        if length > self.max_length:
            error = ('Invalid {arg}: {val}. {arg} cannot exceed length {length}'
                     .format(arg=self.argument, val=value, length=self.max_length))
            raise ValueError(error)

        return value


class float_range:
    """
    用于限制浮点数范围的验证器类。

    A validator class for restricting float values to a specific range.
    """

    def __init__(self, low, high, argument='argument'):
        self.low = low
        self.high = high
        self.argument = argument

    def __call__(self, value):
        """
        验证给定的浮点数是否在指定范围内。

        Validate if the given float value is within the specified range.
        """
        value = _get_float(value)
        if value < self.low or value > self.high:
            error = ('Invalid {arg}: {val}. {arg} must be within the range {lo} - {hi}'
                     .format(arg=self.argument, val=value, lo=self.low, hi=self.high))
            raise ValueError(error)

        return value


class datetime_string:
    """
    用于验证日期时间字符串格式的类。

    A class for validating datetime string formats.
    """

    def __init__(self, format, argument='argument'):
        self.format = format
        self.argument = argument

    def __call__(self, value):
        """
        验证给定的字符串是否符合指定的日期时间格式。

        Validate if the given string conforms to the specified datetime format.
        """
        try:
            datetime.strptime(value, self.format)
        except ValueError:
            error = ('Invalid {arg}: {val}. {arg} must be conform to the format {format}'
                     .format(arg=self.argument, val=value, format=self.format))
            raise ValueError(error)

        return value


def _get_float(value):
    """
    尝试将给定的值转换为浮点数。

    Attempt to convert the given value to a float.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError('{} is not a valid float'.format(value))


def timezone(timezone_string):
    """
    验证给定的时区字符串是否有效。

    Validate if the given timezone string is valid.
    """
    if timezone_string and timezone_string in available_timezones():
        return timezone_string

    error = ('{timezone_string} is not a valid timezone.'
             .format(timezone_string=timezone_string))
    raise ValueError(error)


def generate_string(n):
    """
    生成指定长度的随机字母数字字符串。

    Generate a random alphanumeric string of the specified length.
    """
    letters_digits = string.ascii_letters + string.digits
    result = ""
    for i in range(n):
        result += random.choice(letters_digits)

    return result


def get_remote_ip(request) -> str:
    """
    从请求中获取远程IP地址。

    Get the remote IP address from the request.
    """
    if request.headers.get('CF-Connecting-IP'):
        return request.headers.get('Cf-Connecting-Ip')
    elif request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr


def generate_text_hash(text: str) -> str:
    """
    为给定的文本生成SHA256哈希。

    Generate a SHA256 hash for the given text.
    """
    hash_text = str(text) + 'None'
    return sha256(hash_text.encode()).hexdigest()