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
from log_audit import access_secrets_url, access_pod_url, get_control_plane_internal_ip
from network_model import exec_abnormal_nc_process
from perl_reverse_shell import exec_perl_process, run_perl_command
from bash_reverse_shell_process import run_bash_process_command, exec_bash_reverse_process
from process_model import exec_abnormal_tail_process
from thinkphp5_rce import send_request
from virus_inspect import copy_virus_process
from webshell_inspect import copy_webshell_process

# YAML文件修改器
class YAMLModifier:
    def __init__(self, directory='../yamls'):
        self.directory = directory
    # 修改YAML文件
    def modify_yaml_file(self, file_path, new_secret_name, image_repository, project_name):
        with open(file_path, 'r') as file:
            yaml_contents = list(yaml.safe_load_all(file))
        for content in yaml_contents:
            spec = content['spec']
            if content.get('kind') == 'Pod':
                container = spec['containers'][0]
                new_image = f'{image_repository}/{project_name}/{container["image"].split("/")[-1]}'
                spec['imagePullSecrets'][0]['name'] = new_secret_name
                container['image'] = new_image
            elif content.get('kind') == 'Deployment':
                template_spec = content['spec']['template']['spec']
                container = template_spec['containers'][0]
                new_image = f'{image_repository}/{project_name}/{container["image"].split("/")[-1]}'
                template_spec['imagePullSecrets'][0]['name'] = new_secret_name
                container['image'] = new_image
        with open(file_path, 'w') as file:
            yaml.safe_dump_all(yaml_contents, file)

    # 获取目录下的所有YAML文件
    def modify_all_yaml_files(self, new_secret_name, image_repository, project_name):
        all_yaml_files = glob.glob(os.path.join(self.directory, '*.yaml'))
        for file_path in all_yaml_files:
            self.modify_yaml_file(file_path, new_secret_name, image_repository, project_name)

    # 用户输入并修改YAML文件
    def prompt_and_modify(self):
        while True:
            print("请选择镜像来源：")
            print("1. 本地镜像")
            print("2. 仓库镜像")
            try:
                choice = int(input(">>请输入选项数字1或2："))
                if choice == 1:
                    self.modify_all_yaml_files(
                        SECRETS_NAME_DEFAULT,
                        IMAGE_REPOSITORY_DEFAULT,
                        PROJECT_NAME_DEFAULT
                    )
                    break
                elif choice == 2:
                    repo = input(f">>请输入镜像仓库名称(\033[91m例：core.harbor.safedog.site\033[0m)：") or IMAGE_REPOSITORY_DEFAULT
                    project = input(">>请输入项目名称(\033[91m例：armorpoc20240512\033[0m)：") or PROJECT_NAME_DEFAULT
                    secret = input(">>请输入secrets名称(\033[91m例：harbor-secret\033[0m)：") or SECRETS_NAME_DEFAULT
                    self.modify_all_yaml_files(secret, repo, project)
                    break
                else:
                    print(">>输入错误，请输入1或2")
            except ValueError:
                print(">>输入错误，请输入数字1或2")

# 脚本菜单管理器
class ScriptMenuManager:
    def __init__(self, scripts_menu, highlight_scripts):
        self.scripts = scripts_menu
        self.highlight_scripts = highlight_scripts
        self.script_to_number = {script: number for number, script in self.scripts.items()}
    # 生成分组脚本
    def generate_grouped_scripts(self):
        return {
            bold_text(title): [self.scripts[i] for i in indices]
            for title, indices in [
                ('\n一、一键部署环境', range(1, 3)),
                ('\n二、七步杀伤链之“侦查跟踪”的检测及防护', range(3, 6)),
                ('\n三、七步杀伤链之“武器构建”的检测及防护', range(6, 8)),
                ('\n四、七步杀伤链之“载荷投递”的检测及防护', range(8, 11)),
                ('\n五、七步杀伤链之“漏洞利用”的检测及防护', range(11, 13)),
                ('\n六、七步杀伤链之“安装植入”的检测及防护', range(13, 20)),
                ('\n七、七步杀伤链之”命令与控制“的检测及防护', range(20, 25)),
                ('\n八、七步杀伤链之“目标达成”的检测及防护', range(25, 27)),
            ]
        }
    
    # 打印分组脚本
    def print_grouped_scripts(self):
        grouped_scripts = self.generate_grouped_scripts()
        for group, items in grouped_scripts.items():
            print(group)
            for script in items:
                number = self.script_to_number.get(script, '未知编号')
                if script in self.highlight_scripts:
                    print(f'\033[92m{number}: {script}\033[0m')
                else:
                    print(f'{number}: {script}')

