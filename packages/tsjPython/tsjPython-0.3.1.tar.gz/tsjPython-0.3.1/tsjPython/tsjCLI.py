import os
import re
import shutil
from tqdm import tqdm

#  teminal command or command line interface

def checkFileExists(filename):
    if os.path.exists(filename):
        return True
    else:
        return False
    
# def checkFile(taskfilePath):
#     tmpOSACAfilePath=taskfilePath+"/tmpOSACAfiles"
#     mkdir(tmpOSACAfilePath)
#     return tmpOSACAfilePath

def ls(directory):
    # 使用 os.listdir() 函数获取目录中的所有文件和文件夹
    return os.listdir(directory)

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		ic("---  New folder...  ---")
	else:
		ic("---  Folder existed!  ---")
  
def mkfile(filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    # with open(filename, 'w') as f:
    #     f.write('Hello World!')
  
def chmod(filename):
    import subprocess
    # Replace 'filename' with the actual filename/path
    # Execute the chmod command
    subprocess.call(['chmod', '755', filename])

def mvfile(old, new):
    import shutil
    shutil.move(old, new)
    
def move_file_with_progress(src_file, dst_file):
    # 获取文件大小
    file_size = os.path.getsize(src_file)

    # 使用 tqdm 创建进度条
    with tqdm(total=file_size, unit='B', unit_scale=True, desc=f'Moving {src_file}') as pbar:
        # 定义回调函数来更新进度条
        def update_progress(num_bytes):
            pbar.update(num_bytes)

        # 使用 shutil.copyfileobj 实现文件复制，并设置回调函数
        with open(src_file, 'rb') as fsrc, open(dst_file, 'wb') as fdst:
            shutil.copyfileobj(fsrc, fdst, 1024*1024, callback=update_progress)

    # 删除原文件
    os.remove(src_file)

def cpfile(old, new):
    shutil.copyfile(old, new)
    
def rmfile(file_name):
    if checkFileExists(file_name):
        os.remove(file_name)

def isProcessOccupyCPU(pattern):
    if processCPUUsage(pattern) > 0:
        return True
    else:
        return False
    
def processCPUUsage(pattern):
    # first use pgrep get the pid, and pidstat get real cpu usage
    command = "pgrep -f \""\
                f"{pattern}"\
                "\" "
    ic(command)
    list = CMD_PATH([command],"/")
    pid_list = [str(x)[2:-3] for x in list[0]] # first for
    ic(pid_list)
    run_percentage = 0.0
    for pid in pid_list:
        command = f"pidstat -p {pid}|tail -1|awk "\
                    "'{print $8}'"
        ic(command)
        list = CMD_PATH([command],"/")
        ic(list)
        cpu_list = [str(x)[2:-3] for x in list[0]][0]
        ic(cpu_list)
        if cpu_list != "%CPU":
            run_percentage += float(cpu_list)
    return run_percentage


def processCPUUsage_pasttime(pattern):
    # check using cpu usage rates
    
    # Discarded Code: ps aux cpu usage will be Not Zero when process is sleeping because os its snapshots machanism
    command = f"ps aux|grep '{pattern}'| "\
            "awk '{print $3}'"
    # print(command)
    ic(pattern)
    list = CMD_PATH(command,"/")
    cpu_list = [str(x)[2:-3] for x in list[0]]
    ic(cpu_list)
    run_percentage = 0.0
    for cpu_rate in cpu_list:
        run_regex = re.match("([0-9\.]*)", cpu_rate)
        if run_regex:
            ic(run_regex.group(1))
            first_percentage = float(run_regex.group(1))
            if first_percentage > 0:
                run_percentage += first_percentage
    return run_percentage

def isProcessStateRunning(pattern):
    # check using state flag
    command = f"ps aux|grep '{pattern}'| awk '"\
            "{ if ($8  ~ /^R|R\+|Rl+/) { running++ } else if ($8 == \"S+\") { sleeping++ } } END "\
            "{if (running == 0) print \"Running: 0\"; else print \"Running:\", running; "\
            "if (sleeping == 0) print \"Sleeping: 0\"; else print \"Sleeping:\", sleeping; }'"
    # print(command)
    list = CMD_PATH(command,"/")
    ic(str(list[0][0])[2:-3])
    run_sleep_regex = re.match("Running: ([0-9]*)", str(list[0][0])[2:-3])
    if run_sleep_regex:
        ic(run_sleep_regex.group(1))
        run_num = int(run_sleep_regex.group(1))
        if run_num >= 1:
            return True     
    return False
    
# CMD_PATH(["make injf"],self.path)
def CMD_PATH(command, path, env={}):
    import subprocess
    my_env = os.environ.copy()
    for key, value in env.items():
        my_env[key] = value
    # command is list not string
    p = subprocess.Popen(command, 
                     env=my_env,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     cwd = path,
                     shell=True)
    errors = p.stderr.readlines()
    ic(errors)
    return [p.stdout.readlines(),errors]
       
def TIMEOUT_COMMAND(core, command, timeout=30):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None"""
    import subprocess, datetime, os, time, signal
    cmd = command.split(" ")
    start = datetime.datetime.now()
    my_env = os.environ.copy()
    my_env["OMP_NUM_THREADS"] = str(core)
    process = subprocess.Popen(cmd , env=my_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8",preexec_fn=os.setsid) #让 Popen 成立自己的进程组
    # https://www.cnblogs.com/gracefulb/p/6893166.html
    # 因此利用这个特性，就可以通过 preexec_fn 参数让 Popen 成立自己的进程组， 然后再向进程组发送 SIGTERM 或 SIGKILL，中止 subprocess.Popen 所启动进程的子子孙孙。
    # 当然，前提是这些子子孙孙中没有进程再调用 setsid 分裂自立门户。
    ic("SubProcess-before",process.pid,process.poll())
    time.sleep(0.2)
    while process.poll() is None: # poll()(好像BHive208/有时候变成176.是正常结束)返回0 正常结束， 1 sleep， 2 子进程不存在，-15 kill，None 在运行
        now = datetime.datetime.now()
        ic("SubProcess-During",process.pid,process.poll(),now)
        if (now - start).seconds> timeout:
            # BHive有子进程，需要杀死进程组。但是需要新生成进程组，不然会把自己kill掉
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            # os.killpg(process.pid, signal.SIGTERM) SIGTERM不一定会kill，可能会被忽略，要看代码实现
            # https://blog.csdn.net/zhupenghui176/article/details/109097737
            # os.waitpid(-1, os.WNOHANG)
            (killPid,killSig) = os.waitpid(process.pid, 0)
            if killPid != process.pid or killSig!=9:
                errorPrint("TIMEOUT_COMMAND kill failed! killPid %d process.pid %d killSig %d" % (killPid, process.pid, killSig))
            ic("Killed",process.pid,process.poll())
            return None
        time.sleep(2)
    ic("SubProcess-Finished",process.pid,process.poll())
    ic(process.stderr.readlines())
    return process.stdout.readlines()


def TIMEOUT_COMMAND_2FILE(core, command, filename, timeout=30):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None"""
    import subprocess, datetime, os, time, signal
    cmd = command.split(" ")
    start = datetime.datetime.now()
    my_env = os.environ.copy()
    my_env["OMP_NUM_THREADS"] = str(core)
    file_output = open(filename,"w")
    process = subprocess.Popen(cmd , env=my_env, stdout=file_output, stderr=file_output,encoding="utf-8",preexec_fn=os.setsid) #让 Popen 成立自己的进程组
    # https://www.cnblogs.com/gracefulb/p/6893166.html
    # 因此利用这个特性，就可以通过 preexec_fn 参数让 Popen 成立自己的进程组， 然后再向进程组发送 SIGTERM 或 SIGKILL，中止 subprocess.Popen 所启动进程的子子孙孙。
    # 当然，前提是这些子子孙孙中没有进程再调用 setsid 分裂自立门户。
    ic("SubProcess-before",process.pid,process.poll())
    time.sleep(0.2)
    while process.poll() is None: # poll()(好像BHive208/有时候变成176.是正常结束)返回0 正常结束， 1 sleep， 2 子进程不存在，-15 kill，None 在运行
        now = datetime.datetime.now()
        ic("SubProcess-During",process.pid,process.poll(),now)
        if (now - start).seconds> timeout:
            # BHive有子进程，需要杀死进程组。但是需要新生成进程组，不然会把自己kill掉
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            # os.killpg(process.pid, signal.SIGTERM) SIGTERM不一定会kill，可能会被忽略，要看代码实现
            # https://blog.csdn.net/zhupenghui176/article/details/109097737
            # os.waitpid(-1, os.WNOHANG)
            (killPid,killSig) = os.waitpid(process.pid, 0)
            if killPid != process.pid or killSig!=9:
                errorPrint("TIMEOUT_COMMAND kill failed! killPid %d process.pid %d killSig %d" % (killPid, process.pid, killSig))
            ic("Killed",process.pid,process.poll())
            return None
        time.sleep(2)
    ic("SubProcess-Finished",process.pid,process.poll())
    ic(process.stderr.readlines())
    return ["Finished/Killed"]

def TIMEOUT_severalCOMMAND(command, timeout=10):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None"""
    import subprocess, datetime, os, time, signal
    start = datetime.datetime.now()
    process = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
    ic("LLVM-before",process.pid,process.poll())
    time.sleep(0.2)
    while process.poll() is None: # poll()返回0 正常结束， 1 sleep， 2 子进程不存在，-15 kill，None 在运行
        ic("LLVM-During",process.pid,process.poll())
        now = datetime.datetime.now()
        if (now - start).seconds> timeout:
            os.kill(process.pid, signal.SIGKILL)
            # https://blog.csdn.net/zhupenghui176/article/details/109097737
            # os.waitpid(-1, os.WNOHANG)
            (killPid,killSig) = os.waitpid(process.pid, 0)
            if killPid != process.pid or killSig!=9:
                errorPrint("TIMEOUT_COMMAND kill failed! killPid %d process.pid %d killSig %d" % (killPid, process.pid, killSig))
            ic("LLVM-Killed",process.pid,process.poll())
            return None
        time.sleep(10)
    ic("LLVM-Finished",process.pid,process.poll())
    # ic(process.stderr.readlines())
    return [process.stdout.readlines() , process.stderr.readlines()]

