---
title: "安装"
weight: 2
aliases:
  - /overview-installation/
---

# 安装

请按照您的操作系统的步骤进行操作。

## macOS

在macOS上安装mitmproxy的推荐方法是使用[Homebrew](https://brew.sh/)：

```bash
brew install --cask mitmproxy
```

或者，您可以在[mitmproxy.org](https://mitmproxy.org/)上下载独立的二进制文件。

## Linux

在Linux上安装mitmproxy的推荐方法是在[mitmproxy.org](https://mitmproxy.org/)上下载独立的二进制文件。

一些Linux发行版通过其原生软件包存储库提供社区支持的mitmproxy软件包（例如，Arch Linux、Debian、Ubuntu、Kali Linux、OpenSUSE等）。我们不参与下游打包工作的维护，它们常常滞后于当前的mitmproxy版本。请直接联系存储库维护者解决原生软件包的问题。

## Windows

要在Windows上安装mitmproxy，请从[mitmproxy.org](https://mitmproxy.org/)下载安装程序。我们还提供独立的二进制文件，它们启动需要更长的时间，因为一些文件需要先提取到临时目录。安装后，mitmproxy、mitmdump和mitmweb也会添加到您的PATH中，可以从命令行调用。

我们强烈建议[安装Windows Terminal](https://aka.ms/terminal)以改进控制台界面的渲染。

所有的mitmproxy工具也支持在[WSL（Windows Subsystem for Linux）](https://docs.microsoft.com/en-us/windows/wsl/about)下运行。在[安装WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)后，请按照Linux的mitmproxy安装说明进行操作。

## 高级安装

### 开发设置

如果您想直接从源代码或GitHub主分支安装mitmproxy，请参阅我们在GitHub上的[CONTRIBUTING.md](https://github.com/mitmproxy/mitmproxy/blob/main/CONTRIBUTING.md)。

### 从Python包索引（PyPI）安装

如果您的mitmproxy插件需要安装额外的Python包，您可以从[PyPI](https://pypi.org/project/mitmproxy/)安装mitmproxy。

虽然有很多选择[^1]，但我们推荐使用pipx进行安装：

[^1]: 如果您熟悉Python生态系统，您可能知道有很多方法可以安装Python包。大多数方法（pip、virtualenv、pipenv等）应该可以正常工作，但我们没有能力为其提供支持。

1. 安装最新版本的Python（我们至少需要3.12）。
2. 安装[pipx](https://pipxproject.github.io/pipx/)。
3. `pipx install mitmproxy`

要安装额外的Python包，请运行`pipx inject mitmproxy <您的包名>`。

### Docker镜像

您可以使用[DockerHub](https://hub.docker.com/r/mitmproxy/mitmproxy/)上的官方mitmproxy镜像。

### 二进制包的安全考虑

我们预编译的二进制包和Docker镜像包含一个自包含的Python 3环境、OpenSSL的最新版本以及其他本来很麻烦需要编译和安装的依赖项。

二进制包中的依赖项在发布时被冻结，不能就地更新。这意味着我们必然会捕获可能存在的任何错误或安全问题。我们通常不会仅仅为了更新依赖项而发布新的二进制包（尽管如果我们意识到真正严重的问题，我们可能会这样做）。如果您使用我们的二进制包，请确保定期更新，以确保一切保持最新状态。

作为一般原则，mitmproxy不会"回电"，因此不会进行任何更新检查。 