#!/bin/bash
echo PyCxHelper Termux 依赖安装脚本
echo 正在安装系统依赖
pkg install -y git python clang libxml2 libiconv libxslt
echo 克隆项目
rm -rf pycxclient
git clone https://github.com/greats3an/pycxclient

echo 正在安装 pip 依赖
cd pycxclient
python -m pip install --user -U -r requirements.txt

echo 安装完毕
echo 您可以运行 python pycxclient/main.py 了
