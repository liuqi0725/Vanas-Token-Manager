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

token = Blueprint("token" , __name__)


@token.route('/.well-known/jwks.json')
def _jwks():
    """
    返回签名 公钥
    :return: json
    """
    key = {
        "alg": current_app.config['JWT_ALGORITHM'], # 算法
        "e": "AQAB",
        "n": get_pub_key(),                         # 公钥
        "kty": "RSA",
        "use": "Signature"                          # 用途
    }

    return render_json(key)

@token.route("/oauth/token",methods=['POST'])
def generate_token():
    """
    生成 token
    :return: json
    """
    try:
        data = request.form
        grant_type = data.get('grant_type')
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
        # 封装 token
        res_json = create_token(client_id , client_secret , grant_type)
        return render_json(res_json)
    except Exception as e3:
        return E400(str(e3))

@token.route('/verify_token', methods=['POST'])
def verify_token_data():
    """
    验证 token
    :return:
    """
    try:
        # 报文要用 json报文，使用 双引号 "
        token = request.json['access_token']
        audience = request.json.get('client_id', '')
        res_json = verify_token(token,audience)
        return render_json(res_json)
    except Exception as e:
        return E400(str(e))