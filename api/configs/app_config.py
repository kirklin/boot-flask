from pydantic import Field, computed_field
from pydantic_settings import SettingsConfigDict

from configs.deploy import DeploymentConfig
from configs.extra import ExtraServiceConfig
from configs.feature import FeatureConfig
from configs.middleware import MiddlewareConfig
from configs.packaging import PackagingInfo


class AppConfig(
    # Packaging info
    PackagingInfo,

    # Deployment configs
    DeploymentConfig,

    # Feature configs
    FeatureConfig,

    # Middleware configs
    MiddlewareConfig,

    # Extra service configs
    ExtraServiceConfig,
):
    # 是否启用调试模式
    DEBUG: bool = Field(default=False, description='是否启用调试模式。')

    model_config = SettingsConfigDict(
        # 从 dotenv 格式的配置文件读取配置
        env_file='.env',
        env_file_encoding='utf-8',
        frozen=True,  # 配置冻结，不允许更改
        extra='ignore',  # 忽略额外的属性
    )

    # HTTP 请求节点的最大二进制大小（单位：字节）
    HTTP_REQUEST_NODE_MAX_BINARY_SIZE: int = 1024 * 1024 * 10  # 10MB

    @computed_field
    def HTTP_REQUEST_NODE_READABLE_MAX_BINARY_SIZE(self) -> str:
        """可读的 HTTP 请求节点最大二进制大小"""
        return f'{self.HTTP_REQUEST_NODE_MAX_BINARY_SIZE / 1024 / 1024:.2f}MB'

    # HTTP 请求节点的最大文本大小（单位：字节）
    HTTP_REQUEST_NODE_MAX_TEXT_SIZE: int = 1024 * 1024  # 1MB

    @computed_field
    def HTTP_REQUEST_NODE_READABLE_MAX_TEXT_SIZE(self) -> str:
        """可读的 HTTP 请求节点最大文本大小"""
        return f'{self.HTTP_REQUEST_NODE_MAX_TEXT_SIZE / 1024 / 1024:.2f}MB'

    SSRF_PROXY_HTTP_URL: str | None = None
    SSRF_PROXY_HTTPS_URL: str | None = None
