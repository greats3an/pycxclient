@echo off
pyinstaller -F --add-data "%cd%\;." main.py
del main.exe
copy dist\main.exe main.exe
REM Cleanups.
rmdir dist /S /Q
rmdir build /S /Q
rmdir __pycache__ /S /Q
del *.spec