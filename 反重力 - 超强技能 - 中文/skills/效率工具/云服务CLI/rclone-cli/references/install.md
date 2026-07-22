---
title: "Install"
description: "Rclone 安装"
---

> **官方文档：** [https://rclone.org/install/](https://rclone.org/install/)
# Install

Rclone 是一个 Go 程序，以单个二进制文件形式发布。

## 快速入门

- [下载](/downloads/)对应的二进制文件。
- 从压缩包中提取 `rclone` 可执行文件（Windows 上为 `rclone.exe`）。
- 运行 `rclone config` 进行配置。详见 [rclone config 文档](/docs/)。
- 可选：配置[自动执行](#autostart)。

下方提供了更详细的 Linux / macOS / Windows 安装说明。

关于 rclone 的使用方法，请参阅 [usage](/docs/) 文档，或运行 `rclone -h`。

已安装的 rclone 可通过 [rclone selfupdate](/commands/rclone_selfupdate/) 命令轻松更新到最新版本。

关于如何验证发行版的签名，请参阅[发行版签名文档](/release_signing/)。

## 脚本安装

在 Linux/macOS/BSD 系统上安装 rclone，运行：

```console
sudo -v ; curl https://rclone.org/install.sh | sudo bash
```

安装 beta 版本，运行：

```console
sudo -v ; curl https://rclone.org/install.sh | sudo bash -s beta
```

注意：此脚本会先检查已安装的 rclone 版本，如果不需要更新则不会重新下载。

## Linux 安装 {#linux}

### 预编译二进制文件 {#linux-precompiled}

下载并解压

```console
curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip
unzip rclone-current-linux-amd64.zip
cd rclone-*-linux-amd64
```

复制二进制文件

```console
sudo cp rclone /usr/bin/
sudo chown root:root /usr/bin/rclone
sudo chmod 755 /usr/bin/rclone
```

安装 man 手册页

```console
sudo mkdir -p /usr/local/share/man/man1
sudo cp rclone.1 /usr/local/share/man/man1/
sudo mandb
```

运行 `rclone config` 进行配置。详见 [rclone config 文档](/docs/)。

```console
rclone config
```

## macOS 安装 {#macos}

### 使用 brew 安装 {#macos-brew}

```console
brew install rclone
```

注意：此版本的 rclone 将不再支持 `mount`（参见 [#5373](https://github.com/rclone/rclone/issues/5373)）。如果在 macOS 上需要挂载功能，请安装预编译二进制文件，或在[从源码安装](#source)时启用相关选项。

注意：这是由第三方维护的安装器，不受 rclone 开发者控制，因此可能不是最新版本。当前版本如下。

[![Homebrew package](https://repology.org/badge/version-for-repo/homebrew/rclone.svg)](https://repology.org/project/rclone/versions)

### 使用 MacPorts 安装 {#macos-macports}

在 macOS 上，也可以通过 [MacPorts](https://www.macports.org) 安装 rclone：

```console
sudo port install rclone
```

注意：这是由第三方维护的安装器，不受 rclone 开发者控制，因此可能不是最新版本。当前版本如下。

[![MacPorts port](https://repology.org/badge/version-for-repo/macports/rclone.svg)](https://repology.org/project/rclone/versions)

更多信息请参阅 [macports.org](https://ports.macports.org/port/rclone/)。

### 预编译二进制文件，使用 curl {#macos-precompiled}

为避免 macOS Gatekeeper 强制要求二进制文件经过签名和公证的问题，使用 `curl` 下载即可。

下载最新版本的 rclone。

```console
cd && curl -O https://downloads.rclone.org/rclone-current-osx-amd64.zip
```

解压下载的文件并进入解压后的目录。

```console
unzip -a rclone-current-osx-amd64.zip && cd rclone-*-osx-amd64
```

将 rclone 移动到你的 $PATH 中。系统会提示你输入密码。

```console
sudo mkdir -p /usr/local/bin
sudo mv rclone /usr/local/bin/
```

（`mkdir` 命令是安全的，即使目录已存在也可以运行。）

清理残留文件。

```console
cd .. && rm -rf rclone-*-osx-amd64 rclone-current-osx-amd64.zip
```

运行 `rclone config` 进行配置。详见 [rclone config 文档](/docs/)。

```console
rclone config
```

### 预编译二进制文件，使用网页浏览器 {#macos-precompiled-web}

通过网页浏览器下载二进制文件时，浏览器会设置 macOS Gatekeeper 的隔离属性。从 Catalina 开始，尝试运行 `rclone` 时会弹出提示：

```text
"rclone" cannot be opened because the developer cannot be verified.
macOS cannot verify that this app is free from malware.
```

最简单的修复方法是运行

```console
xattr -d com.apple.quarantine rclone
```

## Windows 安装 {#windows}

### 预编译二进制文件 {#windows-precompiled}

点击以下链接下载适合你处理器类型的二进制文件。如果不确定，请使用第一个链接。

- [Intel/AMD - 64 位](https://downloads.rclone.org/rclone-current-windows-amd64.zip)
- [Intel/AMD - 32 位](https://downloads.rclone.org/rclone-current-windows-386.zip)
- [ARM - 64 位](https://downloads.rclone.org/rclone-current-windows-arm64.zip)

在资源管理器中打开此文件并提取 `rclone.exe`。Rclone 是便携式可执行文件，你可以将其放在任何方便的位置。

打开 CMD 窗口（或 PowerShell）并运行该二进制文件。注意 rclone 默认不会启动 GUI，它在 CMD 窗口中运行。

- 运行 `rclone.exe config` 进行配置。详见 [rclone config 文档](/docs/)。
- 可选：配置[自动执行](#autostart)。

如果你计划使用 [rclone mount](/commands/rclone_mount/) 功能，还需要安装第三方工具 [WinFsp](https://winfsp.dev/)。

### Windows 包管理器 (Winget) {#windows-chocolatey}

[Winget](https://learn.microsoft.com/en-us/windows/package-manager/) 在最新版本的 Windows 中已预装。如果没有，请从 Microsoft Store 更新 [App Installer](https://www.microsoft.com/p/app-installer/9nblggh4nns1) 包。

安装 rclone

```bat
winget install Rclone.Rclone
```

卸载 rclone

```bat
winget uninstall Rclone.Rclone --force
```

### Chocolatey 包管理器 {#windows-chocolatey}

确保已安装 [Choco](https://chocolatey.org/)

```bat
choco search rclone
choco install rclone
```

这将在你的 Windows 机器上安装 rclone。如果你计划使用 [rclone mount](/commands/rclone_mount/)，则

```bat
choco install winfsp
```

将同时安装该依赖。

注意：这是由第三方维护的安装器，不受 rclone 开发者控制，因此可能不是最新版本。当前版本如下。

[![Chocolatey package](https://repology.org/badge/version-for-repo/chocolatey/rclone.svg)](https://repology.org/project/rclone/versions)

### Scoop 包管理器 {#windows-scoop}

确保已安装 [Scoop](https://scoop.sh/)

```bat
scoop install rclone
```

注意：这是由第三方维护的安装器，不受 rclone 开发者控制，因此可能不是最新版本。当前版本如下。

[![Scoop package](https://repology.org/badge/version-for-repo/scoop/rclone.svg)](https://repology.org/project/rclone/versions)

## 包管理器安装 {#package-manager}

许多 Linux、Windows、macOS 及其他操作系统发行版都会打包和分发 rclone。

这些发行版中的 rclone 版本通常相当过时，因此如果可能，我们推荐使用其他安装方法。

你可以在这里了解你的操作系统发行版中 rclone 包的新旧程度。

[![Packaging status](https://repology.org/badge/vertical-allrepos/rclone.svg?columns=3)](https://repology.org/project/rclone/versions)

## Docker 安装 {#docker}

rclone 开发者维护了一个 [rclone 的 Docker 镜像](https://hub.docker.com/r/rclone/rclone)。

**注意：** 我们现在还通过合作伙伴 [SecureBuild](https://securebuild.com/blog/introducing-securebuild) 提供具有企业级安全性和零 CVE 的 rclone 付费版本。如有兴趣，请访问其网站及 [Rclone SecureBuild 镜像](https://securebuild.com/images/rclone)。

这些镜像作为发布流程的一部分构建，基于精简的 Alpine Linux。

`:latest` 标签将始终指向最新的稳定版本。你可以使用 `:beta` 标签获取 master 分支的最新构建。你也可以使用版本标签，例如 `:1.49.1`、`:1.49` 或 `:1`。

```console
$ docker pull rclone/rclone:latest
latest: Pulling from rclone/rclone
Digest: sha256:0e0ced72671989bb837fea8e88578b3fc48371aa45d209663683e24cfdaa0e11
...
$ docker run --rm rclone/rclone:latest version
rclone v1.49.1
- os/arch: linux/amd64
- go version: go1.12.9
```

从 rclone 镜像启动 Docker 容器时，有几个命令行选项需要考虑。

- 你需要将宿主机的 rclone 配置目录挂载到 Docker 容器的 `/config/rclone`。由于 rclone 会在其配置文件中更新令牌，且更新过程涉及文件重命名，因此你需要挂载整个宿主机 rclone 配置目录，而不仅仅是单个配置文件。

- 你需要将宿主机的数据目录挂载到 Docker 容器的 `/data`。

- 默认情况下，Docker 容器内的 rclone 二进制文件以 UID=0（root）运行。因此，运行中创建的所有文件都将具有 UID=0。如果你的配置文件和数据文件在宿主机上具有非 root 的 UID:GID，则需要在容器启动命令行中传递这些值。

- 如果你想访问 RC 接口（通过 API 或 Web UI），需要将 `--rc-addr` 设置为 `:5572`，以便从容器外部连接。关于为何需要这样做的说明，可参阅这篇旧[文章](https://web.archive.org/web/20200808071950/https://pythonspeed.com/articles/docker-connection-refused/)。
  - 注意：如果容器的 Docker 网络设置为 `host`，则应将 `--rc-addr` 设置为仅监听 localhost，即 `127.0.0.1:5572`

- 可以在用户空间 Docker 容器内使用 `rclone mount`，并将生成的 fuse 挂载暴露给宿主机。具体的 `docker run` 选项可能因宿主机而略有不同。参见此[讨论](https://github.com/moby/moby/issues/9448)。

  你还需要挂载宿主机的 `/etc/passwd` 和 `/etc/group`，以便 fuse 在容器内正常工作。

以下是在 Ubuntu 18.04.3 宿主机上测试过的命令：

```sh
# config on host at ~/.config/rclone/rclone.conf
# data on host at ~/data

# add a remote interactively
docker run --rm -it \
    --volume ~/.config/rclone:/config/rclone \
    --user $(id -u):$(id -g) \
    rclone/rclone \
    config

# make sure the config is ok by listing the remotes
docker run --rm \
    --volume ~/.config/rclone:/config/rclone \
    --user $(id -u):$(id -g) \
    rclone/rclone \
    listremotes

# perform mount inside Docker container, expose result to host
mkdir -p ~/data/mount
docker run --rm \
    --volume ~/.config/rclone:/config/rclone \
    --volume ~/data:/data:shared \
    --user $(id -u):$(id -g) \
    --volume /etc/passwd:/etc/passwd:ro --volume /etc/group:/etc/group:ro \
    --device /dev/fuse --cap-add SYS_ADMIN --security-opt apparmor:unconfined \
    rclone/rclone \
    mount dropbox:Photos /data/mount &
ls ~/data/mount
kill %1
```

## Snap 安装 {#snap}

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/rclone)

确保已安装 [Snapd](https://snapcraft.io/docs/installing-snapd)

```console
sudo snap install rclone
```

由于 Snap 的严格沙箱限制，rclone snap 无法访问真正的 `/home/$USER/.config/rclone` 目录，默认配置路径如下。

- 默认配置目录：
  - /home/$USER/snap/rclone/current/.config/rclone

注意：由于 Snap 的严格沙箱限制，`rclone mount` 功能**不受**支持。

如果需要挂载功能，请安装预编译二进制文件，或在[从源码安装](#source)时启用相关选项。

注意：此 Snap 包由[社区维护者](https://github.com/boukendesho/rclone-snap)控制，而非 rclone 开发者，因此可能不是最新版本。当前版本如下。

[![rclone](https://snapcraft.io/rclone/badge.svg)](https://snapcraft.io/rclone)

## 源码安装 {#source}

确保已安装 git 和 [Go](https://golang.org/)。
需要 Go 1.25 或更高版本，推荐使用最新发行版。
你可以通过包管理器获取，或从 [golang.org/dl](https://golang.org/dl/) 下载。然后运行以下命令：

```console
git clone https://github.com/rclone/rclone.git
cd rclone
go build
```

这将在 rclone 子目录中检出 rclone 源码，你可以之后修改并提交 pull request。然后它会在同一目录下构建 rclone 可执行文件。作为初步检查，你现在可以运行 `./rclone version`（Windows 上为 `.\rclone version`）。

注意：在 macOS 和 Windows 上，[mount](https://rclone.org/commands/rclone_mount/) 命令将不可用，除非你指定额外的构建标签 `cmount`。

```console
go build -tags cmount
```

这假定你的 PATH 中有 GCC 兼容的 C 编译器（GCC 或 Clang），因为它使用了 [cgo](https://pkg.go.dev/cmd/cgo)。但在 Windows 上，cmount 实现所基于的 [cgofuse](https://github.com/winfsp/cgofuse) 库也支持[不使用 cgo](https://github.com/golang/go/wiki/WindowsDLLs) 构建，即通过将环境变量 CGO_ENABLED 设置为 0（静态链接）。从 1.59 版本开始，官方 Windows rclone 发行版就是这样构建的。在 Windows 上仍然可以使用 cgo 构建，方法是使用 GCC 的 MinGW 移植版本，例如通过 [MSYS2](https://www.msys2.org) 发行版安装（确保安装在经典 mingw64 子系统中，ucrt64 版本不兼容）。

此外，要在 Windows 上构建带 mount 功能的版本，你必须安装第三方工具 [WinFsp](https://winfsp.dev/)，并选择"Developer"功能。如果使用 cgo 构建，还必须设置环境变量 CPATH 指向 WinFsp 安装目录中的 fuse include 目录（通常为 `C:\Program Files (x86)\WinFsp\inc\fuse`）。

你可以添加参数 `-ldflags -s` 来省略符号表和调试信息，使可执行文件更小，以及 `-trimpath` 来移除对本地文件系统路径的引用。官方 rclone 发行版同时使用了这两个参数。

```console
go build -trimpath -ldflags -s -tags cmount
```

如果你想自定义 `rclone version` 命令报告的版本字符串，可以设置 `fs.Version`、`fs.VersionTag`（保留默认后缀但自定义版本号）或 `fs.VersionSuffix`（保留默认版本号但自定义后缀）变量之一。这可以在构建命令中通过添加到 `-ldflags` 参数值来完成，如下所示。

```console
go build -trimpath -ldflags "-s -X github.com/rclone/rclone/fs.Version=v9.9.9-test" -tags cmount
```

在 Windows 上，官方可执行文件还将版本信息和文件图标作为二进制资源嵌入。要在你自己的构建中获得此效果，你需要在构建命令**之前**运行以下命令。它会生成一个扩展名为 .syso 的 Windows 资源系统对象文件，例如 `resource_windows_amd64.syso`，后续构建命令将自动拾取该文件。

```console
go run bin/resource_windows.go
```

上述命令将根据你运行命令时源码中的 fs.Version 变量生成包含版本信息的资源文件，这意味着如果该变量的值发生变化，你需要重新运行该命令才能反映在版本信息中。此外，如果你在构建命令中按上述方式覆盖了此版本变量，则在生成资源文件时也需要这样做，否则它仍将使用源码中的值。

```console
go run bin/resource_windows.go -version v9.9.9-test
```

除了直接执行 `go build` 命令外，你还可以通过 Makefile 运行。默认目标会将版本后缀从"-DEV"改为"-beta"并附加额外的提交详情，在 Windows 上嵌入版本信息二进制资源，并将生成的 rclone 可执行文件复制到你的 GOPATH bin 目录（`$(go env GOPATH)/bin`，默认对应 `~/go/bin/rclone`）。

```console
make
```

要在 macOS 和 Windows 上通过 Makefile 构建包含 mount 命令的版本：

```console
make GOTAGS=cmount
```

还有其他 make 目标可用于更高级的构建，例如交叉编译所有支持的操作系统/架构，以及将结果打包为发行版产物。
详见 [Makefile](https://github.com/rclone/rclone/blob/master/Makefile) 和 [cross-compile.go](https://github.com/rclone/rclone/blob/master/bin/cross-compile.go)。

源码安装的另一种替代方法是下载源码、构建并安装 rclone——所有操作一步完成，作为常规 Go 包。源码将存储在 Go 模块缓存中，生成的可执行文件将在你的 GOPATH bin 目录（`$(go env GOPATH)/bin`，默认对应 `~/go/bin/rclone`）。

```console
go install github.com/rclone/rclone@latest
```

在某些情况下，当包含所有带有大型 SDK 的后端时，rclone 可执行文件的大小可能对于非常受限环境的部署来说太大。要限制二进制文件大小，可以在使用 `go build` 或 `make` 构建之前，在 `backends/all/all.go` 中注释掉未使用的后端，在 `cmd/all/all.go` 中注释掉未使用的命令。

## Ansible 安装 {#ansible}

这可以通过 [Stefan Weichinger 的 ansible role](https://github.com/stefangweichinger/ansible-rclone) 完成。

说明

1. 将 `git clone https://github.com/stefangweichinger/ansible-rclone.git` 克隆到你的本地 roles 目录
2. 将该 role 添加到需要安装 rclone 的主机：

    ```yaml
    - hosts: rclone-hosts
      roles:
        - rclone
    ```

## 便携式安装 {#portable}

如[上方](https://rclone.org/install/#quickstart)所述，rclone 是单个可执行文件（`rclone`，或 Windows 上的 `rclone.exe`），你可以作为 zip 压缩包下载并解压到你选择的位置。执行不同命令时，它可能会在不同位置创建文件，如配置文件和各种临时文件。默认情况下，这些位置遵循你的操作系统规范，例如配置文件位于用户配置文件目录，临时文件位于标准临时目录，但你可以自定义所有这些位置，例如创建一个完全自包含的便携式安装。

运行 [config paths](/commands/rclone_config_paths/) 命令可查看 rclone 将使用的位置。

要覆盖这些位置，请设置相应选项（作为命令行参数，或作为[环境变量](https://rclone.org/docs/#environment-variables)）：

- [--config](https://rclone.org/docs/#config-string)
- [--cache-dir](https://rclone.org/docs/#cache-dir-string)
- [--temp-dir](https://rclone.org/docs/#temp-dir-string)

## 自动启动

按照上述方法安装和配置 rclone 后，你就可以将 rclone 作为交互式命令行工具使用了。如果你的目标是执行*周期性*操作，例如定期 [sync](https://rclone.org/commands/rclone_sync/)，你可能希望在操作系统的调度器中配置你的 rclone 命令。如果你需要暴露*服务*类功能，如[远程控制](https://rclone.org/rc/)、[GUI](https://rclone.org/gui/)、[serve](https://rclone.org/commands/rclone_serve/) 或 [mount](https://rclone.org/commands/rclone_mount/)，你通常希望 rclone 命令始终在后台运行，将其配置为在服务基础设施中运行可能是更好的选择。以下是在不同操作系统上实现此目标的一些替代方案。

注意：在设置自动运行之前，强烈建议你先在命令提示符中手动测试你的命令。

### Windows 自动启动

Windows 上自动启动的主要替代方案有：

- 使用启动文件夹在用户登录时运行
- 使用任务计划程序在用户登录时、系统启动时或按计划运行
- 使用 Windows 服务在系统启动时运行

#### 后台运行

Rclone 是控制台应用程序，因此如果不是从现有命令提示符启动（例如从快捷方式启动 rclone.exe），它会打开一个命令提示符窗口。配置 rclone 从任务计划程序和 Windows 服务运行时，你可以将其设置为在后台隐藏运行。从 rclone 1.54 版本开始，你还可以通过添加 `--no-console` 选项使其从任何地方隐藏运行（程序启动时可能仍会短暂闪现窗口）。由于 rclone 通常会将信息和错误消息输出到控制台，你必须将其重定向到文件才能查看。Rclone 内置了 `--log-file` 选项用于此目的。

在后台运行 sync 的示例命令：

```bat
c:\rclone\rclone.exe sync c:\files remote:/files --no-console --log-file c:\rclone\logs\sync_files.txt
```

#### 用户账户

如 [mount](https://rclone.org/commands/rclone_mount/) 文档所述，以管理员身份创建的挂载驱动器对其他账户不可见，即使是提升为管理员权限的账户也不可见。通过以内置 `SYSTEM` 用户账户运行 mount 命令，它将创建对系统上所有人都可访问的驱动器。计划任务和 Windows 服务都可用于实现此目标。

注意：请记住，当 rclone 以 `SYSTEM` 用户运行时，它看到的用户配置文件将不是你的。这意味着如果你通常在默认位置运行 rclone 配置文件，要以系统用户运行时使用相同配置，你必须通过 [`--config`](https://rclone.org/docs/#config-string) 选项明确告诉 rclone 配置文件的位置，否则它将在系统用户的配置文件路径（`C:\Windows\System32\config\systemprofile`）中查找。要从命令提示符手动测试你的命令，你可以使用 Microsoft Sysinternals 套件中的 [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) 工具，它接受 `-s` 选项以 `SYSTEM` 用户执行命令。

#### 从启动文件夹启动

要快速执行 rclone 命令，你可以简单地创建一个标准的 Windows 资源管理器快捷方式，指向你要运行的完整 rclone 命令。如果你将此快捷方式存储在特殊的"启动"开始菜单文件夹中，Windows 将在登录时自动运行它。要在 Windows 资源管理器中打开此文件夹，输入路径 `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`，或者如果希望命令对*每个*登录的用户都启动，则使用 `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`。

这是 rclone 自动启动最简单的方法，但它不提供以不同用户运行、设置条件或在特定事件上执行操作的功能。按照下方描述设置计划任务通常能获得更好的结果。

#### 从任务计划程序启动

任务计划程序是 Windows 内置的管理工具，可用于以高度可配置的方式配置 rclone 自动启动，例如按计划定期运行、在用户登录时或系统启动时运行。它可以配置为以当前用户身份运行，或对于需要对所有用户可用的 mount 命令，以 `SYSTEM` 用户身份运行。
技术信息请参阅 [Task Scheduler for developers](https://docs.microsoft.com/windows/win32/taskschd/task-scheduler-start-page)。

#### 作为服务运行

要在系统启动时运行 rclone，你可以创建一个执行 rclone 命令的 Windows 服务，作为配置为在启动时运行的计划任务的替代方案。

##### mount 命令内置服务集成

对于 mount 命令，rclone 通过其使用的第三方 WinFsp 库提供内置的 Windows 服务集成。注册为常规 Windows 服务很简单，只需执行内置的 PowerShell 命令 `New-Service`（需要管理员权限）。

创建 Windows 服务的 PowerShell 命令示例，将 `remote:/files` 挂载为驱动器号 `X:`，供*所有*用户使用（服务将以本地系统账户运行）：

```powershell
New-Service -Name Rclone -BinaryPathName 'c:\rclone\rclone.exe mount remote:/files X: --config c:\rclone\config\rclone.conf --log-file c:\rclone\logs\mount.txt'
```

[WinFsp 服务架构](https://github.com/billziss-gh/winfsp/wiki/WinFsp-Service-Architecture)支持将文件系统实现（如 rclone）的服务整合到其自身的启动器服务中，作为"子服务"。这还有一个额外优势，即它还实现了集成到 Windows 网络驱动器标准管理方法的网络提供程序。目前 Rclone 尚未正式支持此功能，但使用 WinFsp 2019.3 B2 / v1.5B2 或更高版本，应该可以通过如 [#3340](https://github.com/rclone/rclone/issues/3340) 中所述的路径重写实现。

##### 第三方服务集成

要将任何 rclone 命令作为 Windows 服务运行，可以使用出色的第三方工具 [NSSM](http://nssm.cc)，即"Non-Sucking Service Manager"。它包含一些高级功能，如调整进程优先级、定义进程环境变量、将 stdout 输出重定向到文件、对不同退出代码的自定义响应，以及用于配置所有这些的 GUI（虽然也可以从命令行使用）。

还有其他几个替代方案。值得一提的是 [WinSW](https://github.com/winsw/winsw)，即"Windows Service Wrapper"。它需要 .NET Framework，但较新版本的 Windows 已预装，它还提供包含必要运行时（.NET 5）的替代独立发行版。WinSW 是仅命令行的工具，你需要手动创建包含服务配置的 XML 文件。这对某些人来说可能是缺点，但也可能是优点，因为配置设置易于备份和复用，无需在 GUI 中手动操作。需要注意的是，默认情况下它不会在出错时重启服务，必须在配置文件中显式启用此功能（通过"onfailure"参数）。

### Linux 自动启动

#### 作为服务启动

要始终在后台运行 rclone（适用于 mount 命令等），你可以使用 systemd 将 rclone 设置为系统服务或用户服务。以系统服务运行可确保即使运行用户没有活跃会话，也会在启动时运行。以用户服务运行 rclone 可确保仅在配置用户登录系统后才启动。

#### 从 cron 定期运行

要运行周期性命令，如 copy/sync，你可以设置 cron 任务。
