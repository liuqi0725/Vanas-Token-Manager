# 从doker hub 安装 python3.8 镜像
FROM python:3.8

# 复制 根目录(.) 所有文件到 app 中
COPY . /app

# 拷贝签名文件
COPY /keys/self_ca_privkey.pem /app
COPY /keys/self_ca_pubkey.pem /app

# 安装依赖项目
RUN pip install --no-cache-dir -r /app/requirements.txt
# 指向目录时，查找 setup.py 进行安装
RUN pip install /app/

# 暴露端口 , 交给docker-compose 处理了
#EXPOSE 8000

# 执行完以后的命令 , 指向 setup 添加的命令
CMD vanas-tkm