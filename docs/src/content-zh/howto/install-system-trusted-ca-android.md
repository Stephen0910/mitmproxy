---
title: "在Android模拟器上安装系统CA证书"
weight: 4
aliases:
  - /howto-install-system-trusted-ca-android/
---

# 在Android模拟器上安装系统CA证书
从Android 7开始，[应用程序会忽略用户提供的证书](https://android-developers.googleblog.com/2016/07/changes-to-trusted-certificate.html)，除非它们被配置为使用这些证书。
由于大多数应用程序不会明确选择使用用户证书，我们需要将mitmproxy的CA证书放入系统证书存储中，以避免必须修补每个我们想要监控的应用程序。

请注意，应用程序可以决定忽略系统证书存储并维护自己的CA证书。在这种情况下，您必须修补应用程序。

## 1. 先决条件

- 已安装[Android Studio/Android Sdk](https://developer.android.com/studio)（使用Linux 64位版本4.1.3进行测试）
- 已创建Android虚拟设备（AVD）。设置文档可在[此处](https://developer.android.com/studio/run/managing-avds)获取
  - AVD生产版本（标有"Google Play"的那些）将阻止您使用`adb root`。如果您需要安装Google Play，则需要使用[Magisk方法]({{< ref "#instructions-when-using-magisk" >}})。
  - AVD的代理设置已配置为使用mitmproxy。文档在[此处](https://developer.android.com/studio/run/emulator-networking#proxy)

- Android Sdk中的Emulator和adb可执行文件已添加到$PATH变量
  - emulator通常位于Linux系统上的`/home/<your_user_name>/Android/Sdk/emulator/emulator`
  - adb通常位于Linux系统上的`/home/<your_user_name>/Android/Sdk/platform-tools/adb`
  - 我将这些行添加到我的`.bashrc`中
  ``` bash
  export PATH=$PATH:$HOME/Android/Sdk/platform-tools
  export PATH=$PATH:$HOME/Android/Sdk/emulator
  ```

- 已创建Mitmproxy CA证书
  - 通常位于Linux系统上的`~/.mitmproxy/mitmproxy-ca-cert.cer`
  - 如果文件夹为空或不存在，请运行`mitmproxy`以生成证书

## 2. 重命名证书

Android中的CA证书按其哈希值的名称存储，扩展名为'0'（例如：`c8450d0d.0`）。有必要找出CA证书的哈希值并将其复制到以此哈希值为文件名的文件中。否则，Android将忽略该证书。
默认情况下，mitmproxy CA证书位于此文件中：`~/.mitmproxy/mitmproxy-ca-cert.cer`


### 指南

- 进入您的证书文件夹：`cd ~/.mitmproxy/`
- 生成哈希并复制证书：``hashed_name=`openssl x509 -inform PEM -subject_hash_old -in mitmproxy-ca-cert.cer | head -1` && cp mitmproxy-ca-cert.cer $hashed_name.0``

## 3. 将证书插入系统证书存储

现在我们必须将CA证书放入位于Android文件系统中`/system/etc/security/cacerts/`的系统证书存储中。默认情况下，`/system`分区以只读方式挂载。以下步骤描述了如何获得`/system`分区的写入权限以及如何复制在[上一步]({{< ref "#2-rename-certificate" >}})中创建的证书。

### 使用Magisk时的指南
如果您想使用生产版本（标有"Google Play"；即那些安装了Google Play的版本），您可以使用Magisk在AVD中获取root权限。
[Magisk](https://github.com/topjohnwu/Magisk)允许在您的Android设备或模拟器上获取root权限。

有关在AVD上安装Magisk的说明，请参见[此处的说明](https://github.com/shakalaca/MagiskOnEmulator)。
这些说明已在API级别30上进行了测试，但据报道可在API级别22到30以及'S'（API级别28除外）上使用。
注意：说明中提到要启动AVD。此时不要向mitmproxy提供`-http-proxy`指令。

完成后，您的模拟器将允许root权限。您可以通过运行终端模拟器并键入`su`来检查这一点。
Magisk应该会询问您是否要授予程序root权限。授予此权限后，键入`whoami`将显示`root`。

但是，安装Magisk后，您将无法再使用`-writable-system`启动模拟器。这将导致启动循环。（使用`-show-kernel`启动AVD以查看错误。）
但您可以通过将证书放入Magisk模块并安装该模块来安装mitmproxy证书。
Magisk将在启动期间负责将您的证书复制到`/system/etc/security/cacerts/`。

#### 从mitmweb下载Magisk模块
如果您运行mitmweb，您可以简单地下载Magisk模块，而不是手动制作它。
停止AVD，然后使用`-http-proxy 127.0.0.1:8080`（或您运行mitmweb代理的任何IP和端口组合）再次启动它。

然后，在AVD*内部*，启动浏览器并导航到`http://mitm.it/cert/magisk`。
系统将提示您下载`mitmproxy-magisk-module.zip`，这是您需要的Magisk模块。将该文件存储在某个位置（例如在"Downloads"中）。

然后打开Magisk，点击`Modules`并安装您的模块。

重启AVD。

#### 创建包含证书的Magisk模块
如果您不运行mitmweb，您需要自己创建一个Magisk模块。
有关Magisk模块的深入信息，请参见[此处](https://topjohnwu.github.io/Magisk/guides.html#magisk-modules)，但基本上归结为以下几点：

创建以下目录：
- `mitmproxycert`（这将是您模块的根目录）
- `mitmproxycert/com/google/android`
- `mitmproxycert/system/etc/security/cacerts`

将[步骤2]({{< ref "#2-rename-certificate" >}})中重命名的证书放入`mitmproxycert/system/etc/security/cacerts`并执行`chmod 664`。

将[https://github.com/topjohnwu/Magisk/blob/master/scripts/module_installer.sh](https://github.com/topjohnwu/Magisk/blob/master/scripts/module_installer.sh)的内容保存为本地文件`update-binary`并将其放入`mitmproxycert/com/google/android`。

创建一个名为`updater-script`的文件，仅包含字符串`#MAGISK`，并将其放入`mitmproxycert/com/google/android`。

创建一个名为`module.prop`的文件并将其放入`mitmproxycert`。该文件应包含类似以下内容：

```
id=mitmproxycert
name=MITM proxy certificate
version=1
versionCode=1
author=mitmproxycert
description=My shiny MITM proxy certificate to reveal all secrets and obtain world domination!
```

使用类似`cd ./mitmproxycert ; zip -r ./../mitmproxycert.zip ./`的命令将模块打包成zip文件，并使用`adb push ./../mitmproxycert.zip /storage/emulated/0/Download/`将其推送到正在运行的AVD。

然后转到您的AVD，打开Magisk，点击`Modules`并安装您的模块（您会在Downloads文件夹中找到它）。

重启AVD。

### 使用`-writable-system`的API级别 > 28的指南
默认情况下，`/system`分区以只读方式挂载。以下步骤描述了如何获得`/system`分区的写入权限以及如何复制在第2章中创建的证书。

从API级别29（Android 10）开始，似乎无法将"/"分区挂载为读写。Google提供了一个使用OverlayFS的[此问题的解决方法](https://android.googlesource.com/platform/system/core/+/master/fs_mgr/README.overlayfs.md)。不幸的是，在撰写本文时（2021年4月11日），此解决方法中的说明将导致您的模拟器陷入[启动循环](https://issuetracker.google.com/issues/144891973)。Stackoverflow上的一位聪明人[找到了一种方法](https://stackoverflow.com/questions/60867956/android-emulator-sdk-10-api-29-wont-start-after-remount-and-reboot)来使`/system`目录可写。

**请记住：** 如果您想使用您的证书，您必须始终使用`-writable-system`选项启动模拟器。否则，Android将加载"干净"的系统镜像。

在运行API级别29和30的模拟器上测试

 #### 指南
   - 列出您的AVD：`emulator -list-avds`（如果这产生空列表，请在Android Studio AVD管理器中创建一个新的AVD）
   - 启动所需的AVD：`emulator -avd <avd_name_here> -writable-system`（添加`-show-kernel`标志以查看内核日志）
   - 以root身份重启adb：`adb root`
   - 禁用安全启动验证：`adb shell avbctl disable-verification`
   - 重启设备：`adb reboot`
   - 以root身份重启adb：`adb root`
   - 将分区重新挂载为读写：`adb remount`。（如果adb告诉您需要重启，请再次重启`adb reboot`并再次运行`adb remount`。）
   - 推送您在[步骤2]({{< ref "#2-rename-certificate" >}})中重命名的证书：`adb push <path_to_certificate> /system/etc/security/cacerts`
   - 设置证书权限：`adb shell chmod 664 /system/etc/security/cacerts/<name_of_pushed_certificate>`
   - 重启设备：`adb reboot`

### 使用`-writable-system`的API级别 <= 28的指南

在运行API级别26、27和28的模拟器上测试

**请记住：** 如果您想使用您的证书，您必须始终使用`-writable-system`选项启动模拟器。否则，Android将加载"干净"的系统镜像。

   - 列出您的AVD：`emulator -list-avds`（如果这产生空列表，请在Android Studio AVD管理器中创建一个新的AVD）
   - 启动所需的AVD：`emulator -avd <avd_name_here> -writable-system`（添加`-show-kernel`标志以查看内核日志）
   - 以root身份重启adb：`adb root`
   - 将分区重新挂载为读写：`adb remount`。（如果adb告诉您需要重启，请再次重启`adb reboot`并再次运行`adb remount`。）
   - 推送您在[步骤2]({{< ref "#2-rename-certificate" >}})中重命名的证书：`adb push <path_to_certificate> /system/etc/security/cacerts`
   - 设置证书权限：`adb shell chmod 664 /system/etc/security/cacerts/<name_of_pushed_certificate>`
   - 重启设备：`adb reboot`

### 测试您的证书是否从系统证书存储中加载

在您的AVD中，转到设置 → 安全 → 高级 → 加密与凭据 → 受信任的凭据。在列表中找到您的证书（默认名称为`mitmproxy`）。 