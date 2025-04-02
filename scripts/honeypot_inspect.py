import subprocess
import pexpect
import signal
import time

from core_package import get_node_internal_ip


def exec_honeypot_process(test_node_name):
    get_pods_command = ["kubectl", "get", "pod", "-n", "xinfan"]
    process = subprocess.Popen(get_pods_command, stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(">>Error occurred:", error)
        return

    pod_name = None
    for line in output.decode().split('\n'):
        if "centosssh-target" in line:
            pod_name = line.split()[0]
            break

    if not pod_name:
        print(">>No pod found with 'centosssh-target' in its name")
        return

    # 使用获取到的pod名称执行kubectl exec命令获取交互式shell
    exec_command = "kubectl exec -it {} -n xinfan /bin/bash".format(pod_name)

    # 使用pexpect.spawn执行命令
    child = pexpect.spawn(exec_command)
    # 在交互式shell中执行命令
    command_to_attack_honeypot = f"ssh root@{get_node_internal_ip(test_node_name)} -p 1022"
    child.sendline(command_to_attack_honeypot)
    print("\033[92m>>执行ssh连接成功，5s后自动结束进程\033[0m")
    time.sleep(5)
    child.kill(signal.SIGINT)
    return



