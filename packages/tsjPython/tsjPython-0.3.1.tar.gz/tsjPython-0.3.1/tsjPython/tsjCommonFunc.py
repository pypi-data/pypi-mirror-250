from termcolor import colored
import os
import time
import random
import plotille
import pprint
import inspect
import re



def valuePrint(x):
    frame = inspect.currentframe().f_back
    s = inspect.getframeinfo(frame).code_context[0]
    r = re.search(r"\((.*)\)", s).group(1)
    yellowPrint("{} = {}".format(r, x))


def errorPrint(message):
    # os.system('color')
    print(colored(message, 'red'))
    return message

# grey.
# red.
# green.
# yellow.
# blue.
# magenta.
# cyan.
# white.
def colorPrint(message, color):
    # os.system('color')
    print(colored(message, color))
    return message


def pPrint(message):
    print("\n")
    pprint.pprint(message)
    print("\n")


def yellowPrint(message):
    # os.system('color')
    print(colored(message, "yellow"))
    return message


def passPrint(message):
    # os.system('color')
    print(colored(message, 'green'))
    return message


def completePrint(message):
    # os.system('color')
    print("--------------------------------{}--------------------------------".format(colored(message, 'green')))
    return message


def splitLine(string, color="white"):
    print("\n")
    colorPrint(
        "--------------------------------{}--------------------------------".format(string), color)
    print("\n")
    return string


def histogramsPrint(data, type="vertical"):
    if type == "vertical":
        print(plotille.histogram(data))
    else:
        print(plotille.hist(data))

            #
# --------------------------------------------time--------------------------------------------------------

def printTimeList(self,current_milli_time,checkPointList=[],updateCheckPointList=[]):
    for i in checkPointList:
        if i in self.checkPointTime:
            tmpCheckTime=self.checkPointTime[i]
            passPrint("check    {:3d}:            {:6d}ms, {:6.2f}s".format(i ,current_milli_time-tmpCheckTime,float(current_milli_time-tmpCheckTime)/1000))
        else:
            errorPrint("No check {:3d}~ New one check point".format(i))
            self.checkPointTime[i]=current_milli_time
    for i in updateCheckPointList:
        if i in self.checkPointTime:
            tmpCheckTime=self.checkPointTime[i]
            colorPrint("update   {:3d}:            {:6d}ms, {:6.2f}s".format(i ,current_milli_time-tmpCheckTime,float(current_milli_time-tmpCheckTime)/1000),"magenta")
        else:
            errorPrint("NoUpdate {:3d}~ New one check point".format(i))
        self.checkPointTime[i]=current_milli_time

class globalTimeClass:
    count=0
    beginTime =-1
    lastTime =-1
    def __init__(self,time=0):
        self.checkPointTime=dict()
        self.beginTime = time
        self.lastTime = time
    def updateTime(self,message,checkPointList=[],updateCheckPointList=[]):
        if self.beginTime==-1 and self.lastTime==-1:
            splitLine("start time check")
            current_milli_time = round(time.time() * 1000)
            printTimeList(self,current_milli_time,checkPointList,updateCheckPointList)
            self.beginTime =current_milli_time
            self.lastTime =current_milli_time
            self.count =0
        else:
            print(message)
            current_milli_time = round(time.time() * 1000)
            yellowPrint("passTime {:3d} from Last:  {:6d}ms, {:6.2f}s".format(self.count,current_milli_time-self.lastTime,float(current_milli_time-self.lastTime)/1000))
            yellowPrint("passTime {:3d} from start: {:6d}ms, {:6.2f}s".format(self.count,current_milli_time-self.beginTime,float(current_milli_time-self.beginTime)/1000))
            printTimeList(self,current_milli_time,checkPointList,updateCheckPointList)
            self.lastTime =current_milli_time
            self.count+=1

globalTime = globalTimeClass(-1)


def passTime(message="passTime:",CP=[],UP=[]):
    globalTime.updateTime(message,CP,UP)

def sleepRandom(seconds):
    time.sleep(round(random.uniform(0.15, seconds+0.15), 2))


def testTime(whileTimes, function):
    histogramsData = []
    begin = time.time()
    while whileTimes:
        beforeFunction = time.time()
        function()
        afterFunction = time.time()
        deltatime = afterFunction - beforeFunction
        colorPrint("delta time ONECE {}".format(
            deltatime), "yellow")
        histogramsData.append(deltatime)
        whileTimes -= 1
    end = time.time()
    colorPrint("ALL {}".format(end-begin), "red")
    histogramsPrint(histogramsData, "horizontal")


# --------------------------------------------valueCMP--------------------------------------------------------

def Random(num):
    return round(random.uniform(0, num), 2)


def textBelong(small, big):
    for i in small:
        if i in big:
            return 1
    return 0


def isArround(listA, listB, delta):
    if len(listA) != len(listB):
        errorPrint("isArround inputLength not equal!!!")
        return 0
    for i in range(0, len(listA)):
        a = listA[i]
        b = listB[i]
        if a < b-delta or a > b+delta:
            errorPrint("not Arround")
            return 0
    passPrint("isArround")
    return 1


