import threading
import yaml
import glob
import os

from config import *
from core_package.common import *
from core_package.env_deploy import *
from abnormal_cmd import exec_abnormal_process
from abnormal_file import exec_abnormal_file_process
from ssh_bruteforce import ssh_bruteforce
from bash_reverse_shell import copy_file_to_pod, create_bash_script, run_nc_command
from behinder_memshell import send_memshell_request
from cdk_tool_exploit import exec_cdk_process
from file_model import exec_abnormal_touch_process
from honeypot_inspect import exec_honeypot_process
from ioc_alarm import exec_ioc_process, run_ioc_nc_command
from log_audit import manage_static_pod, manage_privilege_yaml, access_secrets_url, \
    access_pod_url, get_control_plane_internal_ip
from network_model import exec_abnormal_nc_process
from perl_reverse_shell import exec_perl_process, run_perl_command
from bash_reverse_shell_process import run_bash_process_command, exec_bash_reverse_process
from process_model import exec_abnormal_tail_process
from thinkphp5_rce import send_request
from virus_inspect import copy_virus_process
from webshell_inspect import copy_webshell_process

# 工具标题
title = """
\033[91m

       _        __                               
      (_)      / _|                              
 __  ___ _ __ | |_ __ _ _ __    _ __   ___   ___ 
 \ \/ / | '_ \|  _/ _` | '_ \  | '_ \ / _ \ / __|
  >  <| | | | | || (_| | | | | | |_) | (_) | (__ 
 /_/\_\_|_| |_|_| \__,_|_| |_| | .__/ \___/ \___|
                               | |               
                               |_|         
                                     
                             云原生安全-信帆POC测试脚本
\033[0m
"""

copyright = "Copyright © 2025 by Cloud Security Team"
width = 50
padding = width - len(copyright) - 1

# 将版权信息放置到标题下方
title_with_copyright = title + ' ' * padding + copyright

print(title_with_copyright)


# 环境一键部署/删除
def script_exec_0():
    print("\033[91m>>脚本创建命名空间xinfan，并在指定测试节点部署所有所需的pod\033[0m")
    input_test_node_name()
    if not node_has_label(node_name, 'nodeSetcontainer=cloudarmortest'):
        label_node(node_name)
    else:
        print(f"\033[91m>>节点{node_name}已经有标签 nodeSetcontainer=cloudarmortest\033[0m")
    optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    while optype not in ['create', 'delete']:
        print(">>输入错误，请输入'create'或'delete'")
        optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    if optype == 'create':
        manage_ssh_yaml('../yamls/armor-ssh.yaml', optype)
        manage_thinkphp_yaml('../yamls/armor-thinkphp.yaml', optype)
        manage_dvwa_yaml('../yamls/armor-dvwa.yaml', optype)
        manage_tomcat_yaml('../yamls/armor-tomcat.yaml', optype)
        pass
    elif optype == 'delete':
        manage_ssh_yaml('../yamls/armor-ssh.yaml', optype)
        manage_thinkphp_yaml('../yamls/armor-thinkphp.yaml', optype)
        manage_dvwa_yaml('../yamls/armor-dvwa.yaml', optype)
        manage_tomcat_yaml('../yamls/armor-tomcat.yaml', optype)
        remove_label(node_name)
        pass


# 暴力破解环境部署/删除
def script_exec_bruteforce_env():
    global node_name
    input_test_node_name()
    if not node_has_label(node_name, 'nodeSetcontainer=cloudarmortest'):
        label_node(node_name)
    else:
        print(f"\033[91m>>节点{node_name}已经有标签 nodeSetcontainer=cloudarmortest\033[0m")
    optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    while optype not in ['create', 'delete']:
        print(">>输入错误，请输入'create'或'delete'")
        optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    if optype == 'create':
        manage_ssh_yaml('../yamls/armor-ssh.yaml', optype)
        pass
    elif optype == 'delete':
        manage_ssh_yaml('../yamls/armor-ssh.yaml', optype)
        remove_label(node_name)
        pass


# SSH暴力破解
def script_exec_ssh_bruteforce():
    print('*******************************')
    server = get_service_ip('ssh-target-clusterip')
    ssh_bruteforce(server, USER_PASS_PAIR)
    print("\033[92m>>正常测试情况下1min内能看到告警\033[0m")


# 蜜罐诱捕
def script_exec_honeypot():
    print('*******************************')
    global node_name
    exec_honeypot_process(node_name)


