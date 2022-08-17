import json
from typing import Optional, List

from pydantic import BaseModel, Field


class Param(BaseModel):
    param_name: str = Field(description="参数名称")
    param_type: str = Field(description="参数类型")
    # optional: bool = Field(description="是否必传")


class SdkApiConfig(BaseModel):
    func_name: str = Field(description="SDK接口函数名称")
    overwrite: Optional[bool] = Field(description="如果已经存在指定路由了， 是否覆盖", default=False)
    summary: Optional[str] = Field(description="API接口描述", default="")
    params: List[Param] = Field(description="接口参数")


if __name__ == '__main__':
    v = Vehicle(
        heading=30,
        locAltitude=0.1,
        locLatitude=31.4307,
        locLongitude=118.3625,
        vehicleId=1009,
        vehicleSpeed=30
    )
    print(v.dict())
    print(1111111111)

    vehicle_json = [{
                "heading": 30,
                "locAltitude": 0.1,
                "locLatitude": 31.4307,
                "locLongitude": 118.3625,
                "vehicleId": 1009,
                "vehicleSpeed": 30,
            }]
    vehicle_json = json.dumps(vehicle_json)
    print(vehicle_json)
