# 安装 Python3
* 本系列课程基于 Python3.9，如果你想要其它的版本也是完全可以的，到官网去下载你想要的版本即可。

## 在 Windows 上安装 Python3.9

* 此教程演示使用的是 64位 Windows10 系统，Windows 7 系统操作也是一样的。

到 [官网](https://www.python.org/downloads/windows/) 去下载 Python3.9 Windows 安装包，可以看到当前最新稳定版是 Python3.9.5。
<img src="/images/0002-download-windows-python.png" align=center />

然后页面滑倒最下面，选择 **Recommended** 那一栏，点击下载。

<img src="/images/0002-python-windows-install.png" align=center />

官网给出的 Python3.9 下载地址在这里（[点此可直接下载](https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe)）。

如果官网无法访问，这里提供一个百度网盘的下载地址。[链接](https://pan.baidu.com/s/13ORuYuKb9GHh6GVgC0x_Fw): https://pan.baidu.com/s/13ORuYuKb9GHh6GVgC0x_Fw  密码: tsok

下载完成之后你会得到一个安装包。

<img src="/images/0002-python-windows-01.png" align=center />

双击这个安装包文件，会出现如下的界面

<img src="/images/0002-python-04.png" align=center />

选择 Customize installation （自定义安装），会出现如下的界面，确保下图中勾选的内容都被打上了勾。

<img src="/images/0002-python-02.png" align=center />

然后点击 Next（下一步），会出现如下的界面

<img src="/images/0002-python-03.png" align=center />

确保图中勾选的内容都被打上了勾，特别是 Add Python to environment variables 一定要被勾选上。安装路径可以任意选择，只要路径中没有中文名称就行。

然后点击 Install，等待一会儿，安装程序自动退出就好。

* **确定自己的 Python 已经被正确安装**

按下 Win 键，如图

<img src="/images/0002-Win 键.png" align=center />

会出现如下的界面，输入 `cmd`, 出现如下的界面
<img src="/images/0002-windows-cmd.png" align=center />

按下 enter （回车）键，就可以弹出命令提示符窗口，输入 `python`，弹出正确的版本信息，说明 python 已经安装成功.

<img src="/images/0002-cmd-01.png" align=center />


输入  `exit()`，退出交互式界面， 输入 `pip -V`，弹出有关 pip 的版本信息，说明 pip 也安装成功了。

<img src="/images/0002-cmd-pip.png" align=center />

我们使用安装一个包，来体验一下 pip。
输入命令 `pip install ipython  -i https://pypi.doubanio.com/simple` 来安装 ipython 包，安装完成之后，在命令行输入 `ipython`，即可进 ipython 交互环境。

<img src="/images/0002-cmd-ipython.png" align=center />

至此，在 Windows 下安装 Python 就大功告成啦！

## 在 Mac 上安装 Python3.9 

到[官网](https://www.python.org/downloads/mac-osx/)下载 Python3.9 macOS 安装包，目前最新稳定版本是 Python3.9.5。
<img src="/images/0002-macOS-python-download.png" align=center />

然后页面滑倒最下面，选择 **Mac OS X** 那一栏，点击下载。

<img src="/images/0002-macOS-python-install.png" align=center />

官网给出的 Python3.9 下载地址在这里（[点此可直接下载](https://www.python.org/ftp/python/3.9.5/python-3.9.5-macos11.pkg)）。

如果官网无法访问，这里提供一个百度网盘的下载地址。[链接](https://pan.baidu.com/s/1cRdXDs4Arb0HBAO7ej_48g): https://pan.baidu.com/s/1cRdXDs4Arb0HBAO7ej_48g  密码: 9mg3

下载完成之后你会得到一个安装包。

下载完成之后，会有一个后缀为 pkg 的文件，如图

<img src="/images/0002-macOS-01.png" align=center />

双击这个文件，进入如下界面

<img src="/images/0002-mac-install-02.png" align=center />

然后一路选择 continue (下一步)即可，等待安装完成。

* **确定自己的 Python 已经被正确安装**


安装完成之后，按下 Mac 上的 Command + Space 键，调出聚焦搜索，输入 `terminal`，回车，调出命令行。

<img src="/images/0002-terminal.png" align=center />

调出的命令行界面是这样的（你的界面和我的可能有些许不同，没有关系）。
输入 `python3.9`，如果弹出对应的 python 版本，说明安装成功。
输入 exit()，退出交互式界面， 输入 `pip3 -V`，弹出有关 pip3 的版本信息，说明 pip3 也安装成功了。

<img src="/images/0002-mac-02.png" align=center />

我们使用安装一个包，来体验一下 pip。
输入命令 `pip3 install ipython  -i https://pypi.doubanio.com/simple` 来安装 ipython 包，安装完成之后，在命令行输入 `ipython`，即可进 ipython 交互环境。

<img src="/images/0002-install-ipython.png" align=center />

至此，在 Mac 下安装 Python 就**大功告成啦！**

## 总结

本文主要介绍了如何在 Windows10 和 macOS 上安装 Python3.9，如何验证 Python 和 pip 都已经正确安装。这些是以后学习 Python 的基础，需要确保都成功执行。

如果有任何问题，可以到 [这里](https://github.com/ruicore/python/discussions) 留言，你也可以通过 `WebRuiCore` 找到我。


<p >
  <p align="left"><a href="README.md">上一课：Python3 介绍</a></p> 
  <p align="right"><a href="第002课：与 Python3 交互.md">下一课：与 Python3 交互</a></p> 
</p>