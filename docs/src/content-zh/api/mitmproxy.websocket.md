---
title: "mitmproxy.websocket 模块"
url: "zh/api/mitmproxy/websocket.html"
menu: api
---

# mitmproxy.websocket 模块

此模块包含用于处理WebSocket连接的类和功能。WebSocket允许在客户端和服务器之间进行双向通信。

## 主要组件

以下是一些重要的类和组件：

- **WebSocketData**: 包含WebSocket连接的消息和事件
- **WebSocketMessage**: 表示单个WebSocket消息

## 常用属性和方法

### WebSocketData

- `messages`: 所有WebSocket消息的列表
- `handshake_flow`: 初始化WebSocket连接的HTTP流量

### WebSocketMessage

- `type`: 消息类型（TEXT或BINARY）
- `from_client`: 布尔值，表示消息是否来自客户端
- `content`: 消息内容的字节表示
- `text`: 消息内容的文本表示（仅适用于文本消息）
- `timestamp`: 消息的时间戳

在mitmproxy 7.0及更高版本中，WebSocket功能通过HTTPFlow的`.websocket`属性访问，而不是作为单独的流量类型。 