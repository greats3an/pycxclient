# atom
Python 用 QuickTime movie Atoms 解析库

# 使用
    import atom
	file = open('meida.mp4','rb')
	header = file.read(256)
	header = atom.unpack(header)

# 说明
详见 `class ATOM` 内注释

# 功能
- MVHD 解析

# TODO
- ATOM 头写操作
- 其他 ATOM 头的操作

# 参考
[Movie Atoms - Apple](https://developer.apple.com/library/archive/documentation/QuickTime/QTFF/QTFFChap2/qtff2.html "Movie Atoms")