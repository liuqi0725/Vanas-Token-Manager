# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : Security.py
# @Created  : 2020/10/23 6:05 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 目的?
# -------------------------------------------------------------------------------
import json
import time

from flask import current_app
from hmac import compare_digest

import jwt,enum

from jwt.exceptions import InvalidKeyError, MissingRequiredClaimError
from vanaspyhelper.util.common import md5

from .ProcessError import NotSupportServiceError, BadSecretKeyError, GrantTypeError, ClientConfigNotFound
from .utils import get_timestamp,json_res_failure,json_res_success

from jwt import InvalidSignatureError, ExpiredSignatureError, InvalidAudienceError, InvalidIssuerError, \
    InvalidIssuedAtError, ImmatureSignatureError, DecodeError, InvalidTokenError, InvalidAlgorithmError


class TokenErrorCode(enum.Enum):
    """
    token 相关错误编码
    """

    # Token 错误
    INVALID_TOKEN_ERROR = 1001
    # Token 解码失败
    TOKEN_DECODE_ERROR = 1002
    # Token 签名不匹配
    TOKEN_INVALID_SIGNATURE_ERROR = 1003
    # Token 已过期
    TOKEN_EXPIRED_ERROR = 1004
    # Token audience【aud】受众 不匹配
    TOKEN_INVALID_AUDIENCE_ERROR = 1005
    # Token 中 iss【令牌发放者】不匹配
    TOKEN_INVALID_ISSUER_ERROR = 1006
    # Token 中 iat【令牌发放时间】错误
    TOKEN_INVALID_ISSUEDAT_ERROR = 1007
    # Token 中 nbf 错误
    TOKEN_IMMATURE_SIGNATURE_ERROR = 1008
    # TOKEN 关键参数缺失
    TOKEN_MISSING_REQUIRED_CLAIM_ERROR = 1009
    # TOKEN 创建时，解密 client data 错误
    TOKEN_DECRYPT_CLIENT_DATA_ERROR = 1010
    # TOKEN 创建时，签名超过时限
    TOKEN_SIGNATURE_TIMEOUT = 1020
    # TOKEN 创建时，签名超过时限
    TOKEN_SIGNATURE_BAD = 1030



    # 键值解析错误
    TOKEN_INVALID_KEY_ERROR = 1100
    # 当指定的算法不能被PyJWT识别时引发
    TOKEN_INVALID_ALGORITHM_ERROR = 1200

    # 不支持的 service
    NOT_SUPPORT_SERVICE_ERROR = 1300

    # Service 对应的 secret key 错误
    BAD_SECRET_KEY_ERROR = 1400

    # 客户端授权认证类型错误
    GRANT_TYPE_ERROR = 1500

    # 服务端的 client 配置文件无法获取
    CLIENT_CONF_NOT_FOUND = 1600


def get_pub_key():
    """
    获取签名公钥
    :return:
    """
    return current_app.config['JWT_SIGNATURE_PLUB_KEY']

def _get_priv_key():
    """
    获取签名秘钥
    :return:
    """
    return current_app.config['JWT_SIGNATURE_PRIV_KEY']

def _is_authorized_app(client_id:str, grant_type:str)->str:
    """
    验证 service 的 client、grant_type。 配置参考 setting.yaml
    :param client_id: service id
    :param grant_type:  客户端授权凭证
    :return: client_secret:  service secret key
    """

    from konfig import Config
    # 获取所有的 client id 对应的 client serct
    c = Config(current_app.config['SECURITY_CONF_PATH'])

    try:
        clients_map = c.get_map('CLIENT_LIST')
    except:
        raise ClientConfigNotFound("无法获取服务端 Client 配置.请研发人员核实. PATH : {}".format(current_app.config['SECURITY_CONF_PATH']))

    secret_key = clients_map.get(client_id)

    if not secret_key:
        raise NotSupportServiceError("未知的 Service ID : [{}]. 请核实!".format(client_id))

    if not compare_digest(current_app.config['JWT_GRANT_TYPE'], grant_type):
        raise GrantTypeError("unKnow `grant_type` . Plz get it from your app development. '{}' . ".format(grant_type))

    return secret_key



