# tkadw

> `tkinter`扩展界面库

---

![PyPI](https://img.shields.io/pypi/v/tkadw?logo=python&logoColor=white&label=Version&labelColor=black&color=blue&link=https%3A%2F%2Ftest.pypi.org%2Fproject%2Ftkadw%2F)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tkadw?logo=python&logoColor=white&label=Support%20interpreter&labelColor=black)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/tkadw?logo=python&logoColor=white&label=Support%20wheel&labelColor=black&color=blue)
![PyPI - License](https://img.shields.io/pypi/l/tkadw?logo=python&logoColor=white&label=License&labelColor=black&color=blue)
---

使用[`tkinter.Canvas`](https://tkdocs.com/tutorial/canvas.html)、[`tcltk`](https://wiki.tcl-lang.org/)扩展自绘技术实现的扩展界面

> - `轻量`
>> 仅用`python`代码实现，不掺杂大型数据文件
> - `支持圆角`
>> 运用`DrawEngine`引擎快速画出圆角矩形
> - `跨平台`
>> `tkinter.Canvas`的跨平台性
> - `主题系统`
>>  新版加入了`tkadw.theme`模块，可快速制作主题和快速使用主题


## 简介
使用`tkinter.Canvas`自绘的界面库
项目是从2023年6月放假那段时间开始


## 作者
一个初中生（绝对不是出生），十分热爱tkinter，完全是自学出来的

> QQ
>> 1379773753

> E-Mail
>> XiangQinxi@outlook.com
> 
>> 1379773753@qq.com
        


## 安装
安装使用的途径仅在`pypi.org`平台上，所以可以直接使用`pip`
```bash
python -m pip install -U tkadw4
```
`Requirement already satisfied: tkadw in $pythonpath\lib\site-packages`

对于`windows`平台，安装时需勾选`tcl/tk`选项安装`tkinter`

对于`linux`平台，需自行查询`python3-tk`的安装步骤


## 编译
此项目使用[`poetry`](https://python-poetry.org/docs/)包管理，所以先安装[`poetry`](https://python-poetry.org/docs/)
```bash
pip install poetry
```
编译
```bash
poetry build
```

## 更新记录
> `<=0.2.0`:
>> 作者都没记下来

> `0.2.0`:
>> `201`主题配置
> 
>> `202`改变修复`AdwDrawEntry`的`Entry`组件在`Linux`平台下出现边框
> 
>> `203`修复各别解释器类似注释的错误

> `0.2.1`
>> `211`扩充README文档
>
>> `212`新增组件`Adw`
> 
>> `213`删除多余文件

> `0.2.2` 
>> `221`扩展额外界面库`BiliBili`，根据`BiliBili桌面版`设计
> 
>> `222`修复`palette`修改完后没完全修改配色的问题
> 
>> `223`扩展额外界面库`Win11`，根据`Sunvalley`设计
> 
>> `224`修复`AdwDrawButton`类边框遮挡的问题

> `0.2.3`
>> `231` `AdwDrawEngine`添加绘画渐变图形的方法
> 
>> `232`扩展额外界面库`Fluent`，作者制作设计

> `0.2.4`
>> `241`补充导入

> `0.3.0`
>> `301`新增`AdwSeparator`分割线组件 新增`AdwWidget`简化组件绘制流程
> 
>> `302`分支`widgets`库，将加入仅使用组件组合起来的控件，而非用canvas绘出来的组件
> 
>> `303`调改`AdwDrawEntry`和`AdwDrawText`的焦点事件绑定
> 
>> `304`新增主题类组件，只需使用`set_default_theme`设置主题。对于经过特殊设计和特殊样式的组件，比如`Fluent`主题组件、`Win11`主题控件`AccentButton`，将不加入主题变量内

> `0.3.2`
>> `321` 新增`AdwMDI`组件
> 
>> `322` 添加`metro`主题

> `0.3.3`
>> `331` 修复`AdwDrawFrame`的边框宽度问题
> 
>> `332` 增加主题属性`AdwDrawFrame` `padding`

> `0.3.4`
>> `341` 为`AdwTButton`增添新样式`win11_accent_light` `win11_accent_dark`

> `0.3.5`
>> `351`补充`AdwTCircularButton`主题组件
> 
>> `352`增添新快速布局`row`、`coloumn`以及高级布局`put`，所有可视化组件已继承布局类。

> `0.3.6`
>> `361` 添加`AdwDragArea`控件，快速制作标题栏

> `0.3.7`
>> 发布包时有些小问题，内容与`361`一样

> `0.3.8`
>> `381`修改示例，添加获取`tkadw版本号`方法`get_version()`

> `0.3.9`
>> `391`添加`pypi`官网设计主题
> 
>> `392`准备着手制作设计器，添加组件AdwDesignerFrame

> `0.4.0`
>> `401`新增`AdwListBox`组件，并也加入主题组件中
>
>> `402`补充`pypi`暗色主题
> 
>> `403`新增`AdwStack`组件，并也加入主题组件中

> `0.4.1`
>> `411`补充`AdwToplevel`，主题组件`Adwitew`

> `0.4.2`
>> `421`添加`AdwTTabs`未加入基础组件仅在主题组件中可用

> `0.4.3`
>> `431`添加`<<SystemSwitchTheme>>`绑定（前提是解释器安装了darkdetect）
>
>> `432`如果安装了`tkadw-material`库，将会自动导入
>
>> `433`修复`AdwRun().run()`无法关闭的错误
> 
>> `434`补充`Adw`修改窗口样式的功能（窗口标题栏颜色仅限Windows），后续将补充其它方法，现在懒得动

> `0.4.4`
>> `441` `Adw`不会自动刷新窗口以修改窗口

> `0.4.5`
>> `451` 添加基于`tkinterflow`的布局`flow`

> `0.4.6`
>> `461` 修复`AdwListBox`圆角无法正常设置的问题
> 
>> `462` 简化主题组件主题化
> 
>> `463` 修改`AdwMDI`样式
> 
>> `464` 尝试制作`pygubu`插件 *可惜文档太少，并且教程太老了，很难继续实现*

> `0.4.7` - `0.4.9`
>> `471` 为了让代码更加整洁，Windows平台下的高级窗口选项已变为`pywinstyles`功能库方法
> 
>> `472` 全新的主题设置，将主题的浅色主题和深色主题合在一起，修改只需要改`default_theme_mode`即可
> 
>> `473` 添加`Adw.style_dark`的`macos`支持
> 
>> `474` `Windows`平台下默认开启`High DPI`

> `0.5.0`
>> `501` 完全重做（不过还是有些地方是借鉴以前的代码）
> 
>> `502` 将`0.4.x`版本的库保留并更名为`tkadw4`，您仍能使用旧版，但是旧版将不在被更新和维护
> 
>> `503`增加新可视化组件`AdwTitleBar`、`AdwMenuBar`、`AdwSizegrip`