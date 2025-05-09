---
title: "概述"
weight: 1
aliases:
  - /addons-overview/
---

# 插件

Mitmproxy的插件机制是其非常强大的部分。事实上，mitmproxy自身的许多功能都是在
[一套内置插件](https://github.com/mitmproxy/mitmproxy/tree/main/mitmproxy/addons)中定义的，
这些插件实现了从[反缓存]({{< relref "/overview/features#anticache" >}})和[粘性Cookie]({{< relref
"/overview/features#sticky-cookies" >}})到我们的引导式Web应用程序等各种功能。

插件通过响应[事件]({{< relref event-hooks >}})与mitmproxy交互，这使它们能够钩入并改变mitmproxy的行为。
它们通过[选项]({{< relref "/addons/options" >}})进行配置，这些选项可以在mitmproxy的配置文件中设置，
由用户交互式更改，或在命令行中传递。最后，它们可以暴露[命令]({{< relref "/addons/commands" >}})，
这允许用户直接调用它们的操作或在交互工具中将它们绑定到按键。

# 插件剖析

{{< example src="examples/addons/anatomy.py" lang="py" >}}

上面是一个简单的插件，它跟踪我们见过的流量数量（更具体地说是HTTP请求）。
每次看到新的流量时，它都会增加并记录其计数。输出可以在交互工具的事件日志中找到，或者在mitmdump的控制台上看到。

通过将其加载到你选择的mitmproxy工具中来试用它，确保它按预期工作。
在这些示例中我们将使用mitmdump，但所有工具的标志都是相同的：

```bash
mitmdump -s ./anatomy.py
```

关于上面的代码，有几点需要注意：

- Mitmproxy会提取`addons`全局列表的内容，并将其加载到插件机制中。
- 插件只是对象 - 在本例中，我们的插件是`Counter`的一个实例。
- `request`方法是*事件*的一个例子。插件只需为它们想要处理的每个事件实现一个方法。
  每个事件及其签名都记录在[API文档]({{< relref "event-hooks" >}})中。

# 简化脚本语法

有时，我们希望编写一个快速脚本而不必麻烦地创建一个类。
插件机制有一种简写方式，允许将整个模块视为插件对象。
这使我们可以将事件处理函数放在模块作用域中。
例如，这里有一个完整的脚本，它向每个请求添加一个标头：

{{< example src="examples/addons/anatomy2.py" lang="py" >}} 