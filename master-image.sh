#!/bin/bash

check_command_exists() {
    command -v "$1" &> /dev/null
    if [ $? -ne 0 ]; then
        echo "错误：$1 命令未找到，请确保已安装。"
        return 1
    fi
    return 0
}

import_image() {
    local tool=$1
    local image=$2
    if [ -f "$image" ]; then
        case "$tool" in
            "docker")
                docker load -i "$image"
                ;;
            "ctr")
                ctr -n k8s.io image import "$image"
                ;;
            "podman")
                podman load -i "$image"
                ;;
            *)
                echo "不支持的工具: $tool"
                return 1
                ;;
        esac
        if [ $? -eq 0 ]; then
            echo "$image 导入成功."
        else
            echo "$image 导入失败."
        fi
    else
        echo "文件 $image 未找到."
    fi
}

delete_image() {
    local tool=$1
    local image_id=$2
    case "$tool" in
        "docker")
            if docker inspect "$image_id" &> /dev/null; then
                docker rmi "$image_id"
                if [ $? -eq 0 ]; then
                    echo "镜像 $image_id 删除成功."
                else
                    echo "镜像 $image_id 删除失败."
                fi
            else
                echo "镜像 $image_id 不存在，跳过删除."
            fi
            ;;
        "ctr")
            if ctr -n k8s.io image ls | grep -q "$image_id"; then
                ctr -n k8s.io image rm "$image_id"
                if [ $? -eq 0 ]; then
                    echo "镜像 $image_id 删除成功."
                else
                    echo "镜像 $image_id 删除失败."
                fi
            else
                echo "镜像 $image_id 不存在，跳过删除."
            fi
            ;;
        "podman")
            if podman inspect "$image_id" &> /dev/null; then
                podman rmi "$image_id"
                if [ $? -eq 0 ]; then
                    echo "镜像 $image_id 删除成功."
                else
                    echo "镜像 $image_id 删除失败."
                fi
            else
                echo "镜像 $image_id 不存在，跳过删除."
            fi
            ;;
        *)
            echo "不支持的工具: $tool"
            return 1
            ;;
    esac
}

check_environment() {
    case "$1" in
        1)
            echo "你选择了 Docker."
            if ! check_command_exists "docker"; then
                return 1
            fi
            tool="docker"
            ;;
        2)
            echo "你选择了 containerd."
            if ! check_command_exists "ctr"; then
                return 1
            fi
            tool="ctr"
            ;;
        3)
            echo "你选择了 podman."
            if ! check_command_exists "podman"; then
                return 1
            fi
            tool="podman"
            ;;
        *)
            echo "无效的选择，请输入 1、2或3."
            return 1
            ;;
    esac

    echo "请选择操作: "
    echo "1) 导入镜像"
    echo "2) 删除镜像"
    while true; do
        read -p "请输入操作编号 (1 或 2): " action
        if [[ "$action" =~ ^[1-2]$ ]]; then
            break
        else
            echo "无效的操作编号，请输入 1 或 2."
        fi
    done

    case "$action" in
        1)
            import_image "$tool" "worker.tar"
            ;;
        2)
            delete_image "$tool" "core.harbor.safedog.site/armorpoc20240512/armor_poc_worker:latest"
            ;;
    esac
    return 0
}

while true; do
    echo "请选择需要导入的环境:"
    echo "1) Docker"
    echo "2) Containerd"
    echo "3) Podman"
    while true; do
        read -p "请输入环境编号 (1, 2 或 3): " env_choice
        if [[ "$env_choice" =~ ^[1-3]$ ]]; then
            break
        else
            echo "无效的环境编号，请输入 1, 2 或 3."
        fi
    done

    check_environment "$env_choice"
    if [ $? -eq 0 ]; then
        break  # 如果输入有效，退出循环
    fi
done

echo "已处理 $env_choice 镜像操作."
