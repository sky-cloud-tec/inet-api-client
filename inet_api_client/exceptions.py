#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sky Cloud API Client 异常类定义
"""


class SkyApiException(Exception):
    """Sky API 基础异常类"""
    pass


class AuthenticationError(SkyApiException):
    """认证失败异常"""
    pass


class APIRequestError(SkyApiException):
    """API请求异常"""
    
    def __init__(self, message, status_code=None, url=None):
        self.status_code = status_code
        self.url = url
        super().__init__(message)


class TokenExpiredError(AuthenticationError):
    """Token过期异常"""
    pass


class InvalidCredentialsError(AuthenticationError):
    """凭据无效异常"""
    pass
