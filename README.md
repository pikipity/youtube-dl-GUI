youtube-dl GUI
==============

这是用 Tkiter 为 youtube-dl 做的一个 GUI，youtube-dl 是用 Python 语言写成的用来下载网站视频的软件，可以在 Unix、Windows 和 Mac OS X 上运行，其官方网站在[这里](http://rg3.github.io/youtube-dl/)。

此 GUI 仅使用其基本的下载功能，由于尚未添加下载任务管理功能，所以限定一次只能下载一个视频。

仅在 OSX 上测试通过，尚未在 Windows 上测试。如果在 OSX 上发现无法使用，请先在终端下移动到此软件的安装目录下，用下面的命令给予 youtube-dl 权限：

    sudo chmod a+x 安装目录/youtube-dl
    
支持的视频网站及问题请到[官网说明文档](http://rg3.github.io/youtube-dl/documentation.html)查询
