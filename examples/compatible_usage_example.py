
import asyncio
import json
import logging
from inet_api_client import ApiClient



class Args:
    """模拟原脚本的Args类"""

    def __init__(self, params):
        self.params = params


# 设置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



# 批量新增业务初始化脚本
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
    # 初始化 ApiClient 类
    api_client = ApiClient()
    await api_client.init_login()

    # 拼接处理参数为完整参数
    base_data_list = []
    count = 0
    for i in process_data_list["request"]:
        base_data = process_data_list.copy()
        base_data.pop("request")
        base_data.update({"request":i})
        # 动态变量赋值
        count += 1
        base_data["title"] = str(params.get("f_title"))+f"_0{count}"
        base_data["itsmId"] = params.get("f_itsmId")
        base_data["description"] = params.get("f_description")
        base_data["createSourceType"] = "API"
        base_data["serviceCatalogId"] = process_id
        base_data["request"]["batch_single_id"] = str(params.get("apply_request_id"))
        base_data["isDelete"] = 0
        base_data_list.append(base_data)
        
    logging.info(f"处理好的接口参数: {base_data_list}")
    # 循环处理好的参数，创建工作流任务,并且获取返回的task_id
    work_order_id_list = []
    for data in base_data_list:
        res = await api_client.create_flow_task(method="post", data=data)
        work_order_id_list.append(res.get("data").get("id"))
        
    ret = {
        "work_order_id_list": work_order_id_list,
        "all_callback_return": "占位字符串"
    }
    logging.info(f"返回值: {ret}")
    return ret


if __name__ == "__main__":
    input_args8 = {
        "process_id": "228980314637991936",
        "process_data_list": {
            "request": [
                {
                    "branch": "xxx",
                    "customerName": "xxx",
                    "idc": "xxx",
                    "switch_a": "xxx",
                    "interface_a": "xxx",
                    "switch_b": "xxx",
                    "interface_b": "xxx",
                    "tor_switch": "xxx",
                    "interface_tor": "xxx",
                    "vlan": "xxx",
                    "pvlan": "xxx",
                    "tor_vlan": "xxx",
                    "rack": "xxx",
                    "unit": "xxx",
                },
                {
                    "branch": "xxx",
                    "customerName": "xxx",
                    "idc": "xxx",
                    "switch_a": "xxx",
                    "interface_a": "xxx",
                    "switch_b": "xxx",
                    "interface_b": "xxx",
                    "tor_switch": "xxx",
                    "interface_tor": "xxx",
                    "vlan": "xxx",
                    "pvlan": "xxx",
                    "tor_vlan": "xxx",
                    "rack": "xxx",
                    "unit": "xxx",
                },
            ]
        },
        "f_title": "批量上线/下线",
        "f_itsmId": "批量上线/下线工单ID",
        "f_description": "批量上线/下线",
        "apply_request_id": 310269893139976192,
    }
    asyncio.run(main(Args(params=input_args8)))