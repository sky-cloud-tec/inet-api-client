#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sky Cloud API 方法定义，重构自原有的ApiBase
"""

from typing import Dict, List, Any


class ApiMethods:
    """Sky Cloud API 方法定义"""

    async def get_node_detail(self, method: str, data: str) -> Dict[str, Any]:
        """
        获取通过数据流程节点管理
        
        Args:
            method: HTTP方法
            data: 节点ID
            
        Returns:
            节点详情数据
        """
        url = f"{self.url}/sky-flow/api/v0/node-detail/{data}"
        res = await self.req(method=method, url=url)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def get_script_info(self, method: str, data: str) -> Dict[str, Any]:
        """
        通过id获取脚本详情接口
        
        Args:
            method: HTTP方法
            data: 脚本ID
            
        Returns:
            脚本详情数据
        """
        url = f"{self.url}/sky-flow/api/v0/script/{data}"
        res = await self.req(method=method, url=url)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def get_sdc_id_list(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取业务域列表数据
        
        Args:
            method: HTTP方法
            data: 查询参数
            
        Returns:
            业务域列表数据
        """
        url = f"{self.url}/api/sky-cmdb/resource/instance/list/sky_biz_domain?page=0&size=2000"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def get_devices_id_list(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取VPN列表数据
        
        Args:
            method: HTTP方法
            data: 查询参数
            
        Returns:
            VPN列表数据
        """
        url = f"{self.url}/api/sky-cmdb/resource/instance/list/sky_vpn?page=0&size=2000"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def get_pipeline_info(self, method: str, data: str) -> Dict[str, Any]:
        """
        获取回滚流水线详情
        
        Args:
            method: HTTP方法
            data: 流水线ID
            
        Returns:
            流水线详情数据
        """
        url = f"{self.url}/api/sky-pipeline/pipeline/statistics/{data}"
        res = await self.req(method=method, url=url)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def rollback_pipeline(self, method: str, data: str, pipeline_id: str) -> Dict[str, Any]:
        """
        回滚流水线
        
        Args:
            method: HTTP方法
            data: 数据ID
            pipeline_id: 流水线ID
            
        Returns:
            回滚结果
        """
        url = f"{self.url}/api/sky-pipeline/device-pipeline/{data}/rollback-all?pipelineId={pipeline_id}"
        res = await self.req(method=method, url=url)
        return res

    async def get_devices_info_for_ip(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        通过设备ip获取交换机设备详情数据接口
        
        Args:
            method: HTTP方法
            data: IP查询参数
            
        Returns:
            设备详情数据
        """
        url = f"{self.url}/api/sky-nap/device/switch-router"
        res = await self.req(method=method, url=url, params=data)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def get_devices_info_for_name(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        通过设备name获取交换机设备详情数据接口
        
        Args:
            method: HTTP方法
            data: 设备名称查询参数
            
        Returns:
            设备详情数据
        """
        url = f"{self.url}/api/sky-cmdb/resource/instance/list/sky_switch_router?page=0&size=2000"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res
    
    async def get_devices_info_for_name_and_type(
        self, 
        method: str, 
        data: Dict[str, Any], 
        device_type: str
    ) -> Dict[str, Any]:
        """
        通过设备name和类型获取设备详情数据接口
        
        Args:
            method: HTTP方法
            data: 查询参数
            device_type: 设备类型
            
        Returns:
            设备详情数据
        """
        url = f"{self.url}/api/sky-cmdb/resource/instance/list/{device_type}?page=0&size=2000"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def get_switch_router_info(self, method: str, device_id: str) -> Dict[str, Any]:
        """
        获取交换机路由器详情
        
        Args:
            method: HTTP方法
            device_id: 设备ID
            
        Returns:
            设备详情数据
        """
        url = f"{self.url}/api/sky-nap/switch-router/{device_id}"
        res = await self.req(method=method, url=url)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{device_id}:{res}")
        return res

    async def get_devices_best_match(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        通过设备ip获取最佳匹配设备
        
        Args:
            method: HTTP方法
            data: 查询参数
            
        Returns:
            匹配设备数据
        """
        url = f"{self.url}/api/sky-nap/network-route/best-match"
        res = await self.req(method=method, url=url, params=data)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def get_interface_info(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        通过接口名称获取接口详情
        
        Args:
            method: HTTP方法
            data: 接口查询参数
            
        Returns:
            接口详情数据
        """
        url = f"{self.url}/api/sky-nap/network-interface/find"
        res = await self.req(method=method, url=url, params=data)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def apply_request_fail_api(self, method: str, data: str) -> Dict[str, Any]:
        """
        工作流失败返回
        
        Args:
            method: HTTP方法
            data: 请求ID
            
        Returns:
            失败处理结果
        """
        url = f"{self.url}/sky-flow/api/v0/apply-request/fail/{data}"
        res = await self.req(method=method, url=url)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    # VPN相关方法
    async def update_vpn(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新单个vpn信息"""
        url = f"{self.url}/sky-flow/api/v0/vpn"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def get_vpn_list(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """获取vpn列表信息"""
        url = f"{self.url}/sky-flow/api/v0/vpn/list"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def add_vpn_batch(self, method: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量新增vpn信息"""
        url = f"{self.url}/sky-flow/api/v0/vpn/batch"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def add_vpn(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """新增vpn信息"""
        url = f"{self.url}/sky-flow/api/v0/vpn"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def delete_vpn_batch(self, method: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量删除vpn"""
        url = f"{self.url}/sky-flow/api/v0/vpn/batch"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    # VLAN相关方法
    async def batch_add_vlan(self, method: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量增加vlan"""
        url = f"{self.url}/sky-flow/api/v0/vlan/batch"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def batch_del_vlan(self, method: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量删除vlan"""
        url = f"{self.url}/sky-flow/api/v0/vlan/batch"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def put_vlan(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """单个更新vlan"""
        url = f"{self.url}/sky-flow/api/v0/vlan"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def list_get_vlan(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """获取vlan列表"""
        url = f"{self.url}/sky-flow/api/v0/vlan/list"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res
    
    async def get_vlan_scan_config_by_device(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """通过设备获取vlan扫描配置关系"""
        url = f"{self.url}/sky-flow/api/v0/vlan-setting/list-discovery-scan-config"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def vlan_correction_status(self, method: str, task_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """vlan状态补全、移除状态变更"""
        url = f"{self.url}/api/sky-nap/v1/detection-task/correction-finish/{task_id}"
        res = await self.req(method=method, url=url, params=data)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def vlan_config_sync(self, method: str) -> Dict[str, Any]:
        """vlan设备配置同步"""
        url = f"{self.url}/sky-flow/api/v0/vlan/sync"
        res = await self.req(method=method, url=url)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{res}")
        return res

    # CMDB相关方法
    async def get_cmdb_vpn(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """获取cmdb vpn列表"""
        url = f"{self.url}/api/sky-cmdb/resource/instance/list/entrust_vpn?page=0&size=20"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def add_cmdb_vpn(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """新增cmdb vpn列表"""
        url = f"{self.url}/api/sky-cmdb/resource/instance/entrust_vpn"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def update_cmdb_vpn(self, method: str, vpn_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新cmdb vpn列表"""
        url = f"{self.url}/api/sky-cmdb/resource/instance/entrust_vpn?id={vpn_id}"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != 200:
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def get_interface_table(self, method: str, device_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """获取设备接口列表数据"""
        url = f"{self.url}/netdb/api/v1/interface/_table?deviceId={device_id}"
        res = await self.req(method=method, url=url, json=data, check_response=False)
        if res.get("code") != 'OK':
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    # 工作流相关方法
    async def create_flow_task(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建工作流任务"""
        url = f"{self.url}/sky-flow/api/v0/apply-request"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res

    async def callback_work_order(self, method: str, url_params: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """触发回调节点"""
        url = f"{self.url}/sky-flow/api/v0/ia-zeebe/pass-trigger-node/{url_params}"
        res = await self.req(method=method, url=url, json=data)
        if res.get("code") != "OK":
            raise Exception(f"API request failed with status code {url}:{data}:{res}")
        return res
