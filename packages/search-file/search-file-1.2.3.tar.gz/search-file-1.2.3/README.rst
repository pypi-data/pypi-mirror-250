search-file - *A python module that supplies tools to search files(or folders).*
一个用于搜索文件或文件夹的Python模块。

:包含的函数 FUNCTIONS:

:directories(path):

- 一个生成器, 列出path下的所有子目录和文件名。
- 如:

.. code-block:: python

    >>> from search_file import directories
    >>> list(directories("C:"))
    ['C:\Users',  #第一层目录
    'C:\\\\Users\\\\Administrator', #第二层目录
    ...,
    'C:\Windows',
    'C:\\\\Windows\\\\System32',
    ...]

dirs: 是否列出目录
files: 是否列出文件

:search(filename,path,minsize=0,maxsize=None):

- 一个生成器,在path中搜索一个文件或文件夹。
- 如:

.. code-block:: python

    >>> from search_file import search
    >>> list(search("cmd.exe","C:"))
    ['C:\\\\Windows\\\\System32\\\\cmd.exe',
    ...]

:版本 VERSION:

 1.2.3

源代码:https://github.com/qfcy/Python/blob/main/search_file.py

最近更新(2022-2):增加了多个测试程序。

作者:*七分诚意 qq:3076711200* 百度贴吧账号:qfcy\_

作者CSDN主页: https://blog.csdn.net/qfcy\_/