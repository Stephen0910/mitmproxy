---
title: "事件钩子"
weight: 2
aliases:
    - /addons-events/
    - api/events.html
---

# 事件钩子

插件通过事件钩子连接到mitmproxy的内部机制。这些钩子在插件上以一组众所周知的名称方法实现。
许多事件接收`Flow`对象作为参数 - 通过修改这些对象，插件可以实时更改流量。
例如，这里有一个插件，它添加了一个响应头，其中包含看到的响应数量的计数：

{{< example src="/examples/addons/http-add-header.py" lang="py" >}}

## 可用钩子

以下插件列出了所有可用的事件钩子。

{{< readfile file="/generated/api/events.html" >}} 