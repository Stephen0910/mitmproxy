---
title: "示例"
weight: 6
aliases:
  - /addons-examples/
---

# 插件示例

## 专用示例插件

以下是一些有用的mitmproxy插件示例，帮助您快速了解如何开发自己的插件。

### 基础示例

* **anatomy.py** — 一个计数HTTP请求的简单插件
* **anatomy2.py** — 使用简化语法的插件示例
* **http-add-header.py** — 向HTTP响应添加头部

### 命令相关

* **commands-simple.py** — 一个带有简单命令的插件
* **commands-flows.py** — 处理流量的命令示例
* **commands-paths.py** — 使用路径参数的命令示例

### 内容视图

* **contentview.py** — 自定义内容视图示例
* **contentview-interactive.py** — 交互式内容视图示例

### 选项相关

* **options-simple.py** — 简单选项示例
* **options-configure.py** — 使用选项配置事件的示例

### HTTP交互

* **http-modify-form.py** — 修改表单数据
* **http-modify-query-string.py** — 修改查询字符串
* **http-redirect-requests.py** — 重定向HTTP请求
* **http-reply-from-proxy.py** — 代理直接回复请求
* **http-stream-simple.py** — 简单的HTTP流处理
* **http-stream-modify.py** — 修改HTTP流
* **http-trailers.py** — 处理HTTP尾部

### 流量操作

* **duplicate-modify-replay.py** — 复制、修改和重放流量
* **filter-flows.py** — 过滤流量

### WebSocket和TCP

* **websocket-simple.py** — 简单的WebSocket插件
* **websocket-inject-message.py** — 向WebSocket连接注入消息
* **tcp-simple.py** — 简单的TCP流量处理

### 其他功能

* **io-read-saved-flows.py** — 读取已保存的流量
* **io-write-flow-file.py** — 写入流量到文件
* **log-events.py** — 记录所有事件
* **nonblocking.py** — 非阻塞处理示例
* **shutdown.py** — 优雅关闭示例
* **wsgi-flask-app.py** — 内嵌Flask应用的示例

## 内置插件

mitmproxy的许多功能都是通过[一套内置插件](https://github.com/mitmproxy/mitmproxy/tree/main/mitmproxy/addons)实现的，
这些插件实现了从反缓存和粘性Cookie到引导Web应用程序的各种功能。
内置插件提供了很好的学习资料，您可以很快发现，复杂的功能通常可以归结为非常小的、完全独立的模块。

## 额外的社区示例

mitmproxy社区贡献的其他示例可以在[GitHub](https://github.com/mitmproxy/mitmproxy/tree/main/examples/contrib)上找到。

## 如何运行示例

要运行任何示例，只需使用`-s`参数启动mitmproxy：

```bash
mitmproxy -s examples/addons/anatomy.py
```

或者：

```bash
mitmdump -s examples/addons/http-add-header.py
``` 