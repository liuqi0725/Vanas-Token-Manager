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
from service.core.utils import openYaml
from service.api import blueprint
import os

# 读取配置
_SETTINGS_PATH = os.path.join(os.path.dirname(__file__), 'setting.yaml')

conf = openYaml(_SETTINGS_PATH)

def create_app():
    app = Flask(__name__)
    # CSRF【跨站点请求伪造】 key
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    # 数据库地址  /// 相对路径， ////绝对路径
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/runnerly.db'
    # 设置值为 True 不然 SQLALCHEMY 没提供默认值。
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.config.update(conf['ca_key'])
    app.config['service_secret_key'] = conf['service_secret_key']
    app.config['jwt_algorithm'] = conf['jwt_algorithm']
    app.config['grant_type'] = conf['grant_type']
    app.config['jwt_iss'] = conf['jwt_iss']

    # 添加蓝图
    for bp in blueprint:
        app.register_blueprint(bp)

    # reading key files
    with open(app.config['priv_key']) as f:
        app.config['priv_key'] = f.read()

    with open(app.config['pub_key']) as f:
        app.config['pub_key'] = f.read()

    return app

def main():
    """
    开始
    :return:
    """
    app = create_app()
    app.run(debug=conf['debug'], port=conf['port'])

if __name__ == "__main__" :
    main()