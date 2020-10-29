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


from flask import Flask
from tokenmanager.core.utils import openYaml
import os

def create_app():
    app = Flask(__name__)
    _init_app_blueprint(app)
    _init_app_conf(app)
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

def _init_app_conf(app):
    """
    初始化配置
    :param app:
    :return:
    """

    # 读取配置
    _HERE = os.path.dirname(__file__)
    _SETTINGS_PATH = os.path.join(_HERE, 'setting.yaml')
    conf = openYaml(_SETTINGS_PATH)

    app.config.update(conf['SERVER'])
    app.config.update(conf[str(app.config['ENV']).upper()])

    # reading key files
    with open(app.config['JWT_SIGNATURE_PIVE_KEY_PATH']) as f:
        app.config['JWT_SIGNATURE_PRIV_KEY'] = f.read()

    with open(app.config['JWT_SIGNATURE_PLUB_KEY_PATH']) as f:
        app.config['JWT_SIGNATURE_PLUB_KEY'] = f.read()

def main():
    """
    开始
    :return:
    """
    app = create_app()
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])

if __name__ == "__main__" :
    main()