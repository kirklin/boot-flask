### 0. 本地
```base
docker build -t mvp-api:v0.0.1 .
docker save -o mvp-api-v0.0.1.tar mvp-api:v0.0.1
```

### 1. 将Docker镜像文件传输到服务器
使用`scp`命令将`mvp-api-v0.0.1.tar`文件从Windows本地传输到Ubuntu服务器。打开Windows的命令行工具，执行以下命令：

```bash
scp -P 22 mvp-api-v0.0.1.tar username@your_server_ip:/path/to/destination
```
这里的`-P 22`指定了SSH端口，`username`是你的服务器用户名，`your_server_ip`是服务器的IP地址，`/path/to/destination`是服务器上的目标路径。

### 2. 在服务器上加载Docker镜像
登录到Ubuntu服务器，然后使用以下命令加载镜像：

```bash
docker load -i /path/to/destination/mvp-api-v0.0.1.tar
```

### 3. 启动Docker容器
使用以下命令启动Docker容器，将容器的5001端口映射到服务器的5001端口：

```bash
docker run -d -p 5001:5001 --name mvp-api-container mvp-api:v0.0.1
```

### 4. 安装Nginx
在Ubuntu服务器上安装Nginx：

```bash
sudo apt-get update
sudo apt-get install nginx
```

### 5. 配置Nginx
编辑Nginx配置文件，为`api.example.com`创建一个新的server块。你可以使用`vim`或你喜欢的文本编辑器编辑配置文件：

```bash
sudo vim /etc/nginx/sites-available/api.example.com
```

添加以下配置：

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

保存并关闭文件。

### 6. 启用配置并重启Nginx
启用配置并测试配置文件是否有语法错误：

```bash
sudo ln -s /etc/nginx/sites-available/api.example.com /etc/nginx/sites-enabled/
sudo nginx -t
```

如果配置文件没有错误，重启Nginx：

```bash
sudo systemctl restart nginx
```

### 7. 设置SSL和HTTPS
为了使用HTTPS，你需要为你的域名获取SSL证书。可以使用Let's Encrypt免费证书。安装Certbot并获取证书：

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d api.example.com
```

Certbot会自动配置Nginx以使用HTTPS。

### 8. 测试
在浏览器中访问`https://api.example.com`，检查是否能够正常访问API。
