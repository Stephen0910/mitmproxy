---
title: "在苹果GameCenter设置高分"
weight: 2
aliases:
  - /tute-highscores/
---

# 在苹果Game Center设置高分

## 设置

在本教程中，我将向您展示使用mitmproxy创造性地干预苹果Game Center流量是多么简单。首先，[安装mitmproxy根证书]({{< relref "/concepts/certificates" >}})。然后在您的桌面上启动mitmproxy，并配置iPhone使用它作为代理。

## 查看Game Center流量

让我们先看一下Game Center流量。我在本教程中使用的游戏是[Super Mega Worm](https://itunes.apple.com/us/app/super-mega-worm/id388541990?mt=8) - 一款很棒的iPhone复古末日横版游戏：

{{< figure src="/tute-highscores/supermega.png" >}}

完成一局游戏后（慢慢来），观察通过mitmproxy的流量：

{{< figure src="/tute-highscores/one.png" >}}

我们看到了一些可能预期的内容 - 初始化、排行榜的检索等。然后，在最后，有一个POST请求发送到这个诱人的URL：

```
https://service.gc.apple.com/WebObjects/GKGameStatsService.woa/wa/submitScore
```

提交的内容特别有趣：

```xml
<plist version="1.0">
  <dict>
    <key>scores</key>
    <array>
      <dict>
        <key>category</key>
        <string>SMW_Adv_USA1</string>
        <key>context</key>
        <integer>0</integer>
        <key>score-value</key>
        <integer>55</integer>
        <key>timestamp</key>
        <integer>1363515361321</integer>
      </dict>
    </array>
  </dict>
</plist>
```

这是一个[属性列表](https://en.wikipedia.org/wiki/Property_list)，包含游戏的标识符、得分（在本例中为55）和时间戳。看起来很容易修改。

## 修改和重放得分提交

让我们编辑得分提交。首先，在mitmproxy中选择它，然后按<span data-role="kbd">enter</span>查看它。确保您正在查看请求，而不是响应 - 您可以使用<span data-role="kbd">tab</span>在两者之间切换。现在按<span data-role="kbd">e</span>进行编辑。系统会提示您要更改请求的哪个部分 - 按<span data-role="kbd">r</span>表示原始正文。您首选的编辑器（从EDITOR环境变量中获取）现在将启动。让我们把分数提高到更有野心的水平：

```xml
<plist version="1.0">
  <dict>
    <key>scores</key>
    <array>
      <dict>
        <key>category</key>
        <string>SMW_Adv_USA1</string>
        <key>context</key>
        <integer>0</integer>
        <key>score-value</key>
        <integer>2200272667</integer>
        <key>timestamp</key>
        <integer>1363515361321</integer>
      </dict>
    </array>
  </dict>
</plist>
```

保存文件并退出编辑器。

最后一步是重放这个修改后的请求。只需按<span data-role="kbd">r</span>进行重放。

## 辉煌的结果和一些有趣的发现

{{< figure src="/tute-highscores/leaderboard.png" >}}

就是这样 - 根据记录，我是有史以来最伟大的Super Mega Worm玩家。

这个故事有一个奇怪的补充。当我第一次写这个教程时，所有顶级选手的分数都是相同的：2,147,483,647（现在情况已不再如此，因为现在有太多使用本教程的作弊者）。如果您认为这个数字看起来很熟悉，您是对的：它是2^31-1，可以放入有符号32位整数的最大值。现在让我告诉您另一个关于Super Mega Worm的奇怪事情 - 在每局游戏结束时，它会向Game Center提交您之前的最高分数，而不是当前分数。这意味着它在某处存储了您的最高分，我猜它将该存储的分数读回到一个有符号整数中。所以，如果您**通过**相对普通的方式作弊，即修改越狱手机上保存的分数，那么2^31-1可能是您能获得的最高分数。另一方面，如果游戏本身在有符号的32位整数中存储其分数，您可以通过完美的游戏获得相同的分数，从而有效地打败游戏。那么，在这种情况下，到底是哪种情况？我将由您自己决定。 