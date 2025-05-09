---
title: "简介"
layout: single
menu:
    overview:
        weight: 1
---

# 简介

mitmproxy是一套工具，提供了一个交互式的、支持SSL/TLS的拦截代理，适用于HTTP/1、HTTP/2和WebSockets。

## 功能特性

- 拦截HTTP和HTTPS请求与响应并即时修改它们
- 保存完整的HTTP会话以便日后重放和分析
- 重放HTTP会话的客户端部分
- 重放之前记录的服务器的HTTP响应
- 反向代理模式，将流量转发到指定服务器
- 在macOS和Linux上支持透明代理模式
- 使用Python对HTTP流量进行脚本化修改
- 动态生成用于拦截的SSL/TLS证书
- 以及[更多、更多功能...]({{< relref "/overview/features">}})

## 3个强大的核心工具

mitmproxy项目的工具是一组前端，它们公开了共同的底层功能。当我们谈论"mitmproxy"时，我们通常指的是三个工具中的任何一个 - 它们只是同一个核心代理的不同前端。

**mitmproxy**是一个交互式的、支持SSL/TLS的拦截代理，具有用于HTTP/1、HTTP/2和WebSockets的控制台界面。

**mitmweb**是mitmproxy的网页界面版本。

**mitmdump**是mitmproxy的命令行版本。可以将其视为HTTP版的tcpdump。

在[mitmproxy网站](https://mitmproxy.org)上可以找到分发包。
开发信息和我们的源代码可以在我们的[GitHub仓库](https://github.com/mitmproxy/mitmproxy)中找到。

### mitmproxy

{{< figure src="/screenshots/mitmproxy.png" alt="终端用户界面的截图" >}}

**mitmproxy**是一个控制台工具，允许交互式检查和修改HTTP流量。它与mitmdump的不同之处在于所有流量都保存在内存中，这意味着它适合获取和操作较小的样本。使用`?`快捷键可以从任何**mitmproxy**屏幕查看上下文相关的文档。

---

### mitmweb

{{< figure src="/screenshots/mitmweb.png" alt="Web用户界面的截图" >}}

**mitmweb**是mitmproxy的基于Web的用户界面，允许交互式检查和修改HTTP流量。与mitmproxy一样，它与mitmdump的不同之处在于所有流量都保存在内存中，这意味着它适合获取和操作较小的样本。

{{% note %}}
Mitmweb目前处于测试阶段。我们认为它对于当前在UI中公开的所有功能都是稳定的，但它仍然缺少很多mitmproxy的功能。
{{% /note %}}

---

### mitmdump

**mitmdump**是mitmproxy的命令行伴侣。它提供类似tcpdump的功能，让您查看、记录和以编程方式转换HTTP流量。查看`--help`标志输出以获取完整文档。

#### 示例：保存流量

```bash
mitmdump -w outfile
```

以代理模式启动mitmdump，并将所有流量写入**outfile**。

#### 过滤保存的流量

```bash
mitmdump -nr infile -w outfile "~m post"
```

启动mitmdump而不绑定到代理端口(`-n`)，从infile读取所有流量，应用指定的过滤器表达式（仅匹配POST请求），并写入outfile。

#### 客户端重放

```bash
mitmdump -nC outfile
```

启动mitmdump而不绑定到代理端口(`-n`)，然后重放outfile中的所有请求(`-C filename`)。标志以明显的方式组合，因此您可以从一个文件重放请求，并将结果流写入另一个文件：

```bash
mitmdump -nC srcfile -w dstfile
```

有关更多信息，请参阅[客户端重放]({{< relref "/overview/features#client-side-replay" >}})部分。

#### 运行脚本

```bash
mitmdump -s examples/simple/add_header.py
```

这运行了**add_header.py**示例脚本，它只是向所有响应添加一个新标头。

#### 脚本数据转换

```bash
mitmdump -ns examples/simple/add_header.py -r srcfile -w dstfile
```

此命令从**srcfile**加载流量，根据指定的脚本转换它，然后将其写回**dstfile**。 