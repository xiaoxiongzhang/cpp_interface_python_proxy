import importlib
import json
import ctypes
from typing import Any

from fastapi import Body
from starlette.routing import Route

from schemas import SdkApiConfig, Param
from utils import process_stdout, sdk_lib

from . import base_views

type_map = {
    "_Bool": "c_bool",
    "char": "c_char",
    "wchar_t": "c_wchar",
    "short": "c_short",
    "unsigned short": "c_ushort",
    "int": "c_int",
    "unsigned int": "c_uint",
    "long": "c_long",
    "unsigned long": "c_ulong",
    "size_t": "c_size_t",
    "ssize_t": "c_ssize_t",
    "float": "c_float",
    "double": "c_double",
    "long double": "c_longdouble",
    "char*": "c_char_p",
    "wchar_t*": "c_wchar_p",
    "void*": "c_void_p",
}


class LoadViews:
    path_set = set()

    def loads(self, api_info: SdkApiConfig):
        from app import app

        func_name = api_info.func_name
        param_config = {}
        for p in api_info.params:
            p: Param
            param_config[p.param_name] = p.param_type

        if not api_info.overwrite:
            if f"/{func_name}" not in self.path_set:
                app.add_api_route(
                    f"/{func_name}",
                    endpoint=gen_func(func_name, param_config),
                    summary=api_info.summary,
                    methods=["POST"],
                    tags=["SDK测试接口"]
                )
        else:
            for r in app.routes:
                r: Route
                if r.path == f"/{func_name}":
                    print(f"remove /{func_name}")
                    app.routes.remove(r)

            app.add_api_route(
                f"/{func_name}",
                endpoint=gen_func(func_name, param_config),
                summary=api_info.summary,
                methods=["POST"],
                tags=["SDK测试接口"]
            )
        self.path_set.add(f"/{func_name}")
        app.openapi_schema = None


def gen_func(func_name, param_config: dict):
    """动态生成函数方法"""
    print(f"param-config: {param_config}")
    example = [
        {k: f"{v}"} for k, v in param_config.items()
    ]

    # _module = importlib.import_module("utils")
    # sdk_lib = _module.sdk_lib  # type: ignore

    def func(params: Any = Body(example=example)):  # params: [{"p1": ""}, {"p2": ""}]
        print(f"params = {params}")

        param_list = []
        for p in params:
            k = list(p.keys())[0]
            _t = type_map.get(param_config[k], "c_char_p")
            type_conv = getattr(ctypes, _t)
            p_value = p[k]
            # if not isinstance(p_value, (int, str, float, bool)):
            if not isinstance(p_value, str):
                p_value = json.dumps(p_value)
            param_c = type_conv(p_value.encode())
            param_list.append(param_c)
        f = getattr(sdk_lib, func_name)
        resp = process_stdout(f)(*param_list)
        return resp

    return func


if __name__ == '__main__':
    print(locals())
