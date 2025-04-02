import subprocess
import time
import pexpect
from core_package import get_node_internal_ip


# 这个方法用来启动异常进程
def exec_abnormal_process(exec_node_name):
    get_pods_command = ["kubectl", "get", "pod", "-n", "xinfan"]
    process = subprocess.Popen(get_pods_command, stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(">>Error occurred:", error)
        return

    pod_name = None
    for line in output.decode().split('\n'):
        if "dvwa-target" in line:
            pod_name = line.split()[0]
            break

    if not pod_name:
        print(">>No pod found with 'dvwa-target' in its name")
        return
    exec_command = "kubectl exec -it {} -n xinfan /bin/bash".format(pod_name)
    child = pexpect.spawn(exec_command)
    abnormal_command = f"ssh root@{get_node_internal_ip(exec_node_name)}"
    child.sendline(abnormal_command)
    print(f"\033[92m>>执行命令{abnormal_command}\033[0m")
    print("\033[92m>>异常命令执行成功2s后自动杀进程\033[0m")
    time.sleep(2)
    child.terminate()
    return
