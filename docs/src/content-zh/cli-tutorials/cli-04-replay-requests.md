---
title: "重放请求"
weight: 4
url: /zh/mitmproxytutorial-replayrequests/
has_asciinema: true
---

# 重放请求

mitmproxy的另一个强大功能是重放之前的流量。
支持两种类型的重放：

* **客户端重放：** mitmproxy重放之前的客户端请求，即再次向服务器发送相同的请求。
* **服务器端重放：** mitmproxy为与先前记录的请求匹配的请求重放服务器响应。

在本教程中，我们专注于更常见的客户端重放用例。
有关服务器端重放的更多信息，请参阅[服务器端重放]({{< relref "/overview/features#server-side-replay" >}})文档。

{{% asciicast file="mitmproxy_replay_requests" poster="0:3" instructions=true %}}

您即将完成本教程。在最后一步中，您将找到更多与mitmproxy相关的资源以供探索。 