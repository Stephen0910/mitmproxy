---
title: "自定义内容视图"
weight: 6
menu:
    addons:
        weight: 6
---

# 自定义内容视图

内容视图美化显示二进制消息数据（例如HTTP响应体），否则这些数据对人类来说会难以理解。
一些内容视图还是_交互式_的，即美化显示的表示可以被编辑，mitmproxy将重新编码为二进制消息。

## 简单示例

所有内容视图都实现了[Contentview]基类：

{{< example src="examples/addons/contentview.py" lang="py" >}}

要使用此内容视图，请将其作为常规插件加载：

```shell
mitmproxy -s examples/addons/contentview.py
```

与所有其他mitmproxy插件一样，当文件内容变化时，内容视图会热重载。
mitmproxy（不包括mitmweb）也会自动重新渲染内容视图。

有关更多详细信息，请参阅[`mitmproxy.contentviews` API文档]。


## 语法高亮

内容视图总是返回未样式化的`str`，但它们可以声明其输出匹配预定义的[`SyntaxHighlight`格式]之一。
特别是，二进制格式可能美化为YAML（或JSON）并使用YAML高亮器。

支持的格式列表目前有限，但实现基于[tree-sitter]，易于扩展（参见[`mitmproxy-highlight`包]）。

## 交互式内容视图

以下示例实现了一个交互式内容视图，允许用户对美化显示的表示进行编辑：

{{< example src="examples/addons/contentview-interactive.py" lang="py" >}}

[`mitmproxy.contentviews` API文档]: {{< relref "api/mitmproxy.contentviews.md" >}}
[Contentview]: {{< relref "api/mitmproxy.contentviews.md#Contentview" >}}
[`SyntaxHighlight`格式]: {{< relref "api/mitmproxy.contentviews.md#Contentview.syntax_highlight" >}}
[`mitmproxy-highlight`包]: https://github.com/mitmproxy/mitmproxy_rs/tree/main/mitmproxy-highlight/src
[tree-sitter]: https://tree-sitter.github.io/tree-sitter/ 