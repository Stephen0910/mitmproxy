---
title: "mitmproxy.http 模块"
url: "zh/api/mitmproxy/http.html"

menu: api
---

# mitmproxy.http 模块

此模块包含处理HTTP协议的类和功能。

## 主要组件

以下是一些重要的类和组件：

- **HTTPFlow**: HTTP请求和响应的容器
- **Request**: 表示HTTP请求
- **Response**: 表示HTTP响应
- **Headers**: 表示HTTP头部

## 常用属性和方法

### HTTPFlow

- `request`: HTTP请求对象
- `response`: HTTP响应对象
- `websocket`: WebSocket连接数据（如果存在）
- `marked`: 用户在UI中标记的流量
- `intercepted`: 流量是否被拦截

### Request/Response

- `headers`: HTTP头部对象
- `content`: 消息内容
- `text`: 文本形式的消息内容（如果可解码）
- `url`: 请求URL（仅Request）
- `status_code`: 状态码（仅Response）

### Headers

- `get(key, default=None)`: 获取指定头部值
- `set(key, value)`: 设置头部值
- `keys()`: 获取所有头部名称 