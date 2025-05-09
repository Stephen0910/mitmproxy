---
title: "命令"
weight: 6
aliases:
  - /concepts-commands/
---

# 命令

命令是允许用户与插件(addons)主动交互的机制。
也许最突出的例子是mitmproxy控制台用户界面 - 这个工具中的每一个交互都由绑定到按键的命令组成。
命令还提供了一种灵活且非常强大的方式，可以从命令提示符与mitmproxy进行交互。在mitmproxy控制台中，您可以使用`:`键进入命令提示符。该提示符对命令名称和许多内置参数类型都有智能的标签完成功能 - 试一试吧。

命令的权威参考是`--commands`标志，每个mitmproxy工具都公开了这个标志。传递此标志将向屏幕显示所有已注册命令、其参数和返回值的注释列表。在mitmproxy控制台中，您还可以在命令浏览器中查看所有命令的面板（默认情况下可通过`C`键绑定访问）。

# 处理流量(Flows)

mitmproxy的许多命令都以流量(flows)为参数。例如，客户端重放命令的签名如下：

```
replay.client [flow]
```

这意味着它需要一个或多个流量的序列。这就是[流量规范]({{< relref "/concepts/filters" >}})发挥作用的地方 - 当调用命令时，mitmproxy会智能地将灵活的流量选择语言扩展为流量列表。

启动mitmproxy控制台，并拦截一些流量，以便我们有流量可供使用。现在输入以下命令：

```
:replay.client @focus
```

确保尝试使用命令名称和流量规范的标签补全。`@focus`指定符扩展为当前焦点流量，因此您应该看到此流量重播。但是，重放可以接受任意数量的流量。尝试以下命令：

```
:replay.client @all
```

现在您应该看到所有流量一个接一个地重播。我们在这里可以使用mitmproxy过滤器语言的全部功能，所以我们也可以，例如，只重播特定域的流量：

```
:replay.client "~d google.com"
```

# 自定义键绑定

Mitmproxy的键绑定可以在`~/.mitmproxy/keys.yaml`文件中根据您的需求进行自定义。此文件由一系列映射组成，包含以下键：

* `key`（**必需**）：要绑定的键。
* `cmd`（**必需**）：按下键时要执行的命令。
* `context`：应该绑定键的上下文列表。默认情况下，这是**global**（即键在任何地方都绑定）。有效上下文包括`chooser`、`commands`、`dataviewer`、`eventlog`、`flowlist`、`flowview`、`global`、`grideditor`、`help`、`keybindings`、`options`。
* `help`：绑定的帮助字符串，将在键绑定浏览器中显示。

#### 示例

{{< example src="/examples/keys.yaml" lang="yaml" >}} 