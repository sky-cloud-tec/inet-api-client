#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sky Cloud API 主客户端类，集成认证和API方法
"""

import os
import jwt
import logging
from datetime import datetime, timezone
from typing import Optional
from .base_client import BaseClient
from .api_methods import ApiMethods
from .exceptions import  AuthenticationError


class ApiClient(BaseClient, ApiMethods):
    """
    Sky Cloud API 客户端
    
    提供完整的Sky Cloud平台API访问功能，包括认证、设备管理、VLAN管理、VPN管理等
    """
    
    def __init__(
        self,
        host: Optional[str] = None,
        port: int = 80,
        protocol: str = "http",
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 60,
        token: Optional[str] = None,
        auto_login: bool = True
    ):
        """
        初始化Sky Cloud API客户端
        
        Args:
            host: Sky Cloud服务器主机地址 (可选，优先从环境变量SKY_API_HOST读取)
            port: 服务器端口，默认80
            protocol: 协议，默认http (http/https)
            username: 用户名 (可选，优先从环境变量SKY_API_USERNAME读取)
            password: 密码 (可选，优先从环境变量SKY_API_PASSWORD读取)
            timeout: 请求超时时间，默认60秒
            token: 可选的预设token，如果提供则跳过登录
            auto_login: 是否自动登录，默认True
            
        Example:
            # 使用环境变量配置
            export SKY_API_HOST="192.168.30.52"
            export SKY_API_USERNAME="admin"
            export SKY_API_PASSWORD="your_password"
            client = ApiClient()
            
            # 兼容原有脚本的用法
            client = ApiClient()
            await client.init_login()
            
            # 新的用法 - 基础配置
            client = ApiClient(host="192.168.1.100")
            
            # 自定义参数
            client = ApiClient(
                host="192.168.1.100",
                port=8080,
                protocol="https",
                username="myuser",
                password="mypassword",
                timeout=120
            )
            
            # 使用预设token
            client = ApiClient(
                host="192.168.1.100",
                token="your_token_here",
                auto_login=False
            )
        """
        # 从环境变量读取配置，如果参数未提供
        if host is None:
            host = os.environ.get("SKY_API_HOST", "192.168.30.52")
        
        if username is None:
            username = os.environ.get("SKY_API_USERNAME", "admin")
            
        if password is None:
            password = os.environ.get("SKY_API_PASSWORD", "r00tme")
            
        super().__init__(host, port, protocol, username, password, timeout)
        self.token = token
        self.auto_login = auto_login
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self):
        """异步上下文管理器入口"""
        if self.auto_login:
            await self.init_login()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        pass

    async def init_login(self):
        """
        初始化登录
        
        如果提供了token，直接使用；否则进行用户名密码登录
        """
        if self.token:
            self.set_headers({"cookie": f"access_token={self.token}"})
            self.logger.info("使用提供的token进行认证")
            
            # 验证token是否有效
            if self.check_token(self.token):
                self.logger.warning("提供的token已过期，尝试重新登录")
                await self._perform_login()
            else:
                self.logger.info("Token验证成功")
        else:
            await self._perform_login()

    async def _perform_login(self):
        """执行登录操作"""
        try:
            self.logger.info("开始用户名密码登录")
            login_token = await self.work_login_init()
            
            if self.check_token(login_token):
                # Token已过期，重新登录
                login_token = await self.work_login_init()
                
            self.token = login_token
            self.logger.info("登录成功")
            
        except Exception as e:
            self.logger.error(f"登录失败: {e}")
            raise AuthenticationError(f"登录失败: {e}")

    def check_token(self, token: str) -> bool:
        """
        检查token是否过期
        
        Args:
            token: JWT token
            
        Returns:
            True表示已过期，False表示未过期
        """
        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            exp_time = decoded_token.get("exp")
            
            if not exp_time:
                self.logger.warning("Token中未找到过期时间")
                return True
                
            current_time = datetime.now(timezone.utc).timestamp()
            is_expired = current_time > exp_time
            
            self.logger.info(f"Token过期检查: {'已过期' if is_expired else '有效'}")
            return is_expired
            
        except jwt.InvalidTokenError as e:
            self.logger.error(f"Token解析失败: {e}")
            return True
        except Exception as e:
            self.logger.error(f"Token检查过程中发生错误: {e}")
            return True



