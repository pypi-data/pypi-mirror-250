

import multiprocessing as mp
from multiprocessing import Pipe,Queue
import multiprocessing
import traceback
from tsjCommonFunc import *
import sys

class Process(mp.Process):
    def __init__(self, *args, **kwargs):
        mp.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = mp.Pipe()
        self._exception = None

    def run(self):
        try:
            mp.Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))
            # raise e  # You can still rise this exception if you need to

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception
    
def SubFunc(signal, task_name, entry, rank, total_size):
    sys.stdout.flush()
    yellowPrint("[   {:2}/{:2}   ] SubTask {:<10} is running……".format( rank, total_size, task_name))
    entry.subTask()
    passPrint("[   {:2}/{:2}   ] SubTask {:<10} finished successfully".format( rank, total_size, task_name))
    signal.put(task_name)

def parallelTask(taskList, limit_core=32, **kwargs):
    pass_count =  Queue()
    pList=[]
    totolCount = len(taskList)
    countId = 0
    for name, entry in taskList.items():
        countId = countId + 1
        pList.append(Process(target=SubFunc, args=(pass_count, name, entry, countId, totolCount)))  
        
    task_nums = len(taskList)
    
    dispatch_number = 0
    for p in pList:
        p.start()
        dispatch_number += 1
        while (dispatch_number - pass_count.qsize())>limit_core:
            print(f"dispatching : {pass_count.qsize()} / {dispatch_number} / {task_nums}")
            sys.stdout.flush()
            time.sleep(5)
    while pass_count.qsize()<task_nums:
        print(f"QueueNum : {pass_count.qsize()} / {task_nums}")
        sys.stdout.flush()
        time.sleep(5)
    yellowPrint("Reducing parallel processes result...")

# def worker(cfg_file):
#     cfg_dir = os.path.dirname(cfg_file)
#     Popen(["rm", "-f", "heartbeat", "out.cfg", "zsim"], cwd=cfg_dir).wait() 
#     Popen([zsim_exec, cfg_file], cwd=cfg_dir).wait() 
    
def parallel_workfun2list(worker, func_list_cfg_files):
    with multiprocessing.Pool(processes=8) as pool:  
        pool.map(worker, func_list_cfg_files)