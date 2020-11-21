# Vanas-Token-Manager


#### 免责声明

该项目是针对 Vanas 项目的的一个 TokenManage 微服务。
主要作用是为给 Vanas 的各个微服务提供 AccessToken 生成，验证功能。
可能存在 BUG，我会不定期更新。如果将其用于您的生产项目，对您项目造成任何损失，我将不承担任何责任。

#### 软件架构

- Python 3.8
- Docker
- Docker-Compose
- Circus
- Nginx

#### 安装

##### 配置挂接路径

`docker-compose.yaml` 文件夹修改 `volumes` 挂接路径
    
##### 配置 security
 
`docker-compose.yaml` 文件中的 `volumes` 里 `/security` 对应的本地文件夹必须存在，目录结构如下图
   ![](http://pic.fangxutuwen.com/16059889168206.jpg)
   
+ `self_ca_privkey.pem` 为私钥。 名称在 `config.py`中修改
+ `self_ca_pubkey.pem` 为公钥。名称在 `config.py`中修改
+ `security.ini` 为所有服务的 client_id,secret_key 配置
   
```ini
[CLIENT_LIST]
vanas_clint_1 = secret_key_1
vanas_clint_2 = secret_key_2
vanas_clint_3 = secret_key_3
vanas_clint_4 = secret_key_4

[AES]
AES_SECRET_KEY = aes_key_d
```

##### config.py 配置
 
 修改 `config.py` 中相关配置
 
##### 部署 docker
 
 项目目录执行 `docker-composer on` 安装部署到 docker

##### 功能说明

- 创建 JWT token
- 验证 JWT token
- 查询公钥
