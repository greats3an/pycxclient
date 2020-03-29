@echo off
echo PyCxHelper Windows 依赖安装脚本
echo.
if not exist atom/__init__.py goto incomplete
if exist requirements.txt (
    python -V >nul
    if %errorlevel% equ 9009 (
        goto nopython
    ) else (
		goto install
    )
) else (
	goto incomplete
)

pause
goto done

:incomplete
echo 文件不全：请将本项目完全 Clone:
echo.
echo (git clone --recursive https://github.com/greats3an/pycxclient)
echo.
echo 或打包下载后完全解压并同时下载本项目所有的 submodule
echo.
echo 详见 README.md
echo.
goto done

:nopython
echo 未安装 Python
echo.
echo 请前往 python.org 下载 3.x 版本
echo.
goto done

:install
echo 安装依赖项...
echo.
python -m pip install --user -U -r requirements.txt
goto done

:done
echo .
pause