from typing import Optional

from pydantic import AliasChoices, Field, NonNegativeInt, PositiveInt, computed_field
from pydantic_settings import BaseSettings


class SecurityConfig(BaseSettings):
    """
    安全相关的配置项。

    Security-related configuration items.
    """
    SECRET_KEY: Optional[str] = Field(
        description='您的应用密钥，用于安全地签署会话cookie。'
                    '确保为您的部署更改此密钥，使用强密钥。'
                    '您可以使用 `openssl rand -base64 42` 生成强密钥。'
                    '或者，您可以通过 `SECRET_KEY` 环境变量设置它。'

                    'Your App secret key will be used for securely signing the session cookie. '
                    'Make sure you are changing this key for your deployment with a strong key. '
                    'You can generate a strong key using `openssl rand -base64 42`. '
                    'Alternatively you can set it with `SECRET_KEY` environment variable.',
        default=None,
    )

    RESET_PASSWORD_TOKEN_EXPIRY_HOURS: PositiveInt = Field(
        description='重置令牌的过期时间（小时）'
                    'Expiry time in hours for reset token',
        default=24,
    )


class FileUploadConfig(BaseSettings):
    """
    文件上传相关的配置项。

    File uploading related configuration items.
    """
    UPLOAD_FILE_SIZE_LIMIT: NonNegativeInt = Field(
        description='上传文件的大小限制（MB）'
                    'Size limit in Megabytes for uploading files',
        default=15,
    )

    UPLOAD_FILE_BATCH_LIMIT: NonNegativeInt = Field(
        description='上传文件的批量大小限制'
                    'Batch size limit for uploading files',
        default=5,
    )

    UPLOAD_IMAGE_FILE_SIZE_LIMIT: NonNegativeInt = Field(
        description='上传图片文件的大小限制（MB）'
                    'Image file size limit in Megabytes for uploading files',
        default=10,
    )

    BATCH_UPLOAD_LIMIT: NonNegativeInt = Field(
        description='批量上传限制',  # todo: to be clarified
        default=20,
    )


class HttpConfig(BaseSettings):
    """
    HTTP相关的配置项。

    HTTP related configuration items.
    """
    API_COMPRESSION_ENABLED: bool = Field(
        description='是否启用HTTP响应的gzip压缩'
                    'Whether to enable HTTP response compression of gzip',
        default=False,
    )

    inner_WEB_API_CORS_ALLOW_ORIGINS: str = Field(
        description='Web API允许的CORS源',
        validation_alias=AliasChoices('WEB_API_CORS_ALLOW_ORIGINS'),
        default='*',
    )

    @computed_field
    @property
    def WEB_API_CORS_ALLOW_ORIGINS(self) -> list[str]:
        return self.inner_WEB_API_CORS_ALLOW_ORIGINS.split(',')


class InnerAPIConfig(BaseSettings):
    """
    内部API相关的配置项。

    Inner API related configuration items.
    """
    INNER_API: bool = Field(
        description='是否启用内部API'
                    'Whether to enable the inner API',
        default=False,
    )

    INNER_API_KEY: Optional[str] = Field(
        description='用于验证内部API的密钥'
                    'The inner API key is used to authenticate the inner API',
        default=None,
    )


class LoggingConfig(BaseSettings):
    """
    日志相关的配置项。

    Logging related configuration items.
    """

    LOG_LEVEL: str = Field(
        description='日志输出级别，默认为INFO。'
                    '建议在生产环境中设置为ERROR。'

                    'Log output level, default to INFO. '
                    'It is recommended to set it to ERROR for production.',
        default='INFO',
    )

    LOG_FILE: Optional[str] = Field(
        description='日志输出文件路径'
                    'Logging output file path',
        default=None,
    )

    LOG_FORMAT: str = Field(
        description='日志格式'
                    'Log format',
        default='%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] [%(filename)s:%(lineno)d] - %(message)s',
    )

    LOG_DATEFORMAT: Optional[str] = Field(
        description='日志日期格式'
                    'Log date format',
        default=None,
    )

    LOG_TZ: Optional[str] = Field(
        description='指定日志时区，例如：America/New_York'
                    'Specify log timezone, eg: America/New_York',
        default=None,
    )


