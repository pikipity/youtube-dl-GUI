youtube-dl GUI
==============

这是用 Tkiter 为 youtube-dl 做的一个 GUI，youtube-dl 是用 Python 语言写成的用来下载网站视频的软件，可以在 Unix、Windows 和 Mac OS X 上运行，其官方网站在[这里](http://rg3.github.io/youtube-dl/)。

此 GUI 仅可用于 OSX，在 Linux 上使用时，"Open in the finder" 按钮无法使用。

### 安装

点击[这里](https://github.com/pikipity/youtube-dl-GUI/archive/master.zip)下载，下载完成后解压，在解压目录下打开终端，输入下面命令即可运行

    python ./main.py

如果发现无法正常下载，请在解压目录下打开终端，用下面的命令给予 youtube-dl 权限：

    sudo chmod a+x ./youtube-dl

### 使用说明

软件分为两大部分：左侧为控制区，右侧为下载任务管理区。使用时，先在"Download Path"中填写或选择视频保存路径，然后在"Download URL"中填写或粘贴视频所在的网址，"Options"处可以选择下载控制选项，不熟悉的话可以不用填写。然后下载就可以了。

下载过程中，左侧控制区下方会显示下载信息，右侧任务管理区会显示出各个任务的实时情况。

只可以删除已经完成或是出错的任务，进行中的任务无法删除。删除时，先选定任务，再按"Delete Task"按钮。

如果想在finder中打开某个任务，先选定一个任务，载按"Open in the finder"。如果无任务选中，将打开"Download Path"中填写的地址。

### 支持网站

经测试 Youku、土豆和Youtube 下载正常，其他网站没有测试，理论上，youtube-dl支持的网站此GUI应全部支持。

youtube-dl支持的视频网站请到[官网说明文档](http://rg3.github.io/youtube-dl/documentation.html)查询

### 软件截图：

![下载中](https://lh3.googleusercontent.com/-rkDZUJACtqo/UhmniKahR7I/AAAAAAAABHM/iwtIZ9ZXXuo/s640/%25E5%25B1%258F%25E5%25B9%2595%25E5%25BF%25AB%25E7%2585%25A7%25202013-08-25%2520%25E4%25B8%258B%25E5%258D%25882.34.08.png)

![选择 Options](https://lh3.googleusercontent.com/-ZNcrGbCx18M/UhmniTT8BYI/AAAAAAAABHQ/ig4RsA_k8OM/s640/%25E5%25B1%258F%25E5%25B9%2595%25E5%25BF%25AB%25E7%2585%25A7%25202013-08-25%2520%25E4%25B8%258B%25E5%258D%25882.34.31.png)
