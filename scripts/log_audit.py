import subprocess
import time

# 这个方法用来访问pod端点
def access_pod_url(node_ip):
    command = f"curl -k https://{node_ip}:6443/api/v1/namespaces/xinfan/pods"
    process = None
    try:
        process = subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("\033[92m>>尝试未授权访问api-server\033[0m")
        time.sleep(2)
    except Exception:
        print("\033[92m>>尝试未授权访问api-server失败\033[0m")
    finally:
        if process:
            process.terminate()
    return


# 这个方法用来访问secrets端点
def access_secrets_url(node_ip):
    command = f"curl -k https://{node_ip}:6443/api/v1/namespaces/xinfan/secrets/"
    process = None
    try:
        process = subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("\033[92m>>尝试未授权访问secrets\033[0m")
        time.sleep(2)
    except Exception:
        print("\033[92m>>尝试未授权访问secrets失败\033[0m")
    finally:
        if process:
            process.terminate()
    return


# 这个方法用来获取节点的内部ip
def get_control_plane_internal_ip():
    output = subprocess.check_output(['kubectl', 'get', 'nodes', '-o', 'wide'], stderr=subprocess.STDOUT).decode()
    lines = output.split('\n')
    for line in lines:
        if 'control-plane' in line.split()[2] or 'master' in line.split()[2]:
            internal_ip = line.split()[5]
            return internal_ip
    return None

