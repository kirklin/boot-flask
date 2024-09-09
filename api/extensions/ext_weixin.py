from weixin import Weixin

weixin = Weixin()


def init_app(app):
    weixin.init_app(app)