# 缓存节点名称
node_name = ""
exec_node_name = ""

# 输入节点名称
def input_node_name(prompt_key: str) -> str:
    global node_name, exec_node_name
    if prompt_key == "测试" and node_name:
        print(f">>已缓存测试节点：{node_name}")
        return node_name
    elif prompt_key == "执行" and exec_node_name:
        print(f">>已缓存执行节点：{exec_node_name}")
        return exec_node_name

    try:
        node_names = get_all_node_names()
    except Exception as e:
        print(e)
        exit(1)

    print(f"\n请选择{prompt_key}节点：")
    for idx, name in enumerate(node_names):
        print(f"{idx + 1}: {name}")

    while True:
        try:
            choice = int(input(">>请输入节点编号："))
            if 1 <= choice <= len(node_names):
                selected_node = node_names[choice - 1]
                print(f">>你选择了节点：{selected_node}")

                # 缓存到对应变量
                if prompt_key == "测试":
                    node_name = selected_node
                elif prompt_key == "执行":
                    exec_node_name = selected_node

                return selected_node
            else:
                print(f">>输入错误，请输入1到{len(node_names)}之间的数字")
        except ValueError:
            print(">>输入错误，请输入数字编号")        

# 清空缓存
def clear_node_cache():
    global node_name, exec_node_name
    node_name = None
    exec_node_name = None