# 武器构建环境部署/删除
def script_exec_weapon_make_env():
    global node_name
    input_test_node_name()
    if not node_has_label(node_name, 'nodeSetcontainer=cloudarmortest'):
        label_node(node_name)
    else:
        print(f"\033[91m节点{node_name}已经有标签 nodeSetcontainer=cloudarmortest\033[0m")
    optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    while optype not in ['create', 'delete']:
        print(">>输入错误，请输入'create'或'delete'")
        optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    if optype == 'create':
        manage_ssh_yaml('../yamls/armor-ssh.yaml', optype)
        pass
    elif optype == 'delete':
        manage_ssh_yaml('../yamls/armor-ssh.yaml', optype)
        remove_label(node_name)
        pass


# bash反弹shell交互执行
def script_exec_bash_reverse_shell():
    print('*******************************')
    thread1 = threading.Thread(target=run_nc_command)
    thread1.start()
    thread2 = threading.Thread(target=create_bash_script('armor-poc-worker'))
    thread2.start()
    thread3 = threading.Thread(target=copy_file_to_pod)
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()


# 病毒防护环境部署/删除
def script_exec_virus_env():
    global node_name
    input_test_node_name()
    if not node_has_label(node_name, 'nodeSetcontainer=cloudarmortest'):
        label_node(node_name)
    else:
        print(f"\033[91m节点{node_name}已经有标签 nodeSetcontainer=cloudarmortest\033[0m")
    optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    while optype not in ['create', 'delete']:
        print(">>输入错误，请输入'create'或'delete'")
        optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    if optype == 'create':
        manage_dvwa_yaml('../yamls/armor-dvwa.yaml', optype)
        pass
    elif optype == 'delete':
        manage_dvwa_yaml('../yamls/armor-dvwa.yaml', optype)
        remove_label(node_name)
        pass


# 二进制病毒动态监测
def script_exec_virus_inspect():
    print('*******************************')
    copy_virus_process()


# webshell动态监测
def script_exec_webshell_inspect():
    print('*******************************')
    copy_webshell_process()


# 漏洞利用环境部署/删除
def script_exec_exploit_env():
    global node_name
    input_test_node_name()
    if not node_has_label(node_name, 'nodeSetcontainer=cloudarmortest'):
        label_node(node_name)
    else:
        print(f"\033[91m节点{node_name}已经有标签 nodeSetcontainer=cloudarmortest\033[0m")
    optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    while optype not in ['create', 'delete']:
        print(">>输入错误，请输入'create'或'delete'")
        optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    if optype == 'create':
        manage_thinkphp_yaml('../yamls/armor-thinkphp.yaml', optype)
        pass
    elif optype == 'delete':
        manage_thinkphp_yaml('../yamls/armor-thinkphp.yaml', optype)
        remove_label(node_name)


# thinkphp5远程代码执行
def script_exec_thinkphp5_rce():
    print('*******************************')
    global node_name
    server = get_node_internal_ip(node_name)
    send_request(server)


# 安装植入环境部署/删除
def script_exec_mem_install_env():
    global node_name
    input_test_node_name()
    if not node_has_label(node_name, 'nodeSetcontainer=cloudarmortest'):
        label_node(node_name)
    else:
        print(f"\033[91m节点{node_name}已经有标签 nodeSetcontainer=cloudarmortest\033[0m")
    optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    while optype not in ['create', 'delete']:
        print(">>输入错误，请输入'create'或'delete'")
        optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    if optype == 'create':
        manage_ssh_yaml('../yamls/armor-ssh.yaml', optype)
        manage_dvwa_yaml('../yamls/armor-dvwa.yaml', optype)
        manage_tomcat_yaml('../yamls/armor-tomcat.yaml', optype)
        pass
    elif optype == 'delete':
        manage_ssh_yaml('../yamls/armor-ssh.yaml', optype)
        manage_dvwa_yaml('../yamls/armor-dvwa.yaml', optype)
        manage_tomcat_yaml('../yamls/armor-tomcat.yaml', optype)
        remove_label(node_name)
        pass


# 内存webshell检测
def script_exec_behinder_memshell():
    print('*******************************')
    send_memshell_request()


# 容器异常命令
def script_exec_abnormal_cmd():
    print('*******************************')
    global node_name
    exec_abnormal_process(node_name)


# 文件异常操作
def script_exec_abnormal_file():
    print('*******************************')
    exec_abnormal_file_process()


# 网络模型
def script_exec_network_model():
    print('*******************************')
    global node_name
    exec_abnormal_nc_process()


# 进程模型
def script_exec_process_model():
    print('*******************************')
    exec_abnormal_tail_process()


