# 从doker hub 安装 python3.8 镜像
FROM python:3.8

# 安装 circus 和 chaussette
RUN pip install circus chaussette

# OpenResty install
RUN apt-get -y update && \
    apt-get -y install libreadline-dev libncurses5-dev && \
    apt-get -y install libpcre3-dev libssl-dev perl make

# 编译，安装 OpenResty 依赖
# 安装在 /usr/local/openresty
RUN curl -sSL https://openresty.org/download/openresty-1.17.8.1.tar.gz \
    | tar -xz && \
    cd openresty-1.17.8.1 && \
    ./configure -j2 && \
    make -j2 && \
    make install

# 添加 ENV 指令,支持 nginx
ENV PATH "/usr/local/openresty/bin:/usr/local/openresty/nginx/sbin:$PATH"

# 复制 根目录(.) 所有文件到 app 中
COPY . /app

# 安装依赖项目
RUN pip install --no-cache-dir -r /app/requirements.txt
# 指向目录时，查找 setup.py 进行安装
RUN pip install /app/

# 创建日志目录，并挂载到主机目录,这样就算 docker 挂了，日志也不会销毁
RUN mkdir /logs
VOLUME /logs

# 暴露端口
EXPOSE 9000

# 执行完以后的命令
CMD circusd /app/docker/circus.ini