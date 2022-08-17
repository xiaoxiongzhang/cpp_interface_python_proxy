# -*- encoding:utf-8 -*-
import os

from fastapi import FastAPI

from utils import BASE_PATH


def AppFactory():
    _app = FastAPI(title="C++SDK接口代理服务")

    with open(os.path.join(BASE_PATH, "reloadWatch.py"), "r+") as _f:
        content = _f.readlines()
        if len(content) < 1:
            _f.write(f'"""代码自动生成, 用于触发uvicorn重启服务以及记录服务重启记录."""\r\n')

    return _app


app = AppFactory()

