---
title: "自定义命令"
weight: 4
aliases:
    - /addons-commands/
---

# 命令

命令允许用户与插件主动交互 - 查询它们的状态、命令它们执行操作以及让它们转换数据。
与[选项]({{< relref "/addons/options" >}})一样，命令是有类型的，
并且命令调用和返回的数据都在运行时进行检查。命令是一个非常强大的结构 - 例如，
mitmproxy控制台中的所有用户交互都是通过将命令绑定到按键来构建的。

## 简单示例

让我们从一个简单的示例开始。

{{< example src="examples/addons/commands-simple.py" lang="py" >}}

要查看此示例的运行效果，请加载插件启动mitmproxy控制台：

```bash
> mitmproxy -s ./examples/addons/commands-simple.py
```

现在，确保事件日志正在显示，然后在提示符处执行命令（通过输入":"开始）：

```
:myaddon.inc
```

注意，制表符补全是有效的 - 我们的插件命令与内置命令具有完全的对等性。关于这个例子有几点需要注意：

- 命令通过`command.command`装饰器声明。每个命令都有一个唯一的名称 - 按照惯例，
  我们使用以句点分隔的名称，并使用插件名称作为前缀。
- 用类型注解命令是必须的，包括返回类型（在本例中为`None`）。
  这使得mitmproxy能够在其整个工具集中支持插件命令 - 运行时调用进行类型检查，
  插件命令包含在内置帮助中，mitmproxy控制台中的命令编辑器可以执行复杂的补全和错误检查，等等。

## 处理流量

由于命令参数是有类型的，我们可以为处理某些重要的数据类型提供特殊的便利性。
其中最有用的是代表mitmproxy流量的`Flows`类。

考虑以下插件：

{{< example src="examples/addons/commands-flows.py" lang="py" >}}

`myaddon.addheader`命令非常简单：它接收一系列流量，并向每个请求添加一个头部。
这个例子真正有趣的方面是用户如何指定流量。因为mitmproxy可以检查类型签名，
它可以将文本流量选择器透明地扩展为一系列流量。这意味着用户可以使用[流量过滤器]({{< relref "/concepts/filters" >}})
的全部灵活性。让我们试一试。

首先将插件加载到mitmproxy中，并通过它发送一些流量，以便我们有流量可以处理：

```bash
> mitmproxy -s ./examples/addons/commands-flows.py
```

现在我们可以以各种方式调用我们的命令。让我们首先只对当前焦点的流量运行它：

```
:myaddon.addheader @focus
```

我们也可以在所有流量上调用它：

```
:myaddon.addheader @all
```

或者只对来自**google.com**的流量：

```
:myaddon.addheader ~d google.com
```

更重要的是，如果我们打算经常使用这些命令，我们可以轻松地将这些命令绑定到mitmproxy中的键盘快捷键。
流量选择器与命令结合使用非常强大，让我们能够构建并暴露用于操作流量的可重用函数。

## 路径

命令可以接受任意数量的参数。让我们在前面的示例基础上进行扩展，以说明这一点，并演示另一种特殊类型：路径。

{{< example src="examples/addons/commands-paths.py" lang="py" >}}

我们的命令计算指定流量集中域的直方图，并将其写入指定为命令第二个参数的路径。尝试像这样调用它：

```
:myaddon.histogram @all /tmp/xxx
```

注意，mitmproxy为流量规范和路径都提供了制表符补全。

## 支持的类型

以下类型可用于选项。如果你需要使用此处未列出的类型，请向我们发送拉取请求。

- 原始类型：`str`、`int`、`bool`
- 序列：`typing.Sequence[str]`
- 流量和流量序列：`flow.Flow`和`typing.Sequence[flow.Flow]`
- 多选字符串：`types.Choice`
- 元类型：`types.Command`和`types.Arg`。这些用于构造调用其他命令的命令。
  这在键绑定中最常用 - 参见内置mitmproxy控制台键绑定，获取丰富的示例套件。
- 数据类型：`types.CutSpec`和`types.Data`。剪切机制目前处于alpha阶段，
  为切割流量数据提供了便捷的方式。
- 路径：`types.Path` 