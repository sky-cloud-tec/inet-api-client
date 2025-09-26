# Sky API Client 迁移指南

## 🎉 好消息！您的脚本几乎不需要修改！

我们已经创建了一个完全兼容您现有脚本的独立PyPI包 `sky-api-client`。这个包提供了与您现有 `ApiClient` 完全相同的接口。

## 📦 安装

```bash
pip install sky-api-client
```

## 🔄 迁移步骤

### 1. 修改导入语句

**原来的代码：**
```python
from inet_api.ApiClinet import ApiClientBase
```

**新的代码：**
```python
from sky_api_client import ApiClient
```

### 2. 其他代码完全不需要修改！

您的现有脚本代码可以保持不变：

```python
# 这些代码完全不需要修改
api_client = ApiClient()
await api_client.init_login()

# self.url代表当前环境的ip
url = f"{api_client.url}/api/sky-cmdb/resource/instance/entrust_vpn"

# self.req() 是调用接口的方法，和requests库的请求参数一样
res = await api_client.req(method=method, url=url, json=data)
```

## ✅ 完全兼容的功能

- ✅ **无参数初始化**: `ApiClient()`
- ✅ **init_login() 方法**: `await api_client.init_login()`
- ✅ **self.url 属性**: `api_client.url`
- ✅ **self.req() 方法**: `await api_client.req(method, url, **kwargs)`
- ✅ **所有现有的API方法**: 设备管理、VLAN管理、VPN管理等

## 🔧 唯一需要注意的变化

### 方法名更新

有一个方法名发生了变化（为了更好的命名规范）：

- `create_flow_task` → `create_workflow_task`

如果您使用了这个方法，只需要更新方法名即可。

## 📋 具体迁移示例

### 示例1: rollback_pipeline.py

**原来的代码：**
```python
from inet_api.ApiClinet import ApiClientBase

async def main(args: Args):
    # 初始化 ApiClient 类
    api_client = ApiClient()
    await api_client.init_login()
    
    # 调用API
    result = await api_client.rollback_pipeline("POST", data_id, pipeline_id)
```

**迁移后的代码：**
```python
from sky_api_client import ApiClient

async def main(args: Args):
    # 初始化 ApiClient 类（完全一样）
    api_client = ApiClient()
    await api_client.init_login()
    
    # 调用API（完全一样）
    result = await api_client.rollback_pipeline("POST", data_id, pipeline_id)
```

### 示例2: 批量业务脚本

**原来的代码：**
```python
from inet_api.ApiClinet import ApiClientBase

async def main(args: Args):
    # 初始化 ApiClient 类
    api_client = ApiClient()
    await api_client.init_login()
    
    # 创建工作流任务
    res = await api_client.create_flow_task(method="post", data=data)
```

**迁移后的代码：**
```python
from sky_api_client import ApiClient

async def main(args: Args):
    # 初始化 ApiClient 类（完全一样）
    api_client = ApiClient()
    await api_client.init_login()
    
    # 创建工作流任务（只需要改方法名）
    res = await api_client.create_workflow_task(data)  # 注意方法名变化
```

## 🚀 新功能优势

使用新的 `sky-api-client` 包，您将获得：

1. **独立部署**: 不再依赖项目的 `config.py` 文件
2. **更好的错误处理**: 更详细的错误信息和异常类型
3. **更灵活的配置**: 支持多种初始化方式
4. **更好的日志**: 内置的日志记录功能
5. **异步上下文管理器**: 支持 `async with` 语法

## 🔧 高级用法（可选）

如果您想使用新功能，可以选择以下方式：

### 方式1: 自定义配置
```python
from sky_api_client import ApiClient

# 自定义服务器配置
api_client = ApiClient(
    host="192.168.1.100",
    port=8080,
    protocol="https",
    username="admin",
    password="your_password"
)
```

### 方式2: 使用上下文管理器
```python
from sky_api_client import ApiClient

async with ApiClient(host="192.168.1.100") as api_client:
    # 自动处理认证和清理
    result = await api_client.get_device_by_ip("192.168.1.1")
```

## 📞 支持

如果您在迁移过程中遇到任何问题，请：

1. 检查导入语句是否正确
2. 确认方法名是否已更新（`create_flow_task` → `create_workflow_task`）
3. 查看包的文档和示例

## 🎯 总结

迁移非常简单：

1. **安装**: `pip install sky-api-client`
2. **修改导入**: `from sky_api_client import ApiClient`
3. **更新方法名**: `create_flow_task` → `create_workflow_task`
4. **完成！** 其他代码无需修改

您的现有脚本将能够无缝运行，同时获得独立部署和更好的功能！
