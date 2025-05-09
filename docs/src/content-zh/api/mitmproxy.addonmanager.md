---
title: "mitmproxy.addonmanager 模块"
url: "zh/api/mitmproxy/addonmanager.html"
menu: api
---

# mitmproxy.addonmanager 模块

此模块包含管理mitmproxy插件的核心功能。插件是mitmproxy功能扩展的基础机制。

以下是一些重要的类和组件：

- **AddonManager**: 负责插件的注册、事件分发和管理
- **Loader**: 在插件加载过程中用于注册选项和命令

当您开发自己的插件时，您将主要通过事件钩子与AddonManager交互。

请参考下面的英文API文档获取详细信息：

{{< readfile file="/generated/api/mitmproxy/addonmanager.html" >}} 