import uvicorn
import importlib


def app_init():
    importlib.import_module("views")
    from app import app
    return app


app = app_init()
for i in app.routes:
    print(i.path)


@app.get("/", include_in_schema=False)
def root():
    """测试接口"""

    return "C++ SDK函数接口调用代理服务"


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True, reload_delay=5.0)
