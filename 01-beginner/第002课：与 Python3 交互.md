# 与 Python3 交互

本文主要讲解如何与 Python 进行交互并编写第一个 Python 程序。

* 交互式环境：我们输入代码，按下回车，**代码马上就会被执行**。如果代码正确，我们就会看到返回的结果。如果代码不正确，就会抛出对应的异常。
* 写代码也是一个需要手感的活儿，下面的以 `>>>` 开头的代码，建议都不要复制粘贴，而是老老实实的手敲，这样才能提升写代码的能力。

## 在 Windows10 上与 Python 进行交互

按下 `Win` 键盘，输入 `cmd`，打开 `命令提示符`，如下图
<img src="/images/0002-windows-cmd.png" align=center />

输入 `python`，即可进入 Python 交互式环境。如果你还没有安装 Python ，可以查看这一篇文章 <a href="第001课：如何安装 Python3.md">如何安装 Python3</a>。

进入交互式环境是这样的
<img src="/images/0002-cmd-01.png" align=center />

接下来我们输入一些代码，看看会有什么效果，符号 `>>>` 开头的表示这一行是代码，否则表示这一行是结果。

让我们来看看 2 + 2 等于多少，

```shell
>>> 2 + 2
4
```

3.14 * 3.14 呢？

```shell
>>> 3.14 * 3.14
9.8596
```
<img src="/images/0003-python-shell.png" align=center />

上面我们使用 python 自带的交互工具进行交互，而 ipython 提供了更为强大的交互功能，它支持高亮、变量提示、自动缩进、内置很多有用的函数。让我们来试一试吧。

首先使用 `exit()` 命令来退出 python 默认的交互环境。然后使用命令 `pip install ipython  -i https://pypi.doubanio.com/simple` 安装 ipython。

<img src="/images/0003-window-ipython-01.png" align=center />

输入 `ipython` ，即可进入 ipython 的交互式界面，让我们来看看在 ipython 中运行命令是什么样的。

<img src="/images/0003-windows-ipython-03.png" align=center />

看到了吗？相比于自带的 python 交互环境，ipython 里面的内容有了颜色高亮，而且还有输入`In` 和 `Out` 输出的提示。

我们输入 `pr`，再按下 `Tab` 键，看看会有什么效果：

<img src="/images/0003-windows-ipython-04.png" align=center />

看到了吗？出现了提示，提示的内容里面都是含有 `pr` 这个字母的，按下键盘的`下方向键`，然后再按右键，就可以在提示的选项里面进行选择，最后按下 `enter` 键确认自己的选项。

ipython 的功能更加丰富，也更强大，如无说明，后面文章中所有与 Python 交互的交互式环境，都默认使用 ipython。

交互式环境及时响应，能够让我们马上看到命令的结果，但是我们关掉交互环境之后，代码就没有了。

而且交互环境下的代码没有办法从一个环境移植到另一个环境使用，因此，我们就需要另一种方式，能够将代码保存下来，可以方便我们二次使用。

这种方式就是 python 代码文件。

**文本编辑器 Visual Studio Code**

工欲善其事，必先利其器。

说到文本编辑，不得不说到 Visual Studio Code（VS Code），VS Code 是微软开发的，能够在 Windows 和 macOS 上运行的代码编辑器。支持语法高亮，自动补全，代码调试，其丰富的插件也让 VS Code 的功能如虎添翼。非常建议大家使用 VS Code 来编写 Python 代码。

