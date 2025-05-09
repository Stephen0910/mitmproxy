---
title: "自定义选项"
weight: 3
aliases:
  - /addons-options/
---

# 选项

mitmproxy的核心是一个全局选项存储，包含决定mitmproxy及其插件行为的设置。
选项可以从配置文件中读取，在命令行中设置，并由用户在运行时交互地更改。

所有选项都标注了一组支持类型中的一种。Mitmproxy知道如何序列化和反序列化这些类型，
并且有标准方式在交互式程序中呈现类型化值以供编辑。尝试设置错误类型的值将导致错误。
这意味着插件选项只需通过声明一个类型，就能在mitmproxy的整个工具链中得到完全支持。

## 简单示例

{{< example src="examples/addons/options-simple.py" lang="py" >}}

`load`事件接收一个`mitmproxy.addonmanager.Loader`实例，它允许插件声明选项和命令。
在这种情况下，插件添加了一个类型为`bool`的单个`addheader`选项。
让我们通过在mitmproxy控制台中运行脚本来尝试一下：

```bash
> mitmproxy -s ./examples/addons/options-simple.py
```

现在您可以使用CURL通过代理发出请求，如下所示：

```bash
> env http_proxy=http://localhost:8080 curl -I http://google.com
```

如果您立即运行此请求，您会注意到没有添加计数头。这是因为我们的选项默认值为`false`。
按`O`进入选项编辑器，并找到`addheader`选项。您会注意到mitmproxy知道这是一个布尔值，
并让您在true和false之间切换值。将值设置为`true`，您应该会看到类似这样的结果：

```bash
> env http_proxy=http://localhost:8080 curl -I http://google.com
HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
Content-Length: 219
count: 1
```

当加载此插件时，`addheader`设置在持久[YAML配置文件]({{< relref "/concepts/options" >}})中可用。
您也可以使用`--set`标志直接从任何工具的命令行覆盖该值：

```bash
mitmproxy -s ./examples/addons/options-simple.py --set addheader=true
```

## 处理配置更新

有时，仅从事件中测试选项的值是不够的。相反，我们希望在用户更改选项时立即作出反应。
这就是`configure`事件的作用 - 当它被触发时，它接收一组已更改的选项。
插件可以检查选项是否在此集合中，然后从上下文的选项对象中读取该值。

这个函数的一个常见用途是检查选项是否有效，并在无效时给用户反馈。
如果在配置过程中引发了`exceptions.OptionsError`异常，更新中的所有更改都会自动回滚，
并向用户显示错误。让我们看一个例子。

{{< example src="examples/addons/options-configure.py" lang="py" >}}

这里有几点需要注意。首先，我们添加的选项使用`typing.Optional`。
这向mitmproxy表明`None`是此选项的有效值 - 也就是说，它可以未设置。
其次，`configure`方法首先用我们的默认值（`None`）调用，然后如果选项更改，则使用更新的值调用。
如果我们尝试加载带有不正确值的脚本，现在会看到一个错误：

```
> mitmdump -s ./examples/addons/options-configure.py --set addheader=1000
Loading script: ./examples/addons/options-configure.py
/Users/cortesi/mitmproxy/mitmproxy/venv/bin/mitmdump: addheader must be <= 100
```

## 支持的类型

以下类型可用于选项。

- 原始类型 - `str`、`int`、`float`、`bool`。
- 可选值，使用`typing.Optional`注解。
- 值序列，使用`collections.abc.Sequence`注解。 