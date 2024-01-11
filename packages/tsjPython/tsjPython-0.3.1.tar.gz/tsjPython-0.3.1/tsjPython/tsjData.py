from collections import defaultdict
from multiprocessing import Queue
import sys
import gVal as glv
# from terminal_command import checkFile

class dataDictClass():
    def __init__(self):
        """在主模块初始化"""
        self.dataDict = {}

    def set(self, name, value):
        """设置"""
        try:
            self.dataDict[name] = value
            return True
        except KeyError:
            return False

    def get(self, name):
        """取值"""
        try:
            return self.dataDict[name]
        except KeyError:
            return "Not Found"