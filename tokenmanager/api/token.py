# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : token.py
# @Created  : 2020/10/23 5:59 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : token api
# -------------------------------------------------------------------------------

from flask import current_app,request,Blueprint

from tokenmanager.core.utils import E400,render_json
from tokenmanager.core.Security import create_token,verify_token,get_pub_key
from vanaspyhelper.LoggerManager import log

token = Blueprint("token" , __name__)

@token.route('/.well-known/jwks.json')
def _jwks():
    """
    返回签名 公钥
    :return: json
    """

    log.info("处理请求：获取公钥")
    key = {
        "alg": current_app.config['JWT_ALGORITHM'], # 算法
        "e": "AQAB",
        "n": get_pub_key(),                         # 公钥
        "kty": "RSA",
        "use": "Signature"                          # 用途
    }
    log.info("处理请求：获取公钥处理完成")

    return render_json(key)

@token.route("/oauth/token",methods=['POST'])
def generate_token():
    """
    生成 token
    :return: json
    """

    try:
        data = request.json
        log.info("处理请求：创建 token . Data: %s ",data)

        grant_type = data.get('grant_type', '')
        client_id = data.get('client_id', '')
        signature = data.get('signature', '')
        timestamp = int(data.get('timestamp', '0'))

        # 封装 token
        res_json = create_token(client_id ,signature, timestamp, grant_type)
        log.info("处理请求：创建 token . Result: %s ", res_json)
        return render_json(res_json)
    except Exception as e3:
        log.error("处理请求：创建 token . Error: %s ", str(e3))
        return E400(str(e3))


@token.route('/verify_token', methods=['POST'])
def verify_token_data():
    """
    验证 token
    :return:
    """
    try:
        # 报文要用 json报文，使用 双引号 "
        data = request.json
        log.info("处理请求：验证 token . Data: %s ", data)

        token = data['access_token']
        audience = data.get('client_id', '')
        res_json = verify_token(token,audience)
        log.info("处理请求：验证 token . Result: %s ", res_json)
        return render_json(res_json)
    except Exception as e:
        log.error("处理请求：验证 token . Error: %s ", str(e))
        return E400(str(e))