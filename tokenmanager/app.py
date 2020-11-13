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

def create_app(config_name):
    from flask import Flask
    from .config import config
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    _init_app_blueprint(app)
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