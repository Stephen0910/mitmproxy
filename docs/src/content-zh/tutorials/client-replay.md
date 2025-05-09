---
title: "客户端回放"
weight: 1
aliases:
  - /tute-clientreplay/
---

# 客户端回放：30秒示例

我常去的本地咖啡厅提供了一个摇摇欲坠且不可靠的无线网络，这是由我们市政府慷慨地用纳税人的钱赞助的。连接后，您会被重定向到一个SSL保护的页面，提示您输入用户名和密码。一旦输入了您的详细信息，您就可以自由地享受间歇性断线、蜗牛般的速度和配置错误的透明代理。

我倾向于在第一时间自动化这类事情，基于这样的理论：现在花费的时间从长远来看会得到更多回报。在这种情况下，我可能会使用[Firebug](https://getfirebug.com/)来找出表单提交参数和目标URL，然后打开编辑器，使用Python的[urllib](https://docs.python.org/library/urllib.html)编写一个小脚本来模拟提交。这需要很多繁琐的工作。使用mitmproxy，我们可以在字面上的30秒内完成这项工作，而不必担心任何细节。以下是方法。

## 1. 运行mitmdump将HTTP会话记录到文件中。

```bash
mitmdump -w wireless-login
```

## 2. 将浏览器指向mitmdump实例。

Firefox有一个名为[FoxyProxy](https://addons.mozilla.org/fi/firefox/addon/foxyproxy-standard/)的插件，可以让您快速切换到mitmproxy并从中切换出来。我假设您已经[使用mitmproxy的SSL证书颁发机构配置了浏览器]({{< relref "/concepts/certificates" >}})。

## 3. 像往常一样登录

就这样！您现在在wireless-login文件中有了登录过程的序列化版本，您可以随时像这样回放它：

```bash
mitmdump -C wireless-login
```

## 改进

到此为止我们实际上已经完成了，但如果我们想的话，可以做一些改进。我使用[wicd](https://launchpad.net/wicd)自动加入我经常使用的无线网络，它允许我指定连接后要运行的命令。我使用上面的客户端回放命令，瞧！- 完全免提的无线网络启动。

我们可能还想修剪掉那些下载CSS、JS、图像等的请求。这些只会增加回放的几分钟时间，但它们并不是真正需要的，我总觉得有必要修剪它们。因此，我们在序列化的会话上启动mitmproxy控制台工具，如下所示：

```bash
mitmproxy -r wireless-login
```

现在我们可以通过使用键盘快捷键<span data-role="kbd">d</span>手动删除我们想要修剪的所有内容。完成后，我们使用<span data-role="kbd">w</span>将会话保存回文件。 