class OAuthConfig(BaseSettings):
    """
    OAuth相关的配置项。

    OAuth related configuration items.
    """
    OAUTH_REDIRECT_PATH: str = Field(
        description='OAuth的重定向路径'
                    'Redirect path for OAuth',
        default='/console/api/oauth/authorize',
    )

    GITHUB_CLIENT_ID: Optional[str] = Field(
        description='GitHub OAuth的客户端ID'
                    'GitHub client id for OAuth',
        default=None,
    )

    GITHUB_CLIENT_SECRET: Optional[str] = Field(
        description='GitHub OAuth的客户端密钥'
                    'GitHub client secret key for OAuth',
        default=None,
    )

    GOOGLE_CLIENT_ID: Optional[str] = Field(
        description='Google OAuth的客户端ID'
                    'Google client id for OAuth',
        default=None,
    )

    GOOGLE_CLIENT_SECRET: Optional[str] = Field(
        description='Google OAuth的客户端密钥'
                    'Google client secret key for OAuth',
        default=None,
    )


class MailConfig(BaseSettings):
    """
    邮件相关的配置项。

    Mail related configuration items.
    """

    MAIL_TYPE: Optional[str] = Field(
        description='邮件提供商类型名称，默认为None，可用值为`smtp`和`resend`。'
                    'Mail provider type name, default to None, available values are `smtp` and `resend`.',
        default=None,
    )

    MAIL_DEFAULT_SEND_FROM: Optional[str] = Field(
        description='默认的发件人邮箱地址'
                    'Default email address for sending from',
        default=None,
    )

    RESEND_API_KEY: Optional[str] = Field(
        description='Resend的API密钥'
                    'API key for Resend',
        default=None,
    )

    RESEND_API_URL: Optional[str] = Field(
        description='Resend的API URL'
                    'API URL for Resend',
        default=None,
    )

    SMTP_SERVER: Optional[str] = Field(
        description='SMTP服务器主机'
                    'SMTP server host',
        default=None,
    )

    SMTP_PORT: Optional[int] = Field(
        description='SMTP服务器端口'
                    'SMTP server port',
        default=465,
    )

    SMTP_USERNAME: Optional[str] = Field(
        description='SMTP服务器用户名'
                    'SMTP server username',
        default=None,
    )

    SMTP_PASSWORD: Optional[str] = Field(
        description='SMTP服务器密码'
                    'SMTP server password',
        default=None,
    )

    SMTP_USE_TLS: bool = Field(
        description='是否使用TLS连接SMTP服务器'
                    'Whether to use TLS connection to SMTP server',
        default=False,
    )

    SMTP_OPPORTUNISTIC_TLS: bool = Field(
        description='是否使用机会性TLS连接SMTP服务器'
                    'Whether to use opportunistic TLS connection to SMTP server',
        default=False,
    )


class DataSetConfig(BaseSettings):
    """
    数据集相关的配置项。

    Dataset related configuration items.
    """

    CLEAN_DAY_SETTING: PositiveInt = Field(
        description='清理数据集的间隔天数'
                    'Interval in days for cleaning up dataset',
        default=30,
    )

    DATASET_OPERATOR_ENABLED: bool = Field(
        description='是否启用数据集操作符'
                    'Whether to enable dataset operator',
        default=False,
    )


class WorkspaceConfig(BaseSettings):
    """
    工作区相关的配置项。

    Workspace related configuration items.
    """

    INVITE_EXPIRY_HOURS: PositiveInt = Field(
        description='工作区邀请的过期时间（小时）'
                    'Workspaces invitation expiration in hours',
        default=72,
    )


class IndexingConfig(BaseSettings):
    """
    索引相关的配置项。

    Indexing related configuration items.
    """

    INDEXING_MAX_SEGMENTATION_TOKENS_LENGTH: PositiveInt = Field(
        description='索引的最大分段令牌长度'
                    'Max segmentation token length for indexing',
        default=1000,
    )


class ImageFormatConfig(BaseSettings):
    """
    图像格式相关的配置项。

    Image format related configuration items.
    """
    MULTIMODAL_SEND_IMAGE_FORMAT: str = Field(
        description='多模型发送图像格式，支持base64、url，默认为base64'
                    'Multi model send image format, support base64, url, default is base64',
        default='base64',
    )


class CeleryBeatConfig(BaseSettings):
    """
    Celery Beat相关的配置项。

    Celery Beat related configuration items.
    """
    CELERY_BEAT_SCHEDULER_TIME: int = Field(
        description='Celery调度器的时间，默认为1天'
                    'The time of the Celery scheduler, default to 1 day',
        default=1,
    )


class FeatureConfig(
    # place the configs in alphabet order
    DataSetConfig,
    FileUploadConfig,
    HttpConfig,
    ImageFormatConfig,
    InnerAPIConfig,
    IndexingConfig,
    LoggingConfig,
    MailConfig,
    OAuthConfig,
    SecurityConfig,
    WorkspaceConfig,

    CeleryBeatConfig,
):
    """
    包含所有特性配置的主配置类。

    Main configuration class containing all feature configurations.
    """
    pass