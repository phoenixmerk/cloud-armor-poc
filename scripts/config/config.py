# 用户名密码列表
USER_PASS_PAIR = [
    ("root", "password1"),
    ("root", "password2"),
    ("root", "password3"),
    ("root", "password4"),
    ("root", "password5"),
    ("root", "password6"),
    ("root", "password7"),
    ("root", "password8"),
    ("root", "password9"),
    ("root", "password10"),
    ("root", "password11"),
]

# 仓库信息
IMAGE_REPOSITORY_DEFAULT = 'core.harbor.safedog.site'
PROJECT_NAME_DEFAULT = 'armorpoc20240512'
SECRETS_NAME_DEFAULT = 'harbor-secret'

# 脚本菜单（键是数字，值是脚本名称）
SCRIPTS_MENU = {
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

# 高亮显示的脚本
HIGHLIGHT_SCRIPTS = {'环境一键部署/删除', '一键生成入侵数据', '日志审计一键入侵数据生成'}

# 分组标题
GROUP_TITLES = {
    '\n一、一键部署环境',
    '\n二、七步杀伤链之“侦查跟踪”的检测及防护',
    '\n三、七步杀伤链之“武器构建”的检测及防护',
    '\n四、七步杀伤链之“载荷投递”的检测及防护',
    '\n五、七步杀伤链之“漏洞利用”的检测及防护',
    '\n六、七步杀伤链之“安装植入”的检测及防护',
    '\n七、七步杀伤链之”命令与控制“的检测及防护',
    '\n八、七步杀伤链之“目标达成”的检测及防护',
}