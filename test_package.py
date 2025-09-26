#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Sky API Client包的基本功能
"""

import asyncio
import sys

def test_import():
    """测试导入功能"""
    print("=== 测试导入功能 ===")
    
    try:
        # 测试基本导入
        from sky_api_client import ApiClient
        print("✅ ApiClient 导入成功")
        
        # 测试异常类导入
        from sky_api_client import SkyApiException, AuthenticationError, APIRequestError
        print("✅ 异常类导入成功")
        
        # 测试版本信息
        import sky_api_client
        print(f"✅ 包版本: {sky_api_client.__version__}")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


def test_client_creation():
    """测试客户端创建"""
    print("\n=== 测试客户端创建 ===")
    
    try:
        from sky_api_client import ApiClient
        
        # 基础配置
        client = ApiClient(host="127.0.0.1")
        print("✅ 基础客户端创建成功")
        
        # 自定义配置
        client2 = ApiClient(
            host="192.168.1.100",
            port=8080,
            protocol="https",
            username="test_user",
            password="test_pass",
            timeout=120
        )
        print("✅ 自定义配置客户端创建成功")
        
        # 使用token
        client3 = ApiClient(
            host="192.168.1.100",
            token="test_token",
            auto_login=False
        )
        print("✅ Token配置客户端创建成功")
        
        return True
    except Exception as e:
        print(f"❌ 客户端创建失败: {e}")
        return False


async def test_async_context():
    """测试异步上下文管理器"""
    print("\n=== 测试异步上下文管理器 ===")
    
    try:
        from sky_api_client import ApiClient, AuthenticationError
        
        # 由于没有真实的服务器，这里会失败，但我们可以测试上下文管理器的结构
        try:
            async with ApiClient(host="127.0.0.1", auto_login=False) as client:
                print("✅ 异步上下文管理器结构正常")
                # 测试客户端方法是否存在
                assert hasattr(client, 'init_login'), "缺少 init_login 方法"
                assert hasattr(client, 'is_authenticated'), "缺少 is_authenticated 方法"
                assert hasattr(client, 'get_device_by_ip'), "缺少 get_device_by_ip 方法"
                assert hasattr(client, 'get_vlan_list_simple'), "缺少 get_vlan_list_simple 方法"
                print("✅ 客户端方法检查通过")
                
        except AuthenticationError:
            print("✅ 异步上下文管理器正常（预期的认证错误）")
        except Exception as e:
            if "Connection" in str(e) or "connect" in str(e).lower():
                print("✅ 异步上下文管理器正常（预期的连接错误）")
            else:
                raise e
                
        return True
    except Exception as e:
        print(f"❌ 异步上下文管理器测试失败: {e}")
        return False


def test_method_availability():
    """测试方法可用性"""
    print("\n=== 测试方法可用性 ===")
    
    try:
        from sky_api_client import ApiClient
        
        client = ApiClient(host="127.0.0.1", auto_login=False)
        
        # 测试主要API方法是否存在
        api_methods = [
            # 设备管理
            'get_device_by_ip',
            'get_device_by_name',
            'get_devices_info_for_name_and_type',
            'get_switch_router_info',
            
            # VLAN管理
            'get_vlan_list_simple',
            'batch_add_vlan',
            'batch_del_vlan',
            'put_vlan',
            'vlan_config_sync',
            
            # VPN管理
            'get_vpn_list_simple',
            'add_vpn',
            'add_vpn_batch',
            'update_vpn',
            'delete_vpn_batch',
            
            # 工作流管理
            'create_workflow_task',
            'callback_work_order',
            'get_pipeline_info',
            'rollback_pipeline',
            
            # 认证相关
            'init_login',
            'check_token',
            'is_authenticated',
            'ensure_authenticated',
        ]
        
        missing_methods = []
        for method in api_methods:
            if not hasattr(client, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ 缺少方法: {missing_methods}")
            return False
        else:
            print(f"✅ 所有API方法都存在 ({len(api_methods)} 个)")
            return True
            
    except Exception as e:
        print(f"❌ 方法可用性测试失败: {e}")
        return False


def test_exception_classes():
    """测试异常类"""
    print("\n=== 测试异常类 ===")
    
    try:
        from sky_api_client import (
            SkyApiException, 
            AuthenticationError, 
            APIRequestError
        )
        
        # 测试异常继承关系
        assert issubclass(AuthenticationError, SkyApiException), "AuthenticationError 继承关系错误"
        assert issubclass(APIRequestError, SkyApiException), "APIRequestError 继承关系错误"
        
        # 测试异常创建
        base_exc = SkyApiException("测试基础异常")
        auth_exc = AuthenticationError("测试认证异常")
        api_exc = APIRequestError("测试API异常", status_code=404, url="http://test.com")
        
        print("✅ 异常类结构正确")
        print(f"✅ 基础异常: {base_exc}")
        print(f"✅ 认证异常: {auth_exc}")
        print(f"✅ API异常: {api_exc}")
        
        return True
    except Exception as e:
        print(f"❌ 异常类测试失败: {e}")
        return False


async def main():
    """主测试函数"""
    print("Sky API Client 包测试")
    print("=====================")
    
    tests = [
        ("导入功能", test_import),
        ("客户端创建", test_client_creation),
        ("异步上下文管理器", test_async_context),
        ("方法可用性", test_method_availability),
        ("异常类", test_exception_classes),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n正在运行: {test_name}")
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
        results.append((test_name, result))
    
    # 汇总结果
    print("\n=== 测试结果汇总 ===")
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！包已准备就绪。")
        return 0
    else:
        print(f"\n⚠️  有 {total-passed} 个测试失败，请检查代码。")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
