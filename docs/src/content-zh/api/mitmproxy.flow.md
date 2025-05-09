---
title: "mitmproxy.flow 模块"
url: "zh/api/mitmproxy/flow.html"
menu: api
---

# mitmproxy.flow 模块

此模块包含表示网络流量的基本类。Flow（流量）是mitmproxy拦截的所有网络通信的基本单位。

## 主要组件

以下是一些重要的类和组件：

- **Flow**: 所有流量类型的基类
- **Error**: 表示在流量处理过程中发生的错误

## 常用属性和方法

### Flow

- `id`: 流量的唯一标识符
- `client_conn`: 客户端连接对象
- `server_conn`: 服务器连接对象
- `type`: 流量类型（"http"、"tcp"等）
- `error`: 如果发生错误，包含错误信息
- `intercepted`: 流量是否被拦截
- `marked`: 用户在UI中标记的流量
- `modified`: 流量是否被修改
- `kill(flow_error=None)`: 终止流量处理
- `resume()`: 恢复被拦截的流量
- `reply()`: 用于异步处理流量的回复机制

您可以在插件开发中使用这些类来访问和修改流量信息。 