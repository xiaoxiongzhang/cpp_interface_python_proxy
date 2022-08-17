import json
import os
import select
from ctypes import cdll
from io import StringIO


BASE_PATH = os.path.dirname(__file__)
sdk_lib = cdll.LoadLibrary("./sdk/sdk.so")


def more_data(pipe_out):
    r, _, _ = select.select([pipe_out], [], [], 0)
    return bool(r)


# read the whole pipe
def read_pipe(pipe_out):
    """ 读取管道中的数据"""
    out = b''
    while more_data(pipe_out):
        out += os.read(pipe_out, 1024)

    _content = out.decode()

    content = {"comment": "", "data": ""}
    _data_flag = False
    with StringIO(_content) as str_io:
        # print(str_io.getvalue())
        for i in str_io:
            i = i.replace(r"\n", "").replace(r"\r", "").replace(r"\t", "").strip()
            if not _data_flag and i in {"[", "{"}:
                _data_flag = True
            if _data_flag:
                content["data"] += i
            else:
                content["comment"] += i
    if content["data"]:
        content["data"] = json.loads(content["data"])

    return content


def process_stdout(func):
    """ 将外部程序（c++动态库）的打印输出捕获到python变量接收"""

    def wrapper(*args, **kwargs):
        # sys.stdout.write(' \b')
        pipe_out, pipe_in = os.pipe()
        stdout = os.dup(1)
        os.dup2(pipe_in, 1)

        # -----------------------------------------------------------
        # code here
        # process handle
        func(*args, **kwargs)
        # -----------------------------------------------------------

        os.dup2(stdout, 1)

        return read_pipe(pipe_out)

    return wrapper


def update_sdk(sdk_path="./sdk/sdk.so"):
    global sdk_lib
    sdk_lib = cdll.LoadLibrary(sdk_path)


if __name__ == '__main__':
    import time
    print(os.path.dirname(__file__))
    print(os.path.basename(__file__))
    print(os.path.getmtime(os.path.dirname(__file__)))
    a = time.localtime(os.path.getmtime(os.path.dirname(__file__)))
    print(time.strftime("%Y-%m-%d %H:%M:%S", a))

