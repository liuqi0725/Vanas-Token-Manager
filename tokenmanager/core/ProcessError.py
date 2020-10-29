# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# @File     : ProcessError.py
# @Created  : 2020/10/23 6:05 下午
# @Software : PyCharm
# 
# @Author   : Liu.Qi
# @Contact  : liuqi_0725@aliyun.com
# 
# @Desc     : 处理中的异常
# -------------------------------------------------------------------------------

class TokenError(Exception):
    pass

class NotSupportServiceError(TokenError):
    """
    不支持的service
    """
    pass

class BadSecretKeyError(TokenError):
    """
    错误的秘钥错误
    """
    pass

class GrantTypeError(TokenError):
    """
    客户端凭证错误
    """
    pass