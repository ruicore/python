# Python 解释器

这篇文章主要讲一下有关 Python 解释器的内容（如果你暂时对 Python 解释没有兴趣，可以跳过这篇文章。跳过此文章对阅读后面的内容没有影响）。

## 机器语言

在说 Python 的解释器之前，必须先说一下机器语言。

我们人类之间通过语言进行交流，咱们中国人之间相互说中文，相互能理解，因为我们听得懂中文，能理解中文。

英国人之间相互说英语，也能相互理解，因为他们都能听懂英文。

那计算机听得懂什么呢？我们把计算机能听得懂的语言称为「机器语言」。

机器语言不是中文，也不是英语，所以你给计算机说中文，说英文，它是听不懂的。想要计算机能理解你的意思，就必须给它说它能理解的「机器语言」。

## 解释器解释什么

我们写的代码（源文件），称为高级语言，人类能够理解，但是机器不能。

想要机器能理解我们的语言，就需要一个翻译者，来将「高级语言」翻译成「机器语言」。**解释器**就承担了这一样一个翻译者的角色。

本质上 Python 是一门先**编译**，再**解释**的语言。这里的编译和解释都是翻译，说的通俗一点就是把一种语言变成另一种语言。

**编译**：把我们写的源代码变成字节码（ByteCode）
**解释**：将解释后的字节码翻译成机器码（MachineCode）

<img src="/images/0003-01.png" align=center />

也就是说 **Python 解释器 = 编译器 + 虚拟机**

**编译器**：将 Python 代码编译成 ByteCode
**虚拟机**：将 ByteCode 解释成机器码

因此 Python 被称为解释型语言并不是因为解释运行 Python 代码，而是解释运行 ByteCode。

## pyc 文件

我们写的代码文件以 <code>.py</code> 结尾，你以后还会发现 <code>.pyc</code> 结尾的文件，这就是编译的结果。

假设我们现在有一个 Python 代码文件 <code>code.py</code>。

* 我们直接运行 <code>python code.py</code> 并不会生成 <code>code.pyc</code> 文件。
>
* 如果这个代码中引入了别的模块，如 `urllib`，那么 python 会为 `urllib.py` 保存编译生成的字节码文件，生成 `urllib.pyc`。
>
* 我就是想要生成一个 <code>code.pyc</code> 文件可以吗？ 当然可以，使用命令 `python -m py_compile code.py` 就会生成 <code>code.pyc</code> 文件。

在加载模块的时候，如果同时存在 `.py` 和 `.pyc ` 文件，python 会比较 `.pyc ` 的编译时间和 `.py` 的最后修改时间。

如果 `.pyc ` 的编译时间更晚，那么 python 就会使用 `.pyc ` 文件。否则 python 会重新编译 `.py` 文件并更新 `.pyc ` 文件。

>
> 小知识点
> 
> * 命令 `python -m py_compile code.py` ，因为安装的是 python3 的版本，所以如果执行命令报错，可以尝试`python3 -m py_compile code.py`。
> >
> * `-m` 的含义以导入模块（module）

## 常见的 Python 解释器

* **Cpython**

这是最常见，也是最常用的 python 解释器。

当我们从官网下载安装好了 Python 之后，就会默认安装 CPython 解释器，这是官方在维护的解释器。因为这个解释器是用 C 语言开发的，所以叫 CPython。

上节课中的与 Python 交互中，默认使用的就是 CPython。

* **IPython**

IPython 是基于 CPython 写的一个增强型交互式解释器。也是说，IPython 仅仅是在交互体验上进行了增强，从执行代码功能的角度而言，与 CPython 是完全一样的。

* **PyPy**

PyPy 是 Python 的另一个比较出名的解释器，它看中的是执行速度。使用 JIT 技术，对 Python 代码进行动态编译，能够显著的提高 Python 代码的执行速度。

需要特别注意的是，不是所有能在 CPython 下运行的代码都能够在 PyPy 下运行「虽然绝大部分都是可以的」，会出现同样的代码跑出不同结果的现象。

* **Jython**

Jython 是运行在 Java 平台上的 Python 解释器，能够直接把 Python 代码编译成 Java 字节码（ByteCode） 进行执行。

* **IronPython**

IronPython 是运行在微软 .Net 平台上的解释器，可以把 Python 代码编译成 .Net 字节码。


## 总结

这篇文章主要讲解了有关 Python 解释器的内容。Python 是一门先编译，再解释的语言。Python 的解释器实际上承担了 编译+ 解释的功能。

Python 有多种解释器，最常用的还是 CPython 解释器，这是用 C 语言编写的，官方维护的解释器。

<p >
  <p align="left"> <a href="第002课：与 Python3 交互.md"> 上一课：与 Python3 交互 </a></p> 
  <p align="right"><a href="第004课：第一个 Python 程序.md"> 下一课：第一个 Python 程序 </a></p> 
</p>