@echo off
echo PyCxHelper Windows 依赖安装脚本
if exist requirements.txt (
    python -V >nul
    if %errorlevel% equ 0 (
        echo 安装依赖项
        python -m pip install --user -U -r requirements.txt
    ) else (
        echo 未安装 Python
        echo 请前往 python.org 下载 3.x 版本
    )
) else (
    echo 文件不全：请将本项目完全 Clone 
    echo 或打包下载后完全解压
)
pause