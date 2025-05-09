---
title: "透明代理"
weight: 1
aliases:
 - /howto-transparent/
---

# 透明代理

使用透明代理时，流量会在网络层被重定向到代理，而不需要任何客户端配置。这使得透明代理非常适合那些无法更改客户端行为的情况 - 对代理无感知的移动应用程序就是一个常见示例。

{{% note %}}
新的[WireGuard]({{< relref "/concepts/modes#wireguard" >}})
和[本地捕获]({{< relref "/concepts/modes#local-capture" >}})模式
提供了透明代理的替代实现。这些方式更容易设置，因为不需要设置IP转发或修改路由规则。
{{% /note %}}

要设置透明代理，我们需要两个新组件。第一个是透明地将目的地为互联网上服务器的TCP连接重定向到监听代理服务器的重定向机制。这通常采用与代理服务器在同一主机上的防火墙的形式 - 
Linux上的[iptables](http://www.netfilter.org/)或
OSX上的[pf](https://en.wikipedia.org/wiki/PF_(firewall))。当代理
接收到重定向的连接时，它看到的是普通的HTTP请求，没有主机
规范。这就是第二个新组件发挥作用的地方 - 主机模块
允许我们查询重定向器以获取TCP连接的原始目的地。

目前，mitmproxy支持在OSX Lion及更高版本以及
所有当前版本的Linux上进行透明代理。

## Linux

在Linux上，mitmproxy与iptables重定向机制集成
以实现透明模式。

### 1. 启用IP转发。

```bash
sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv6.conf.all.forwarding=1
```

这确保了您的机器转发数据包，而不是拒绝它们。

如果您想在重启后保持此设置，您需要调整您的`/etc/sysctl.conf`或
新创建的`/etc/sysctl.d/mitmproxy.conf`（参见[这里](https://superuser.com/a/625852)）。

### 2. 禁用ICMP重定向。

```bash
sysctl -w net.ipv4.conf.all.send_redirects=0
```

如果您的测试设备在同一物理网络上，您的机器不应该通知设备
有一条更短的路由可用，即跳过代理。

如果您想在重启后保持此设置，请参见上文。

### 3. 创建将所需流量重定向到mitmproxy的iptables规则集。

详细信息将根据您的设置而有所不同，但规则集应该看起来
像这样：

```bash
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 8080
ip6tables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080
ip6tables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 8080
```

如果您想在重启后保持此设置，您可以使用`iptables-persistent`包（参见
[这里](http://www.microhowto.info/howto/make_the_configuration_of_iptables_persistent_on_debian.html)）。

### 4. 启动mitmproxy。

您可能需要像这样的命令：

```bash
mitmproxy --mode transparent --showhost
```

`--mode transparent`选项打开透明模式，而`--showhost`参数告诉
 mitmproxy使用Host头的值进行URL显示。

### 5. 最后，配置您的测试设备。

将测试设备设置为使用运行mitmproxy的主机作为默认网关，并且
[在测试设备上安装mitmproxy证书颁发机构]({{< relref "/concepts/certificates" >}})。

### 重定向源自机器本身的流量的解决方法

按照上面的步骤**1, 2**进行操作，但*代替*步骤**3**中的命令，运行以下命令

创建一个用户来运行mitmproxy

```bash
sudo useradd --create-home mitmproxyuser
sudo -u mitmproxyuser -H bash -c 'cd ~ && pip install --user mitmproxy'
```

然后，配置iptables规则以将我们本地机器的所有流量重定向到mitmproxy。**注意**，一旦您运行这些命令，您将无法成功执行网络调用，*直到*您启动mitmproxy。如果您遇到问题，`iptables -t nat -F`是一种强力方法，可以刷新（清除）iptables `nat`表中的*所有*规则（包括您配置的任何其他规则）。

```bash
iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner mitmproxyuser --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner mitmproxyuser --dport 443 -j REDIRECT --to-port 8080
ip6tables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner mitmproxyuser --dport 80 -j REDIRECT --to-port 8080
ip6tables -t nat -A OUTPUT -p tcp -m owner ! --uid-owner mitmproxyuser --dport 443 -j REDIRECT --to-port 8080
```

这将重定向机器上`mitmproxyuser`以外的所有用户的数据包到mitmproxy。为了避免循环，请以`mitmproxyuser`用户身份运行mitmproxy。因此，步骤**4**应如下所示：

```bash
sudo -u mitmproxyuser -H bash -c '$HOME/.local/bin/mitmproxy --mode transparent --showhost --set block_global=false'
```

## OpenBSD

### 1. 启用IP转发。

```bash
sudo sysctl -w net.inet.ip.forwarding=1
```

### 2. 在**/etc/pf.conf**中放置以下两行。

```
mitm_if = "re2"
pass in quick proto tcp from $mitm_if to port { 80, 443 } divert-to 127.0.0.1 port 8080
```

这些规则告诉pf将来自`$mitm_if`的所有流量转移到
运行在8080端口上的本地mitmproxy实例。您应该替换
`$mitm_if`的值为您的测试设备将出现的接口。

### 3. 使用规则配置pf。

```bash
doas pfctl -f /etc/pf.conf
```

### 4. 现在启用它。

```bash
doas pfctl -e
```

### 5. 启动mitmproxy。

您可能需要像这样的命令：

```bash
mitmproxy --mode transparent --listen-host 127.0.0.1 --showhost
```

`--mode transparent`选项打开透明模式，而`--showhost`参数告诉
mitmproxy使用Host头的值进行URL显示。

### 6. 最后，配置您的测试设备。

将测试设备设置为使用运行mitmproxy的主机作为默认网关，并
[在测试设备上安装mitmproxy证书颁发机构]({{< relref "/concepts/certificates" >}})。

{{% note %}}
注意，上面给出的pf.conf中的**divert-to**规则仅适用
于入站流量。**这意味着它们不会重定向来自
运行pf的机器本身的流量。** 我们无法区分
来自非mitmproxy应用程序的出站连接和来自
mitmproxy本身的出站连接 - 如果您想拦截自己的流量，
应该使用外部主机来运行mitmproxy。尽管如此，pf是
灵活的，可以满足一系列创造性的可能性，比如
拦截来自虚拟机的流量。有关更多信息，请参见**pf.conf**手册页。
{{% /note %}}

## macOS

OSX Lion集成了来自OpenBSD项目的[pf](https://en.wikipedia.org/wiki/PF_(firewall))
数据包过滤器，mitmproxy使用它在OSX上实现
透明模式。请注意，这意味着我们不支持早期版本的OSX的透明模式。

### 1. 启用IP转发。

```bash
sudo sysctl -w net.inet.ip.forwarding=1
```

### 2. 将以下行放在一个名为**pf.conf**的文件中。

```
rdr pass on en0 inet proto tcp to any port {80, 443} -> 127.0.0.1 port 8080
```

此规则告诉pf将所有目的端口为80或443的流量重定向
到运行在8080端口上的本地mitmproxy实例。您应该将
`en0`替换为您的测试设备将出现的接口。

### 3. 使用规则配置pf。

```bash
sudo pfctl -f pf.conf
```

### 4. 现在启用它。

```bash
sudo pfctl -e
``` 