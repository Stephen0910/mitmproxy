---
title: "代理模式"
weight: 2
aliases:
  - /concepts-modes/
---

# 代理模式

mitmproxy支持不同的代理模式来捕获流量。
您可以将任何模式与任何mitmproxy工具（mitmproxy、mitmweb或mitmdump）一起使用。


### 推荐模式

- [常规代理](#常规代理): 默认模式。配置您的客户端使用HTTP(S)代理。
- [本地捕获](#本地捕获): 捕获同一设备上的应用程序流量。
- [WireGuard](#wireguard): 捕获外部设备或单个Android应用的流量。
- [反向代理](#反向代理): 将mitmproxy放在服务器前面。

### 高级模式

- [透明代理](#透明代理): 使用自定义网络路由捕获流量。
- [TUN接口](#tun接口): 创建虚拟网络设备来捕获流量。
- [上游代理](#上游代理): 链接两个HTTP(S)代理。
- [SOCKS代理](#socks代理): 运行SOCKS5代理服务器。
- [DNS服务器](#dns服务器): 运行可编程DNS服务器。


## 常规代理

Mitmproxy的常规模式是最简单且最稳健的设置方式。
如果您的目标可以配置为使用HTTP代理，我们建议您从这里开始。

1. 启动`mitmproxy`、`mitmdump`或`mitmweb`。您不需要传递任何参数。
2. 通过显式设置HTTP代理来配置您的客户端使用mitmproxy。默认情况下，mitmproxy监听8080端口。
3. 快速检查：您应该已经能够通过代理访问未加密的HTTP站点。
4. 打开魔法域名**mitm.it**并为您的设备安装证书。

### 故障排除

1. 如果您在mitmproxy中看不到任何流量，请打开mitmproxy的事件日志。
   您应该在那里看到`client connect`消息。
   如果您没有看到`client connect`消息，那么您的客户端根本无法到达代理：
      - 您可能配置错了IP地址或端口。
      - 或者您的无线网络可能使用了_客户端隔离_功能，
        这会阻止客户端之间相互通信。
2. 有些应用程序会绕过操作系统的HTTP代理设置 -
   Android应用程序是一个常见的例子。在这些情况下，您需要
   使用mitmproxy的[WireGuard](#wireguard)、[本地捕获](#本地捕获)或[透明](#透明代理)模式。

#### 网络拓扑

如果您正在代理外部设备，您的网络可能看起来像这样：

{{< figure src="/schematics/proxy-modes-regular.png" >}}

方括号表示源和目标IP地址。
您的客户端显式连接到mitmproxy，而mitmproxy显式
连接到目标服务器。


## 本地捕获

本地捕获模式透明地捕获来自同一设备上运行的应用程序的流量。
您可以捕获当前设备上的所有流量，或者只捕获特定进程名称或进程ID（PID）的流量：

```shell
mitmproxy --mode local       # 拦截此机器上的所有流量
mitmproxy --mode local:curl  # 仅拦截cURL的流量
mitmproxy --mode local:42    # 仅拦截PID为42的进程流量
```

本地捕获使用低级操作系统API实现，因此拦截是透明的，目标
应用程序不会意识到被代理。

如果您对实现细节感兴趣，请查看
[公告博客文章](https://mitmproxy.org/tags/local-capture/)。本地捕获在Windows、Linux和macOS上都可用。

#### 拦截规范

可以通过在目标选择前加上感叹号来否定选择：

```shell
mitmproxy --mode local:!curl  # 拦截此机器上除cURL外的所有流量
```

也可以提供逗号分隔的列表：

```shell
mitmproxy --mode local:curl,wget    # 仅拦截cURL和wget的流量
mitmproxy --mode local:!curl,!wget  # 拦截除cURL和wget外的所有流量
```

#### Linux上的本地捕获限制

- **仅出站流量：** mitmproxy将只捕获出站连接。
  对于入站连接，我们建议使用反向代理模式。
- **root权限：** 要加载BPF程序，mitmproxy需要使用`sudo`启动特权子进程。
  对于Web UI，这意味着mitmweb需要在命令行上直接使用`--mode local`启动
  以获取sudo密码提示。
- **内核兼容性：** 我们的eBPF工具需要相对较新的内核。
  我们正式支持Linux 6.8及以上版本，这与Ubuntu 22.04相匹配。
- **拦截规范：** 程序名称仅匹配前16个字符（基于内核的[TASK_COMM_LEN]）。
- **容器：** 除非容器使用主机网络，否则从容器捕获流量将失败。
  例如，容器可以使用`docker/podman run --network host`启动。
- **Windows子系统Linux（WSL 1/2）：** 不支持WSL，因为默认情况下禁用了eBPF。

[TASK_COMM_LEN]: https://github.com/torvalds/linux/blob/fbfd64d25c7af3b8695201ebc85efe90be28c5a3/include/linux/sched.h#L306

#### macOS上的本地捕获限制

- **仅出站流量：** mitmproxy将只捕获出站连接。
  对于入站连接，我们建议使用反向代理模式。

## WireGuard

在WireGuard模式下，mitmproxy启动一个WireGuard VPN服务器。设备可以使用标准WireGuard客户端
应用程序连接，mitmproxy将透明地拦截它们的流量。

1. 启动`mitmweb --mode wireguard`。
2. 在目标设备上安装WireGuard客户端。
3. 导入mitmproxy提供的WireGuard客户端配置。

不需要额外的路由配置。WireGuard服务器完全在用户空间运行，
因此在此模式下不需要管理员权限。

### 配置

#### WireGuard服务器

默认情况下，WireGuard服务器将监听`51820/udp`端口，这是WireGuard
服务器的默认端口。可以通过设置`listen_port`选项或指定明确的端口
（`--mode wireguard@51821`）来更改此设置。

WireGuard连接的加密密钥存储在
`~/.mitmproxy/wireguard.conf`中。可以使用
`--mode wireguard:path`指定自定义路径。如果
指定的文件尚不存在，将自动生成新密钥。例如，要同时连接两个客户端，
您可以运行
`mitmdump --mode wireguard:wg-keys-1.conf --mode wireguard:wg-keys-2.conf@51821`。

#### WireGuard客户端

可以将通过WireGuard隧道发送的流量限制为特定IP范围。
在这种情况下，可以将WireGuard客户端配置中的`AllowedIPs`设置
从`0.0.0.0/0`（即"通过WireGuard隧道路由*所有* IPv4流量"）更改为所需的IP
地址范围（此设置允许多个逗号分隔的值）。

对于更复杂的网络布局，可能还需要覆盖
自动检测到的`Endpoint` IP地址（即运行mitmproxy和其WireGuard服务器的主机地址）。

### 限制

#### 透明代理mitmproxy主机流量

在当前实现中，无法代理运行mitmproxy本身的主机的所有流量，
因为这会导致出站WireGuard数据包通过WireGuard隧道发送。

#### 对IPv6流量的有限支持

mitmproxy内部的WireGuard服务器支持从客户端设备接收IPv6数据包，
但对代理IPv6数据包本身的支持仍然有限。因此，生成的WireGuard客户端
配置中的`AllowedIPs`设置尚未列出任何IPv6地址。要启用对IPv6流量的不完整
支持，可以将`::/0`（即"通过WireGuard隧道路由*所有* IPv6流量"）或其他IPv6
地址范围添加到允许的IP地址列表中。


## 反向代理

```shell
mitmdump --mode reverse:https://example.com
```

在反向代理模式下，mitmproxy充当普通服务器。
客户端的请求将被转发到预先配置的目标服务器，
响应将被转发回客户端：

{{< figure src="/schematics/proxy-modes-reverse.png" >}}

### 监听端口

除DNS外，反向代理服务器默认监听8080端口（DNS使用53端口）。
要监听不同的端口，请在模式后附加`@portnumber`。您还可以
多次传递`--mode`参数，在不同端口上运行多个反向代理服务器。例如，
以下命令将在80和443端口上运行指向example.com的反向代理服务器：

```text
mitmdump --mode reverse:https://example.com@80 --mode reverse:https://example.com@443
``` 