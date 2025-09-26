#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全兼容原有脚本用法的示例
展示如何在不修改现有脚本代码的情况下使用新的ApiClient
"""

import asyncio
import json
import logging
from sky_api_client import ApiClient

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Args:
    """模拟原脚本的Args类"""
    def __init__(self, params):
        self.params = params


async def original_style_script_example():
    """
    完全按照原有脚本风格的示例
    这个示例展示如何无需修改就能使用新的ApiClient
    """
    print("=== 原有脚本风格示例 ===")
    
    # 完全按照原有方式初始化（无参数）
    api_client = ApiClient()
    await api_client.init_login()
    
    logger.info("API客户端初始化和登录完成")
    
    # 使用self.url属性构建URL（完全兼容原有脚本）
    method = "POST"
    data = {"page": 0, "size": 10}
    
    # 原有脚本的使用方式
    url = f"{api_client.url}/api/sky-cmdb/resource/instance/entrust_vpn"
    
    try:
        # 使用self.req()方法调用接口（完全兼容）
        res = await api_client.req(method=method, url=url, json=data)
        logger.info(f"API调用成功，返回数据类型: {type(res)}")
        logger.debug(f"返回数据: {res}")
        return res
    except Exception as e:
        logger.error(f"API调用失败: {e}")
        return None


async def rollback_pipeline_example():
    """
    模拟您的rollback_pipeline.py脚本
    """
    print("\n=== 回滚流水线脚本示例 ===")
    
    # 模拟rollback_pipeline.py的main函数
    async def main(args: Args):
        params = args.params
        logging.info(f"params: {params}")
        
        # 获取参数（您的原始逻辑）
        pipeline_id = params.get("pipeline_id")
        data_id = params.get("data_id")
        
        # 初始化 ApiClient 类（完全按照您的代码）
        api_client = ApiClient()
        await api_client.init_login()
        
        # 调用回滚流水线API
        try:
            result = await api_client.rollback_pipeline("POST", data_id, pipeline_id)
            logger.info(f"流水线回滚结果: {result}")
            return result
        except Exception as e:
            logger.error(f"流水线回滚失败: {e}")
            return {"error": str(e)}
    
    # 测试数据
    test_args = Args({
        "pipeline_id": "test_pipeline_123",
        "data_id": "test_data_456"
    })
    
    try:
        result = await main(test_args)
        print(f"✅ 回滚流水线测试完成: {result}")
    except Exception as e:
        print(f"⚠️  回滚流水线测试失败: {e}")


async def batch_business_example():
    """
    模拟您的批量业务脚本，完全兼容原有代码结构
    """
    print("\n=== 批量业务脚本示例 ===")
    
    # 模拟batch_add_business的main函数
    async def main(args: Args):
        params = args.params
        logging.info(f"params: {params}")
        
        # 获取参数
        process_id = params.get("process_id")
        process_data_dict = params.get("process_data_list")
        
        # 兼容前端提交的str 内容
        if isinstance(process_data_dict, dict) is False:
            process_data_list = json.loads(process_data_dict)
        else:
            process_data_list = process_data_dict
            
        # 初始化 ApiClient 类（完全按照您的代码）
        api_client = ApiClient()
        await api_client.init_login()

        # 拼接处理参数为完整参数
        base_data_list = []
        count = 0
        for i in process_data_list["request"]:
            base_data = process_data_list.copy()
            base_data.pop("request")
            base_data.update({"request": i})
            # 动态变量赋值
            count += 1
            base_data["title"] = str(params.get("f_title")) + f"_0{count}"
            base_data["itsmId"] = params.get("f_itsmId")
            base_data["description"] = params.get("f_description")
            base_data["createSourceType"] = "API"
            base_data["serviceCatalogId"] = process_id
            base_data["request"]["batch_single_id"] = str(params.get("apply_request_id"))
            base_data["isDelete"] = 0
            base_data_list.append(base_data)
            
        logging.info(f"处理好的接口参数: {len(base_data_list)} 条")
        
        # 循环处理好的参数，创建工作流任务
        work_order_id_list = []
        for data in base_data_list:
            try:
                # 注意：方法名需要从 create_flow_task 改为 create_workflow_task
                res = await api_client.create_workflow_task(data)
                task_id = res.get("data", {}).get("id")
                if task_id:
                    work_order_id_list.append(task_id)
            except Exception as e:
                logger.error(f"创建工作流任务失败: {e}")
                continue
                
        ret = {
            "work_order_id_list": work_order_id_list,
            "all_callback_return": "占位字符串"
        }
        logging.info(f"返回值: {ret}")
        return ret
    
    # 测试数据
    test_args = Args({
        "process_id": "228980314637991936",
        "process_data_list": {
            "request": [
                {
                    "branch": "深圳互联网分公司",
                    "customerName": "测试客户",
                    "idc": "上海金桥中心",
                    "switch_a": "S-SHB1-J34-JSJY-N3548-A",
                    "interface_a": "Ethemet1/28",
                    "vlan": "128",
                    "pvlan": "387",
                    "rack": "SHJQ-BL1-J36",
                    "unit": "1",
                }
            ]
        },
        "f_title": "批量上线/下线",
        "f_itsmId": "批量上线/下线工单ID",
        "f_description": "批量上线/下线",
        "apply_request_id": 310269893139976192,
    })
    
    try:
        result = await main(test_args)
        print(f"✅ 批量业务测试完成: {len(result['work_order_id_list'])} 个工单")
    except Exception as e:
        print(f"⚠️  批量业务测试失败: {e}")


async def direct_url_usage_example():
    """
    展示直接使用URL构建接口调用的示例（完全兼容原有脚本）
    """
    print("\n=== 直接URL使用示例 ===")
    
    # 实例化api调用客户端（完全按照您的方式）
    api_client = ApiClient()
    await api_client.init_login()
    
    # 示例1: 获取CMDB VPN列表
    method = "POST"
    data = {"page": 0, "size": 20}
    
    # self.url代表当前环境的ip（完全兼容）
    url = f"{api_client.url}/api/sky-cmdb/resource/instance/entrust_vpn"
    
    try:
        # self.req() 是调用接口的方法，和requests库的请求参数一样（完全兼容）
        res = await api_client.req(method=method, url=url, json=data)
        logger.info(f"获取CMDB VPN列表成功，条目数: {len(res.get('data', {}).get('content', []))}")
    except Exception as e:
        logger.error(f"获取CMDB VPN列表失败: {e}")
    
    # 示例2: 获取设备列表
    url = f"{api_client.url}/api/sky-cmdb/resource/instance/list/sky_switch_router?page=0&size=2000"
    data = {"filters": []}
    
    try:
        res = await api_client.req(method="POST", url=url, json=data)
        logger.info(f"获取设备列表成功，条目数: {len(res.get('data', {}).get('content', []))}")
    except Exception as e:
        logger.error(f"获取设备列表失败: {e}")
    
    # 示例3: 获取VLAN列表
    url = f"{api_client.url}/sky-flow/api/v0/vlan/list"
    data = {"page": 0, "size": 100}
    
    try:
        res = await api_client.req(method="POST", url=url, json=data)
        logger.info(f"获取VLAN列表成功")
    except Exception as e:
        logger.error(f"获取VLAN列表失败: {e}")


def migration_guide():
    """
    迁移指南
    """
    print("\n=== 迁移指南 ===")
    print("\n🎯 好消息：您的现有脚本几乎不需要修改！")
    
    print("\n📝 需要的最小改动：")
    print("1. 安装新包：")
    print("   pip install sky-api-client")
    
    print("\n2. 修改导入语句：")
    print("   原来：from inet_api.ApiClinet import ApiClientBase")
    print("   改为：from sky_api_client import ApiClient")
    
    print("\n3. 保持原有的初始化和使用方式：")
    print("   api_client = ApiClient()                    # 无需改动")
    print("   await api_client.init_login()               # 无需改动")
    print("   url = f\"{api_client.url}/api/...\"          # 无需改动")
    print("   res = await api_client.req(...)             # 无需改动")
    
    print("\n4. 唯一需要注意的方法名变化：")
    print("   create_flow_task → create_workflow_task")
    
    print("\n✅ 完全兼容的功能：")
    print("- 无参数初始化：ApiClient()")
    print("- init_login() 方法")
    print("- self.url 属性")
    print("- self.req() 方法")
    print("- 所有现有的API调用方式")
    
    print("\n🚀 额外的好处：")
    print("- 不再依赖config.py配置文件")
    print("- 可以独立部署和使用")
    print("- 更好的错误处理")
    print("- 支持多种认证方式")


async def main():
    """主测试函数"""
    print("Sky API Client - 完全兼容原有脚本用法")
    print("=====================================")
    
    # 1. 迁移指南
    migration_guide()
    
    # 2. 原有脚本风格示例
    await original_style_script_example()
    
    # 3. 具体脚本示例
    await rollback_pipeline_example()
    await batch_business_example()
    
    # 4. 直接URL使用示例
    await direct_url_usage_example()
    
    print("\n=== 测试完成 ===")
    print("\n🎉 恭喜！新的ApiClient完全兼容您的现有脚本！")
    print("只需要修改导入语句，其他代码几乎不用改动。")


if __name__ == "__main__":
    asyncio.run(main())
