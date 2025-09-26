# Inet API Client

Inet API Client 是一个用于访问Sky Cloud平台API的Python客户端库，支持设备管理、VLAN管理、VPN管理等功能。

## 特性

- 异步HTTP客户端
- 自动认证和Token管理
- 密码加密保护
- 完整的API接口覆盖

## 安装

```bash
pip install inet-api-client
```

## 快速开始

### 基础用法

```python
import asyncio
from sky_api_client import ApiClient

async def main():
    # 创建客户端实例
    async with ApiClient(host="192.168.1.100") as client:
        # 获取设备信息
        device_info = await client.get_device_by_ip("192.168.1.1")
        print(device_info)
        
        # 获取VLAN列表
        vlan_list = await client.get_vlan_list_simple()
        print(vlan_list)

# 运行异步函数
asyncio.run(main())
```

### 自定义配置

```python
import asyncio
from sky_api_client import ApiClient

async def main():
    # 自定义配置
    client = ApiClient(
        host="192.168.1.100",
        port=443,
        protocol="https",
        username="admin",
        password="password",
        timeout=30
    )
    
    await client.init_login()
    
    # 使用API
    devices = await client.get_device_list()
    print(devices)

asyncio.run(main())
```

## API 方法

- 设备管理：`get_device_list()`, `get_device_by_ip()`
- VLAN管理：`get_vlan_list()`, `create_vlan()`
- VPN管理：`get_vpn_list()`, `create_vpn()`
- 工作流管理：`get_workflow_list()`, `create_workflow()`

## 许可证

MIT License