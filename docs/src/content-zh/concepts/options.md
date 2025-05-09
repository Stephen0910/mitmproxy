---
title: "选项"
weight: 5
aliases:
  - /concepts-options/
---

# 选项

mitmproxy工具共享一个位于`~/.mitmproxy/config.yaml`的通用[YAML](http://yaml.org/)配置文件。这个文件控制**选项** - 确定mitmproxy行为的类型化值。选项机制非常全面 - 实际上，选项控制了mitmproxy的所有运行时行为。大多数命令行标志只是底层选项的别名，而在**mitmproxy**和**mitmweb**中进行的交互式设置更改只是更改我们运行时选项存储中的值。这意味着mitmproxy的几乎任何方面的行为都可以通过选项来控制。

选项的权威参考是每个mitmproxy工具公开的`--options`标志。传递此标志将向控制台输出带注释的YAML配置，其中包括所有选项及其默认值。

选项机制是可扩展的 - 第三方附加组件可以定义的选项与mitmproxy自己的选项处理方式完全相同。这意味着附加组件也可以通过中央配置文件进行配置，并且它们的选项将出现在交互式工具的选项编辑器中。

## 工具

**mitmproxy**和**mitmweb**都有内置编辑器，可以让您查看和操作mitmproxy的完整配置状态。您交互式更改的值在运行实例中立即生效，并可以通过将设置保存到YAML配置文件中使其持久化（有关如何执行此操作的详细信息，请参见特定工具的交互式帮助）。

对于所有工具，可以使用`--set`命令行选项直接按名称设置选项。请参阅命令行帮助(`--help`)了解用法。例如：
```
mitmproxy --set anticomp=true
mitmweb --set ignore_hosts=example.com --set ignore_hosts=example.org 
```

## 可用选项

此列表可能不反映您当前mitmproxy环境中实际可用的选项。要获取最新列表，请对每个mitmproxy工具使用`--options`标志。

{{< readfile file="/generated/options.html" >}} 