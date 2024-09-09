## Docker 部署 README

欢迎使用 Docker Compose 部署 APP 的新 `docker` 目录。本 README 概述了更新内容、部署说明以及现有用户的迁移细节。

### 更新内容
- **持久环境变量**：环境变量现在通过 `.env` 文件管理，确保配置在各次部署中持久化。

  > 什么是 `.env` 文件？</br></br>
  > `.env` 文件是 Docker 和 Docker Compose 环境中的关键组件，作为集中配置文件，您可以在其中定义环境变量，这些变量在运行时对容器可用。此文件简化了开发、测试和生产不同阶段的环境设置管理，提供了配置的一致性和易用性。

- **统一向量数据库服务**：所有向量数据库服务现在由单个 Docker Compose 文件 `docker-compose.yaml` 管理。您可以通过在 `.env` 文件中设置 `VECTOR_STORE` 环境变量来切换不同的向量数据库。
- **必须的 .env 文件**：现在运行 `docker compose up` 需要 `.env` 文件。此文件对配置您的部署和任何自定义设置在升级中持久化非常重要。
- **遗留支持**：以前的部署文件现在位于 `docker-legacy` 目录中，将不再维护。

### 使用 `docker-compose.yaml` 部署 APP
1. **先决条件**：确保您的系统上安装了 Docker 和 Docker Compose。
2. **环境设置**：
   - 导航到 `docker` 目录。
   - 通过运行 `cp .env.example .env` 将 `.env.example` 文件复制到新的 `.env` 文件。
   - 根据需要自定义 `.env` 文件。参考 `.env.example` 文件以获取详细配置选项。
3. **运行服务**：
   - 从 `docker` 目录执行 `docker compose up` 以启动服务。
   - 要指定向量数据库，请在 `.env` 文件中设置 `VECTOR_STORE` 变量为您所需的向量数据库服务，例如 `milvus`, `weaviate` 或 `opensearch`。

### 部署用于开发 APP 的中间件
1. **中间件设置**：
   - 使用 `docker-compose.middleware.yaml` 设置数据库和缓存等基本中间件服务。
   - 导航到 `docker` 目录。
   - 通过运行 `cp middleware.env.example middleware.env` 确保创建了 `middleware.env` 文件（参考 `middleware.env.example` 文件）。
2. **运行中间件服务**：
   - 执行 `docker-compose -f docker-compose.middleware.yaml up -d` 启动中间件服务。

### `.env` 概述

#### 关键模块和自定义

- **向量数据库服务**：根据使用的向量数据库类型（`VECTOR_STORE`），用户可以设置特定的端点、端口和认证细节。
- **存储服务**：根据存储类型（`STORAGE_TYPE`），用户可以配置 S3、Azure Blob、Google Storage 等的特定设置。
- **API 和 Web 服务**：用户可以定义 URL 和其他设置，影响 API 和 Web 前端的操作。

#### 其他重要变量
在 Docker 设置中提供的 `.env.example` 文件非常全面，涵盖了各种配置选项。它被结构化为几个部分，每个部分涉及应用程序及其服务的不同方面。以下是一些关键部分和变量：

1. **常用变量**：
   - `SERVICE_API_URL`：不同 API 服务的 URL。
   - `APP_WEB_URL`：前端应用程序 URL。
   - `FILES_URL`：文件下载和预览的基本 URL。

2. **服务器配置**：
   - `LOG_LEVEL`, `DEBUG`, `FLASK_DEBUG`：日志和调试设置。
   - `SECRET_KEY`：用于加密会话 cookie 和其他敏感数据的密钥。

3. **数据库配置**：
   - `DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_DATABASE`：PostgreSQL 数据库凭据和连接详情。

4. **Redis 配置**：
   - `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`：Redis 服务器连接设置。

5. **Celery 配置**：
   - `CELERY_BROKER_URL`：Celery 消息代理的配置。

6. **存储配置**：
   - `STORAGE_TYPE`, `S3_BUCKET_NAME`, `AZURE_BLOB_ACCOUNT_NAME`：本地、S3、Azure Blob 等文件存储选项的设置。

7. **向量数据库配置**：
   - `VECTOR_STORE`：向量数据库类型（例如 `weaviate`, `milvus`）。
   - 每种向量存储的具体设置，如 `WEAVIATE_ENDPOINT`, `MILVUS_HOST`。

8. **CORS 配置**：
   - `WEB_API_CORS_ALLOW_ORIGINS`：跨源资源共享设置。

9. **其他服务特定的环境变量**：
   - 每个服务如 `nginx`, `redis`, `db` 和向量数据库都有直接在 `docker-compose.yaml` 中引用的特定环境变量。

### 其他信息
- **持续改进阶段**：我们积极寻求社区的反馈，以改进和增强部署过程。随着更多用户采用这种新方法，我们将根据您的经验和建议继续进行改进。
- **支持**：有关详细配置选项和环境变量设置，请参考 `.env.example` 文件和 `docker` 目录中的 Docker Compose 配置文件。
