# pycxclient
Python 实现的超星网课客户端

# 使用
	python main.py

# 说明
本工具旨在利用 [超星【学习通】](http://www.chaoxing.com/ "超星【学习通】") Web端的API,以 Python 作为前端进行操作；且通过对Web端的逆向发掘出一些正常使用不能主动触发的API

# 功能
- 获取下载链接
- 视频项目
- - 获取封面
- - 下载为MP3
- - 设置观看时长（伪装正常观看）
- 文档项目
- - 一键设置考核点（任务点）

# TODO
- 实现通知拉取
- 实现 PM 推拉
- 签到功能
- 弄个 GUI ？
- 集成下载逻辑 （Aria2 ?）
- 自动识别 Captcha （Tesseract ？）

# Need some help here!
目前为止，所有的逆向工作都是基于Web端进行；而移动端的一些常用的API则无缘发掘；若各位有方法对 Android / iOS 设备的学习通 App 抓包或逆向，欢迎指点迷津🙏

e-mail : greats3an@gmail.com