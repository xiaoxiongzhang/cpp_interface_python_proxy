import ast
import json
from _ast import Module, FunctionDef, arguments, Name, Attribute, Assign, Call, Store, Load, Return, arg, ImportFrom, \
    alias
from ctypes import c_char_p, cdll
from pprint import pprint
import importlib
from typing import List

from schemas import Vehicle


# param: {"p1": {"type": ""}, "p2": {"type": ""}}
x = """
def func(param):
    from utils import process_stdout
    
    params = []
    for p in param:
        _t = type_map.get(param[p]["type"], "c_char_p")
        type_conv = getattr(ctypes, _t)
        p_json = json.dumps(param)
        param_c = type_conv(param_json.encode())
    lib = A()
    resp = process_stdout(lib.b(vehicle_json_char_p))
    return resp
"""

#
# def gen_func(func_name, param_config: dict):  # param_config: {"p1": {"type": ""}, "p2": {"type": ""}}
#     def func(param: List[dict]):  # param: ["p1": "", "p2": ""]
#         from utils import process_stdout
#
#         params = []
#         for p in param:
#             _t = type_map.get(param_config[p]["type"], "c_char_p")
#             type_conv = getattr(ctypes, _t)
#             p_json = json.dumps(param[p])
#             param_c = type_conv(p_json.encode())
#             params.append(param_c)
#         lib = A()  # TODO
#         f = getattr(lib, func_name)
#         resp = process_stdout(f(*params))
#         return resp
#     return func


class A:
    a = 1

    def b(self, x):
        print(1111)
        return x


'''
@app.post("/dataType", summary="Python C++数据类型映射", tags=["SDK配置接口"])
async def batchAddSdkApi(api_infos: List[SdkApiConfig]):
    """
    C++：Python  数据类型映射
    """

    return type_map
'''

if __name__ == '__main__':
    r_node = ast.parse(x)
    print(ast.dump(r_node))
    import ctypes
    t = "c_char_p"
    a = getattr(ctypes, t)
    print(a)
    __ = Module(
        body=[
            FunctionDef(
                name='func',
                args=arguments(
                    args=[arg(arg='vehicle', annotation=Name(id='dict', ctx=Load()))],
                    vararg=None,
                    kwonlyargs=[],
                    kw_defaults=[],
                    kwarg=None,
                    defaults=[]
                ),
                body=[
                    ImportFrom(
                        module='utils', names=[alias(name='process_stdout', asname=None)], level=0
                    ),
                    Assign(
                        targets=[Name(id='vehicle_json', ctx=Store())],
                        value=Call(
                            func=Attribute(
                                value=Name(id='json', ctx=Load()),
                                attr='dumps',
                                ctx=Load()
                            ),
                            args=[Name(id='vehicle', ctx=Load())],
                            keywords=[]
                        )
                    ),
                    Assign(
                        targets=[Name(id='vehicle_json_char_p', ctx=Store())],
                        value=Call(
                            func=Name(id='c_char_p', ctx=Load()),
                            args=[
                                Call(
                                    func=Attribute(
                                        value=Name(id='vehicle_json', ctx=Load()),
                                        attr='encode',
                                        ctx=Load()
                                    ),
                                    args=[],
                                    keywords=[]
                                )
                            ], keywords=[]
                        )
                    ),
                    Assign(
                        targets=[Name(id='lib', ctx=Store())],
                        value=Call(
                            func=Name(id='A', ctx=Load()),
                            args=[],
                            keywords=[]
                        )
                    ),
                    Assign(
                        targets=[Name(id='resp', ctx=Store())],
                        value=Call(
                            func=Name(id='process_stdout', ctx=Load()),
                            args=[
                                Call(
                                    func=Attribute(
                                        value=Name(id='lib', ctx=Load()),
                                        attr='b',
                                        ctx=Load()
                                    ),
                                    args=[Name(id='vehicle_json_char_p', ctx=Load())],
                                    keywords=[]
                                )
                            ],
                            keywords=[]
                        )
                    ),
                    Return(value=Name(id='resp', ctx=Load()))
                ],
                decorator_list=[],
                returns=None
            )
        ]
    )



