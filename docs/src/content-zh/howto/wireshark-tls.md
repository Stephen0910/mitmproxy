---
title: "Wireshark和SSL/TLS"
weight: 1
aliases:
  - /howto-wireshark-tls/
---

# Wireshark和SSL/TLS主密钥

SSL/TLS主密钥可以由mitmproxy记录下来，以便外部程序可以解密进出代理的SSL/TLS连接。Wireshark的最新版本可以使用这些日志文件来解密数据包。有关更多信息，请参阅[Wireshark维基](https://wiki.wireshark.org/TLS#using-the-pre-master-secret)。

通过设置环境变量`SSLKEYLOGFILE`指向一个可写的文本文件，即可启用密钥日志记录：

```bash
SSLKEYLOGFILE="$PWD/.mitmproxy/sslkeylogfile.txt" mitmproxy
```

您也可以`export`这个环境变量，使其对当前Shell会话中启动的所有应用程序都有效。

您可以通过`编辑 -> 首选项 -> 协议 -> TLS -> (Pre)-Master-Secret日志文件名`在Wireshark中指定密钥文件路径。如果您的SSLKEYLOGFILE尚不存在，只需创建一个空文本文件，以便您可以在Wireshark中选择它（或运行mitmproxy来创建并收集主密钥）。

请注意，其他程序也会遵循`SSLKEYLOGFILE`，例如Firefox和Chrome。如果这会造成任何问题，您可以使用`MITMPROXY_SSLKEYLOGFILE`代替，而不会影响其他应用程序。 