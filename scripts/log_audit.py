import subprocess
import shutil
import os
import time

from core_package import print_func_name


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


def manage_static_pod(optype):
    src_file = '../yamls/armor-static.yaml'
    dst_file = '/etc/kubernetes/manifests/armor-static.yaml'
    if optype == 'create':
        shutil.copy(src_file, dst_file)
        print("\033[92m>>static-pod创建成功\033[0m")
    elif optype == 'delete':
        os.remove(dst_file)
        print("\033[92m>>static-pod删除成功\033[0m")


# 这个方法用来管理ubuntu部署
@print_func_name
def manage_privilege_yaml(file_path, optype):
    try:
        output = subprocess.check_output(['kubectl', optype, '-f', file_path], stderr=subprocess.STDOUT).decode()
        if 'deployment.apps/privilege-target-deployment created' in output:
            print("\033[92mprivilege-target-deployment创建成功\033[0m")
        if 'deployment.apps "privilege-target-deployment" deleted' in output:
            print("\033[92mprivilege-target-deployment删除成功\033[0m")
        if 'deployment.apps/privilege-target-deployment configured' in output:
            print("\033[92mprivilege-target-deployment重新配置\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mError occurred:\033[0m", e.output.decode())
        raise
