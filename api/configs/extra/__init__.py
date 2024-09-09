from configs.extra.sentry_config import SentryConfig
from configs.extra.weixin_config import WeixinConfig


class ExtraServiceConfig(
    # place the configs in alphabet order
    SentryConfig,
    WeixinConfig
):
    pass