# 显示脚本横幅
def show_banner():
    banner = """
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
    print(banner + ' ' * padding + copyright)


# 环境一键部署/删除
def script_exec_0():
    print("\033[91m>>脚本创建命名空间xinfan，并在指定测试节点部署所有所需的pod\033[0m")
    global node_name
    input_node_name("测试")
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
        clear_node_cache()
        pass


# 暴力破解环境部署/删除
def script_exec_bruteforce_env():
    global node_name
    input_node_name("测试")
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
        clear_node_cache()
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
    input_node_name("测试")
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
        clear_node_cache()
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
    input_node_name("测试")
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
        clear_node_cache()
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
    input_node_name("测试")
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
        clear_node_cache()


# thinkphp5远程代码执行
def script_exec_thinkphp5_rce():
    print('*******************************')
    global node_name
    server = get_node_internal_ip(node_name)
    send_request(server)


# 安装植入环境部署/删除
def script_exec_mem_install_env():
    global node_name
    input_node_name("测试")
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
        clear_node_cache()
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
    input_node_name("测试")
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
        clear_node_cache()
        pass

# 黑客工具逃逸
def script_exec_cdk_exploit():
    print('*******************************')
    exec_cdk_process()

# 后门检测环境部署/删除
def script_exec_backdoor_env():
    global node_name
    input_node_name("测试")
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
        clear_node_cache()
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
    print("\033[91m>>脚本创建命名空间xinfan，后续测试最好在master节点中进行\033[0m")
    input_node_name("测试")
    if not node_has_label(node_name, 'nodeSetcontainer=cloudarmortest'):
        label_node(node_name)
    else:
        print(f"\033[91m>>节点 {node_name} 已经有标签 nodeSetcontainer=cloudarmortest\033[0m")
    internal_ip = get_control_plane_internal_ip()
    access_pod_url(internal_ip)
    access_secrets_url(internal_ip)
    print(f"\033[91m>>一键生成日志审计入侵数据成功\033[0m")
    clear_node_cache()

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
def get_all_node_names() -> list:
    command = ["kubectl", "get", "nodes", "-o", "jsonpath={.items[*].metadata.name}"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        raise RuntimeError(f"获取节点失败：{error.decode()}")

    if not output:
        raise RuntimeError(">>没有可用节点")

    return output.decode().split()

# 脚本颜色高亮
def bold_text(text):
    return f'\033[1m{text}\033[0m'

# 获取用户选择的脚本
def get_user_choice():
    while True:
        try:
            choice = int(input('\n>>请输入一个数字来选择要执行的脚本(\033[91m例：0-26，输入0则退出脚本\033[0m)：'))
            if 0 <= choice <= 26:
                return choice
            else:
                print(">>输入错误，请输入0-26之间的数字")
        except ValueError:
            print(">>输入错误，请输入一个数字")

# 显示脚本列表
def run_script_by_choice(choice, yaml_modifier=None):
    if yaml_modifier is None:
        yaml_modifier = YAMLModifier(directory='../yamls')
    SCRIPT_MAP = {
        '环境一键部署/删除': lambda: (
            yaml_modifier.prompt_and_modify(),
            script_exec_0()
        ),
        '一键生成入侵数据': lambda: (
            input_node_name("测试"),
            input_node_name("执行"),
            script_exec_ssh_bruteforce(),
            script_exec_honeypot(),
            script_exec_bash_reverse_shell(),
            script_exec_virus_inspect(),
            script_exec_webshell_inspect(),
            script_exec_thinkphp5_rce(),
            script_exec_behinder_memshell(),
            script_exec_abnormal_cmd(),
            script_exec_abnormal_file(),
            script_exec_network_model(),
            script_exec_process_model(),
            script_exec_file_model(),
            script_exec_cdk_exploit(),
            script_exec_perl_reverse_shell(),
            script_exec_bash_reverse_shell_process(),
            script_exec_ioc_alarm()
        ),
        '暴力破解环境部署/删除': lambda: (
            yaml_modifier.prompt_and_modify(),
            script_exec_bruteforce_env()
        ),
        'SSH暴力破解': lambda: (
            input_node_name("测试"),
            script_exec_ssh_bruteforce()
        ),
        '蜜罐诱捕': lambda: (
            input_node_name("测试"),
            script_exec_honeypot()
        ),
        '武器构建环境部署/删除': lambda: (
            yaml_modifier.prompt_and_modify(),
            script_exec_weapon_make_env()
        ),
        'Bash反弹交互执行': lambda: (
            input_node_name("执行"),
            script_exec_bash_reverse_shell()
        ),
        '病毒防护环境部署/删除': lambda: (
            yaml_modifier.prompt_and_modify(),
            input_node_name("测试"),
            script_exec_virus_env()
        ),
        '二进制病毒动态监测': script_exec_virus_inspect,
        'webshell动态监测': script_exec_webshell_inspect,
        '漏洞利用环境部署/删除': script_exec_exploit_env,
        'ThinkPHP5远程代码执行': lambda: (
            input_node_name("测试"),
            script_exec_thinkphp5_rce()
        ),
        '内存webshell检测': script_exec_behinder_memshell,
        '容器异常命令': lambda: (
            input_node_name("测试"),
            script_exec_abnormal_cmd()
        ),
        '文件异常操作': script_exec_abnormal_file,
        '网络模型': script_exec_network_model,
        '文件模型': script_exec_file_model,
        '进程模型': script_exec_process_model,
        '容器逃逸环境部署/删除': lambda: (
            yaml_modifier.prompt_and_modify(),
            script_exec_escape_env()
        ),
        'CDK黑客工具利用': script_exec_cdk_exploit,
        '后门检测环境部署/删除': lambda: (
            yaml_modifier.prompt_and_modify(),
            script_exec_backdoor_env()
        ),
        'Perl反弹Shell': lambda: (
            input_node_name("执行"),
            script_exec_perl_reverse_shell()
        ),
        'Bash反弹Shell进程参数': lambda: (
            input_node_name("执行"),
            script_exec_bash_reverse_shell_process()
        ),
        '日志审计一键入侵数据生成': lambda: (
            yaml_modifier.prompt_and_modify(),
            script_exec_log_audit()
        ),
        '威胁情报': lambda: (
            input_node_name("执行"),
            script_exec_ioc_alarm()
        ),
    }

    script_name = SCRIPTS_MENU.get(choice)
    if script_name is None:
        print('>>错误: 无效的选择')
        return

    try:
        handler = SCRIPT_MAP.get(script_name)
        if handler:
            handler()
            print(f'>>\033[92m脚本{script_name}执行成功\033[0m')
        else:
            print(f">>未实现该脚本：{script_name}")
    except subprocess.CalledProcessError as e:
        print(f'>>执行脚本{script_name}时发生错误: {str(e)}')

# 主流程函数，依次调用获取用户输入和执行对应脚本
def main():
    show_banner()  
    menu_manager = ScriptMenuManager(SCRIPTS_MENU, HIGHLIGHT_SCRIPTS)
    menu_manager.print_grouped_scripts()
    while True:
        choice = get_user_choice()
        if choice == 0:
            print(">>感谢使用信帆POC测试脚本，再见！")
            break
        run_script_by_choice(choice)


if __name__ == "__main__":
    main()



