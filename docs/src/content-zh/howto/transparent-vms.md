---
title: "透明代理虚拟机"
weight: 3
aliases:
  - /howto-transparent-vms/
---

# 透明代理虚拟机

本教程说明如何使用mitmproxy设置透明代理。在此示例中，我们使用带有Ubuntu代理机器的VirtualBox虚拟机，但一般的*互联网 \<--\> 代理虚拟机 \<--\> (虚拟)内部网络*设置可以应用于其他设置。

## 1. 配置代理虚拟机

首先，我们需要找出Ubuntu将我们的网络接口映射到哪些名称下。您可以通过以下命令找到此信息：

```bash
ip link
```

通常使用Ubuntu和VirtualBox时，**eth0**或**enp0s3**（Ubuntu 15.10及更新版本）连接到互联网，**eth1**或**enp0s8**（Ubuntu 15.10及更新版本）连接到将被代理的内部网络，并配置为使用静态IP（192.168.3.1）。如果名称不同，请使用您从*ip link*命令获得的名称。

### VirtualBox配置

{{< figure src="/transparent-vms/step1_vbox_eth0.png" >}}

{{< figure src="/transparent-vms/step1_vbox_eth1.png" >}}

### 虚拟机网络配置

{{< figure src="/transparent-vms/step1_proxy.png" >}}

## 2. 配置DHCP和DNS

我们使用dnsmasq在内部网络中提供DHCP和DNS服务。Dnsmasq是一个轻量级服务器，旨在为小型网络提供DNS（以及可选的DHCP和TFTP）服务。在此之前，我们需要修复一些Ubuntu的特性：**Ubuntu \>12.04**默认运行内部dnsmasq实例（仅监听回环）[\[1\]](https://www.stgraber.org/2012/02/24/dns-in-ubuntu-12-04/)。对于我们的用例，需要通过将**/etc/NetworkManager/NetworkManager.conf**中的`dns=dnsmasq`更改为`#dns=dnsmasq`来禁用它，如果是Ubuntu 16.04或更新版本，请运行：

```bash
sudo systemctl restart NetworkManager
```

如果是Ubuntu 12.04或14.04，请运行：

```bash
sudo restart network-manager
```

之后，可以安装和配置dnsmasq：

```bash
sudo apt-get install dnsmasq
```

将**/etc/dnsmasq.conf**替换为以下配置：

```
# 在内部网络上监听DNS请求
interface=eth1
bind-interfaces
# 作为DHCP服务器，为客户端分配IP地址
dhcp-range=192.168.3.10,192.168.3.100,96h
# 广播网关和dns服务器信息
dhcp-option=option:router,192.168.3.1
dhcp-option=option:dns-server,192.168.3.1
```

应用更改：

如果是Ubuntu 16.04或更新版本：

```bash
sudo systemctl restart dnsmasq
```

如果是Ubuntu 12.04或14.04：

```bash
sudo service dnsmasq restart
```

内部虚拟网络中的**被代理机器**现在应该通过DHCP接收IP地址：

{{< figure src="/transparent-vms/step2_proxied_vm.png" >}}

## 3. 将流量重定向到mitmproxy

要将流量重定向到mitmproxy，我们需要启用IP转发并添加两条iptables规则：

```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 8080
sudo iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 443 -j REDIRECT --to-port 8080
```

## 4. 运行mitmproxy

最后，我们可以在透明模式下运行mitmproxy：

```bash
mitmproxy --mode transparent
```

被代理的机器不能泄漏HTTP或DNS请求之外的任何数据。如果需要，您现在可以[在被代理机器上安装mitmproxy证书]({{< relref "/concepts/certificates" >}})。 