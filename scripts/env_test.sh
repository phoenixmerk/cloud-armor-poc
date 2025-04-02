#!/bin/bash

# 检查Python3是否存在
if command -v python3 &> /dev/null
then
    version=$(python3 -V 2>&1 | awk '{print $2}')
    if [[ "$version" < "3.6" ]]; then
        echo -e "\e[31mPython 3.6 or higher is required.\e[0m\t\e[91m【失败】\e[0m"
        exit 1
    else
        echo -e "\e[32mPython3 exists with version $version\e[0m\t\e[92m【成功】\e[0m"
    fi
else
    echo -e "\e[31mPython3 does not exist\e[0m\t\e[91m【失败】\e[0m"
    exit 1
fi

# 检查python3-pip是否存在
if command -v pip3 &> /dev/null
then
    echo -e "\e[32mpip3 exists\e[0m\t\e[92m【成功】\e[0m"
else
    echo -e "\e[31mpip3 does not exist\e[0m\t\e[91m【失败】\e[0m"
    exit 1
fi

# 检查Python包
packages=("paramiko" "pexpect" "requests" "PyYAML")
for package in "${packages[@]}"; do
    pip3 show $package > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "\e[32m$package is installed.\e[0m\t\e[92m【成功】\e[0m"
    else
        echo -e "\e[31m$package is NOT installed. e.g. pip3 install $package\e[0m\t\e[91m【失败】\e[0m"
    fi
done