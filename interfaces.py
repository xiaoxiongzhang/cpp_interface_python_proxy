# -*- encoding:utf-8 -*-
from abc import ABC, abstractmethod
from ctypes import c_char_p, c_bool


class DMSSdkLibInterface(ABC):

    @abstractmethod
    def initWithMapData(self, dataPath: c_char_p) -> c_bool:
        """
        :param dataPath: 输入静态地图数据存储路径
        :return:
        """
        ...

    @abstractmethod
    def mapMatch(self, fileJson: c_char_p) -> c_char_p:
        """ 车辆位置匹配功能接口
        :param fileJson: 车辆数据
        :return:
        """
        ...

    @abstractmethod
    def GetLinkState(self, fileJson: c_char_p) -> c_char_p:
        """ 交通拥堵态势功能接口
        :param fileJson: 车辆数据
        :return:
        """
        ...




