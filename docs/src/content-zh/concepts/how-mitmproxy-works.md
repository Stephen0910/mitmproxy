---
title: "mitmproxy工作原理"
weight: 1
aliases:
  - /concepts-howmitmproxyworks/
---

# mitmproxy工作原理

Mitmproxy是一个非常灵活的工具。准确了解代理过程的工作原理将帮助您创造性地部署它，并考虑其基本假设以及如何绕过它们。本文详细解释了mitmproxy的代理机制，从最简单的未加密显式代理开始，逐步讲解到最复杂的交互 - 在存在[服务器名称指示(SNI)](https://en.wikipedia.org/wiki/Server_Name_Indication)的情况下透明代理TLS保护的流量[^1]。

## 显式HTTP代理

将客户端配置为使用mitmproxy作为显式代理是拦截流量最简单且最可靠的方式。代理协议在[HTTP RFC](https://tools.ietf.org/html/rfc7230)中有明确定义，因此客户端和服务器的行为都有良好定义，通常也很可靠。在与mitmproxy最简单的交互中，客户端直接连接到代理，并发出如下请求：

```http
GET http://example.com/index.html HTTP/1.1
```

这是一个代理GET请求 - 普通HTTP GET请求的扩展形式，包括了模式(schema)和主机规范，其中包含了mitmproxy继续处理所需的所有信息。

{{< figure src="/schematics/how-mitmproxy-works-explicit.png" title="显式代理" >}}

1. 客户端连接到代理并发出请求。
2. Mitmproxy连接到上游服务器并简单地转发请求。

## 显式HTTPS代理

显式代理的HTTPS连接过程有很大不同。客户端连接到代理并发出如下请求：

```http
CONNECT example.com:443 HTTP/1.1
```

传统的代理既不能查看也不能操作TLS加密的数据流，所以CONNECT请求仅要求代理在客户端和服务器之间建立一个管道。这里的代理只是一个促进者 - 它盲目地在两个方向上转发数据，而不了解内容。TLS连接的协商通过这个管道完成，随后的请求和响应流对代理来说是完全不透明的。

### mitmproxy中的MITM

这就是mitmproxy的基本技巧发挥作用的地方。它名称中的MITM代表中间人(Man-In-The-Middle) - 指我们用来拦截和干预这些理论上不透明的数据流的过程。基本思想是对客户端假装是服务器，对服务器假装是客户端，而我们坐在中间解码来自双方的流量。棘手的部分是[证书颁发机构](https://en.wikipedia.org/wiki/Certificate_authority)系统设计用来防止这种攻击，通过允许受信任的第三方对服务器的证书进行加密签名来验证其合法性。如果此签名不匹配或来自非信任方，安全的客户端将简单地断开连接并拒绝继续。尽管今天存在的CA系统有许多缺点，但这通常会导致出于分析目的MITM一个TLS连接的尝试失败。我们对这个难题的答案是自己成为一个受信任的证书颁发机构。Mitmproxy包含一个完整的CA实现，可以动态生成拦截证书。为了让客户端信任这些证书，我们[手动将mitmproxy注册为设备上的可信CA]({{< relref "/concepts/certificates" >}})。

### 复杂情况1：远程主机名是什么？

要继续这个计划，我们需要知道在拦截证书中使用的域名 - 客户端将验证证书是否用于它正在连接的域，如果不是这种情况，则中止。乍看之下，上面的CONNECT请求似乎给了我们所有需要的东西 - 在这个例子中，这两个值都是"example.com"。但是如果客户端以如下方式发起连接怎么办：

```http
CONNECT 10.1.1.1:443 HTTP/1.1
```

使用IP地址是完全合法的，因为它为我们提供了足够的信息来启动管道，即使它没有揭示远程主机名。

Mitmproxy有一个巧妙的机制来解决这个问题 - [上游证书嗅探]({{< relref "/concepts/certificates/#upstream-certificate-sniffing" >}})。当我们看到CONNECT请求时，我们暂停客户端部分的会话，并同时向服务器发起连接。我们完成与服务器的TLS握手，并检查它使用的证书。现在，我们使用上游证书中的通用名称(Common Name)为客户端生成虚拟证书。瞧，即使从未指定，我们也有了正确的主机名来呈现给客户端。

### 复杂情况2：主题备用名称

接下来是另一个复杂情况。有时，证书的通用名称实际上不是客户端连接到的主机名。这是因为证书中可选的[主题备用名称](https://en.wikipedia.org/wiki/SubjectAltName)字段允许指定任意数量的替代域。如果预期的域与这些域中的任何一个匹配，客户端将继续，即使该域与证书CN不匹配。这里的答案很简单：当我们从上游证书中提取CN时，我们也提取SANs，并将它们添加到生成的虚拟证书中。

### 复杂情况3：服务器名称指示

普通TLS的一个重大限制是每个证书需要自己的IP地址。这意味着您不能进行虚拟主机托管，其中具有独立证书的多个域共享相同的IP地址。在IPv4地址池迅速减少的世界中，这是一个问题，我们有一个解决方案，即TLS协议的[服务器名称指示](https://en.wikipedia.org/wiki/Server_Name_Indication)扩展。这让客户端可以在TLS握手开始时指定远程服务器名称，从而让服务器选择正确的证书来完成该过程。

SNI打破了我们的上游证书嗅探过程，因为当我们不使用SNI连接时，我们得到的是默认证书，可能与客户端期望的证书无关。解决方案是对客户端连接过程进行另一个棘手的复杂化。在客户端连接后，我们允许TLS握手继续，直到**刚刚**在SNI值传递给我们之后。现在我们可以暂停会话，并使用正确的SNI值发起上游连接，然后为我们提供正确的上游证书，从中我们可以提取预期的CN和SANs。

### 整合在一起

让我们将所有这些整合在一起，形成完整的显式代理HTTPS流程。

{{< figure src="/schematics/how-mitmproxy-works-explicit-https.png" title="显式HTTPS代理" >}}

1. 客户端连接到mitmproxy，并发出HTTP CONNECT请求。
2. Mitmproxy响应`200 Connection Established`，就像它已经设置了CONNECT管道一样。
3. 客户端认为它在与远程服务器通信，并启动TLS连接。它使用SNI指示它连接的主机名。
4. Mitmproxy连接到服务器，并使用客户端指示的SNI主机名建立TLS连接。
5. 服务器响应匹配的证书，其中包含生成拦截证书所需的CN和SAN值。
6. Mitmproxy生成拦截证书，并继续在步骤3中暂停的客户端TLS握手。
7. 客户端通过建立的TLS连接发送请求。
8. Mitmproxy通过在步骤4中启动的TLS连接将请求传递给服务器。

## 透明HTTP代理

当使用透明代理时，连接在网络层被重定向到代理，无需任何客户端配置。这使得透明代理非常适合于那些您无法更改客户端行为的情况 - 不支持代理的Android应用程序是一个常见的例子。

要实现这一点，我们需要引入两个额外的组件。第一个是重定向机制，将原本发往互联网服务器的TCP连接透明地重定向到监听的代理服务器。这通常采用代理服务器同一主机上的防火墙形式 - Linux上的[iptables](http://www.netfilter.org/)或OSX上的[pf](https://en.wikipedia.org/wiki/PF_\(firewall\))。一旦客户端发起连接，它会发出一个普通的HTTP请求，可能看起来像这样：

```http
GET /index.html HTTP/1.1
```

请注意，这个请求与显式代理变体不同，因为它省略了模式和主机名。那么，我们如何知道要将请求转发到哪个上游主机呢？执行重定向的路由机制为我们跟踪原始目标。每个路由机制都有不同的方式暴露这些数据，所以这引入了工作透明代理所需的第二个组件：一个主机模块，知道如何从路由器检索原始目标地址。在mitmproxy中，这采取内置的一组[模块](https://github.com/mitmproxy/mitmproxy/tree/main/mitmproxy/platform)形式，这些模块知道如何与每个平台的重定向机制通信。一旦我们有了这些信息，该过程就相当直接。

{{< figure src="/schematics/how-mitmproxy-works-transparent.png" title="透明代理" >}}

1. 客户端与服务器建立连接。
2. 路由器将连接重定向到mitmproxy，通常监听同一主机的本地端口。然后mitmproxy查询路由机制以确定原始目标是什么。
3. 现在，我们只需读取客户端的请求...
4. ...并将其转发到上游。

## 透明HTTPS代理

第一步是确定我们是否应该将传入连接视为HTTPS。这样做的机制很简单 - 我们使用路由机制找出原始目标端口是什么。所有传入连接都通过不同的层，可以确定要使用的实际协议。自动TLS检测通过在每个连接开始时查找*ClientHello*消息来检测SSLv3、TLS 1.0、TLS 1.1和TLS 1.2。这独立于使用的TCP端口工作。

从这里开始，该过程是我们描述的透明代理HTTP和显式代理HTTPS方法的合并。我们使用路由机制建立上游服务器地址，然后按照显式HTTPS连接的方式进行，以建立CN和SANs，并处理SNI。

{{< figure src="/schematics/how-mitmproxy-works-transparent-https.png" title="透明HTTPS代理" >}}

1. 客户端与服务器建立连接。
2. 路由器将连接重定向到mitmproxy，通常监听同一主机的本地端口。然后mitmproxy查询路由机制以确定原始目标是什么。
3. 客户端认为它在与远程服务器通信，并启动TLS连接。它使用SNI指示它连接的主机名。
4. Mitmproxy连接到服务器，并使用客户端指示的SNI主机名建立TLS连接。
5. 服务器响应匹配的证书，其中包含生成拦截证书所需的CN和SAN值。
6. Mitmproxy生成拦截证书，并继续在步骤3中暂停的客户端TLS握手。
7. 客户端通过建立的TLS连接发送请求。
8. Mitmproxy通过在步骤4中启动的TLS连接将请求传递给服务器。

### 脚注

[^1]: 这里使用的"TLS"通常指的是SSL(过时且不安全)和TLS(1.0及以上)，除非另有说明。 