你可以在 [这里](https://code.visualstudio.com/sha/download?build=stable&os=win32-user) 下载 VsCode 的 Windows 版本，下载之后像安装普通的软件一样就好。

如果访问官网的下载速度比较慢，这里提供百度网盘的下载方式：[链接](https://pan.baidu.com/s/1usPAxDQGIGdKbXM9Xw_2Fw): https://pan.baidu.com/s/1usPAxDQGIGdKbXM9Xw_2Fw  密码: jolo

打开 VS Code，点击图中箭头指向的图标，你会看到如下的界面
<img src="/images/0003-vs-code-windows.png" align=center />

然后点击 `Open Folder`，会进入到 Windows 自带的文件夹选择页面，我们进入桌面，然后点击鼠标右键，在这里创建一个名为 `learnpython` 的文件夹（你的界面或许和我有些许不同，没有关系，能创建文件夹就行）
<img src="/images/0003-vscode-windows-01.png" align=center />

然后我们选中刚刚创建的文件夹，点击 `选择文件夹`，就能打开刚刚创建的文件夹
<img src="/images/0003-vscode-windows-03.png" align=center />

然后我们进入下面的页面，点击图中箭头所指向的位置，新建一个名叫 `hello.py` 的文件。
<img src="/images/0003-vscode-04.png" align=center />

新建完成之后，现在的 vscode 是这样的

<img src="/images/0003-vscode-05.png" align=center />

然后在文件里输入 `print('hello wrold!')`，按下 `Ctl` + `S` 进行保存，
然后把输入法切换到英文状态，按下 `Ctl` +  <code> `</code> ,调出命令行工具，输入 <code>python hello.py </code> 即可运行程序。

<img src="/images/0003-vscode-06.png" align=center />

至此，我们的第一个 Python 程序就成功的运行啦，是不是很有成就感 😘 ～～～

## 在 macOS 上与 Python 进行交互

按下 Mac 上的 Command + Space 键，调出聚焦搜索，输入 `terminal`，回车，调出命令行。
<img src="/images/0002-terminal.png" align=center />
调出的命令行界面是这样的（你的界面和我的可能有些许不同，没有关系）。

输入 `python3`，即可进入 Python 交互式环境。如果你还没有安装 Python ，可以查看这一篇文章 <a href="第001课：如何安装 Python3.md">如何安装 Python3</a>。

进入交互式环境是这样的
<img src="/images/0003-macos-01.png" align=center />

接下来我们输入一些代码，看看会有什么效果，符号 `>>>` 开头的表示这一行是代码，否则表示这一行是结果。

让我们来看看 2 + 2 等于多少，

```shell
>>> 2 + 2
4
```

3.14 * 3.14 呢？

```shell
>>> 3.14 * 3.14
9.8596
```
<img src="/images/0003-macos-02.png" align=center />

上面我们使用 python3 自带的交互工具进行交互，而 ipython 提供了更为强大的交互功能，它支持高亮、变量提示、自动缩进、内置很多有用的函数。让我们来试一试吧。

首先使用 `exit()` 命令来退出 python3 默认的交互环境。然后使用命令 `pip3 install ipython  -i https://pypi.doubanio.com/simple` 安装 ipython。

<img src="/images/0003-macos-03.png" align=center />

输入 `ipython` ，即可进入 ipython 的交互式界面，让我们来看看在 ipython 中运行命令是什么样的。

<img src="/images/0003-macos-04.png" align=center />

看到了吗？相比于自带的 python 交互环境，ipython 里面的内容有了颜色高亮，而且还有输入`In` 和 `Out` 输出的提示。

我们输入 `pr`，再按下 `Tab` 键，看看会有什么效果：

<img src="/images/0003-macos-05.png" align=center />

看到了吗？出现了提示，提示的内容里面都是含有 `pr` 这个字母的，按下键盘的`下方向键`，然后再按`右键`，就可以在提示的选项里面进行选择，最后按下 `enter` 键确认自己的选项。

ipython 的功能更加丰富，也更强大，如无说明，后面文章中所有与 Python 交互的交互式环境，都默认使用 ipython。

交互式环境及时响应，能够让我们马上看到命令的结果，但是我们关掉交互环境之后，代码就没有了。

而且交互环境下的代码没有办法从一个环境移植到另一个环境使用，因此，我们就需要另一种方式，能够将代码保存下来，可以方便我们二次使用。

这种方式就是 python 代码文件。

**文本编辑器 Visual Studio Code**

工欲善其事，必先利其器。

说到文本编辑，不得不说到 Visual Studio Code（VS Code），VS Code 是微软开发的，能够在 Windows 和 macOS 上运行的代码编辑器。支持语法高亮，自动补全，代码调试，其丰富的插件也让 VS Code 的功能如虎添翼。非常建议大家使用 VS Code 来编写 Python 代码。

你可以在 [这里](https://code.visualstudio.com/sha/download?build=stable&os=darwin-universal) 下载 VsCode 的 macOS 版本，下载之后像安装普通的软件一样就好。

如果访问官网的下载速度比较慢，这里提供百度网盘的下载方式：[链接](https://pan.baidu.com/s/1lxX-liL523bNHYVso9bFLw): https://pan.baidu.com/s/1lxX-liL523bNHYVso9bFLw  密码: 9ska

首先我们进入 macOS 的桌面，然后在这里创建一个名为 `learnpython` 的文件夹。

然后我们打开 VS Code，点击图中箭头指向的图标，你会看到如下的界面
<img src="/images/0003-macos-10.png" align=center />

然后点击 `Open Folder`，找到我们刚才在桌面创建的 `learnpython` 文件夹，

然后我们选中刚刚创建的文件夹，点击 `选择文件夹`，就能打开刚刚创建的文件夹
<img src="/images/0003-macos-07.png" align=center />

然后我们进入下面的页面，点击图中箭头所指向的位置，新建一个名叫 `hello.py` 的文件。
<img src="/images/0003-macos-08.png" align=center />

新建完成之后，在文件里输入 `print('hello wrold!')`，按下 `Ctl` + `S` 进行保存，

然后把输入法切换到英文状态，按下 `Ctl` +  <code> `</code> ,调出命令行工具，输入 <code>python3 hello.py </code> 即可运行程序。

<img src="/images/0003-macos-09.png" align=center />
至此，我们的第一个 Python 程序就成功的运行啦，是不是很有成就感 😘 ～～～

## 补充知识
* [ipython 文档](https://ddeevv.com/docs/ipython/8.0.0/)

## 总结

本文主要介绍了如何在 Windows 和 macOS 下与 Python 进行交互，如何使用 ipython ，如何编写自己的第一个 `hello.py` 程序。

由于操作方式的些许不同，针对 Windows 和 macOS 分别进行了说明。

在后续的文章中，如无特殊说明，交互式环境都将使用 `ipython`, 如果 macOS 和 Windows 操作方式不同，也会详尽的说明，力求做到简洁，易上手。

如果有任何问题，欢迎到 [这里](https://github.com/ruicore/python/discussions/10) 留言，你也可以通过微信 `WebRuiCore` 找到我。


<p >
  <p align="left"> <a href="第001课：如何安装 Python3.md"> 上一课：如何安装 Python3 </a></p> 
  <p align="right"><a href="第003课：Python 解释器.md"> 下一课：Python 解释器 </a></p> 
</p>