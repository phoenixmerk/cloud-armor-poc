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
    print("\033[92m>>执行复制二进制病毒到/usr/bin路径成功, 等待5s校验文件投递情况\033[0m")
    time.sleep(5)  
    # 检查文件是否存在, 给一次重试机会
    files_to_check = ["/usr/bin/CoinMiner", "/usr/bin/mssecsvc.exe"]
    retry_count = 0
    max_retries = 1  
    file_exists = False

    while retry_count <= max_retries:
        file_exists = True
        for file_path in files_to_check:
            check_file_command = f"ls {file_path}"
            child.sendline(check_file_command)
            try:
                child.expect(r'[$#] ')  
                print(f"\033[92m>>文件 {file_path} 存在\033[0m")
            except pexpect.TIMEOUT:
                print(f"\033[91m>>文件 {file_path} 不存在，校验失败\033[0m")
                file_exists = False
                break

        if file_exists:
            break  # 所有文件都存在，跳出循环

        if retry_count < max_retries:
            print("\033[93m>>准备进行一次重试...\033[0m")
            time.sleep(5)  
            retry_count += 1
        else:
            print("\033[91m>>投递失败，部分或全部文件不存在\033[0m")
            break
    command_to_kill_bash = "pkill -f /bin/bash"
    child.sendline(command_to_kill_bash)
    child.kill(signal.SIGINT)
    return
