---
title: "mitmproxy.websocket 模块"
url: "zh/api/mitmproxy/websocket.html"
menu: api
---

# mitmproxy.websocket 模块

此模块包含用于处理WebSocket连接的类和功能。WebSocket允许在客户端和服务器之间进行双向通信。

以下是一些重要的类和组件：

- **WebSocketData**: 包含WebSocket连接的消息和事件
- **WebSocketMessage**: 表示单个WebSocket消息

在mitmproxy 7.0及更高版本中，WebSocket功能通过HTTPFlow的`.websocket`属性访问，而不是作为单独的流量类型。

请参考下面的英文API文档获取详细信息：

{{< readfile file="/generated/api/mitmproxy/websocket.html" >}} 