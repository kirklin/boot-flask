from flask import Blueprint

from libs.external_api import ExternalApi

bp = Blueprint('service_api', __name__, url_prefix='/v1')
api = ExternalApi(bp)

from . import index
from .wechat import auth
