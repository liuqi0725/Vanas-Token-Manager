# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : config.py
# @Created  : 2020/11/9 3:35 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 项目的配置文件
# -------------------------------------------------------------------------------

import os

basedir = os.path.abspath(os.path.dirname(__file__))

from vanaspyhelper.util.crypto import AESTool
global aes

class config:

    @staticmethod
    def init_app(app):
        # 初始化日志
        from vanaspyhelper.LoggerManager import init_global_logger

        # 要么传入配置路径，要么获取当前目录的上一级 `os.path.dirname(basedir)`
        current_dir_parent = os.path.dirname(basedir)

        if 'APP_LOG_DIR' in app.config:
            log_dir = app.config['APP_LOG_DIR']
        else:
            log_dir = current_dir_parent

        if 'APP_LOG_LEVEL' in app.config:
            log_level = app.config['APP_LOG_LEVEL']
        else:
            log_level = "error"

        from konfig import Config
        # 初始化 aes
        c = Config(app.config['SECURITY_CONF_PATH'])
        app.config.update(c.get_map('AES'))

        global aes
        aes = AESTool(key=c.get_map('AES').get('AES_SECRET_KEY'))

        # 初始化日志对象
        init_global_logger(log_dir, level=log_level, log_prefix="VanasToken")

        # reading key files
        with open(app.config['JWT_SIGNATURE_PIVE_KEY_PATH']) as f:
            app.config['JWT_SIGNATURE_PRIV_KEY'] = f.read()

        with open(app.config['JWT_SIGNATURE_PLUB_KEY_PATH']) as f:
            app.config['JWT_SIGNATURE_PLUB_KEY'] = f.read()


class DevelopmentConfig(config):
    DEBUG = True

    # 日志相关
    APP_LOG_DIR = '/Users/alexliu/tmp/vanas_token/logs'
    APP_LOG_LEVEL = "debug"

    # 保存 aes-key， 授权的第三方服务获取 token 的 key
    SECURITY_CONF_PATH = '/Users/alexliu/tmp/vanas_token/security.ini'

    # json web token 签名发布者
    # 注意此域名 必须和你部署后的 域名一致
    JWT_ISS = 'https://www.35liuqi.com'
    # json web token(JWT) 算法 , 需要安装算法库 cryptography
    JWT_ALGORITHM = 'RS512'
    # 客户端授权凭证  client_credentials 或 password
    JWT_GRANT_TYPE = 'client_credentials'
    # 签名秘钥
    JWT_SIGNATURE_PIVE_KEY_PATH = '/Users/alexliu/tmp/vanas_token/self_ca_privkey.pem'
    # 签名公钥
    JWT_SIGNATURE_PLUB_KEY_PATH =  '/Users/alexliu/tmp/vanas_token/self_ca_pubkey.pem'



class TestingConfig(config):
    DEBUG = True

    # 日志相关
    APP_LOG_DIR = '/Users/alexliu/tmp/vanas_token/logs'
    APP_LOG_LEVEL = "debug"

    # 保存 aes-key， 授权的第三方服务获取 token 的 key
    SECURITY_CONF_PATH = '/Users/alexliu/tmp/vanas_token/security.ini'

    # json web token 签名发布者
    # 注意此域名 必须和你部署后的 域名一致
    JWT_ISS = 'https://www.35liuqi.com'
    # json web token(JWT) 算法 , 需要安装算法库 cryptography
    JWT_ALGORITHM = 'RS512'
    # 客户端授权凭证  client_credentials 或 password
    JWT_GRANT_TYPE = 'client_credentials'
    # 签名秘钥
    JWT_SIGNATURE_PIVE_KEY_PATH = '/Users/alexliu/tmp/vanas_token/self_ca_privkey.pem'
    # 签名公钥
    JWT_SIGNATURE_PLUB_KEY_PATH = '/Users/alexliu/tmp/vanas_token/self_ca_pubkey.pem'

class ProductionConfig(config):
    DEBUG = True

    # 日志相关
    APP_LOG_DIR = '/logs' # logs 为挂接目录
    APP_LOG_LEVEL = "info"

    # 保存 aes-key， 授权的第三方服务获取 token 的 key  , security 为挂接目录
    SECURITY_CONF_PATH = '/security/security.ini'

    # json web token 签名发布者
    # 注意此域名 必须和你部署后的 域名一致
    JWT_ISS = 'https://www.35liuqi.com'
    # json web token(JWT) 算法 , 需要安装算法库 cryptography
    JWT_ALGORITHM = 'RS512'
    # 客户端授权凭证  client_credentials 或 password
    JWT_GRANT_TYPE = 'client_credentials'
    # 签名秘钥
    JWT_SIGNATURE_PIVE_KEY_PATH = '/security/self_ca_privkey.pem'
    # 签名公钥
    JWT_SIGNATURE_PLUB_KEY_PATH = '/security/self_ca_pubkey.pem'

config= {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}