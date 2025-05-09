---
title: "mitmproxy.addonmanager 模块"
url: "zh/api/mitmproxy/addonmanager.html"
menu: api
---

# mitmproxy.addonmanager 模块

此模块包含管理mitmproxy插件的核心功能。插件是mitmproxy功能扩展的基础机制。

## 主要组件

以下是一些重要的类和组件：

- **AddonManager**: 负责插件的注册、事件分发和管理
- **Loader**: 在插件加载过程中用于注册选项和命令

## 常用属性和方法

### AddonManager

- `add(addons)`: 添加一个或多个插件
- `remove(addons)`: 移除一个或多个插件
- `get(name)`: 按名称获取插件
- `has_addon(addon)`: 检查特定插件是否已注册
- `trigger(event_name, *args, **kwargs)`: 触发命名事件

### Loader

- `add_option(name, typespec, default, help, choices=None)`: 添加配置选项
- `add_command(path, func)`: 添加命令

当您开发自己的插件时，您将主要通过事件钩子与AddonManager交互。常见的事件钩子包括`request`、`response`、`clientconnect`等。 