---
title: "协议"
weight: 7
aliases:
  - /concepts-protocols/
---

# 协议

mitmproxy不仅支持HTTP，还支持其他重要的Web协议。
本页列出了各个协议实现的详细信息和已知限制。
大多数协议可以通过切换相应的[选项]({{< relref "/concepts/options" >}})来禁用。

## HTTP/1

mitmproxy中的HTTP/1.0和HTTP/1.1支持基于我们自定义的HTTP堆栈，该堆栈基于[h11](https://github.com/python-hyper/h11)，对HTTP语法错误特别健壮。协议违规通常会被故意在代理处转发或插入。

##### 已知限制

- 尾部数据(Trailers)：mitmproxy目前不支持HTTP/1.x的尾部数据，但我们欢迎贡献。

## HTTP/2

mitmproxy中的HTTP/2支持基于[hyper-h2](https://github.com/python-hyper/hyper-h2)。如果上游服务器不支持HTTP/2，mitmproxy会无缝地将消息转换为HTTP/1。

##### 已知限制

- *优先级信息*：mitmproxy目前忽略HTTP/2 PRIORITY帧。这不会影响传输的内容，但可能会影响消息发送的顺序。
- *推送承诺*：mitmproxy目前不宣传对HTTP/2推送承诺的支持。
- *明文HTTP/2*：mitmproxy目前不支持未加密的HTTP/2(h2c)。

## HTTP/3

mitmproxy中的HTTP/3支持基于[aioquic](https://github.com/aiortc/aioquic)。Mitmproxy的HTTP/3功能在反向代理、本地和WireGuard模式下可用。

##### 已知限制

- *重放*：客户端重放目前不可用。
- *支持的版本*：mitmproxy目前仅支持QUIC版本1。版本2(RFC 9369)尚不支持。
- *实现兼容性*：mitmproxy的HTTP/3支持仅在cURL上进行过广泛测试。其他实现可能会出现错误。

## WebSocket

mitmproxy中的WebSocket支持基于[wsproto](https://github.com/python-hyper/wsproto)项目，包括对消息压缩的支持。

##### 已知限制

- *重放*：客户端或服务器重放尚不可用。
- *Ping*：mitmproxy将转发PING和PONG帧，但不存储它们。有效负载仅记录到事件日志中。
- *未知扩展*：未知的WebSocket扩展将导致警告消息被记录，但会按原样传递。这可能导致不符合规范的行为。

## DNS

mitmproxy中的DNS支持基于自定义DNS实现。

##### 已知限制

- *重放*：客户端或服务器重放尚不可用。
- 我们尚未开始DoT/DoH/DoQ(DNS-over-TLS/HTTPS/QUIC)的任何工作。欢迎贡献。

## 通用TCP/TLS代理

Mitmproxy还可以作为通用TCP代理。在此模式下，mitmproxy仍然会在连接开始时检测TLS的存在并在必要时执行中间人攻击，但除此之外会不加修改地转发消息。

用户可以通过设置[`tcp_hosts`选项]({{< relref "/concepts/options" >}})明确选择通用TCP代理。

##### 已知限制

- *重放*：客户端或服务器重放尚不可用。
- *机会性TLS*：mitmproxy不会检测纯文本协议何时升级到TLS(STARTTLS)。

## 通用UDP/DTLS代理

Mitmproxy还可以作为通用UDP代理。在此模式下，mitmproxy仍然会在连接开始时检测DTLS的存在并在必要时执行中间人攻击，但除此之外会不加修改地转发消息。

用户可以通过设置[`udp_hosts`选项]({{< relref "/concepts/options" >}})明确选择通用UDP代理。

##### 已知限制

- *重放*：客户端或服务器重放尚不可用。 