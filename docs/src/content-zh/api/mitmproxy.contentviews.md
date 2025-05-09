---
title: "mitmproxy.contentviews 模块"
url: "zh/api/mitmproxy/contentviews.html"
menu: api
---

# mitmproxy.contentviews 模块

此模块包含用于美化显示HTTP消息内容的功能。内容视图帮助用户以更易读的方式查看二进制数据，如JSON、XML等。

以下是一些重要的类和组件：

- **Contentview**: 所有内容视图的基类
- **ViewResult**: 表示内容视图渲染的结果
- **format_text**, **format_json** 等函数: 用于格式化特定类型的内容

在mitmproxy 12中，内容视图API进行了简化，使其更易于使用和扩展。

请参考下面的英文API文档获取详细信息：

{{< readfile file="/generated/api/mitmproxy/contentviews.html" >}} 