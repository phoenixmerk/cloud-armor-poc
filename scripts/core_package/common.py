import subprocess


# 显示当前执行了什么方法
def print_func_name(func):
    def wrapper(*args, **kwargs):
        print('*******************************')
        print(f">>开始执行方法: {func.__name__}")
        result = func(*args, **kwargs)
        return result

    return wrapper


# 这个方法用来命令执行
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(">>Error occurred:", error.decode())
        return
    print(output.decode())


# 获取所有node名称逗号分隔形式
def get_all_node_names():
    command = ["kubectl", "get", "nodes", "-o", "jsonpath={.items[*].metadata.name}"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(">>Error occurred:", error)
        return
    node_names = output.decode().split()
    node_names_str = ','.join(node_names)
    return node_names_str


# 获取所有node名称列表形式
def get_node_names():
    output = subprocess.check_output(['kubectl', 'get', 'nodes'], stderr=subprocess.STDOUT).decode()
    lines = output.split('\n')[1:]
    node_names = [line.split()[0] for line in lines if line]
    return node_names


# 获取指定node节点的IP
def get_node_internal_ip(exec_node_name):
    output = subprocess.check_output(['kubectl', 'get', 'nodes', '-o', 'wide'], stderr=subprocess.STDOUT).decode()
    lines = output.split('\n')
    for line in lines:
        if exec_node_name in line.split()[0]:
            internal_ip = line.split()[5]
            return internal_ip
    return None


# 获取指定服务名的服务 IP
def get_service_ip(service_name, namespace=None):
    try:
        cmd = ['kubectl', 'get', 'svc', '-A', '-o', 'wide']
        if namespace:
            cmd.extend(['-n', namespace])
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
        lines = output.split('\n')
        for line in lines:
            if service_name in line:
                parts = line.split()
                if len(parts) > 3:
                    service_ip = parts[3]
                    return service_ip
                else:
                    print(f"\033[91m>>警告：服务 {service_name} 的信息不完整\033[0m")
                    return None
        print(f"\033[91m>>错误：未找到服务 {service_name}\033[0m")
        return None
    except subprocess.CalledProcessError as e:
        print("\033[91m>>执行 kubectl 命令时发生错误:\033[0m", e.output.decode())
        return None
    except Exception as e:
        print("\033[91m>>发生未知错误:\033[0m", str(e))
        return None


# 获取指定pod的内部ip
def get_pod_internal_ip(pod_name):
    output = subprocess.check_output(['kubectl', 'get', 'pods', '-n', 'xinfan', '-o', 'wide'],
                                     stderr=subprocess.STDOUT).decode()
    lines = output.split('\n')
    for line in lines:
        if line.split()[0].startswith(pod_name):
            if line.split()[3] == "0":
                internal_ip = line.split()[5]
                return internal_ip
            else:
                internal_ip = line.split()[7]
                return internal_ip
    return None


# 这个方法用来给节点打标签
def label_node(node_name):
    try:
        subprocess.check_output(['kubectl', 'label', 'nodes', node_name, 'nodeSetcontainer=cloudarmortest'],
                                stderr=subprocess.STDOUT)
        print(f"\033[91m>>节点 {node_name} 已成功打上标签 nodeSetcontainer=cloudarmortest\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91m>>Error occurred:\033[0m", e.output.decode())
        raise


# 这个方法用来给节点下标签
def remove_label(node_name):
    try:
        subprocess.check_output(['kubectl', 'label', 'nodes', node_name, 'nodeSetcontainer-'], stderr=subprocess.STDOUT)
        print(f"\033[91m>>节点 {node_name} 的标签 nodeSetcontainer 已成功移除\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91m>>Error occurred:\033[0m", e.output.decode())
        raise


# 这个方法用来显示是否有label
def node_has_label(node_name, label):
    output = subprocess.check_output(['kubectl', 'describe', 'node', node_name], stderr=subprocess.STDOUT).decode()
    return label in output


# 确定命名空间存在
def ensure_namespace_exists(namespace):
    try:
        subprocess.check_output(['kubectl', 'get', 'namespaces', namespace])
        print(f">>命名空间{namespace}已存在")
        return True
    except subprocess.CalledProcessError:
        return False


# 输入测试节点名
def input_test_node_name():
    global node_name
    node_name = input(f">>请输入测试节点名（\033[91m例：{get_all_node_names()}\033[0m）：\n")
    node_list = get_node_names()
    while node_name not in node_list:
        print(">>请输入正确的节点名")
        node_name = input(f">>请输入测试节点名（\033[91m例：{get_all_node_names()}\033[0m）：\n")


# 输入执行节点名
def input_exec_node_name():
    global exec_node_name
    exec_node_name = input(f">>请输入执行节点名（\033[91m例：{get_all_node_names()}\033[0m）：\n")
    node_list = get_node_names()
    while exec_node_name not in node_list:
        print(">>请输入正确的节点名")
        exec_node_name = input(f">>请输入执行节点名（\033[91m例：{get_all_node_names()}\033[0m）：\n")