# 文件模型
def script_exec_file_model():
    print('*******************************')
    exec_abnormal_touch_process()


# 容器逃逸环境部署/删除
def script_exec_escape_env():
    global node_name
    input_test_node_name()
    if not node_has_label(node_name, 'nodeSetcontainer=cloudarmortest'):
        label_node(node_name)
    else:
        print(f"\033[91m>>节点{node_name}已经有标签 nodeSetcontainer=cloudarmortest\033[0m")
    optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    while optype not in ['create', 'delete']:
        print(">>输入错误，请输入'create'或'delete'")
        optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    if optype == 'create':
        manage_ssh_yaml('../yamls/armor-ssh.yaml', optype)
        pass
    elif optype == 'delete':
        manage_ssh_yaml('../yamls/armor-ssh.yaml', optype)
        remove_label(node_name)
        pass


# 黑客工具逃逸
def script_exec_cdk_exploit():
    print('*******************************')
    exec_cdk_process()


# 后门检测环境部署/删除
def script_exec_backdoor_env():
    global node_name
    input_test_node_name()
    if not node_has_label(node_name, 'nodeSetcontainer=cloudarmortest'):
        label_node(node_name)
    else:
        print(f"\033[91m节点 {node_name} 已经有标签 nodeSetcontainer=cloudarmortest\033[0m")
    optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    while optype not in ['create', 'delete']:
        print(">>输入错误，请输入'create'或'delete'")
        optype = input(">>请输入环境部署操作类型（\033[91m例：create/delete\033[0m）：\n")
    if optype == 'create':
        manage_ssh_yaml('../yamls/armor-dvwa.yaml', optype)
        pass
    elif optype == 'delete':
        manage_ssh_yaml('../yamls/armor-dvwa.yaml', optype)
        remove_label(node_name)
        pass


# perl反弹shell
def script_exec_perl_reverse_shell():
    print('*******************************')
    thread1 = threading.Thread(target=run_perl_command)
    thread1.start()
    thread2 = threading.Thread(target=exec_perl_process())
    thread2.start()
    thread1.join()
    thread2.join()


# bash反弹shell进程参数
def script_exec_bash_reverse_shell_process():
    print('*******************************')
    thread1 = threading.Thread(target=run_bash_process_command)
    thread1.start()
    thread2 = threading.Thread(target=exec_bash_reverse_process)
    thread2.start()
    thread1.join()
    thread2.join()


# 日志审计环境一键部署/删除&一键入侵数据生成
def script_exec_log_audit():
    global node_name
    print("\033[91m>>脚本创建命名空间xinfan，后续测试最好在主节点中进行\033[0m")
    input_test_node_name()
    if not node_has_label(node_name, 'nodeSetcontainer=cloudarmortest'):
        label_node(node_name)
    else:
        print(f"\033[91m>>节点 {node_name} 已经有标签 nodeSetcontainer=cloudarmortest\033[0m")
    internal_ip = get_control_plane_internal_ip()
    manage_privilege_yaml('../yamls/armor-privilege.yaml', 'create')
    access_pod_url(internal_ip)
    access_secrets_url(internal_ip)
    manage_static_pod('create')
    print(f"\033[91m>>一键生成日志审计入侵数据成功，5s后回收所有部署\033[0m")
    manage_privilege_yaml('../yamls/armor-privilege.yaml', 'delete')
    manage_static_pod('delete')


# 恶意外联入侵数据生成
def script_exec_ioc_alarm():
    print('*******************************')
    thread1 = threading.Thread(target=run_ioc_nc_command)
    thread1.start()
    thread2 = threading.Thread(target=exec_ioc_process())
    thread2.start()
    thread1.join()
    thread2.join()


