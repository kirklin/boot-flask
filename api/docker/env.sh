#!/bin/bash

# 定义环境变量
ENV_FILE_PATH="/home/.env"  # 替换为你的 .env 文件的路径
CONTAINER_NAME="mvp-api-container"
IMAGE_NAME="mvp-api:v0.0.1"
HOST_PORT=5001
CONTAINER_PORT=5001
WEIXIN_APP_ID=
WEIXIN_APP_SECRET=
DEBUG=false

# 停止并移除已存在的同名容器
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

# 运行 Docker 容器，挂载 .env 文件，并映射端口
docker run -d \
  --name $CONTAINER_NAME \
  -p $HOST_PORT:$CONTAINER_PORT \
  --env-file $ENV_FILE_PATH \
  $IMAGE_NAME

echo "容器 $CONTAINER_NAME 已启动，并挂载了 .env 文件。"