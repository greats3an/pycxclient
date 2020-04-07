@echo off
copy "%cd%\temp\%~nx1" "F:\Global Shared\share\captcha\"
echo 请在“验证码令牌认领”处输入该令牌:
echo %~nx1