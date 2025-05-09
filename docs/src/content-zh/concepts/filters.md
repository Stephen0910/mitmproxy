---
title: "过滤器表达式"
weight: 4
aliases:
  - /concepts-filters/
---

# 过滤器表达式

mitmproxy工具中的许多命令都使用过滤器表达式。过滤器表达式由以下运算符组成：

{{< readfile file="/generated/filters.html" >}}

- 正则表达式是Python风格的。
- 正则表达式可以指定为引号字符串。
- 正则表达式默认不区分大小写。[^1]
- 头部匹配(~h, ~hq, ~hs)是针对"name: value"形式的字符串。
- 没有运算符的字符串将匹配请求URL。
- 默认的二元运算符是&。

[^1]: 可以通过设置环境变量`MITMPROXY_CASE_SENSITIVE_FILTERS=1`来禁用此功能。

## 视图流选择器

在交互式环境中，mitmproxy有一套方便的流选择器，可以在当前视图中操作：

<table class="table filtertable"><tbody>
<tr><th>@all</th><td>所有流量</td></tr>
<tr><th>@focus</th><td>当前焦点所在的流量</td></tr>
<tr><th>@shown</th><td>当前显示的所有流量</td></tr>
<tr><th>@hidden</th><td>当前隐藏的所有流量</td></tr>
<tr><th>@marked</th><td>所有标记的流量</td></tr>
<tr><th>@unmarked</th><td>所有未标记的流量</td></tr>
</tbody></table>

这些选择器经常用于命令和键绑定中。

## 示例

URL包含"google.com"：

    google\.com

请求主体包含字符串"test"的请求：

    ~q ~b test

除了内容类型为text/html的请求之外的任何内容：

    !(~q & ~t "text/html")

替换请求中的整个GET字符串（需要引号才能使其工作）：

    ":~q ~m GET:.*:/replacement.html" 