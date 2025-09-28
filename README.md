# Inet API Client

Inet API Client 是一个用于访问 Sky Cloud 平台 API 的 Python 客户端库，提供完整的设备管理、VLAN 管理、VPN 管理、工作流管理等功能。

## ✨ 特性

- 🚀 **异步 HTTP 客户端** - 基于 aiohttp 的高性能异步请求
- 🔐 **自动认证管理** - 支持多种认证方式，自动处理 Token 刷新
- 📦 **完整 API 覆盖** - 涵盖 Sky Cloud 平台所有核心功能
- 🔄 **完全向后兼容** - 无需修改现有脚本即可使用
- 🛡️ **错误处理** - 完善的异常处理和错误信息
- 📝 **类型提示** - 完整的类型注解支持

## 📦 安装

```bash
pip install inet-api-client
```

## 🚀 快速开始
## 🔧 环境变量

您可以通过环境变量来配置客户端：

```bash
export SKY_API_HOST="192.168.1.100"
export SKY_API_USERNAME="admin"
export SKY_API_PASSWORD="password" 
```

### 使用封装接口用法

```python
import asyncio
from inet_api_client import ApiClient    

async def main():
    
    api_client = ApiClient(host="192.168.1.100")
    await api_client.init_login()
    # 获取设备信息
    device_info = await client.get_device_by_ip("192.168.1.1")
    print(f"设备信息: {device_info}")
    
    # 获取 VLAN 列表
    vlan_list = await client.get_vlan_list_simple()
    print(f"VLAN 列表: {vlan_list}")

# 运行异步函数
asyncio.run(main())
```

### 直接使用url请求用法

```python
import asyncio
from inet_api_client import ApiClient

async def main():
    # 初始化方式（完全兼容现有脚本）
    api_client = ApiClient()
    await api_client.init_login()
    
    # 使用 self.url 构建 URL（完全兼容）
    url = f"{api_client.url}/api/sky-cmdb/resource/instance/entrust_vpn"
    data = {"page": 0, "size": 10}
    
    # 使用 self.req() 方法调用接口（完全兼容）
    res = await api_client.req(method="POST", url=url, json=data)
    print(f"API 调用结果: {res}")

asyncio.run(main())
```

### 自定义配置

```python
import asyncio
from inet_api_client import ApiClient

async def main():
    # 自定义配置
    client = ApiClient(
        host="192.168.1.100",
        port=80,
        protocol="http",
        username="xxx",
        password="xxx",
        timeout=30
    )
    
    await client.init_login()
    
    # 使用 API
    devices = await client.get_device_list()
    print(f"设备列表: {devices}")

asyncio.run(main())
```

## 📚 API 方法

### 设备管理
- `get_device_list()` - 获取设备列表
- `get_device_by_ip(ip)` - 根据 IP 获取设备信息
- `get_device_by_id(device_id)` - 根据 ID 获取设备信息

### VLAN 管理
- `get_vlan_list()` - 获取 VLAN 列表
- `get_vlan_list_simple()` - 获取简化 VLAN 列表
- `create_vlan(vlan_data)` - 创建 VLAN
- `update_vlan(vlan_id, vlan_data)` - 更新 VLAN

### VPN 管理
- `get_vpn_list()` - 获取 VPN 列表
- `create_vpn(vpn_data)` - 创建 VPN
- `update_vpn(vpn_id, vpn_data)` - 更新 VPN

### 工作流管理
- `get_workflow_list()` - 获取工作流列表
- `create_workflow_task(task_data)` - 创建工作流任务
- `rollback_pipeline(method, data_id, pipeline_id)` - 回滚流水线

### 业务域管理
- `get_sdc_id_list(data)` - 获取业务域列表
- `get_sdc_detail(method, data)` - 获取业务域详情


## 📖 使用示例

### 示例 1：批量业务处理

```python
import asyncio
import json
from inet_api_client import ApiClient

async def batch_business_example():
    """批量业务处理示例"""
    api_client = ApiClient()
    await api_client.init_login()
    
    # 处理业务数据
    process_data = {
        "request": [
            {
                "branch": "xxx",
                "customerName": "xxx",
                "idc": "xxx",
                "switch_a": "xxx",
                "interface_a": "xxx",
                "vlan": "12",
                "pvlan": "56",
                "rack": "xxx",
                "unit": "xxx",
            }
        ]
    }
    
    # 创建工作流任务
    work_order_id_list = []
    for data in process_data["request"]:
        try:
            res = await api_client.create_workflow_task(data)
            task_id = res.get("data", {}).get("id")
            if task_id:
                work_order_id_list.append(task_id)
        except Exception as e:
            print(f"创建工作流任务失败: {e}")
    
    print(f"成功创建 {len(work_order_id_list)} 个工单")

asyncio.run(batch_business_example())
```

### 示例 2：设备管理

```python
import asyncio
from inet_api_client import ApiClient

async def device_management_example():
    """设备管理示例"""
    api_client = ApiClient()
    await api_client.init_login()
    # 获取所有设备
    devices = await client.get_device_list()
    print(f"总设备数: {len(devices.get('data', {}).get('content', []))}")
    
    # 根据 IP 查找特定设备
    device_info = await client.get_device_by_ip("192.168.1.1")
    print(f"设备详情: {device_info}")

asyncio.run(device_management_example())
```

### 示例 3：VLAN 管理

```python
import asyncio
from inet_api_client import ApiClient

async def vlan_management_example():
    """VLAN 管理示例"""
    api_client = ApiClient()
    await api_client.init_login()
    # 获取 VLAN 列表
    vlan_list = await client.get_vlan_list_simple()
    print(f"VLAN 列表: {vlan_list}")
    
    # 创建新 VLAN
    new_vlan = {
        "name": "xxx",
        "vlan_id": 100,
        "description": "xxx"
    }
    result = await client.create_vlan(new_vlan)
    print(f"创建 VLAN 结果: {result}")

asyncio.run(vlan_management_example())
```

## ⚙️ 配置选项

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `host` | str | 从环境变量读取 | Sky Cloud 服务器地址 |
| `port` | int | 80 | 服务器端口 |
| `protocol` | str | "https" | 协议类型 |
| `username` | str | 从环境变量读取 | 用户名 |
| `password` | str | 从环境变量读取 | 密码 |
| `timeout` | int | 30 | 请求超时时间（秒） |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License