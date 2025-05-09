---
title: "忽略域名"
weight: 2
aliases:
  - /howto-ignoredomains/
---

# 忽略域名

有两个主要原因可能导致您想要从mitmproxy的拦截机制中排除某些流量：

- **证书固定:** 某些流量使用[证书固定](https://security.stackexchange.com/questions/29988/what-is-certificate-pinning)进行保护，mitmproxy的拦截会导致错误。例如，Twitter应用、Windows更新或Apple应用商店如果在mitmproxy活动时会无法工作。
- **方便性:** 您真的不关心某些部分的流量，只想让它们消失。注意，mitmproxy的[view_filter]({{< relref "/concepts/options/#view_filter" >}})选项通常是更好的替代方案，因为它不受下面列出的限制影响。

如果您想查看（SSL保护的）非HTTP连接，请查看**tcp_proxy**功能。如果您想因为大型响应体而从mitmproxy的处理中忽略流量，请查看[流式处理]({{< relref "/overview/features#streaming" >}})功能。

## ignore_hosts

`ignore_hosts`选项允许您指定一个正则表达式，该正则表达式与连接的`host:port`字符串（例如"example.com:443"）进行匹配。匹配的主机将从拦截中排除，并且不做修改地传递。

|                    |                                                                    |
| ------------------ | ------------------------------------------------------------------ |
| 命令行别名 | `--ignore-hosts regex`                                             |
| mitmproxy选项   | `ignore_hosts` |

## 限制

有两个重要的特性需要考虑：

- **在透明模式下，ignore模式与IP和ClientHello SNI主机进行匹配。** 虽然我们通常从Host头中推断主机名（如果设置了`ignore_hosts`选项），但在SSL握手之前我们无法访问此信息。但是，如果客户端使用SNI，那么我们将SNI主机视为ignore目标。
- **在常规和上游代理模式下，显式HTTP请求永远不会被忽略。**[^1] ignore模式应用于CONNECT请求，这些请求发起HTTPS或明文WebSocket连接。

## 教程

如果您只想忽略一个特定域，通常有一个万无一失的方法：

1. 运行mitmproxy或mitmdump并观察事件日志中`server connect`消息后面的`host:port`信息。mitmproxy将对这些信息进行过滤。
2. 获取`host:port`字符串，用^和$将其包围，转义所有点（.变为\\.），并将其用作您的ignore模式：

```
>>> mitmdump
Proxy server listening at http://*:8080
127.0.0.1:57089: client connect
127.0.0.1:57089: server connect example.com:443 (93.184.216.34:443)
127.0.0.1:57089: GET https://example.com/ HTTP/2.0
     << HTTP/2.0 200 OK 1.23k
127.0.0.1:57089: client disconnect
127.0.0.1:57089: server disconnect example.com:443 (93.184.216.34:443)
^C
>>> mitmproxy --ignore-hosts '^example\.com:443$'
```

以下是一些其他ignore模式的例子：

```
# 排除来自iOS应用商店的流量（正则表达式较宽松，但通常有效）：
--ignore-hosts apple.com:443
# 没有误判的"正确"版本：
--ignore-hosts '^(.+\.)?apple\.com:443$'

# 忽略example.com，但不忽略其子域名：
--ignore-hosts '^example.com:'

# 透明模式：
--ignore-hosts 17\.178\.96\.59:443
# IP地址范围：
--ignore-hosts 17\.178\.\d+\.\d+:443
```

如果您只想捕获某些特定域，您可以使用`--allow-hosts`选项，这会使mitmproxy忽略所有其他流量。

[^1]: 这源于显式HTTP代理的限制：单个连接可以被重用于多个目标域 - `GET http://example.com/`请求后可能在同一连接上跟着一个`GET http://evil.com/`请求。如果我们在第一个请求后开始忽略连接，我们将错过相关的第二个请求。 