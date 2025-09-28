#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sky Cloud API 基础客户端，重构自原有的BaseClient，移除config依赖
"""

import aiohttp
import logging
from typing import Dict, Any
from .exceptions import APIRequestError, AuthenticationError


class BaseClient:
    """Sky Cloud API 基础客户端"""
    
    def __init__(
        self,
        host: str,
        port: int = 80,
        protocol: str = "http",
        username: str = "admin",
        password: str = "r00tme",
        timeout: int = 60
    ):
        """
        初始化基础客户端
        
        Args:
            host: 服务器主机地址
            port: 服务器端口，默认80
            protocol: 协议，默认http
            username: 用户名，默认admin
            password: 密码，默认r00tme
            timeout: 请求超时时间，默认60秒
        """
        self.host = host
        self.port = port
        self.protocol = protocol
        self.username = username
        self.password = password
        self.timeout = timeout
        
        self.url = f"{protocol}://{host}:{port}"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        
        # 设置日志
        self.logger = logging.getLogger(__name__)

    def set_headers(self, headers: Dict[str, str]):
        """更新请求头"""
        self.headers.update(headers)

    def get_headers(self) -> Dict[str, str]:
        """获取当前请求头"""
        return self.headers.copy()
        

    async def work_login_init(self) -> str:
        """
        获取登录的token
        
        Returns:
            认证token
        """
        url = f"{self.url}/api/sky-platform/auth/user/v2/login"
        data = {
            "username": self.username,
            "password": self.password
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, 
                    json=data, 
                    headers=self.headers, 
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    response_data = await response.json()
                    
                    if response_data.get("code") != 200:
                        raise AuthenticationError(f"登录失败，原因为：{response_data}")
                        
                    token = response_data.get("data")
                    self.logger.info(f"登录完成，token：{token}")
                    self.headers["cookie"] = f"access_token={token}"
                    return token
        except aiohttp.ClientError as e:
            raise AuthenticationError(f"网络连接失败: {e}")
        except Exception as e:
            raise AuthenticationError(f"登录过程中发生错误: {e}")

    async def req(
        self, 
        method: str, 
        url: str, 
        check_response: bool = True, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        Args:
            method: HTTP方法
            url: 请求URL
            check_response: 是否检查响应状态
            **kwargs: 其他请求参数
            
        Returns:
            响应数据
        """
        method = method.lower()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method, 
                    url, 
                    headers=self.headers, 
                    timeout=aiohttp.ClientTimeout(total=self.timeout), 
                    **kwargs
                ) as response:
                    response_data = await response.json()
                    
                    if check_response:
                        if response.status == 401:
                            return {
                                'code': response.status, 
                                'message': f"Unauthorized access {url}:{response_data}"
                            }
                        if response.status >= 400:
                            raise APIRequestError(
                                f"API request failed with {url}:{response_data}",
                                status_code=response.status,
                                url=url
                            )
                    
                    self.logger.info(f"请求url: {url}, method: {method} result: ok")
                    return response_data
                    
        except aiohttp.ClientError as e:
            raise APIRequestError(f"网络请求失败: {e}", url=url)
        except Exception as e:
            raise APIRequestError(f"请求过程中发生错误: {e}", url=url)
