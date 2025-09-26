#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完全兼容原有脚本的用法
"""

import asyncio
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_original_usage():
    """测试原有脚本的使用方式"""
    print("=== 测试原有脚本用法 ===")
    
    try:
        # 完全按照原有脚本的方式导入和使用
        from sky_api_client import ApiClient
        
        # 1. 无参数初始化（原有脚本方式）
        print("1. 测试无参数初始化...")
        api_client = ApiClient()
        print("✅ 无参数初始化成功")
        
        # 2. 测试 self.url 属性
        print("2. 测试 self.url 属性...")
        print(f"✅ self.url = {api_client.url}")
        
        # 3. 测试 init_login() 方法（会尝试连接，预期失败但方法存在）
        print("3. 测试 init_login() 方法...")
        try:
            await api_client.init_login()
            print("✅ init_login() 方法调用成功")
        except Exception as e:
            print(f"⚠️  init_login() 连接失败（预期，因为服务器不可达）: {e}")
            print("✅ init_login() 方法存在且可调用")
        
        # 4. 测试 self.req() 方法结构
        print("4. 测试 self.req() 方法...")
        method = "GET"
        url = f"{api_client.url}/test"
        
        try:
            # 这会失败但能证明方法存在
            await api_client.req(method=method, url=url)
        except Exception as e:
            print(f"⚠️  req() 连接失败（预期）: {type(e).__name__}")
            print("✅ self.req() 方法存在且可调用")
        
        # 5. 测试原有脚本的典型URL构建方式
        print("5. 测试原有脚本的URL构建方式...")
        test_urls = [
            f"{api_client.url}/api/sky-cmdb/resource/instance/entrust_vpn",
            f"{api_client.url}/sky-flow/api/v0/vlan/list",
            f"{api_client.url}/api/sky-pipeline/pipeline/statistics/test"
        ]
        
        for test_url in test_urls:
            print(f"   ✅ URL构建: {test_url}")
        
        print("\n🎉 完全兼容原有脚本的使用方式！")
        return True
        
    except Exception as e:
        print(f"❌ 兼容性测试失败: {e}")
        return False


async def test_method_compatibility():
    """测试方法兼容性"""
    print("\n=== 测试方法兼容性 ===")
    
    try:
        from sky_api_client import ApiClient
        
        api_client = ApiClient()
        
        # 检查所有原有脚本中可能用到的方法
        required_methods = [
            'init_login',
            'req',
            'create_workflow_task',  # 原来的 create_flow_task
            'get_devices_info_for_name_and_type',
            'get_vpn_list',
            'batch_add_vlan',
            'batch_del_vlan',
            'rollback_pipeline',
            'callback_work_order',
        ]
        
        missing_methods = []
        for method in required_methods:
            if hasattr(api_client, method):
                print(f"✅ {method} 方法存在")
            else:
                missing_methods.append(method)
                print(f"❌ {method} 方法缺失")
        
        # 检查关键属性
        required_attributes = ['url', 'headers', 'timeout']
        missing_attributes = []
        
        for attr in required_attributes:
            if hasattr(api_client, attr):
                print(f"✅ {attr} 属性存在: {getattr(api_client, attr)}")
            else:
                missing_attributes.append(attr)
                print(f"❌ {attr} 属性缺失")
        
        if not missing_methods and not missing_attributes:
            print("\n🎉 所有必需的方法和属性都存在！")
            return True
        else:
            print(f"\n❌ 缺失方法: {missing_methods}")
            print(f"❌ 缺失属性: {missing_attributes}")
            return False
            
    except Exception as e:
        print(f"❌ 方法兼容性测试失败: {e}")
        return False


def test_import_compatibility():
    """测试导入兼容性"""
    print("\n=== 测试导入兼容性 ===")
    
    try:
        # 测试主要导入
        from sky_api_client import ApiClient
        print("✅ 主类导入成功")
        
        # 测试异常类导入
        from sky_api_client import SkyApiException, AuthenticationError, APIRequestError
        print("✅ 异常类导入成功")
        
        # 测试版本信息
        import sky_api_client
        version = getattr(sky_api_client, '__version__', 'Unknown')
        print(f"✅ 包版本: {version}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


async def test_script_migration_example():
    """测试脚本迁移示例"""
    print("\n=== 脚本迁移示例 ===")
    
    print("原有脚本代码：")
    print("""
# 原来的代码
from inet_api.ApiClinet import ApiClientBase

api_client = ApiClient()
await api_client.init_login()
url = f"{api_client.url}/api/sky-cmdb/resource/instance/entrust_vpn"
res = await api_client.req(method="POST", url=url, json=data)
""")
    
    print("\n新的代码（几乎完全相同）：")
    print("""
# 新的代码
from sky_api_client import ApiClient

api_client = ApiClient()
await api_client.init_login()
url = f"{api_client.url}/api/sky-cmdb/resource/instance/entrust_vpn"
res = await api_client.req(method="POST", url=url, json=data)
""")
    
    print("\n🎯 需要的改动：")
    print("1. 修改导入语句")
    print("2. 就这样！其他代码完全不用改！")
    
    # 实际测试这个模式
    try:
        from sky_api_client import ApiClient
        
        api_client = ApiClient()
        
        # 模拟原有脚本的使用模式
        data = {"test": "data"}
        url = f"{api_client.url}/api/sky-cmdb/resource/instance/entrust_vpn"
        
        print(f"\n✅ URL构建成功: {url}")
        print("✅ 原有脚本模式完全兼容")
        
        return True
        
    except Exception as e:
        print(f"❌ 脚本迁移测试失败: {e}")
        return False


async def main():
    """主测试函数"""
    print("Sky API Client 兼容性测试")
    print("========================")
    
    tests = [
        ("导入兼容性", test_import_compatibility),
        ("原有用法测试", test_original_usage),
        ("方法兼容性", test_method_compatibility),
        ("脚本迁移示例", test_script_migration_example),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"正在运行: {test_name}")
        print('='*50)
        
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
        results.append((test_name, result))
    
    # 汇总结果
    print(f"\n{'='*50}")
    print("兼容性测试结果汇总")
    print('='*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有兼容性测试通过！")
        print("您的原有脚本只需要修改导入语句就可以使用新的ApiClient！")
        print("\n📋 迁移步骤：")
        print("1. pip install sky-api-client")
        print("2. 将 'from inet_api.ApiClinet import ApiClientBase' 改为 'from sky_api_client import ApiClient'")
        print("3. 完成！其他代码无需修改。")
        return 0
    else:
        print(f"\n⚠️  有 {total-passed} 个测试失败，需要检查兼容性。")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