# 获取所有node名称
def get_all_node_names():
    command = ["kubectl", "get", "nodes", "-o", "jsonpath={.items[*].metadata.name}"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print("Error occurred:", error)
        return

    node_names = output.decode().split()
    node_names_str = ','.join(node_names)
    return node_names_str


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


# 定义一个字典，键是数字，值是脚本名
scripts = {
    0: '退出脚本',
    1: '环境一键部署/删除',
    2: '一键生成入侵数据',
    3: '暴力破解环境部署/删除',
    4: 'SSH暴力破解',
    5: '蜜罐诱捕',
    6: '武器构建环境部署/删除',
    7: 'Bash反弹交互执行',
    8: '病毒防护环境部署/删除',
    9: '二进制病毒动态监测',
    10: 'webshell动态监测',
    11: '漏洞利用环境部署/删除',
    12: 'ThinkPHP5远程代码执行',
    13: '安装植入环境部署/删除',
    14: '内存webshell检测',
    15: '容器异常命令',
    16: '文件异常操作',
    17: '进程模型',
    18: '文件模型',
    19: '网络模型',
    20: '容器逃逸环境部署/删除',
    21: 'CDK黑客工具利用',
    22: '后门检测环境部署/删除',
    23: 'Perl反弹Shell',
    24: 'Bash反弹Shell进程参数',
    25: '日志审计一键入侵数据生成',
    26: '威胁情报'

}


# 定义一个新的字典，键是组名，值是一个包含该组中脚本的列表
def bold_text(text):
    return f'\033[1m{text}\033[0m'


grouped_scripts = {
    bold_text('\n一、一键部署环境'): [scripts[i] for i in range(1, 3)],
    bold_text('\n二、七步杀伤链之“侦查跟踪”的检测及防护'): [scripts[i] for i in range(3, 6)],
    bold_text('\n三、七步杀伤链之“武器构建”的检测及防护'): [scripts[i] for i in range(6, 8)],
    bold_text('\n四、七步杀伤链之“载荷投递”的检测及防护'): [scripts[i] for i in range(8, 11)],
    bold_text('\n五、七步杀伤链之“漏洞利用”的检测及防护'): [scripts[i] for i in range(11, 13)],
    bold_text('\n六、七步杀伤链之“安装植入”的检测及防护'): [scripts[i] for i in range(13, 20)],
    bold_text('\n七、七步杀伤链之”命令与控制“的检测及防护'): [scripts[i] for i in range(20, 25)],
    bold_text('\n八、七步杀伤链之“目标达成”的检测及防护'): [scripts[i] for i in range(25, 27)],
}

# 打印出所有分组的脚本
highlight_scripts = {'环境一键部署/删除', '一键生成入侵数据', '日志审计一键入侵数据生成'}
for group, item in grouped_scripts.items():
    print(f'{group}:')
    for script in item:
        number = list(scripts.values()).index(script)
        if script in highlight_scripts:
            print(f'\033[92m{number}: {script}\033[0m')
        else:
            print(f'{number}: {script}')


# 对yaml解析并修改
def modify_yaml_file(file_path, new_secret_name, image_repository, project_name):
    with open(file_path, 'r') as file:
        yaml_contents = list(yaml.safe_load_all(file))
    for yaml_content in yaml_contents:
        spec = yaml_content['spec']
        if yaml_content['kind'] == 'Pod':
            spec = yaml_content['spec']
            new_image_name = f'{image_repository}/{project_name}/{spec["containers"][0]["image"].split("/")[-1]}'
            spec['imagePullSecrets'][0]['name'] = new_secret_name
            spec['containers'][0]['image'] = new_image_name
        elif yaml_content['kind'] == 'Deployment':
            spec = yaml_content['spec']['template']['spec']
            new_image_name = f'{image_repository}/{project_name}/{spec["containers"][0]["image"].split("/")[-1]}'
            spec['imagePullSecrets'][0]['name'] = new_secret_name
            spec['containers'][0]['image'] = new_image_name
    with open(file_path, 'w') as file:
        yaml.safe_dump_all(yaml_contents, file)


# 获取目录下的所有YAML文件
def get_all_yaml_files(directory):
    return glob.glob(os.path.join(directory, '*.yaml'))


# 修改所有YAML文件
def modify_all_yaml_files(directory, new_secret_name, image_repository, project_name):
    all_yaml_files = get_all_yaml_files(directory)
    for file_path in all_yaml_files:
        modify_yaml_file(file_path, new_secret_name, image_repository, project_name)


# 修改YAML文件交互
def modify_yaml_files_based_on_user_input():
    while True:
        print("请选择镜像来源：")
        print("1. 本地镜像")
        print("2. 仓库镜像")
        try:
            choice = int(input(">>请输入选项数字1或2："))
            if choice == 1:
                modify_all_yaml_files('../yamls', SECRETS_NAME_DEFAULT, IMAGE_REPOSITORY_DEFAULT,
                                      PROJECT_NAME_DEFAULT)
                break
            elif choice == 2:
                image_repository = input(f">>请输入镜像仓库名称(\033[91m例：core.harbor.safedog.site\033[0m)：")
                if not image_repository:
                    image_repository = IMAGE_REPOSITORY_DEFAULT
                project_name = input(">>请输入项目名称(\033[91m例：armorpoc20240512\033[0m)：")
                if not project_name:
                    project_name = PROJECT_NAME_DEFAULT
                secrets_name = input(">>请输入secrets名称(\033[91m例：harbor-secret\033[0m)：")
                if not secrets_name:
                    secrets_name = SECRETS_NAME_DEFAULT
                modify_all_yaml_files('../yamls', secrets_name, image_repository, project_name)
                break
            else:
                print(">>输入错误，请输入1或2")
        except ValueError:
            print(">>输入错误，请输入数字1或2")


# 供用户选择脚本
while True:
    try:
        choice = int(input('\n>>请输入一个数字来选择要执行的脚本(\033[91m例：0-26，输入0则退出脚本\033[0m)：'))
        if 0 <= choice <= 26:
            break
        else:
            print(">>输入错误，请输入0-26之间的数字")
    except ValueError:
        print(">>输入错误，请输入一个数字")

script_name = scripts.get(choice)
node_name = ''
exec_node_name = ''
if script_name is None:
    print('>>错误: 无效的选择')
else:
    try:
        if script_name == '环境一键部署/删除':
            modify_yaml_files_based_on_user_input()
            script_exec_0()
        elif script_name == '一键生成入侵数据':
            input_test_node_name()
            input_exec_node_name()
            script_exec_ssh_bruteforce()
            script_exec_honeypot()
            script_exec_bash_reverse_shell()
            script_exec_virus_inspect()
            script_exec_webshell_inspect()
            script_exec_thinkphp5_rce()
            script_exec_behinder_memshell()
            script_exec_abnormal_cmd()
            script_exec_abnormal_file()
            script_exec_network_model()
            script_exec_process_model()
            script_exec_file_model()
            script_exec_cdk_exploit()
            script_exec_perl_reverse_shell()
            script_exec_bash_reverse_shell_process()
            script_exec_ioc_alarm()
        elif script_name == '暴力破解环境部署/删除':
            modify_yaml_files_based_on_user_input()
            script_exec_bruteforce_env()
        elif script_name == 'SSH暴力破解':
            input_test_node_name()
            script_exec_ssh_bruteforce()
        elif script_name == '蜜罐诱捕':
            input_test_node_name()
            script_exec_honeypot()
        elif script_name == '武器构建环境部署/删除':
            modify_yaml_files_based_on_user_input()
            script_exec_weapon_make_env()
        elif script_name == 'Bash反弹交互执行':
            input_exec_node_name()
            script_exec_bash_reverse_shell()
        elif script_name == '病毒防护环境部署/删除':
            modify_yaml_files_based_on_user_input()
            input_test_node_name()
            script_exec_virus_env()
        elif script_name == '二进制病毒动态监测':
            script_exec_virus_inspect()
        elif script_name == 'webshell动态监测':
            script_exec_webshell_inspect()
        elif script_name == '漏洞利用环境部署/删除':
            script_exec_exploit_env()
        elif script_name == 'ThinkPHP5远程代码执行':
            input_test_node_name()
            script_exec_thinkphp5_rce()
        elif script_name == '内存webshell检测':
            script_exec_behinder_memshell()
        elif script_name == '容器异常命令':
            input_test_node_name()
            script_exec_abnormal_cmd()
        elif script_name == '文件异常操作':
            script_exec_abnormal_file()
        elif script_name == '网络模型':
            script_exec_network_model()
        elif script_name == '文件模型':
            script_exec_file_model()
        elif script_name == '进程模型':
            script_exec_process_model()
        elif script_name == '容器逃逸环境部署/删除':
            modify_yaml_files_based_on_user_input()
            script_exec_escape_env()
        elif script_name == 'CDK黑客工具利用':
            script_exec_cdk_exploit()
        elif script_name == '后门检测环境部署/删除':
            modify_yaml_files_based_on_user_input()
            script_exec_backdoor_env()
        elif script_name == 'Perl反弹Shell':
            input_exec_node_name()
            script_exec_perl_reverse_shell()
        elif script_name == 'Bash反弹Shell进程参数':
            input_exec_node_name()
            script_exec_bash_reverse_shell_process()
        elif script_name == '日志审计一键入侵数据生成':
            modify_yaml_files_based_on_user_input()
            script_exec_log_audit()
        elif script_name == '威胁情报':
            input_exec_node_name()
            script_exec_ioc_alarm()
        print(f'>>\033[92m脚本{script_name}执行成功\033[0m')
    except subprocess.CalledProcessError as e:
        print(f'>>执行脚本{script_name}时发生错误: {str(e)}')
