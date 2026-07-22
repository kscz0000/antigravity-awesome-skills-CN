---
title: "rclone nfsmount"
description: "将远程作为文件系统挂载到挂载点。触发词：nfsmount、NFS 挂载、挂载、mount、文件系统挂载、FUSE"
status: Experimental
versionIntroduced: v1.65
# 自动生成 - 请勿编辑，如有修改请编辑 cmd/nfsmount/ 中的源代码，并在发布时运行 "make commanddocs"
---

> **官方文档：** [https://rclone.org/commands/rclone_nfsmount/](https://rclone.org/commands/rclone_nfsmount/)
# rclone nfsmount

将远程作为文件系统挂载到挂载点。

## 概要

Rclone nfsmount 允许 Linux、FreeBSD、macOS 和 Windows
通过 FUSE 将任意 Rclone 云存储系统挂载为文件系统。

首先使用 `rclone config` 设置你的远程。可用 `rclone ls` 等命令检查其是否正常工作。

在 Linux 和 macOS 上，你可以以前台或后台（即守护进程）模式运行 mount。mount 默认以前台模式运行。使用 `--daemon` 参数
强制后台模式。在 Windows 上，mount 只能以前台模式运行，该参数会被忽略。

在后台模式下，rclone 充当通用的 Unix mount 程序：主程序启动后，
派生后台 rclone 进程来建立和维护挂载，等待直至成功或超时，
并以适当的退出码退出（如果失败则终止子进程）。

在 Linux/macOS/FreeBSD 上，按以下方式启动挂载，其中 `/path/to/local/mount`
是一个**空的**且**已存在**的目录：

```console
rclone nfsmount remote:path/to/files /path/to/local/mount
```

在 Windows 上，你可以用不同方式启动挂载。详见[下文](#mounting-modes-on-windows)。
如果交互式地从控制台窗口使用前台挂载，rclone 将为该挂载提供服务
并占用控制台，因此应使用另一个窗口来处理该挂载，直至 rclone
被中断（例如按 Ctrl-C）。

以下示例将挂载到自动分配的驱动器、特定的盘符 `X:`、路径 `C:\path\parent\mount`
（其中父目录或驱动器必须存在，且 mount **不得**存在，
且在[作为网络驱动器挂载](#mounting-modes-on-windows)时不支持），
最后一个示例将作为网络共享 `\\cloud\remote` 挂载并将其映射到
自动分配的驱动器：

```console
rclone nfsmount remote:path/to/files *
rclone nfsmount remote:path/to/files X:
rclone nfsmount remote:path/to/files C:\path\parent\mount
rclone nfsmount remote:path/to/files \\cloud\remote
```

当前台模式下的程序结束时，无论是通过 Ctrl+C 还是接收到
SIGINT 或 SIGTERM 信号，挂载都应被自动停止。

在后台模式下运行时，用户必须手动停止挂载：

```console
# Linux
fusermount -u /path/to/local/mount
#... or on some systems
fusermount3 -u /path/to/local/mount
# OS X or Linux when using nfsmount
umount /path/to/local/mount
```

umount 操作可能会失败，例如当挂载点正忙时。
发生这种情况时，由用户负责手动停止挂载。

挂载的文件系统大小将根据从远程检索的信息设置，
与 [rclone about](https://rclone.org/commands/rclone_about/) 命令返回的信息相同。
具有无限存储的远程可能只报告已用大小，
此时假定还有 1 PiB 的可用空间。如果远程根本
不[支持](https://rclone.org/overview/#optional-features) about 功能，
则将 1 PiB 同时设置为总大小和可用大小。

## 在 Windows 上安装

要在 Windows 上运行 `rclone nfsmount`，你需要
下载并安装 [WinFsp](https://winfsp.dev)。

[WinFsp](https://github.com/winfsp/winfsp) 是一个开源的
Windows 文件系统代理，它使得为 Windows 编写用户空间文件系统
变得容易。它提供了一个 FUSE 仿真层，rclone
结合 [cgofuse](https://github.com/winfsp/cgofuse) 使用。
这两个软件包都由 Bill Zissimopoulos 编写，他在
rclone nfsmount for Windows 的实现过程中给予了极大帮助。

### Windows 上的挂载模式

与其他操作系统不同，Microsoft Windows 为网络和固定驱动器提供了不同的文件系统类型。
它会在假设固定磁盘驱动器快速可靠的前提下优化访问，而网络驱动器则具有相对较高的延迟
和较低的可靠性。某些设置也可以在两种类型之间区分，
例如 Windows 资源管理器应仅显示图标，而不为网络驱动器上的
图像和视频文件创建预览缩略图。

在大多数情况下，rclone 默认会将远程作为普通固定磁盘驱动器挂载。
不过，你也可以选择将其作为远程网络驱动器挂载，
通常称为网络共享。如果你使用默认的固定驱动器模式
挂载 rclone 远程并遇到意外的程序错误、卡顿或其他问题，
请考虑改用网络驱动器方式挂载。

作为固定磁盘驱动器挂载时，你可以挂载到未使用的盘符，
或挂载到表示**已存在**父目录或驱动器中**不存在**的子目录的路径。
使用特殊值 `*` 将告诉 rclone 自动分配下一个可用的盘符，
从 Z: 开始并向前递减。示例：

```console
rclone nfsmount remote:path/to/files *
rclone nfsmount remote:path/to/files X:
rclone nfsmount remote:path/to/files C:\path\parent\mount
rclone nfsmount remote:path/to/files X:
```

选项 `--volname` 可用于为挂载的文件系统设置自定义卷名。
默认使用远程名称和路径。

要以网络驱动器方式挂载，可在你的 nfsmount 命令中添加选项 `--network-mode`。
此模式下不支持挂载到目录路径，这是 Windows 对 junction 的限制，
因此远程必须始终挂载到盘符。

```console
rclone nfsmount remote:path/to/files X: --network-mode
```

使用 `--volname` 指定的卷名将用于创建网络共享路径。
完整的 UNC 路径（如 `\\cloud\remote`）以及可选的路径
`\\cloud\remote\madeup\path` 将按原样使用。任何其他
字符串将用作共享部分，前缀为默认的 `\\server\`。
如果未指定卷名，则将使用 `\\server\share`。
当你挂载多个驱动器时，必须确保卷名是唯一的，
否则 mount 命令将失败。共享名将作为映射驱动器的卷标，
显示在 Windows 资源管理器等中，而完整的
`\\server\share` 将作为远程 UNC 路径由
`net use` 等报告，就像普通的网络驱动器映射一样。

如果使用 `--volname` 指定完整的网络共享 UNC 路径，则会
隐式设置 `--network-mode` 选项，因此以下两个示例具有相同的结果：

```console
rclone nfsmount remote:path/to/files X: --network-mode
rclone nfsmount remote:path/to/files X: --volname \\server\share
```

你也可以将网络共享 UNC 路径直接指定为挂载点本身。然后 rclone
将自动分配一个盘符，与使用 `*` 相同，并将其作为挂载点，
而将指定的 UNC 路径用作卷名，如同使用 `--volname` 选项
指定一样。这也会隐式设置 `--network-mode` 选项。
这意味着以下两个示例具有相同的结果：

```console
rclone nfsmount remote:path/to/files \\cloud\remote
rclone nfsmount remote:path/to/files * --volname \\cloud\remote
```

还有另一种启用网络模式并设置共享路径的方法，
即直接传递"原生"的 libfuse/WinFsp 选项：
`--fuse-flag --VolumePrefix=\server\share`。注意在这种情况下
路径必须使用单个反斜杠前缀。

*注意：*在早期版本的 rclone 中，这是唯一受支持的方法。

[详细了解驱动器映射](https://en.wikipedia.org/wiki/Drive_mapping)

另请参见下文的 [Limitations](#limitations) 一节。

### Windows 文件系统权限

Windows 上的 FUSE 仿真层必须在 FUSE 所使用的基于 POSIX 的权限模型
和 Windows 所使用的基于访问控制列表 (ACL) 的权限模型之间进行转换。

挂载的文件系统通常在其访问控制列表 (ACL) 中包含三个条目，
表示 POSIX 权限作用域：所有者、组和其他人。
默认情况下，所有者和组将取自当前用户，
并将内置组"Everyone"用于表示其他人。
用户/组可以通过 FUSE 选项 "UserName" 和 "GroupName" 自定义，
例如 `-o UserName=user123 -o GroupName="Authenticated Users"`。
每个条目的权限将根据 [options](#options) 中的
`--dir-perms` 和 `--file-perms` 设置，这些参数使用传统的 Unix
[数字表示法](https://en.wikipedia.org/wiki/File-system_permissions#Numeric notation)取值。

默认权限对应于 `--file-perms 0666 --dir-perms 0777`，
即每个人都有读写权限。这意味着你将无法
从挂载中启动任何程序。若要能够执行此操作，必须添加
执行权限，例如 `--file-perms 0777 --dir-perms 0777` 可为
所有人添加执行权限。如果程序需要写入文件，你可能
还需要启用 [VFS File Caching](#vfs-file-caching)（另见
[limitations](#limitations)）。请注意，默认的写权限
对所有者以外的帐户有一些限制，具体来说，它缺少
"write extended attributes"（写扩展属性）权限，这将在下文中解释。

权限的映射并不总是那么简单，你在
Windows 资源管理器中看到的结果可能并不完全符合预期。例如，当设置
包含组或其他作用域的写访问权限的值时，这将被映射为
"write attributes"（写属性）、"write data"（写数据）和
"append data"（追加数据）权限，但不包括
"write extended attributes"（写扩展属性）权限。
Windows 会将其显示为基本权限"Special"（特殊）而不是"Write"（写入），
因为"Write"还涵盖了"write extended attributes"权限。
当为组或其他作用域设置数字 0 以表示无权限时，
它们仍会获得"read attributes"（读属性）、
"read extended attributes"（读扩展属性）和
"read permissions"（读权限）这些单独的权限。
这样做是出于兼容性考虑，例如允许没有额外权限的用户
能够像在 Unix 中一样读取文件的基本元数据。

WinFsp 2021（1.9 版）引入了一个新的 FUSE 选项 "FileSecurity"，
它允许使用
[SDDL](https://docs.microsoft.com/en-us/windows/win32/secauthz/security-descriptor-string-format)
完整地指定文件安全描述符。借此你可以对结果权限进行细粒度的控制，
与使用上述 POSIX 权限相比，并且不会为了与 Unix 兼容而自动
添加任何额外的权限。以下将给出一些使用示例。

如果你设置 POSIX 权限仅允许所有者访问，
使用 `--file-perms 0600 --dir-perms 0700`，用户组和内置的
"Everyone"组仍将被授予一些特殊权限，如上所述。
一些程序可能会（错误地）将其解释为该文件对所有人可访问，
例如 SSH 客户端可能会警告"unprotected
private key file"（未受保护的私钥文件）。你可以通过指定
`-o FileSecurity="D:P(A;;FA;;;OW)"` 来解决此问题，
该设置将文件的所有访问权限 (FA) 授予所有者 (OW)，而不授予其他任何对象。

当设置写权限时，除所有者外，不包括
"write extended attributes"权限，如上所述。
这可能会阻止应用程序写入文件，并给出权限被拒绝的错误。
要为内置的"Everyone"组设置可正常工作的写权限，
类似于其默认获得的权限，但额外添加
"write extended attributes"，你可以指定
`-o FileSecurity="D:P(A;;FRFW;;;WD)"`，
该设置将文件读 (FR) 和文件写 (FW) 权限授予所有人 (WD)。
如果还需要文件执行 (FX)，则更改为
`-o FileSecurity="D:P(A;;FRFWFX;;;WD)"`，或设置文件所有访问权限 (FA)
以获得包括删除在内的完整访问权限：
`-o FileSecurity="D:P(A;;FA;;;WD)"`。

### Windows 注意事项

以管理员身份创建的驱动器对其他帐户不可见，
即使是通过用户帐户控制 (UAC) 提升为管理员的帐户也不可见。
其结果是，如果你以管理员身份从命令提示符挂载到某个盘符，
然后尝试从 Windows 资源管理器（不是以管理员身份运行）访问
同一驱动器，你将无法看到该挂载的驱动器。

如果你不需要从以管理员权限运行的应用程序访问该驱动器，
最简单的解决方法是始终从非提升的命令提示符创建挂载。

若要使映射的驱动器对创建它们的用户帐户可用，
无论该帐户是否已提升，都可以使用一个特殊的 Windows 设置
[linked connections](https://docs.microsoft.com/en-us/troubleshoot/windows-client/networking/mapped-drives-not-available-from-elevated-command#detail-to-configure-the-enablelinkedconnections-registry-entry) 来启用。

也可以通过以内置的 SYSTEM 帐户运行创建驱动器的进程，
使驱动器挂载对系统上的所有人可用。有多种方法可以做到这一点：
一种是使用命令行实用程序 [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec)，
来自 Microsoft 的 Sysinternals 套件，它具有 `-s` 选项以
SYSTEM 帐户身份启动进程。另一种替代方案是从 Windows 计划任务
或 Windows 服务运行 mount 命令，并配置为以 SYSTEM 帐户运行。
第三种替代方案是使用
[WinFsp.Launcher 基础设施](https://github.com/winfsp/winfsp/wiki/WinFsp-Service-Architecture)。
请参阅[安装文档](https://rclone.org/install/) 了解更多信息。
请注意，当以其他用户身份运行 rclone 时，它将不会使用
你配置文件中的配置文件，除非你通过
[`--config`](https://rclone.org/docs/#config-string) 选项显式告知它。
还要注意，现在拥有所有者权限的是 SYSTEM 帐户，
其他帐户将根据组或其他作用域获得权限。如上所述，
这些帐户将不会获得"write extended attributes"权限，
这可能会阻止写入文件。你可以使用 FileSecurity 选项解决此问题，
请参见上面的示例。

请注意，映射到目录路径（而不是盘符）
则不存在上述限制。

## 在 macOS 上挂载

在 macOS 上的挂载可以通过[内置 NFS 服务器](/commands/rclone_serve_nfs/)、
[macFUSE](https://osxfuse.github.io/)（也称为 osxfuse）或
[FUSE-T](https://www.fuse-t.org/) 来完成。macFUSE 是利用
macOS 内核扩展 (kext) 的传统 FUSE 驱动程序。FUSE-T 是另一种 FUSE 系统，
它通过 NFSv4 本地服务器进行"挂载"。

### Unicode 规范化

强烈建议在 macOS 上为所有 `mount` 和 `serve` 命令
保留 `--no-unicode-normalization=false` 的默认值。有关详细信息，请参阅 [vfs-case-sensitivity](https://rclone.org/commands/rclone_mount/#vfs-case-sensitivity)。

### NFS 挂载

此方法使用 [serve nfs](/commands/rclone_serve_nfs/)
命令启动一个 NFS 服务器，并将其挂载到指定的挂载点。如果你使用
|--daemon| 在后台模式下运行此命令，则需要使用
|kill| 命令向 rclone 进程发送 SIGTERM 信号以停止挂载。

请注意，`--nfs-cache-handle-limit` 控制 `nfsmount` 缓存处理程序保存的最大文件
句柄数。此值不应设得过低，否则访问文件时可能会遇到错误。
默认值为 1000000，但如果服务器的系统资源占用导致问题，可以考虑降低此限制。

### macFUSE 说明

如果使用[网站上的 dmg 软件包](https://github.com/osxfuse/osxfuse/releases)
安装 macFUSE，rclone 将自动定位 macFUSE 库，无需任何额外操作。
但是，如果使用 [macports](https://www.macports.org/) 包管理器
安装 macFUSE，则需要进行以下额外步骤。

```console
sudo mkdir /usr/local/lib
cd /usr/local/lib
sudo ln -s /opt/local/lib/libfuse.2.dylib
```

### FUSE-T 的限制、注意事项和说明

关于其工作方式，有一些限制、注意事项和说明。
这些内容对应 FUSE-T 1.0.14 版的当前情况。

#### 读取时更新 ModTime

根据 [FUSE-T wiki](https://github.com/macos-fuse-t/fuse-t/wiki#caveats)：

> 文件访问时间和修改时间无法单独设置，因为这似乎是
> NFS 客户端的一个问题，它始终会同时修改两者。可以使用
> 'touch -m' 和 'touch -a' 命令复现

这意味着，使用各种工具（特别是 macOS Finder）查看文件时，会导致
rclone 更新文件的修改时间。这可能会使 rclone 上传文件的完整新副本。

#### 只读挂载

使用 `--read-only` 挂载时，写入文件的尝试将以*静默*方式失败，
而不是像在 macFUSE 中那样出现明确的警告。

# 在 Linux 上挂载

在较新版本的 Ubuntu 上，运行 `rclone mount` 时可能会遇到以下错误：

> NOTICE: mount helper error: fusermount3: mount failed: Permission denied
> CRITICAL: Fatal error: failed to mount FUSE fs: fusermount: exit status 1
这可能是由于较新的 [Apparmor](https://wiki.ubuntu.com/AppArmor) 限制所致，
可以通过 `sudo aa-disable /usr/bin/fusermount3` 禁用
（你可能需要事先 `sudo apt install apparmor-utils`）。

## 局限性

如果未使用 `--vfs-cache-mode`，则只能顺序写入文件，
只能在读取时进行 seek。这意味着在不使用
`--vfs-cache-mode writes` 或 `--vfs-cache-mode full` 的情况下，
许多应用程序将无法在 rclone 挂载上正常使用其文件。
有关详细信息，请参阅 [VFS File Caching](#vfs-file-caching) 一节。
在 macOS 上使用 NFS 挂载时，如果不指定 |--vfs-cache-mode|，
挂载点将是只读的。

基于 bucket 的远程 - Azure Blob、Swift、S3、Google Cloud Storage 和 B2 -
无法存储空目录。其中，只有 Azure Blob、Google Cloud Storage
和 S3 可以在你添加 `--xxx-directory_markers` 时保留它们；
否则，一旦空目录退出目录缓存，它们就会消失。

在 Unix 上使用 `--daemon` 标志调用 `rclone mount` 时，主 rclone
程序将等待后台挂载就绪，或等待由 `--daemon-wait` 标志指定的超时。
在 Linux 上，它可以通过 ProcFS 检查挂载状态，因此该标志实际上设置的是
**最大**等待时间，而真实等待时间可能更短。在 macOS / BSD 上，
等待时间是固定的，且仅在最后进行检查。我们建议你在 macOS 上合理设置等待时间。

目前仅支持 Linux、FreeBSD、OS X 和 Windows。

## rclone nfsmount 与 rclone sync/copy 的对比

文件系统期望 100% 可靠，而云存储系统
距离 100% 可靠还差得很远。rclone sync/copy
命令通过大量重试来处理这一问题。然而 rclone nfsmount
无法以相同方式使用重试，除非对上传进行本地复制。
有关使 nfsmount 更可靠的解决方案，请参阅
[VFS File Caching](#vfs-file-caching)。

## 属性缓存

你可以使用 `--attr-timeout` 标志设置内核缓存
目录条目属性（大小、修改时间等）的时间。

默认值为 `1s`，即仅将文件缓存足够长的时间，
以避免内核对 rclone 的过多回调。

从理论上讲，对于那些可能在不受内核控制的情况下发生更改的文件系统，
0s 应该是正确的值。然而，这会导致一些问题，例如
[rclone 占用过多内存](https://github.com/rclone/rclone/issues/2157)、
[rclone 不向 samba 提供文件](https://forum.rclone.org/t/rclone-1-39-vs-1-40-mount-issue/5112)，
以及[列目录耗时过长](https://github.com/rclone/rclone/issues/2095#issuecomment-371141147)。

内核可以按 `--attr-timeout` 给定的时间缓存文件信息。
如果远程文件在此期间更改了长度，你可能会看到损坏现象，
表现为文件被截断，或文件末尾出现乱码。使用 `--attr-timeout 1s` 时
这种情况极少发生但并非不可能。`--attr-timeout` 设置得越高，
发生这种情况的可能性就越大。默认设置"1s"是
缓解上述问题的最低设置。

如果将其设置得更高（例如 `10s` 或 `1m`），则内核对 rclone
的回调会减少，从而提高效率，但出现上述损坏问题的
可能性也会增加。

如果远程上的文件不会在 rclone 控制之外发生更改，
则不会出现损坏问题。

这与在 mount.fuse 中设置 attr_timeout 选项的效果相同。

## 过滤器

请注意，所有 rclone 过滤器都可用于选择要在挂载中可见的
文件子集。

## systemd

将 rclone nfsmount 作为 systemd 服务运行时，
可以使用 Type=notify。在这种情况下，服务将在
挂载点成功建立后进入 started 状态。
将 rclone nfsmount 服务指定为依赖项的单元
将在此模式下立即看到所有文件和文件夹。

请注意，systemd 在没有任何环境变量（包括
`PATH` 或 `HOME`）的情况下运行 mount 单元。
这意味着波浪号（`~`）展开将不起作用，
并且你应该通过 rclone 参数显式提供 `--config` 和 `--cache-dir` 的
绝对路径。由于挂载需要 `fusermount` 或 `fusermount3` 程序，
rclone 在此场景下将使用回退的 PATH `/bin:/usr/bin`。
请确保 `fusermount`/`fusermount3` 存在于该 PATH 上。

## Rclone 作为 Unix mount 辅助程序

核心 Unix 程序 `/bin/mount` 通常接受 `-t FSTYPE` 参数，
然后运行 `/sbin/mount.FSTYPE` 辅助程序，并以
`-o key=val,...` 或 `--opt=...` 形式传递 mount 选项。
Automount（经典版或 systemd 版）行为类似。

rclone 默认期望使用 GNU 风格的标志 `--key val`。要将其作为 mount
辅助程序运行，你应该将 rclone 二进制文件符号链接到 `/sbin/mount.rclone`，
并可选地链接到 `/usr/bin/rclonefs`，例如 `ln -s /usr/bin/rclone /sbin/mount.rclone`。
rclone 将检测到这一点并相应地转换命令行参数。

现在你可以运行经典的 mount 命令，如下所示：

```console
mount sftp1:subdir /mnt/data -t rclone -o vfs_cache_mode=writes,sftp_key_file=/path/to/pem
```

或创建 systemd mount 单元：

```ini
# /etc/systemd/system/mnt-data.mount
[Unit]
Description=Mount for /mnt/data
[Mount]
Type=rclone
What=sftp1:subdir
Where=/mnt/data
Options=rw,_netdev,allow_other,args2env,vfs-cache-mode=writes,config=/etc/rclone.conf,cache-dir=/var/rclone
```

可选地附带 systemd automount 单元

```ini
# /etc/systemd/system/mnt-data.automount
[Unit]
Description=AutoMount for /mnt/data
[Automount]
Where=/mnt/data
TimeoutIdleSec=600
[Install]
WantedBy=multi-user.target
```

或者在 `/etc/fstab` 中添加如下一行

```console
sftp1:subdir /mnt/data rclone rw,noauto,nofail,_netdev,x-systemd.automount,args2env,vfs_cache_mode=writes,config=/etc/rclone.conf,cache_dir=/var/cache/rclone 0 0
```

或使用经典的 Automountd。
请记得提供显式的 `config=...,cache-dir=...` 作为变通方法，
以解决 mount 单元在没有 `HOME` 的情况下运行的问题。

rclone 在 mount 辅助程序模式下将通过逗号拆分 `-o` 参数，
将 `_` 替换为 `-`，并在前面添加 `--` 以获取命令行标志。
包含逗号或空格的选项可以用单引号或双引号括起来。
同类型引号内的内部引号应使用双引号。

Mount 选项语法包含一些特殊处理的额外选项：

- `env.NAME=VALUE` 将为 mount 进程设置一个环境变量。
  这对于不允许为 mount 辅助程序设置自定义环境的
  Automountd 和 Systemd.mount 很有帮助。
  通常你将使用 `env.HTTPS_PROXY=proxy.host:3128` 或 `env.HOME=/root`
- `command=cmount` 可用于运行 `cmount` 或任何其他 rclone 命令，
  而非默认的 `mount`。
- `args2env` 将通过环境变量而不是命令行参数将 mount 选项
  传递给在后台运行的 mount 辅助程序。这允许从 `ps` 或
  `pgrep` 等命令中隐藏密钥。
- `vv...` 将被转换为相应的 `--verbose=N`
- 标准的 mount 选项，如 `x-systemd.automount`、`_netdev`、`nosuid` 等，
  仅供 Automountd 使用，rclone 会忽略它们。

## VFS - 虚拟文件系统

此命令使用 VFS 层。它将 rclone 所使用的云存储对象
适配为看起来更像是磁盘文件系统的东西。

云存储对象具有许多不像磁盘文件的属性 -
无法扩展它们，也无法在文件中间进行写入，
因此 VFS 层必须处理这些问题。由于不存在唯一正确的方法，
下文会解释各种选项。

VFS 层还实现了目录缓存 -
它在内存中缓存有关文件和目录的信息（但不缓存数据）。

## VFS 目录缓存

使用 `--dir-cache-time` 标志，你可以控制
目录应被视为最新并从后端刷新的时间。
通过 VFS 所做的更改将立即生效或使缓存失效。

```text
    --dir-cache-time duration   Time to cache directory entries for (default 5m0s)
    --poll-interval duration    Time to wait between polling for changes. Must be smaller than dir-cache-time. Only on supported remotes. Set to 0 to disable (default 1m0s)
```

但是，如果在云存储后端通过 Web 界面或其他 rclone 副本直接进行的更改，
仅当所配置的后端不支持变更轮询时，才会在目录缓存过期后被检测到。
如果后端支持轮询，更改将在轮询间隔内被检测到。

你可以向 rclone 发送 `SIGHUP` 信号以使其刷新所有
目录缓存，无论其新旧程度。假设只有一个
rclone 实例在运行，你可以按如下方式重置缓存：

```console
kill -SIGHUP $(pidof rclone)
```

如果使用[远程控制](/rc)配置 rclone，则可以使用
rclone rc 刷新整个目录缓存：

```console
rclone rc vfs/forget
```

或者刷新单个文件或目录：

```console
rclone rc vfs/forget file=path/to/file dir=path/to/dir
```

## VFS 文件缓冲

`--buffer-size` 标志确定将用于
提前缓冲数据的内存量。

每个打开的文件将始终尝试在内存中保留指定数量的数据。
缓冲数据绑定到单个打开的文件，不会在多个打开文件之间共享。

此标志是每个打开文件所用内存的上限。
缓冲区仅为已下载但尚未读取的数据使用内存。
如果缓冲区为空，则仅使用少量内存。

rclone 用于缓冲的最大内存可达
`--buffer-size * 打开的文件数`。

## VFS 文件缓存

这些标志控制 VFS 文件缓存选项。文件缓存对于
使 VFS 层看起来与普通文件系统兼容是必需的。
可以禁用它，但代价是损失一定的兼容性。

例如，如果你想同时读写一个文件，就需要启用 VFS 缓存。
更多详细信息请参见下文。

请注意，VFS 缓存独立于缓存后端，你可能
发现需要其中之一或两者兼需。

```text
    --cache-dir string                     Directory rclone will use for caching.
    --vfs-cache-mode CacheMode             Cache mode off|minimal|writes|full (default off)
    --vfs-cache-max-age duration           Max time since last access of objects in the cache (default 1h0m0s)
    --vfs-cache-max-size SizeSuffix        Max total size of objects in the cache (default off)
    --vfs-cache-min-free-space SizeSuffix  Target minimum free space on the disk containing the cache (default off)
    --vfs-cache-poll-interval duration     Interval to poll the cache for stale objects (default 1m0s)
    --vfs-write-back duration              Time to writeback files after last use when using cache (default 5s)
```

如果使用 `-vv` 运行，rclone 将打印文件缓存的位置。
文件存储在用户缓存文件区域中，该位置因操作系统而异，
但可以通过 `--cache-dir` 或设置相应的
环境变量来控制。

缓存有 4 种不同的模式，可通过 `--vfs-cache-mode` 选择。
缓存模式越高，rclone 的兼容性越好，但代价是占用磁盘空间。

请注意，文件仅在关闭时才会被写回到远程，
并且在 `--vfs-write-back` 秒内未被访问过。
如果 rclone 在有未上传文件的情况下退出或崩溃，
这些文件将在下次使用相同标志运行 rclone 时被上传。

如果使用 `--vfs-cache-max-size` 或 `--vfs-cache-min-free-space`，
请注意缓存可能会因两个原因超出这些配额。
首先，因为仅每 `--vfs-cache-poll-interval` 检查一次。
其次，因为打开的文件无法从缓存中逐出。当
`--vfs-cache-max-size` 或 `--vfs-cache-min-free-space` 被超出时，
rclone 将尝试首先从缓存中逐出最近最少访问的文件。
rclone 将从最长时间未被访问的文件开始。
这种缓存刷新策略效率较高，更相关的文件可能仍保留在缓存中。

`--vfs-cache-max-age` 将在设定的自上次访问时间过后
将文件从缓存中逐出。默认值为 1 小时，即开始将
1 小时内未被访问的文件从缓存中逐出。当访问缓存中的文件时，
1 小时计时器将重置为 0，并再等待 1 小时后才逐出。
使用标准符号 s、m、h、d、w 指定时间。

如果使用 `--vfs-cache-mode > off`，则**不应**
使用同一 VFS 缓存运行两个 rclone 副本，且这些副本使用相同或重叠的远程。
这样做可能会导致数据损坏。你可以通过使用
`--cache-dir` 为每个 rclone 提供独立的缓存层次结构来解决此问题。
如果使用的远程不重叠，则无需担心此问题。

### --vfs-cache-mode off

在此模式（默认）下，缓存将直接从远程读取并直接写入
远程，而不在磁盘上缓存任何内容。

这意味着某些操作无法执行

- 无法以读和写两种方式打开文件
- 以写方式打开的文件无法进行 seek
- 以写方式打开的现有文件必须设置 O_TRUNC
- 以读和 O_TRUNC 方式打开的文件将以只写方式打开
- 以只写方式打开的文件将表现为已提供 O_TRUNC
- 忽略打开模式 O_APPEND、O_TRUNC
- 如果上传失败则无法重试

### --vfs-cache-mode minimal

这与"off"非常相似，只是以读和写两种方式打开的文件
将缓冲到磁盘。这意味着以写方式打开的文件将具有
更好的兼容性，但仅使用最少的磁盘空间。

这些操作无法执行

- 以只写方式打开的文件无法进行 seek
- 以写方式打开的现有文件必须设置 O_TRUNC
- 以只写方式打开的文件将忽略 O_APPEND、O_TRUNC
- 如果上传失败则无法重试

### --vfs-cache-mode writes

在此模式下，仅以读方式打开的文件仍然直接从
远程读取，而只写和读/写文件首先被缓冲到磁盘。

此模式应支持所有正常的文件系统操作。

如果上传失败，将以指数递增的间隔进行重试，
最长重试间隔为 1 分钟。

### --vfs-cache-mode full

在此模式下，所有读取和写入都通过磁盘进行缓冲。
从远程读取数据时，也会将其缓冲到磁盘。

在此模式下，缓存中的文件将是稀疏文件，rclone
将跟踪它已下载文件的哪些部分。

因此，如果应用程序仅读取每个文件的开头，则 rclone
将仅缓冲文件的开头。这些文件在缓存中看起来是
其完整大小，但它们是稀疏文件，其中仅包含
已下载的数据。

此模式应支持所有正常的文件系统操作，否则
与 `--vfs-cache-mode` writes 相同。

读取文件时，rclone 将读取 `--buffer-size` 加上
`--vfs-read-ahead` 字节。`--buffer-size` 在内存中缓冲，
而 `--vfs-read-ahead` 在磁盘上缓冲。

使用此模式时，建议不要将 `--buffer-size` 设置得
太大，并根据需要将 `--vfs-read-ahead` 设置得较大。

**重要** 并非所有文件系统都支持稀疏文件。特别是
FAT/exFAT 不支持。如果缓存目录位于不支持稀疏文件的
文件系统上，rclone 将运行得非常糟糕，并在检测到时
记录一条 ERROR 消息。

### 指纹识别

VFS 的各个部分使用指纹识别来查看本地文件
副本是否已相对于远程文件发生更改。指纹由以下内容生成：

- 大小
- 修改时间
- 哈希

在对象上可用的位置。

在某些后端上，这些属性中的一些读取速度较慢（每个对象
需要额外的 API 调用，或每个对象需要额外的工作）。

例如，使用 `local` 和 `sftp` 后端时 `hash` 较慢，
因为它们必须读取整个文件并对其进行哈希运算；而 `s3`、`swift`、
`ftp` 和 `qinqstor` 后端上 `modtime` 较慢，因为它们
需要进行额外的 API 调用来获取它。

如果使用 `--vfs-fast-fingerprint` 标志，则 rclone 不会
在指纹中包含这些较慢的操作。这使得指纹识别
的准确性降低但速度大大提高，并会改善
缓存文件的打开时间。

如果你在 `local`、`s3` 或 `swift` 后端上运行 vfs 缓存，
则建议使用此标志。

请注意，如果更改此标志的值，缓存中文件的指纹
可能会失效，文件将需要重新下载。

## VFS 分块读取

当 rclone 从远程读取文件时，它会以块的方式读取。
这意味着 rclone 不是请求整个文件，而是读取
指定的块。这可以通过仅请求实际被读取的远程块来减少
某些远程的下载配额使用，代价是请求次数增加。

这些标志控制分块行为：

```text
    --vfs-read-chunk-size SizeSuffix        Read the source objects in chunks (default 128M)
    --vfs-read-chunk-size-limit SizeSuffix  Max chunk doubling size (default off)
    --vfs-read-chunk-streams int            The number of parallel streams to read at once
```

分块行为根据 `--vfs-read-chunk-streams` 参数的不同而有所不同。

### `--vfs-read-chunk-streams` == 0

Rclone 将开始读取大小为 `--vfs-read-chunk-size` 的块，
然后每次读取时将大小翻倍。当指定了
`--vfs-read-chunk-size-limit` 且大于 `--vfs-read-chunk-size` 时，
每个打开文件的块大小将仅翻倍至达到指定值。如果
该值为"off"（默认值），则禁用该限制，块大小将
无限增长。

使用 `--vfs-read-chunk-size 100M` 和 `--vfs-read-chunk-size-limit 0`
时，将下载以下部分：0-100M、100M-200M、200M-300M、300M-400M，
依此类推。当指定 `--vfs-read-chunk-size-limit 500M` 时，结果将是
0-100M、100M-300M、300M-700M、700M-1200M、1200M-1700M，依此类推。

将 `--vfs-read-chunk-size` 设置为 `0` 或"off"将禁用分块读取。

这些块不会在内存中进行缓冲。

### `--vfs-read-chunk-streams` > 0

Rclone 并发读取 `--vfs-read-chunk-streams` 个大小为
`--vfs-read-chunk-size` 的块。每次读取的大小将保持
恒定。

这在高延迟链路上或到高性能对象存储的高带宽链路上
极大地提升了性能。

需要通过一些实验找到 `--vfs-read-chunk-size` 和
`--vfs-read-chunk-streams` 的最佳值，因为这些值将
取决于所使用的后端以及到后端的延迟。

对于高性能对象存储（例如 AWS S3），合理的起点
可能是 `--vfs-read-chunk-streams 16` 和
`--vfs-read-chunk-size 4M`。在 AWS S3 的测试中，性能
大致与 `--vfs-read-chunk-streams` 设置成比例。

类似的设置应适用于高延迟链路，但根据
延迟情况，可能需要更多的 `--vfs-read-chunk-streams`
以获得吞吐量。

## VFS 性能

出于性能或其他原因，可以使用这些标志启用/禁用 VFS 的某些功能。
另请参阅 [chunked reading](#vfs-chunked-reading) 功能。

特别是 S3 和 Swift 极大地受益于 `--no-modtime` 标志
（或使用 `--use-server-modtime` 以获得稍有不同的效果），
因为每次读取修改时间都需要一次事务。

```text
    --no-checksum     Don't compare checksums on up/download.
    --no-modtime      Don't read/write the modification time (can speed things up).
    --no-seek         Don't allow seeking in files.
    --read-only       Only allow read-only access.
```

有时 rclone 收到的读取或写入是乱序的。rclone 将
等待一小段时间以等待按顺序到达的读或写，而不是
执行 seek。这些标志仅在不使用磁盘缓存文件时生效。

```text
    --vfs-read-wait duration   Time to wait for in-sequence read before seeking (default 20ms)
    --vfs-write-wait duration  Time to wait for in-sequence write before giving error (default 1s)
```

使用 VFS 写缓存（`--vfs-cache-mode` 值为 writes 或 full）时，
可设置全局标志 `--transfers` 以调整从缓存并行上传
修改文件的数量（相关的全局标志 `--checkers` 对 VFS 无效）。

```text
    --transfers int  Number of file transfers to run in parallel (default 4)
```

## 符号链接

默认情况下，VFS 不支持符号链接。但是可以使用以下任一标志启用：

```text
    --links      Translate symlinks to/from regular files with a '.rclonelink' extension.
    --vfs-links  Translate symlinks to/from regular files with a '.rclonelink' extension for the VFS
```

由于大多数云存储系统不直接支持符号链接，rclone
将符号链接存储为具有特殊扩展名的普通文件。
因此，文件系统中显示为符号链接 `link-to-file.txt` 的文件
将作为 `link-to-file.txt.rclonelink` 存储在云存储中，
其内容将是符号链接目标的路径。

请注意，`--links` 在 rclone 中全局启用符号链接转换 -
这包括支持此概念的任何后端（例如 local 后端）。
`--vfs-links` 仅对 VFS 层启用此功能。

此方案与
[local 后端使用 --local-links 标志](/local/#symlinks-junction-points) 的方案兼容。

`--vfs-links` 标志是为 `rclone mount`、`rclone
nfsmount` 和 `rclone serve nfs` 设计的。

尚未在其他 `rclone serve` 命令中进行测试。

当前实现的一个限制是，它期望调用方解析子符号链接。
例如，给定此目录树

```text
.
├── dir
│   └── file.txt
└── linked-dir -> dir
```

VFS 将正确解析 `linked-dir`，但无法解析
`linked-dir/file.txt`。对于已测试的命令这不是问题，
但对其他命令可能是个问题。

**请注意**，符号链接支持存在一个未解决的问题
[issue #8245](https://github.com/rclone/rclone/issues/8245)，
当符号链接被移动到其中存在同名文件的目录中时
（或反之），会导致创建重复文件。

## VFS 大小写敏感性

Linux 文件系统是大小写敏感的：两个文件只能通过
大小写来区分，并且打开文件时必须使用准确的大小写。

现代 Windows 中的文件系统是大小写不敏感但大小写保留的：
尽管可以使用任何大小写打开现有文件，但创建文件时
使用的确切大小写会被保留，程序可以查询。
同一目录中两个文件仅大小写不同是不允许的。

通常 macOS 上的文件系统是大小写不敏感的。可以使 macOS
文件系统大小写敏感，但这不是默认设置。

`--vfs-case-insensitive` VFS 标志控制 rclone 如何处理这两种
情况。如果其值为"false"，rclone 将文件名按原样传递给远程。
如果该标志为"true"（或在命令行中不提供值出现），
rclone 可能会执行如下所述的"修正"。

用户可以指定与远程存储的大小写不同的文件名来
打开/删除/重命名/等操作。如果参数引用的是
与现有文件名称完全相同的文件，则将使用磁盘上现有文件的
大小写。但是，如果找不到名称完全相同的文件，
但存在仅大小写不同的名称，则 rclone 将透明地
修正该名称。此修正仅在请求现有文件时发生。
由 rclone 新创建的文件名的大小写敏感性
由底层远程控制。

请注意，运行 rclone 的操作系统（目标）的大小写敏感性
可能与 rclone 提供的文件系统（源）的大小写敏感性不同。
该标志控制是否执行"修正"以满足目标。

如果未在命令行中提供该标志，则其默认值取决于
运行 rclone 的操作系统：在 Windows 和 macOS 上为"true"，
否则为"false"。如果提供该标志但未提供值，则为"true"。

`--no-unicode-normalization` 标志控制是否对
[规范等价](https://en.wikipedia.org/wiki/Unicode_equivalence) 但
unicode 不同的文件名执行类似的"修正"。Unicode 规范化
对 macOS 用户特别有用，因为 macOS 偏好 NFD 形式，
而大多数其他平台使用 NFC 形式。因此，强烈建议
在 macOS 上保留 `false` 的默认值，以避免编码兼容性问题。

在（可能不太可能）发生应用大小写和 unicode 规范化后
目录中存在多个重复文件名的罕见情况下，
`--vfs-block-norm-dupes` 标志允许隐藏这些重复项。
这会带来性能方面的权衡，因为
rclone 在列目录时必须扫描整个目录以查找重复项。
因此，建议如果不需要此功能则将其禁用。
但是，macOS 用户可能希望考虑使用它，因为否则，如果
远程目录同时包含同一文件名的 NFC 和 NFD 两种形式，
则会出现一种奇怪的情况：两个版本的文件都将在挂载中可见，
并且看起来都可编辑，但编辑任一版本实际上
都会导致仅有 NFD 版本在底层被编辑。`--vfs-block-
norm-dupes` 通过检测此场景、隐藏重复项并记录错误来防止
这种混淆，这与 `rclone sync` 中的处理方式类似。

## VFS 磁盘选项

此标志允许你手动设置有关文件系统的统计信息。
在无法自动正确读取这些统计信息时，这很有用。

```text
    --vfs-disk-space-total-size    Manually set the total disk space size (example: 256G, default: -1)
```

## 已用字节数的替代报告

某些后端（最显著的是 S3）不报告已用字节数。
如果在文件系统上运行 `df` 时需要此信息，
请向 rclone 传递标志 `--vfs-used-is-size`。
设置此标志后，rclone 将不再依赖后端报告此
信息，而是类似 `rclone size` 一样扫描整个远程
并自行计算总已用空间。

**警告**：与 `rclone size` 相反，此标志忽略过滤器，
以使结果准确。但是，这非常低效，可能导致大量 API
调用并产生额外费用。仅将其作为最后手段使用，
且仅与缓存一起使用。

## VFS 元数据

如果使用 `--vfs-metadata-extension` 标志，你可以让 VFS
公开那些包含[元数据](/docs/#metadata) 作为 JSON blob
的文件。这些文件不会出现在目录列表中，但可以被
`stat` 并打开，一旦它们被访问，它们**将**出现在
目录列表中，直到目录缓存过期为止。

请注意，除非你传入 `--metadata` 标志，否则某些后端
不会创建元数据。

例如，使用 `rclone mount` 并加上 `--metadata --vfs-metadata-extension .metadata`，我们得到

```console
$ ls -l /mnt/
total 1048577
-rw-rw-r-- 1 user user 1073741824 Mar  3 16:03 1G

$ cat /mnt/1G.metadata
{
        "atime": "2025-03-04T17:34:22.317069787Z",
        "btime": "2025-03-03T16:03:37.708253808Z",
        "gid": "1000",
        "mode": "100664",
        "mtime": "2025-03-03T16:03:39.640238323Z",
        "uid": "1000"
}

$ ls -l /mnt/
total 1048578
-rw-rw-r-- 1 user user 1073741824 Mar  3 16:03 1G
-rw-rw-r-- 1 user user        185 Mar  3 16:03 1G.metadata
```

如果文件没有元数据，则将返回为 `{}`；如果读取元数据时
出错，则错误将作为 `{"error":"error string"}` 返回。

```
rclone nfsmount remote:path /path/to/mountpoint [flags]
```

## 选项

```
      --addr string                            IPaddress:Port or :Port to bind server to
      --allow-non-empty                        Allow mounting over a non-empty directory (not supported on Windows)
      --allow-other                            Allow access to other users (not supported on Windows)
      --allow-root                             Allow access to root user (not supported on Windows)
      --async-read                             Use asynchronous reads (not supported on Windows) (default true)
      --attr-timeout Duration                  Time for which file/directory attributes are cached (default 1s)
      --daemon                                 Run mount in background and exit parent process (as background output is suppressed, use --log-file with --log-format=pid,... to monitor) (not supported on Windows)
      --daemon-timeout Duration                Time limit for rclone to respond to kernel (not supported on Windows) (default 0s)
      --daemon-wait Duration                   Time to wait for ready mount from daemon (maximum time on Linux, constant sleep time on OSX/BSD) (not supported on Windows) (default 1m0s)
      --debug-fuse                             Debug the FUSE internals - needs -v
      --default-permissions                    Makes kernel enforce access control based on the file mode (not supported on Windows)
      --devname string                         Set the device name - default is remote:path
      --dir-cache-time Duration                Time to cache directory entries for (default 5m0s)
      --dir-perms FileMode                     Directory permissions (default 777)
      --direct-io                              Use Direct IO, disables caching of data
      --file-perms FileMode                    File permissions (default 666)
      --fuse-flag stringArray                  Flags or arguments to be passed direct to libfuse/WinFsp (repeat if required)
      --gid uint32                             Override the gid field set by the filesystem (not supported on Windows) (default 1000)
  -h, --help                                   help for nfsmount
      --link-perms FileMode                    Link permissions (default 666)
      --max-read-ahead SizeSuffix              The number of bytes that can be prefetched for sequential reads (not supported on Windows) (default 128Ki)
      --mount-case-insensitive Tristate        Tell the OS the mount is case insensitive (true) or sensitive (false) regardless of the backend (auto) (default unset)
      --network-mode                           Mount as remote network drive, instead of fixed disk drive (supported on Windows only)
      --nfs-cache-dir string                   The directory the NFS handle cache will use if set
      --nfs-cache-handle-limit int             max file handles cached simultaneously (min 5) (default 1000000)
      --nfs-cache-type memory|disk|symlink     Type of NFS handle cache to use (default memory)
      --no-checksum                            Don't compare checksums on up/download
      --no-modtime                             Don't read/write the modification time (can speed things up)
      --no-seek                                Don't allow seeking in files
      --noappledouble                          Ignore Apple Double (._) and .DS_Store files (supported on OSX only) (default true)
      --noapplexattr                           Ignore all "com.apple.*" extended attributes (supported on OSX only)
  -o, --option stringArray                     Option for libfuse/WinFsp (repeat if required)
      --poll-interval Duration                 Time to wait between polling for changes, must be smaller than dir-cache-time and only on supported remotes (set 0 to disable) (default 1m0s)
      --read-only                              Only allow read-only access
      --sudo                                   Use sudo to run the mount/umount commands as root.
      --uid uint32                             Override the uid field set by the filesystem (not supported on Windows) (default 1000)
      --umask FileMode                         Override the permission bits set by the filesystem (not supported on Windows) (default 002)
      --vfs-block-norm-dupes                   If duplicate filenames exist in the same directory (after normalization), log an error and hide the duplicates (may have a performance cost)
      --vfs-cache-max-age Duration             Max time since last access of objects in the cache (default 1h0m0s)
      --vfs-cache-max-size SizeSuffix          Max total size of objects in the cache (default off)
      --vfs-cache-min-free-space SizeSuffix    Target minimum free space on the disk containing the cache (default off)
      --vfs-cache-mode CacheMode               Cache mode off|minimal|writes|full (default off)
      --vfs-cache-poll-interval Duration       Interval to poll the cache for stale objects (default 1m0s)
      --vfs-case-insensitive                   If a file name not found, find a case insensitive match
      --vfs-disk-space-total-size SizeSuffix   Specify the total space of disk (default off)
      --vfs-fast-fingerprint                   Use fast (less accurate) fingerprints for change detection
      --vfs-links                              Translate symlinks to/from regular files with a '.rclonelink' extension for the VFS
      --vfs-metadata-extension string          Set the extension to read metadata from
      --vfs-read-ahead SizeSuffix              Extra read ahead over --buffer-size when using cache-mode full
      --vfs-read-chunk-size SizeSuffix         Read the source objects in chunks (default 128Mi)
      --vfs-read-chunk-size-limit SizeSuffix   If greater than --vfs-read-chunk-size, double the chunk size after each chunk read, until the limit is reached ('off' is unlimited) (default off)
      --vfs-read-chunk-streams int             The number of parallel streams to read at once
      --vfs-read-wait Duration                 Time to wait for in-sequence read before seeking (default 20ms)
      --vfs-refresh                            Refreshes the directory cache recursively in the background on start
      --vfs-used-is-size rclone size           Use the rclone size algorithm for Used size
      --vfs-write-back Duration                Time to writeback files after last use when using cache (default 5s)
      --vfs-write-wait Duration                Time to wait for in-sequence write before giving error (default 1s)
      --volname string                         Set the volume name (supported on Windows and OSX only)
      --write-back-cache                       Makes kernel buffer writes before sending them to rclone (without this, writethrough caching is used) (not supported on Windows)
```

与其他命令共享的选项将在下文中描述。
请参阅 [global flags page](/flags/) 了解此处未列出的全局选项。

### 过滤器选项

用于过滤目录列表的标志

```text
      --delete-excluded                     Delete files on dest excluded from sync
      --exclude stringArray                 Exclude files matching pattern
      --exclude-from stringArray            Read file exclude patterns from file (use - to read from stdin)
      --exclude-if-present stringArray      Exclude directories if filename is present
      --files-from stringArray              Read list of source-file names from file (use - to read from stdin)
      --files-from-raw stringArray          Read list of source-file names from file without any processing of lines (use - to read from stdin)
  -f, --filter stringArray                  Add a file filtering rule
      --filter-from stringArray             Read file filtering patterns from a file (use - to read from stdin)
      --hash-filter string                  Partition filenames by hash k/n or randomly @/n
      --ignore-case                         Ignore case in filters (case insensitive)
      --include stringArray                 Include files matching pattern
      --include-from stringArray            Read file include patterns from file (use - to read from stdin)
      --max-age Duration                    Only transfer files younger than this in s or suffix ms|s|m|h|d|w|M|y (default off)
      --max-depth int                       If set limits the recursion depth to this (default -1)
      --max-size SizeSuffix                 Only transfer files smaller than this in KiB or suffix B|K|M|G|T|P (default off)
      --metadata-exclude stringArray        Exclude metadatas matching pattern
      --metadata-exclude-from stringArray   Read metadata exclude patterns from file (use - to read from stdin)
      --metadata-filter stringArray         Add a metadata filtering rule
      --metadata-filter-from stringArray    Read metadata filtering patterns from a file (use - to read from stdin)
      --metadata-include stringArray        Include metadatas matching pattern
      --metadata-include-from stringArray   Read metadata include patterns from file (use - to read from stdin)
      --min-age Duration                    Only transfer files older than this in s or suffix ms|s|m|h|d|w|M|y (default off)
      --min-size SizeSuffix                 Only transfer files bigger than this in KiB or suffix B|K|M|G|T|P (default off)
```

## 另请参见

<!-- markdownlint-capture -->
<!-- markdownlint-disable ul-style line-length -->

* [rclone](/commands/rclone/)	 - 显示 rclone 命令、标志和后端的帮助。


<!-- markdownlint-restore -->
