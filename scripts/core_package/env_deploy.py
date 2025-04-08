import subprocess


# 显示当前执行了什么方法
def print_func_name(func):
    def wrapper(*args, **kwargs):
        print('*******************************')
        print(f">>开始执行方法: {func.__name__}")
        result = func(*args, **kwargs)
        return result

    return wrapper


# 这个方法用来部署ssh pod
@print_func_name
def manage_ssh_yaml(file_path, optype):
    try:
        command = ['kubectl', 'apply' if optype == 'create' else optype, '-f', file_path]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode()
        if 'deployment.apps/centosssh-target-deployment created' in output:
            print("\033[92m>>ssh-deployment创建成功\033[0m")
        if 'service/ssh-target-nodeport created' in output:
            print("\033[92m>>ssh-service创建成功\033[0m")
        if 'deployment.apps "centosssh-target-deployment" deleted' in output:
            print("\033[92m>>ssh-deployment删除成功\033[0m")
        if 'service "ssh-target-nodeport" deleted' in output:
            print("\033[92m>>ssh-service删除成功\033[0m")
        if 'deployment.apps/centosssh-target-deployment configured' in output:
            print("\033[92m>>ssh-deployment重新配置\033[0m")
        if 'service/ssh-target-nodeport unchanged' in output:
            print("\033[92m>>ssh-service未改变\033[0m")
    except subprocess.CalledProcessError as e:
        if "Unable to connect to the server: dial tcp" in e.stderr:
            print("\033[91m>>错误原因: DNS 解析失败或 Kubernetes 服务不可用\033[0m")
        elif "The connection to the server localhost:8080 was refused" in e.stderr:
            print("\033[91m>>错误原因: kubectl 认证失败或 Kubernetes 服务未启动\033[0m")
        else:
            print("\033[91m>>错误原因:\033[0m", e.output.decode())
        raise


# 这个方法用来管理thinkphp部署
@print_func_name
def manage_thinkphp_yaml(file_path, optype):
    try:
        command = ['kubectl', 'apply' if optype == 'create' else optype, '-f', file_path]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode()
        if 'deployment.apps/thinkphp-target-deployment created' in output:
            print("\033[92m>>thinkphp-deployment创建成功\033[0m")
        if 'service/thinkphp-service created' in output:
            print("\033[92m>>thinkphp-service创建成功\033[0m")
        if 'deployment.apps "thinkphp-target-deployment" deleted' in output:
            print("\033[92m>>thinkphp-deployment删除成功\033[0m")
        if 'service "thinkphp-service" deleted' in output:
            print("\033[92m>>thinkphp-service删除成功\033[0m")
        if 'deployment.apps/thinkphp-target-deployment configured' in output:
            print("\033[92m>>thinkphp-deployment重新配置\033[0m")
        if 'service/thinkphp-service unchanged' in output:
            print("\033[92m>>thinkphp-service未改变\033[0m")
    except subprocess.CalledProcessError as e:
        if "Unable to connect to the server: dial tcp" in e.stderr:
            print("\033[91m>>错误原因: DNS 解析失败或 Kubernetes 服务不可用\033[0m")
        elif "The connection to the server localhost:8080 was refused" in e.stderr:
            print("\033[91m>>错误原因: kubectl 认证失败或 Kubernetes 服务未启动\033[0m")
        else:
            print("\033[91m>>错误原因:\033[0m", e.output.decode())
        raise

# 这个方法用来管理dvwa部署
@print_func_name
def manage_dvwa_yaml(file_path, optype):
    try:
        command = ['kubectl', 'apply' if optype == 'create' else optype, '-f', file_path]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode()
        if 'deployment.apps/dvwa-target-deployment created' in output:
            print("\033[92m>>dvwa-deployment创建成功\033[0m")
        if 'deployment.apps "dvwa-target-deployment" deleted' in output:
            print("\033[92m>>dvwa-deployment删除成功\033[0m")
        if 'deployment.apps/dvwa-target-deployment configured' in output:
            print("\033[92m>>dvwa-deployment重新配置\033[0m")
    except subprocess.CalledProcessError as e:
        if "Unable to connect to the server: dial tcp" in e.stderr:
            print("\033[91m>>错误原因: DNS 解析失败或 Kubernetes 服务不可用\033[0m")
        elif "The connection to the server localhost:8080 was refused" in e.stderr:
            print("\033[91m>>错误原因: kubectl 认证失败或 Kubernetes 服务未启动\033[0m")
        else:
            print("\033[91m>>错误原因:\033[0m", e.output.decode())
        raise


# 这个方法用来管理tomcat部署
@print_func_name
def manage_tomcat_yaml(file_path, optype):
    try:
        command = ['kubectl', 'apply' if optype == 'create' else optype, '-f', file_path]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode()
        if 'deployment.apps/tomcat-target-deployment created' in output:
            print("\033[92m>>tomcat-deployment创建成功\033[0m")
        if 'service/tomcat-webframe created' in output:
            print("\033[92m>>tomcat-service创建成功\033[0m")
        if 'deployment.apps "tomcat-target-deployment" deleted' in output:
            print("\033[92m>>tomcat-deployment删除成功\033[0m")
        if 'service "tomcat-webframe" deleted' in output:
            print("\033[92m>>tomcat-service删除成功\033[0m")
        if 'deployment.apps/tomcat-target-deployment configured' in output:
            print("\033[92m>>tomcat-deployment重新配置\033[0m")
        if 'service/tomcat-webframe unchanged' in output:
            print("\033[92m>>tomcat-service未改变\033[0m")
    except subprocess.CalledProcessError as e:
        if "Unable to connect to the server: dial tcp" in e.stderr:
            print("\033[91m>>错误原因: DNS 解析失败或 Kubernetes 服务不可用\033[0m")
        elif "The connection to the server localhost:8080 was refused" in e.stderr:
            print("\033[91m>>错误原因: kubectl 认证失败或 Kubernetes 服务未启动\033[0m")
        else:
            print("\033[91m>>错误原因:\033[0m", e.output.decode())
        raise
