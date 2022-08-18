import datetime
import os
from typing import List

from fastapi import UploadFile, File, Request

from app import app
from schemas import SdkApiConfig
from utils import BASE_PATH


@app.post("/uploadSDK", summary="SDK上传/更新接口", tags=["SDK配置接口"])
async def uploadSDK(request: Request, sdk: UploadFile = File(..., description="SDK包")):
    """
    SDK上传、更新接口
    """
    result = "上传成功, 请稍等5秒后再进行后续接口测试, 服务正在重启更新SDK！"
    contents = await sdk.read()
    if (len(contents) / 1024 / 1024) > 20:
        result = "上传失败，数据文件大于了20M限制，请联系开发者修改配置"
    with open(os.path.join(BASE_PATH, "sdk", "sdk.so"), "wb") as f:
        f.write(contents)

    # update_sdk()  # 更新sdk, 其他需要调用sdk_lib的地方必须动态导入或者 局部创建cdll对象
    """ TODO 
    目前sdk动态替换sdk会报错导致服务挂掉，暂时以重启的方式加载新sdk。
    修改指定py文件，uvicorn监控全局py，自动重启加载新的sdk。
    （默认只会监控py文件，如果需要监控其他类型的文件需要安装watchfiles依赖（仅支持py3.7+，开发环境为py3.6））
    """
    with open(os.path.join(BASE_PATH, "reloadWatch.py"), "r+") as _f:
        content_list = _f.readlines()
        record = f"# {datetime.datetime.now()}: update sdk-[{sdk.filename}] from {request.client.host} \r\n"
        if len(content_list) > 10:
            content_list.pop(1)
        content_list.append(record)
        _f.seek(0)
        _f.writelines(content_list)
    return {"msg": result, "filename": sdk.filename, "content_type": sdk.content_type}


@app.post("/addSdkApi", summary="新增sdk接口", tags=["SDK配置接口"])
async def addSdkApi(api_info: SdkApiConfig):
    """
    根据SDK设置配置文件，新增sdk对应的接口
    """
    from views import LoadViews

    LoadViews().loads(api_info)

    return {"code": 10000, "codeMsg": "successful"}


@app.post("/batchAddSdkApi", summary="批量新增sdk接口", tags=["SDK配置接口"])
async def batchAddSdkApi(api_infos: List[SdkApiConfig]):
    """
    批量新增sdk对应的接口
    """
    from views import LoadViews
    for api_info in api_infos:
        LoadViews().loads(api_info)

    return {"code": 10000, "codeMsg": "successful"}


@app.get("/dataType", summary="Python C++数据类型映射", tags=["SDK配置接口"])
async def batchAddSdkApi():
    """
    C++：Python  数据类型映射
    """
    from views import type_map

    return type_map


