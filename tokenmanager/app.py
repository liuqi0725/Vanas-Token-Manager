# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : app.py
# @Created  : 2020/10/23 5:58 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 启动 app
# -------------------------------------------------------------------------------

def create_app(conf_path):
    from flask import Flask

    app = Flask(__name__)
    _init_app_blueprint(app)
    _init_app_conf(app ,conf_path)
    return app

def _init_app_blueprint(app):
    """
    添加蓝图
    :param app:
    :return:
    """
    from tokenmanager.api import blueprint
    for bp in blueprint:
        app.register_blueprint(bp)

def _init_app_conf(app , conf_path):
    """
    初始化配置
    :param app:
    :return:
    """
    from tokenmanager.core.utils import openYaml
    import os

    # 读取配置
    if conf_path is None:
        _HERE = os.path.dirname(__file__) # 当前文件目录
        conf_path = os.path.join(os.path.dirname(_HERE) , "config/settings.yaml") # 父目录路径 + 配置文件相对路径
    conf = openYaml(conf_path)

    app.config.update(conf['SERVER'])
    app.config.update(conf[str(app.config['ENV']).upper()])

    app.logger.info("JWT_SIGNATURE_PIVE_KEY_PATH : %s",(app.config['JWT_SIGNATURE_PIVE_KEY_PATH']))

    # reading key files
    with open(app.config['JWT_SIGNATURE_PIVE_KEY_PATH']) as f:
        app.logger.info("JWT_SIGNATURE_PIVE_KEY_PATH : %s", (f.read()))
        app.config['JWT_SIGNATURE_PRIV_KEY'] = f.read()

    with open(app.config['JWT_SIGNATURE_PLUB_KEY_PATH']) as f:
        app.config['JWT_SIGNATURE_PLUB_KEY'] = f.read()