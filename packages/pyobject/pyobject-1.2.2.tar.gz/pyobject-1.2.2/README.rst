pyobject - 一个提供操作Python底层对象工具的Python包, 包含一些子模块。A tool of operating internal python object with some various submodules.

所包含模块 Included modules: 
============================

__init__ - 打印出Python对象的各个属性

pyobject.browser - 以图形方式浏览Python对象

pyobject.code\_ - Python bytecode的操作工具

pyobject.search - 搜索python对象

pyobject.newtypes - 定义一些新的类型

pyobj_extension(新增) - 操作Python底层对象引用, 以及对象指针的模块, 使用C语言编写

包含的函数 Functions:
=====================

describe(obj, level=0, maxlevel=1, tab=4, verbose=False, file=sys.stdout, mode='w' encoding='utf-8')::

    "描述"一个对象,即打印出对象的各个属性。
    参数说明:
    maxlevel:打印对象属性的层数。
    tab:缩进的空格数,默认为4。
    verbose:一个布尔值,是否打印出对象的特殊方法(如__init__)。
    file:一个类似文件的对象。

browse(object, verbose=False, name='obj')::

    以图形方式浏览一个Python对象。
    verbose:与describe相同,是否打印出对象的特殊方法(如__init__)

objectname(obj)::

    objectname(obj) - 返回一个对象的名称,形如xxmodule.xxclass。
    如:objectname(int) -> 'builtins.int'

bases(obj, level=0, tab=4)::

    bases(obj) - 打印出该对象的基类
    tab:缩进的空格数,默认为4。

新增函数 New Functions:
=======================

make_list(start_obj, recursions=2, all=False)::

    创建一个对象的列表, 列表中无重复的对象。
    start:开始搜索的对象
    recursion:递归次数
    all:是否将对象的特殊属性(如__init__)加入列表

make_iter(start_obj, recursions=2, all=False)::

    功能、参数与make_list相同, 但创建迭代器, 且迭代器中可能有重复的对象。

search(obj, start, recursions=3)::

    从一个起点开始搜索对象
    obj:待搜索的对象
    start:起点对象
    recursion:递归次数

新增类: ``pyobject.newtypes.Code``
==================================

用法\: (下面的示例是从doctest中摘取的)::

    >>> def f():print("Hello")
    >>> c=Code.fromfunc(f)
    >>> c.co_consts
    (None, 'Hello')
    >>> c.co_consts=(None, 'Hello World!')
    >>> c.exec()
    Hello World!
    >>>
    >>> import os,pickle
    >>> temp=os.getenv('temp')
    >>> with open(os.path.join(temp,"temp.pkl"),'wb') as f:
    ...     pickle.dump(c,f)
    ... 
    >>> f=open(os.path.join(temp,"temp.pkl"),'rb')
    >>> pickle.load(f).to_func()()
    Hello World!
    >>> 
    >>> c.to_pycfile(os.path.join(temp,"temppyc.pyc"))
    >>> sys.path.append(temp)
    >>> import temppyc
    Hello World!
    >>> Code.from_pycfile(os.path.join(temp,"temppyc.pyc")).exec()
    Hello World!


新增模块: ``pyobj_extension`` 
=============================

本模块使用了C语言编写。可直接使用import pyobj_extension, 导入该独立模块。其中包含的函数如下:

convptr(pointer)::

    将整数指针转换为Python对象，与id()相反。
	Convert a integer pointer to a Python object,as a reverse of id().

py_decref(object,n)::

	将对象的引用计数减小n。Decrease the reference count of an object for n.

py_incref(object,n)::

    将对象的引用计数增加n。Increase the reference count of an object for n.

*警告: 不恰当地使用上述3个函数可能导致Python崩溃。*

*Warning:improper using of three functions above may cause Python to crash.*

版本:1.2.2

更新日志: 

2022-7-25(v1.2.2):增加了操作Python底层对象引用, 以及对象指针的C语言模块pyobj_extension。

2022-2-2(v1.2.0):修复了一些bug,优化了search类的性能; pyobject.code_中增加了Code类,browser中增加编辑属性功能, 增加了Code类的测试。

源码:见 https://github.com/qfcy/Python/tree/main/pyobject

作者 Author: 七分诚意 qq:3076711200

作者CSDN主页: https://blog.csdn.net/qfcy\_/