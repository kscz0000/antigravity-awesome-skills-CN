---
title: "FAQ"
description: "Rclone 常见问题解答"
---

> **官方文档：** [https://rclone.org/faq/](https://rclone.org/faq/)
<!-- markdownlint-disable heading-increment -->

# Frequently Asked Questions

### 所有云存储系统都支持所有 rclone 命令吗

是的。所有 rclone 命令（例如 `sync`、`copy` 等）都可以在所有远程存储系统上使用。

### 我可以把配置从一台机器复制到另一台吗

当然可以！Rclone 将所有配置存储在单个文件中。如果你想找到这个文件，运行 `rclone config file` 即可查看其位置。

更多信息请参阅[远程设置文档](/remote_setup/)。

### 如何在没有浏览器的远程/无头机器上配置 rclone？

此内容已在专门的[远程设置页面](/remote_setup/)中说明。

### 如何消除"Config file not found"提示？

如果你看到类似 'NOTICE: Config file "rclone.conf" not found' 的提示，说明你尚未配置任何远程存储。

如果需要配置远程存储，请参阅[配置帮助文档](/docs/#configure)。

如果你完全使用[即时远程存储](/docs/#backend-path-to-dir)运行 rclone，可以创建一个空配置文件来消除此提示，例如：

```console
rclone config touch
```

### rclone 能否直接从 Drive 同步到 S3

Rclone 可以在两个远程云存储系统之间正常同步。

请注意，它实际上会先下载文件再重新上传，因此运行 rclone 的节点需要较大的带宽。

同步是增量的（按文件逐个进行）。

例如：

```console
rclone sync --interactive drive:Folder s3:bucket
```

### 同时从多个位置使用 rclone

你可以同时从多个位置使用 rclone，只需为输出选择不同的子目录，例如：

```console
Server A> rclone sync --interactive /tmp/whatever remote:ServerA
Server B> rclone sync --interactive /tmp/whatever remote:ServerB
```

如果你同步到同一目录，则应使用 rclone copy，否则两个 rclone 实例可能会删除对方的文件，例如：

```console
Server A> rclone copy /tmp/whatever remote:Backup
Server B> rclone copy /tmp/whatever remote:Backup
```

在这种情况下，从服务器 A 和服务器 B 上传的文件名应不同，否则某些文件系统（例如 Drive）可能会创建重复文件。

### 为什么 rclone 不像 rsync 那样支持部分传输/二进制差异？

Rclone 将你传输的每个文件作为原生对象存储在远程云存储系统上。这意味着你可以使用其他访问方式（例如 Google Drive 网页界面）查看上传的文件，与预期一致。硬盘上的文件与云存储系统中创建的对象之间存在 1:1 的映射关系。

云存储系统（至少我目前遇到的所有系统）不支持部分上传对象。你无法获取一个现有对象并更改其中间的某些字节。

理论上可以制作一个像 rsync 那样存储二进制差异而非完整对象的同步系统，但这会破坏硬盘文件到远程云存储对象之间的 1:1 映射关系。

所有云存储系统都支持内容的部分下载，因此理论上可以实现部分下载功能。然而，要使此功能高效运行，需要存储大量元数据，这同样会破坏文件到对象的 1:1 映射关系。

### rclone 能做双向同步吗？

可以，从 rclone v1.58.0 起，[双向云同步](/bisync/)已可用。

### 我可以通过 HTTP 代理使用 rclone 吗？

可以。rclone 会遵循代理的标准环境变量，类似于 cURL 和其他程序。

通常，这些变量名为 `http_proxy`（用于通过 `http` 访问的服务）和 `https_proxy`（用于通过 `https` 访问的服务）。大多数公共服务使用 `https`，但你可能需要同时设置两者。

变量的内容格式为 `protocol://server:port`。协议值是与代理服务器通信时使用的协议，通常为 `http` 或 `socks5`。

有点烦人的是，变量名没有*统一标准*；有些应用程序使用 `http_proxy`，而另一些使用 `HTTP_PROXY`。`rclone` 使用的 `Go` 库会尝试两种变体，但你可能希望设置所有可能的值。因此在 Linux 上，你可能会写出类似以下的代码：

```console
export http_proxy=http://proxyserver:12345
export https_proxy=$http_proxy
export HTTP_PROXY=$http_proxy
export HTTPS_PROXY=$http_proxy
```

注意：如果代理服务器需要用户名和密码，则使用：

```console
export http_proxy=http://username:password@proxyserver:12345
export https_proxy=$http_proxy
export HTTP_PROXY=$http_proxy
export HTTPS_PROXY=$http_proxy
```

`NO_PROXY` 变量允许你对特定主机禁用代理。主机之间必须用逗号分隔，可以包含域名或部分域名。例如 "foo.com" 也会匹配 "bar.foo.com"。

例如：

```console
export no_proxy=localhost,127.0.0.0/8,my.host.name
export NO_PROXY=$no_proxy
```

注意，FTP 后端尚不支持 `ftp_proxy`。

你可以使用命令行参数 `--http-proxy` 来设置代理，如果只想为单个后端设置，还可以在配置文件中使用覆盖项，例如 `override.http_proxy = http://...`。

FTP 和 SFTP 后端有各自的 `http_proxy` 设置来支持 HTTP CONNECT 代理（
[--ftp-http-proxy](https://rclone.org/ftp/#ftp-http-proxy) 和
[--sftp-http-proxy](https://rclone.org/ftp/#sftp-http-proxy) ）

### rclone 报告 x509 SSL 根证书错误

`x509: failed to load system roots and no roots provided` 表示 `rclone` 无法找到 SSL 根证书。很可能你正在精简版 Linux 操作系统的 NAS 上运行 `rclone`，或者可能在 Solaris 上运行。

`x509: certificate signed by unknown authority` 错误可能出现在过时的系统上，`rclone` 无法使用 SSL 根证书验证服务器。

Rclone（通过 Go 运行时）会尝试从 Linux 上的以下位置加载根证书。

```text
"/etc/ssl/certs/ca-certificates.crt", // Debian/Ubuntu/Gentoo etc.
"/etc/pki/tls/certs/ca-bundle.crt",   // Fedora/RHEL
"/etc/ssl/ca-bundle.pem",             // OpenSUSE
"/etc/pki/tls/cacert.pem",            // OpenELEC
```

因此执行类似以下操作应该可以解决问题。同时也设置了时间，这对 SSL 正常工作很重要。

```console
mkdir -p /etc/ssl/certs/
curl -o /etc/ssl/certs/ca-certificates.crt https://raw.githubusercontent.com/bagder/ca-bundle/master/ca-bundle.crt
ntpclient -s -h pool.ntp.org
```

[x509 包](https://godoc.org/crypto/x509)中提到的两个环境变量 `SSL_CERT_FILE` 和 `SSL_CERT_DIR`，提供了在 macOS 以外的 Unix 系统上提供 SSL 根证书的另一种方式。

注意，如果 `curl` 命令不加 `--insecure` 选项无法工作，你可能需要添加该选项。

```console
curl --insecure -o /etc/ssl/certs/ca-certificates.crt https://raw.githubusercontent.com/bagder/ca-bundle/master/ca-bundle.crt
```

在 macOS 上，你可以使用 Homebrew 安装
[ca-certificates](https://formulae.brew.sh/formula/ca-certificates)，并使用
[--ca-cert](/docs/#ca-cert-stringarray) 标志指定 SSL 根证书。

```console
brew install ca-certificates
find $(brew --prefix)/etc/ca-certificates -type f
```

### rclone 报告 Failed to load config file: function not implemented 错误

这可能意味着你在 Go 运行时不支持的 Linux 版本上运行 rclone，即早于 2.6.23 版本。

详情请参阅 [Go 安装文档中的系统要求部分](https://golang.org/doc/install)。

### 我上传的所有 docx/xlsx/pptx 文件都显示为 archive/zip

这是由于从未安装 Microsoft Office 套件的 Windows 计算机上传这些文件导致的。最简单的修复方法是安装 Word 查看器和 Microsoft Office Word、Excel 和 PowerPoint 2007 及更高版本文件格式的兼容包

### tcp lookup some.domain.com no such host

当 rclone 无法解析域名时会出现此问题。请检查你的 DNS 设置是否正常工作，例如：

```sh
# both should print a long list of possible IP addresses
dig www.googleapis.com          # resolve using your default DNS
dig www.googleapis.com @8.8.8.8 # resolve with Google's DNS server
```

如果你使用的是 `systemd-resolved`（Arch Linux 默认），请确保版本在 233 或更高。之前的版本包含一个 bug，会导致某些域名无法正确解析。

Go 解析器的决策可以通过 `GODEBUG=netdns=...` 环境变量来影响。这也允许解决某些 DNS 解析问题。在 Windows 或 macOS 系统上，尝试通过在运行时设置 `GODEBUG=netdns=go` 来强制使用内部 Go 解析器。在其他系统（Linux、\*BSD 等）上，尝试通过设置 `GODEBUG=netdns=cgo` 来强制使用系统名称解析器（如有必要，需启用 CGO 从源码重新编译 rclone）。请参阅 [Go 文档中的名称解析部分](https://golang.org/pkg/net/#hdr-Name_Resolution)。

### 在 Windows 上启动认证 Web 服务器失败

```text
Error: config failed to refresh token: failed to start auth webserver: listen tcp 127.0.0.1:53682: bind: An attempt was made to access a socket in a way forbidden by its access permissions.
...
yyyy/mm/dd hh:mm:ss Fatal error: config failed to refresh token: failed to start auth webserver: listen tcp 127.0.0.1:53682: bind: An attempt was made to access a socket in a way forbidden by its access permissions.
```

这有时是由主机网络服务在主机上打开端口时出现问题导致的。

一个简单的解决方法是使用 PowerShell 重启主机网络服务，例如：

```powershell
Restart-Service hns
```

### 同步统计中报告的总大小不正确且不断变化

很可能你有超过 10,000 个文件需要同步。默认情况下，rclone 在同步时最多只提前获取 10,000 个文件，以避免占用过多内存。你可以使用
[--max-backlog](/docs/#max-backlog-int) 标志更改此默认值。

### rclone 占用内存过多或似乎有内存泄漏

Rclone 使用 Go 语言编写，Go 使用垃圾回收器。垃圾回收器的默认设置是在堆大小翻倍时运行。

不过，可以通过将 [GOGC](https://dave.cheney.net/tag/gogc) 设置为较低的值（例如 `export GOGC=20`）来调整垃圾回收器以使用更少内存。这会使垃圾回收器更频繁地工作，以减少内存占用为代价增加 CPU 使用率。

rclone 使用大量内存的最常见原因是单个目录中有数百万个文件。

在 rclone v1.70 之前，必须将整个目录加载到内存中作为 rclone 对象。每个 rclone 对象占用 0.5k-1k 内存。有一个[针对此问题的变通方案](https://github.com/rclone/rclone/wiki/Big-syncs-with-millions-of-files)，需要一些脚本编写。

然而在 rclone v1.70 及更高版本中，当检测到目录包含超过
[`--list-cutoff`](/docs/#list-cutoff)（默认为 1,000,000）个条目时，rclone 会自动将目录条目保存到磁盘。

从 v1.70 起，rclone 还提供了 [--max-buffer-memory](/docs/#max-buffer-memory) 标志，这在多线程传输占用过多内存时特别有用。

### rclone 更改文件名中的全角 Unicode 标点符号

例如：在 Windows 系统上，你有一个名为 `Test：1.jpg` 的文件，其中 `：` 是 Unicode 全角冒号符号。使用 rclone 将此文件复制到 Google Drive 时，你会注意到文件被重命名为 `Test:1.jpg`，其中 `:` 是常规（半角）冒号。

这种重命名的原因在于 rclone 处理不同云存储系统上不同[受限文件名](/overview/#restricted-filenames)的方式。它试图尽可能避免模糊的文件名，并允许在多个云存储系统之间透明地移动文件，方法是在传输到某个存储系统时将无效字符替换为外观相似的 Unicode 字符，在传输到支持原始字符的另一个存储系统时再替换回来。当文件名中故意使用相同的 Unicode 字符时，这种替换策略会导致不需要的重命名。详情请阅读[注意事项](/overview/#restricted-filenames-caveats)部分。

### 为什么 rclone 通过 TLS 连接失败，但另一个客户端可以？

如果你看到 TLS 握手失败（或数据包捕获显示服务器拒绝了所有提供的密码套件），服务器/代理可能只支持旧版 TLS 密码套件（例如 RSA 密钥交换密码，如 `RSA_WITH_AES_256_CBC_SHA256`，或旧版 3DES 密码）。最近的 Go 版本（rclone 基于此构建）已**从默认列表中移除了不安全的密码**，因此即使其他工具仍在协商这些密码，rclone 也可能拒绝使用。

如果你无法更新/重新配置服务器/代理以支持现代 TLS（TLS 1.2/1.3）和基于 ECDHE 的密码套件，可以通过 `GODEBUG` 重新启用旧版密码：

- Windows (cmd.exe)：

  ```bat
  set GODEBUG=tlsrsakex=1
  rclone copy ...
  ```

- Windows (PowerShell)：

  ```powershell
  $env:GODEBUG="tlsrsakex=1"
  rclone copy ...
  ```

- Linux/macOS：

  ```sh
  GODEBUG=tlsrsakex=1 rclone copy ...
  ```

如果服务器仅支持 3DES，请尝试：

```sh
GODEBUG=tls3des=1 rclone ...
```

这适用于**任何使用 TLS 的 rclone 功能**（HTTPS、FTPS、基于 TLS 的 WebDAV、带 TLS 拦截的代理等）。这些变通方案仅应在更新服务器/代理之前临时使用。