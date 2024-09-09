from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class WeixinConfig(BaseSettings):
    """
    WEIXIN configs
    """
    WEIXIN_APP_ID: Optional[str] = Field(
        description='WEIXIN_APP_ID',
        default=None,
    )
    WEIXIN_APP_SECRET: Optional[str] = Field(
        description='WEIXIN_APP_SECRET',
        default=None,
    )
