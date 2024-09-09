import os

# 检查环境变量"DEBUG"，如果不是"true"，进行补丁
if os.environ.get("DEBUG", "false").lower() != 'true':
    from gevent import monkey

    monkey.patch_all()
    import grpc.experimental.gevent  # 导入grpc的gevent实验性模块

    grpc.experimental.gevent.init_gevent()  # 初始化gevent

import json
import logging
import sys
import threading
from logging.handlers import RotatingFileHandler  # 从logging.handlers导入RotatingFileHandler

from flask import Flask, Response, request
from flask_cors import CORS

from configs import app_config  # 从configs模块导入dify_config
from extensions import (  # 从extensions模块导入各个扩展模块
    ext_celery,
    ext_compress,
    ext_database,
    ext_login,
    ext_mail,
    ext_migrate,
    ext_redis,
    ext_storage,
    ext_weixin,
)
from extensions.ext_database import db  # 从extensions.ext_database导入db
from extensions.ext_login import login_manager  # 从extensions.ext_login导入login_manager

# -------------
# 创建 Flask 应用
# -------------

class SimpleApp(Flask):
    pass


# 配置
config_type = os.getenv('EDITION', default='SELF_HOSTED')  # 从环境变量中获取EDITION，默认为SELF_HOSTED


# 创建Flask应用工厂函数
def create_flask_app_with_configs() -> Flask:
    """
    创建一个原始的Flask应用，并从.env文件中加载配置
    """
    app = SimpleApp(__name__)
    app.config.from_mapping(app_config.model_dump())

    # 将配置加载到系统环境变量中
    for key, value in app.config.items():
        if isinstance(value, str):
            os.environ[key] = value
        elif isinstance(value, int | float | bool):
            os.environ[key] = str(value)
        elif value is None:
            os.environ[key] = ''

    return app  # 返回Flask应用实例


def create_app() -> Flask:
    app = create_flask_app_with_configs()  # 创建应用

    app.secret_key = app.config['SECRET_KEY']  # 设置应用的secret_key

    log_handlers = None  # 日志处理器
    log_file = app.config.get('LOG_FILE')  # 获取日志文件路径
    if log_file:
        log_dir = os.path.dirname(log_file)  # 获取日志文件目录
        os.makedirs(log_dir, exist_ok=True)  # 创建日志文件目录
        log_handlers = [
            RotatingFileHandler(
                filename=log_file,
                maxBytes=1024 * 1024 * 1024,
                backupCount=5
            ),
            logging.StreamHandler(sys.stdout)  # 日志处理器，输出到标准输出
        ]

    logging.basicConfig(
        level=app.config.get('LOG_LEVEL'),  # 设置日志级别
        format=app.config.get('LOG_FORMAT'),  # 设置日志格式
        datefmt=app.config.get('LOG_DATEFORMAT'),  # 设置日志日期格式
        handlers=log_handlers,  # 设置日志处理器
        force=True  # 强制覆盖现有日志配置
    )
    log_tz = app.config.get('LOG_TZ')  # 获取日志时区
    if log_tz:
        from datetime import datetime  # 导入datetime模块

        import pytz  # 导入pytz模块
        timezone = pytz.timezone(log_tz)  # 获取时区对象

        def time_converter(seconds):
            return datetime.utcfromtimestamp(seconds).astimezone(timezone).timetuple()

        for handler in logging.root.handlers:
            handler.formatter.converter = time_converter
    initialize_extensions(app)  # 初始化扩展
    register_blueprints(app)  # 注册蓝图

    return app  # 返回应用实例


def initialize_extensions(app):
    # 传递应用实例到各个Flask扩展实例，绑定到Flask应用实例
    ext_compress.init_app(app)
    ext_database.init_app(app)
    ext_migrate.init(app, db)
    ext_redis.init_app(app)
    ext_storage.init_app(app)
    ext_celery.init_app(app)
    ext_login.init_app(app)
    ext_mail.init_app(app)
    ext_weixin.init_app(app)


def register_blueprints(app):
    from controllers.service_api import bp as service_api_bp
    from controllers.web import bp as web_bp

    CORS(service_api_bp,
         allow_headers=['Content-Type', 'Authorization', 'X-App-Code'],
         methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH']
         )
    app.register_blueprint(service_api_bp)

    CORS(web_bp,
         resources={
             r"/*": {"origins": app.config['WEB_API_CORS_ALLOW_ORIGINS']}},
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization', 'X-App-Code'],
         methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH'],
         expose_headers=['X-Version', 'X-Env']
         )

    app.register_blueprint(web_bp)


# 创建应用
app = create_app()
celery = app.extensions["celery"]

if app.config.get('TESTING'):
    print("App is running in TESTING mode")


@app.after_request
def after_request(response):
    """Add Version headers to the response."""
    response.set_cookie('remember_token', '', expires=0)
    response.headers.add('X-Version', app.config['CURRENT_VERSION'])
    response.headers.add('X-Env', app.config['DEPLOY_ENV'])
    return response


@app.route('/health')
def health():
    return Response(json.dumps({
        'status': 'ok',
        'version': app.config['CURRENT_VERSION']
    }), status=200, content_type="application/json")


@app.route('/threads')
def threads():
    num_threads = threading.active_count()
    threads = threading.enumerate()

    thread_list = []
    for thread in threads:
        thread_name = thread.name
        thread_id = thread.ident
        is_alive = thread.is_alive()

        thread_list.append({
            'name': thread_name,
            'id': thread_id,
            'is_alive': is_alive
        })

    return {
        'thread_num': num_threads,
        'threads': thread_list
    }


@app.route('/db-pool-stat')
def pool_stat():
    engine = db.engine
    return {
        'pool_size': engine.pool.size(),
        'checked_in_connections': engine.pool.checkedin(),
        'checked_out_connections': engine.pool.checkedout(),
        'overflow_connections': engine.pool.overflow(),
        'connection_timeout': engine.pool.timeout(),
        'recycle_time': db.engine.pool._recycle
    }


if __name__ == '__main__':
    # 运行 Flask 应用
    app.run(host='0.0.0.0', port=5001)
