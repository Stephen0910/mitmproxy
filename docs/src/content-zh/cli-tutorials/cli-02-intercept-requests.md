---
title: "拦截请求"
weight: 2
url: /zh/mitmproxytutorial-interceptrequests/
has_asciinema: true
---

# 拦截请求

mitmproxy的一个强大功能是拦截请求。
被拦截的请求会被暂停，以便用户可以在将请求发送到服务器之前修改（或丢弃）该请求。
mitmproxy的`set intercept`命令用于配置拦截。
默认情况下，该命令绑定到快捷键`i`。

拦截*所有*请求通常不是我们想要的，因为这会不断中断您的浏览。
因此，mitmproxy期望`set intercept`的第一个参数是一个[流量过滤表达式]({{< relref "/concepts/filters" >}})，用于选择性地拦截请求。
在下面的教程中，我们使用流量过滤器`~u <regex>`，它通过将正则表达式与请求的URL匹配来过滤流量。

{{% asciicast file="mitmproxy_intercept_requests" poster="0:3" instructions=true %}}

在下一课中，您将学习在将拦截的流量发送到服务器之前对其进行修改。 