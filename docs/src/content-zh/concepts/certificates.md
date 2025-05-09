---
title: "证书"
weight: 3
aliases:
  - /concepts-certificates/
---

# 关于证书

Mitmproxy可以即时解密加密流量，只要客户端信任mitmproxy内置的证书颁发机构。通常这意味着需要在客户端设备上安装mitmproxy的CA证书。

## 快速设置

安装mitmproxy CA证书最简单的方法是使用内置的证书安装应用。首先启动mitmproxy并为目标设备配置正确的代理设置。然后在设备上启动浏览器，访问魔法域名[mitm.it](http://mitm.it/)。您应该会看到类似下面的界面：

{{< figure src="/certinstall-webapp.png" class="has-border" >}}

点击相关图标，按照您所使用平台的设置说明进行操作，然后您就可以开始使用了。

## mitmproxy证书颁发机构

首次运行mitmproxy时，它会在配置目录（默认为`~/.mitmproxy`）中创建证书颁发机构(CA)的密钥。这个CA用于即时生成每个访问网站的临时证书。由于您的浏览器默认不信任mitmproxy CA，您要么需要在每个域上点击通过TLS证书警告，要么一次性安装CA证书使其受信任。

以下文件会被创建：

| 文件名                | 内容                                               |
| --------------------- | -------------------------------------------------- |
| mitmproxy-ca.pem      | PEM格式的证书**和私钥**。                          |
| mitmproxy-ca-cert.pem | PEM格式的证书。在大多数非Windows平台上使用此文件。 |
| mitmproxy-ca-cert.p12 | PKCS12格式的证书。在Windows上使用。                 |
| mitmproxy-ca-cert.cer | 与.pem相同的文件，但使用一些Android设备期望的扩展名。|

出于安全原因，mitmproxy CA在首次启动时是唯一生成的，不会在不同设备上的mitmproxy安装之间共享。这确保其他mitmproxy用户无法拦截您的流量。

### 手动安装mitmproxy CA证书

有时使用[快速安装应用](#快速设置)不是一个选项，您需要手动安装CA。下面是一些常见平台的手动证书安装文档链接。mitmproxy CA证书在首次启动mitmproxy后位于`~/.mitmproxy`目录。

- 命令行中的curl:  
  `curl --proxy 127.0.0.1:8080 --cacert ~/.mitmproxy/mitmproxy-ca-cert.pem https://example.com/`
- 命令行中的wget:  
  `wget -e https_proxy=127.0.0.1:8080 --ca-certificate ~/.mitmproxy/mitmproxy-ca-cert.pem https://example.com/`
- [macOS](https://support.apple.com/guide/keychain-access/add-certificates-to-a-keychain-kyca2431/mac)
- [macOS (自动化)](https://www.dssw.co.uk/reference/security.html):
  `sudo security add-trusted-cert -d -p ssl -p basic -k /Library/Keychains/System.keychain ~/.mitmproxy/mitmproxy-ca-cert.pem`
- [Ubuntu/Debian]( https://askubuntu.com/questions/73287/how-do-i-install-a-root-certificate/94861#94861)
- [Fedora](https://docs.fedoraproject.org/en-US/quick-docs/using-shared-system-certificates/#proc_adding-new-certificates)
- [Arch Linux](https://wiki.archlinux.org/title/Transport_Layer_Security#Add_a_certificate_to_a_trust_store)
- [Mozilla Firefox](https://wiki.mozilla.org/MozillaRootCertificate#Mozilla_Firefox)
- [Linux上的Chrome](https://stackoverflow.com/a/15076602/198996)
- [iOS](http://jasdev.me/intercepting-ios-traffic)  
  在最新的iOS版本上，您还需要为mitmproxy根证书启用完全信任：
    1. 前往设置 > 通用 > 关于本机 > 证书信任设置。
    2. 在"启用完全信任的根证书"下，打开对mitmproxy证书的信任。
- iOS模拟器
  1. 确保运行模拟器的macOS机器已在其网络设置中配置使用mitmproxy。
  2. 在模拟器上打开Safari并访问`mitm.it`下载iOS证书。
  3. 导航至设置 > 通用 > VPN和设备管理以安装证书。
  4. 前往设置 > 关于本机 > 证书信任设置并启用对已安装根证书的信任。
- [Java](https://docs.oracle.com/cd/E19906-01/820-4916/geygn/index.html):  
  `sudo keytool -importcert -alias mitmproxy -storepass changeit -keystore $JAVA_HOME/lib/security/cacerts -trustcacerts -file ~/.mitmproxy/mitmproxy-ca-cert.pem`
- [Android/Android模拟器](http://wiki.cacert.org/FAQ/ImportRootCert#Android_Phones_.26_Tablets)
- [Windows](https://web.archive.org/web/20160612045445/http://windows.microsoft.com/en-ca/windows/import-export-certificates-private-keys#1TC=windows-7)
- [Windows (自动化)](https://technet.microsoft.com/en-us/library/cc732443.aspx):  
  `certutil -addstore root mitmproxy-ca-cert.cer`

### 上游证书嗅探

当mitmproxy接收到建立TLS的请求（以ClientHello消息的形式）时，它会暂停客户端连接，首先连接到上游服务器以"嗅探"其TLS证书的内容。获取的信息——通用名称、组织、主题备用名称——然后用于即时生成一个新的拦截证书，由mitmproxy CA签名。然后mitmproxy返回客户端，并使用新伪造的证书继续握手。

上游证书嗅探默认是开启的，可以通过关闭`upstream_cert`选项来禁用。

### 证书固定

一些应用程序使用[证书固定](https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning)来防止中间人攻击。这意味着如果不修改这些应用程序，它们将不会接受**mitmproxy**的证书。如果这些连接的内容不重要，建议使用[ignore_hosts]({{< relref "/howto/ignore-domains">}})功能来防止**mitmproxy**拦截到这些特定域的流量。如果您想拦截固定连接，您需要手动修补应用程序。对于Android和（越狱的）iOS设备，存在各种工具来实现这一点：

 - [apk-mitm](https://github.com/shroudedcode/apk-mitm)是一个CLI应用程序，可自动从Android APK文件中移除证书固定。
 - [objection](https://github.com/sensepost/objection)是一个由Frida提供支持的运行时移动探索工具包，支持iOS和Android上的证书固定绕过。
 - [ssl-kill-switch2](https://github.com/nabla-c0d3/ssl-kill-switch2)是一个用于在iOS和macOS应用程序中禁用证书固定的黑盒工具。
 - [android-unpinner](https://github.com/mitmproxy/android-unpinner)修改Android APK以注入Frida和HTTP Toolkit的解除固定脚本。

*请使用本页右上角的"在GitHub上编辑"按钮提议其他有用工具。*

## 使用自定义服务器证书

您可以通过向mitmproxy传递`--certs [domain=]path_to_certificate`选项来使用自己的（叶）证书。mitmproxy然后使用提供的证书来拦截指定域，而不是生成由其自己的CA签名的证书。

证书文件应为PEM格式。您可以在叶证书下方直接包含中间证书，以便您的PEM文件大致如下所示：

    -----BEGIN PRIVATE KEY-----
    <私钥>
    -----END PRIVATE KEY-----
    -----BEGIN CERTIFICATE-----
    <证书>
    -----END CERTIFICATE-----
    -----BEGIN CERTIFICATE-----
    <中间证书（可选）>
    -----END CERTIFICATE-----

例如，您可以使用以下说明生成这种格式的证书：

```bash
openssl genrsa -out cert.key 2048
# （将mitm域指定为通用名称，例如\*.google.com）
openssl req -new -x509 -key cert.key -out cert.crt
cat cert.key cert.crt > cert.pem
```

现在，您可以使用生成的证书运行mitmproxy：

**对于所有域名**

```bash
mitmproxy --certs *=cert.pem
```

**对于特定域名**

```bash
mitmproxy --certs *.example.com=cert.pem
```

**注意：** `*.example.com`适用于所有子域名。您也可以使用`www.example.com`来指定特定子域名。

## 使用自定义证书颁发机构

默认情况下，mitmproxy将使用`~/.mitmproxy/mitmproxy-ca.pem`作为证书颁发机构，为所有未提供自定义证书的域生成证书（见上文）。您可以通过向mitmproxy传递`--set confdir=DIRECTORY`选项来使用自己的证书颁发机构。mitmproxy然后将在指定目录中查找`mitmproxy-ca.pem`。如果不存在这样的文件，它将自动生成。

`mitmproxy-ca.pem`证书文件大致应该如下所示：

    -----BEGIN PRIVATE KEY-----
    <私钥>
    -----END PRIVATE KEY-----
    -----BEGIN CERTIFICATE-----
    <证书>
    -----END CERTIFICATE-----

当使用`openssl x509 -noout -text -in ~/.mitmproxy/mitmproxy-ca.pem`查看证书时，它至少应具有以下X509v3扩展，以便mitmproxy可以使用它来生成证书：

    X509v3 extensions:
        X509v3 Key Usage: critical
            Certificate Sign
        X509v3 Basic Constraints: critical
            CA:TRUE

例如，使用OpenSSL时，您可以按如下方式创建CA权限：

```shell
openssl req -x509 -new -nodes -key ca.key -sha256 -out ca.crt -addext keyUsage=critical,keyCertSign
cat ca.key ca.crt > mitmproxy-ca.pem
``` 