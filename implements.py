import ctypes
import importlib
from ctypes import c_char_p, c_bool, cdll

from interfaces import DMSSdkLibInterface
from utils import process_stdout


class DMSSdkLibImpl(DMSSdkLibInterface):

    def __init__(self, sdk_path="./sdk/sdk.so"):
        _module = importlib.import_module("utils")
        # self._sdk_lib = cdll.LoadLibrary(sdk_path)
        self._sdk_lib = _module.sdk_lib  # type: ignore

    @process_stdout
    def initWithMapData(self, dataPath: c_char_p) -> c_bool:
        self._sdk_lib.initWithMapData.argtypes = [ctypes.c_char_p]
        res = self._sdk_lib.initWithMapData(dataPath)
        return res

    @process_stdout
    def mapMatch(self, fileJson: c_char_p) -> c_char_p:
        self._sdk_lib.mapMatch.argtypes = [ctypes.c_char_p]
        res = self._sdk_lib.mapMatch(fileJson)
        return res

    @process_stdout
    def GetLinkState(self, fileJson: c_char_p) -> c_char_p:
        self._sdk_lib.GetLinkState.argtypes = [ctypes.c_char_p]
        res = self._sdk_lib.GetLinkState(fileJson)
        return res


dms_sdk_lib = DMSSdkLibImpl()


def reload_sdk():
    global dms_sdk_lib
    print(f"old: {id(dms_sdk_lib)}")
    dms_sdk_lib = DMSSdkLibImpl()
    print(f"new: {id(dms_sdk_lib)}")


if __name__ == '__main__':
    import json
    file_json = json.dumps(
        {
            "heading": 30,
            "locAltitude": 0.1000000001,
            "locLatitude": 31.43070000002,
            "locLongitude": 118.3625,
            "vehicleId": 1009,
            "vehicleSpeed": 30,
        }
    )
    dms = DMSSdkLibImpl()
    r = dms.mapMatch(c_char_p(file_json.encode()))
    print(r)