def create_token(client_id:str, signature:str, timestamp:int, grant_type:str, exp_time:int=86400):
    """
    创建 token
    验证 service 的 secret key、grant_type。 配置参考 setting.yaml
    :param client_id: 客户端服务 id
    :param signature: 签名 . 加密方式 : MD5(<aes_key> + <client_secret> + <timestamp>).lower()
                        <aes_key> 服务端 aes_key
                        <client_secret> 客户端 秘钥
                        <timestamp> 客户端 获取 token 时的 post 参数 timestamp , 有效时间 30 秒
    :param grant_type:  客户端授权凭证
    :param exp_time: 过期时间[秒] 默认 一天
    :return:
    """


    # 如果 timestamp > 30 秒 无效签名
    current_time = int(time.time())
    if (current_time - timestamp) > 30:
        return json_res_failure("无效 signature。请核实!", TokenErrorCode.TOKEN_SIGNATURE_TIMEOUT)

    # 验证 client_id, grant_type 并获取 secret_key
    try:
        secret_key = _is_authorized_app(client_id, grant_type)
    except NotSupportServiceError as e1:
        return json_res_failure(str(e1), TokenErrorCode.NOT_SUPPORT_SERVICE_ERROR)
    except GrantTypeError as e3:
        return json_res_failure(str(e3), TokenErrorCode.GRANT_TYPE_ERROR)
    except ClientConfigNotFound as e4:
        return json_res_failure(str(e4), TokenErrorCode.CLIENT_CONF_NOT_FOUND)

    # 验证客户端签名
    server_signature = md5(current_app.config['AES_SECRET_KEY'] + secret_key + str(timestamp)).lower()

    if signature != server_signature:
        return json_res_failure("无效 signature。请核实!", TokenErrorCode.TOKEN_SIGNATURE_BAD)

    now = get_timestamp()

    token = {
        'iss': current_app.config['JWT_ISS'],   # 令牌发放者，生成令牌的实体名称。通常是一个主机名
        'aud': client_id,                       # 受众：用来告知谁是令牌的接收人。客户端可以判断是否自己是接收人[接收jwt的一方]
        'iat': now,                             # 令牌发放时间
        'exp': now + exp_time,                  # 令牌到期时间
        'nbf': now,                             # 令牌在这个时间之前无效
        'sub': '',                              # 令牌所面向的用户
        'jti': ''                               # 令牌的唯一身份标识，主要用来作为一次性token, 从而回避重放攻击。
    }

    try:
        # algorithm 指定算法
        token = jwt.encode(token, _get_priv_key(), algorithm=current_app.config['JWT_ALGORITHM'])
        return json_res_success({'access_token': token.decode('utf8')})
    except InvalidSignatureError:
        return json_res_failure("Token 签名不匹配" , TokenErrorCode.TOKEN_INVALID_SIGNATURE_ERROR)
    except InvalidIssuedAtError:
        return json_res_failure("Token 中 iat【令牌发放时间】错误。必须为整形数字。", TokenErrorCode.TOKEN_INVALID_ISSUEDAT_ERROR)
    except InvalidAlgorithmError as e:
        return json_res_failure("Token 指定的算法不能被PyJWT识别。", TokenErrorCode.TOKEN_INVALID_ALGORITHM_ERROR , str(e))
    except InvalidTokenError as e:
        return json_res_failure("Token 错误。", TokenErrorCode.INVALID_TOKEN_ERROR , str(e))
    except InvalidKeyError as e:
        return json_res_failure("Token 键值解析错误。", TokenErrorCode.TOKEN_INVALID_KEY_ERROR,str(e))


def verify_token(token , client_id):
    """
    验证 token
    :param token: token
    :param client_id: 受众,对应 token 中 audience 字段
    :return:
    """
    try:
        return json_res_success(jwt.decode(token, get_pub_key(), audience=client_id))
    except InvalidSignatureError:
        return json_res_failure("Token 签名不匹配。", TokenErrorCode.TOKEN_INVALID_SIGNATURE_ERROR)
    except ExpiredSignatureError:
        return json_res_failure("Token 已过期。", TokenErrorCode.TOKEN_EXPIRED_ERROR)
    except InvalidAudienceError:
        return json_res_failure("client_id 错误。", TokenErrorCode.TOKEN_INVALID_AUDIENCE_ERROR)
    except InvalidIssuerError:
        return json_res_failure("Token 中 iss【令牌发放者】错误。", TokenErrorCode.TOKEN_INVALID_ISSUER_ERROR)
    except InvalidIssuedAtError:
        return json_res_failure("Token 中 iat【令牌发放时间】错误。必须为整形数字。", TokenErrorCode.TOKEN_INVALID_ISSUEDAT_ERROR)
    except ImmatureSignatureError:
        return json_res_failure("Token 中 nbf 未生效。", TokenErrorCode.TOKEN_IMMATURE_SIGNATURE_ERROR)
    except InvalidAlgorithmError as e:
        return json_res_failure("Token 指定的算法不能被PyJWT识别。", TokenErrorCode.TOKEN_INVALID_ALGORITHM_ERROR , str(e))
    except MissingRequiredClaimError as e:
        return json_res_failure("Token 关键参数缺失。", TokenErrorCode.TOKEN_MISSING_REQUIRED_CLAIM_ERROR , str(e))
    except DecodeError as e:
        return json_res_failure("Token 解码错误。", TokenErrorCode.TOKEN_DECODE_ERROR , str(e))
    except InvalidTokenError as e:
        return json_res_failure("Token 错误。", TokenErrorCode.INVALID_TOKEN_ERROR , str(e))
    except InvalidKeyError as e:
        return json_res_failure("Token 键值解析错误。", TokenErrorCode.TOKEN_INVALID_KEY_ERROR,str(e))