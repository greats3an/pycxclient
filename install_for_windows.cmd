@echo off
echo PyCxHelper Windows ������װ�ű�
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
echo �ļ���ȫ���뽫����Ŀ��ȫ Clone:
echo.
echo (git clone --recursive https://github.com/greats3an/pycxclient)
echo.
echo �������غ���ȫ��ѹ��ͬʱ���ر���Ŀ���е� submodule
echo.
echo ��� README.md
echo.
goto done

:nopython
echo δ��װ Python
echo.
echo ��ǰ�� python.org ���� 3.x �汾
echo.
goto done

:install
echo ��װ������...
echo.
python -m pip install --user -U -r requirements.txt
goto done

:done
echo .
pause