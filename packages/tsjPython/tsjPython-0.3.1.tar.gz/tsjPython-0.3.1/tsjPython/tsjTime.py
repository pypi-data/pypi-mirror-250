

from datetime import datetime, timedelta
import time
from tsjCommonFunc import *

def time_gap(start_time_str, end_time_str):
    # start_time_str = "Fri Aug  4 18:53:48 2023"
    # heartbeat_time_str = "Fri Aug  4 18:55:40 2023"

    # 将日期时间字符串转换为 datetime 对象
    start_time = datetime.strptime(start_time_str, "%a %b %d %H:%M:%S %Y")
    heartbeat_time = datetime.strptime(end_time_str, "%a %b %d %H:%M:%S %Y")

    # 计算时间差
    time_difference = heartbeat_time - start_time

    # 输出时间差
    # print("Time passed：", time_difference)
    return time_difference

def isNearTime(input_time:datetime, limit_seconds:int=30):

    # Calculate the current time
    current_time = datetime.now()

    # Calculate the time difference
    time_difference = current_time - input_time

    # Compare the time difference to 30 seconds
    if time_difference < timedelta(seconds=limit_seconds):
        ic(f"The gap is less than {limit_seconds} seconds.")
        return True
    else:
        ic(f"The gap is {limit_seconds} seconds or more.")
        return False

def nowStr():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def todayStr():
    return datetime.today().strftime('%Y-%m-%d')

def time2String(timeNum):
    if timeNum < 60:
        return "{:.2f}".format(timeNum)
    elif timeNum < 3600:
        timeNum=int(timeNum)
        minutes=timeNum//60
        secends=timeNum%60
        return "{:0>2d}:{:0>2d}".format(minutes,secends)
    else:
        timeNum=int(timeNum)
        hour=timeNum//3600
        minutes=(timeNum-hour*3600)//60
        secends=timeNum%60
        return "{:0>2d}:{:0>2d}:{:0>2d}".format(hour,minutes,secends)
    
def timeBeginPrint(Msg):
    processBeginTime=time.time()
    colorPrint("\n\rSTART {} at: {}".format(Msg,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),"magenta")
    return processBeginTime

def timeEndPrint(Msg, beginTime):
    colorPrint("wait {} to FINISH {} at: {}".format(time2String(int(time.time()-beginTime)),Msg,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),"magenta")