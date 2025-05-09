---
title: "入门指南"
weight: 3
aliases:
  - /overview-getting-started/
---

# 入门指南

我们假设您已经在您的机器上[安装]({{< relref "/overview/installation">}})了mitmproxy。

## 启动您需要的工具

您可以从命令行/终端启动我们的三种工具中的任何一种。

* **mitmproxy** 提供交互式命令行界面
* **mitmweb** 提供基于浏览器的图形界面
* **mitmdump** 提供非交互式终端输出

## 配置您的浏览器或设备

默认情况下，mitmproxy作为[普通HTTP代理]({{< relref "/concepts/modes#regular-proxy">}})启动，并监听`http://localhost:8080`。

您需要配置您的浏览器或设备，将所有流量通过mitmproxy路由。浏览器版本和配置选项经常变更，因此我们建议您简单地在网上搜索如何为您的系统配置HTTP代理。一些操作系统有全局设置，一些浏览器有自己的设置，其他应用程序使用环境变量等。

您可以通过浏览http://mitm.it来检查您的网络流量是否通过mitmproxy - 它应该向您展示一个[简单页面]({{< relref "/concepts/certificates#quick-setup">}})来安装mitmproxy证书颁发机构 - 这也是下一步。按照您的操作系统/系统的说明安装CA证书。

## 验证一切正常工作

在这一点上，您正在运行的mitmproxy实例应该已经显示来自您客户端的第一批HTTP流量。您可以通过浏览https://mitmproxy.org来测试所有TLS加密的网络流量是否按预期工作 - 它应该显示为新的流量，您可以检查它。

## 资源

* [**GitHub**](https://github.com/mitmproxy/mitmproxy): 如果您想提问使用问题、贡献代码给mitmproxy或提交错误报告，请使用GitHub。 