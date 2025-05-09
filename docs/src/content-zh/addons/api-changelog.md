---
title: "API 变更日志"
weight: 9
aliases:
  - /addons-api-changelog/
---

# API 变更日志

我们尽量避免它们，但本页列出了mitmproxy插件API中的重大变更。

## mitmproxy 12

内容视图API已大幅简化，详情请参阅新的[内容视图文档]。

[内容视图文档]: {{< relref "/addons/contentviews" >}}

`mitmproxy.dns.Message`已更名为`mitmproxy.dns.DNSMessage`。

## mitmproxy 9.1

`mitmproxy.connection.Client`和`mitmproxy.connection.Server`现在只接受关键字参数。

## mitmproxy 9.0

#### 日志记录

我们已弃用mitmproxy的自制日志系统，转而使用Python内置的`logging`模块。
这意味着插件现在应使用标准日志功能而不是`mitmproxy.ctx.log`：

```python
# 已弃用：
from mitmproxy import ctx
ctx.log.info("hello world")

# 新方式：
import logging
logging.info("hello world")
```

相应地，`add_log`事件已被弃用。依赖日志条目的开发者应该注册自己的
`logging.Handler`。示例可以在`EventStore`插件中找到。

## mitmproxy 7.0

#### 连接事件

作为新代理核心的一部分，我们修订了mitmproxy的连接特定事件钩子。`.client_conn`和
`.server_conn`对象在整个API中有重大变化。详情请参阅新的
[事件钩子文档]({{< relref "/addons/event-hooks#ConnectionEvents" >}})。

| 属性           | 客户端 (v6)  | 服务器 (v6)      | mitmproxy v7 |
|----------------|-------------|-------------------|--------------|
| 远程 IP:端口   | `.address`  | `.ip_address`     | `.peername`  |
| 本地 IP:端口   | ❌          | `.source_address` | `.sockname`  |
| 远程域名       | N/A         | `.address`        | `.address`   |


由于传递的对象现在不同，我们也借此机会引入了更一致的事件名称：

| mitmproxy 6        | mitmproxy 7           |
| ------------------ | --------------------- |
| `clientconnect`    | `client_connected`    |
| `clientdisconnect` | `client_disconnected` |
| ❌                 | `server_connect`      |
| `serverconnect`    | `server_connected`    |
| `serverdisconnect` | `server_disconnected` |

#### 日志记录

`log`事件已更名为`add_log`。这修复了一个持续的错误源，用户导入名为"log"的模块，然后被意外捕获。

#### 内容视图

内容视图现在实现`render_priority`而不是`should_render`。这使得额外的专业化成为可能，
例如，现在可以编写只美化显示特定JSON响应的内容视图。
详情请参阅[contentview.py]({{< relref "/addons/examples#contentview" >}})示例。

#### WebSocket流量

mitmproxy 6有一个自定义的WebSocketFlow类，它与相关的HTTPFlow有
[丑陋的相互依赖](https://github.com/mitmproxy/mitmproxy/issues/4425)。长话短说，
WebSocketFlow不再存在，相反HTTPFlow有一个整洁的
[`.websocket`属性]({{< relref "api/mitmproxy.http.md#HTTPFlow.websocket" >}})。现在所有WebSocket流量
都会传递设置了此属性的原始`HTTPFlow`。和往常一样，现有的转储文件会在加载时自动转换。

#### 证书

mitmproxy现在使用`cryptography`而不是`pyOpenSSL`生成证书。因此，
`mitmproxy.certs`的API已更改。

#### HTTP头部

`mitmproxy.net.http.Headers` -> `mitmproxy.http.Headers`，以保持一致性。 