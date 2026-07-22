---
title: "Docker 卷插件"
description: "Docker 卷插件"
versionIntroduced: "v1.56"
---

> **官方文档：** [https://rclone.org/docker/](https://rclone.org/docker/)
# Docker Volume Plugin

## 简介

Docker 1.9 增加了对通过[命令行界面](https://docs.docker.com/engine/reference/commandline/volume_create/)创建[命名卷](https://docs.docker.com/storage/volumes/)并将其挂载到容器中作为容器间共享数据方式的支持。
从 Docker 1.10 开始，你可以通过 [Docker Compose](https://docs.docker.com/compose/) 在 [docker-compose.yml](https://docs.docker.com/compose/compose-file/compose-file-v2/#volume-configuration-reference) 文件中的描述来创建命名卷，供单主机上的容器组使用。
从 Docker 1.12 起，Docker Engine 自带的 [Docker Swarm](https://docs.docker.com/engine/swarm/key-concepts/) 支持卷功能，可通过 [swarm compose v3](https://docs.docker.com/compose/compose-file/compose-file-v3/#volume-configuration-reference) 文件中的描述来创建卷，供跨多个集群节点的 *swarm 堆栈* 使用。

[Docker 卷插件](https://docs.docker.com/engine/extend/plugins_volume/) 扩展了 Docker 内置的默认 `local` 卷驱动，提供跨容器和主机的有状态共享卷。与本地卷不同，当此类卷被删除时，你的数据 *不会* 被删除。插件可以由 Docker 守护进程托管运行，也可以作为原生系统服务（在 systemd、*sysv* 或 *upstart* 下）或作为独立可执行文件运行。
Rclone 可以在所有这些模式下作为 Docker 卷插件运行。它通过[插件 API](https://docs.docker.com/engine/extend/plugin_api/) 与本地 Docker 守护进程交互，并处理远程文件系统到 Docker 容器的挂载，因此它必须与 Docker 守护进程在同一主机上运行，或者在每个 Swarm 节点上运行。

## 快速入门

在第一个示例中，我们将在一台独立的 Ubuntu 机器上使用 [SFTP](/sftp/) rclone 卷配合 Docker 引擎。

首先在主机上[安装 Docker](https://docs.docker.com/engine/install/)。

*FUSE* 驱动是 rclone 挂载的先决条件，需要在主机上安装：

```console
sudo apt-get -y install fuse3
```

创建 rclone Docker 插件所需的两个目录：

```console
sudo mkdir -p /var/lib/docker-plugins/rclone/config
sudo mkdir -p /var/lib/docker-plugins/rclone/cache
```

为你的架构（此处为 `amd64`）安装托管式 rclone Docker 插件：

```console
docker plugin install rclone/docker-volume-rclone:amd64 args="-v" --alias rclone --grant-all-permissions
docker plugin list
```

创建你的 [SFTP 卷](/sftp/#standard-options)：

```console
docker volume create firstvolume -d rclone -o type=sftp -o sftp-host=_hostname_ -o sftp-user=_username_ -o sftp-pass=_password_ -o allow-other=true
```

请注意，由于所有选项都是静态的，你甚至不需要运行 `rclone config` 或创建 `rclone.conf` 文件（但 `config` 目录仍然需要存在）。在最简单的情况下，你可以使用 `localhost` 作为 *hostname*，使用你的 SSH 凭据作为 *username* 和 *password*。你还可以将远程路径更改为主机上的主目录，例如 `-o path=/home/username`。

现在创建一个测试容器并将卷挂载到其中：

```console
docker run --rm -it -v firstvolume:/mnt --workdir /mnt ubuntu:latest bash
```

如果一切顺利，你将进入新容器并直接切换到已挂载的 SFTP 远程目录。你可以输入 `ls` 列出挂载目录的内容或进行其他操作。完成后输入 `exit`。容器将停止，但卷会保留，可以重复使用。当不再需要时，删除它：

```console
docker volume list
docker volume remove firstvolume
```

现在让我们尝试**更复杂的操作**：在多节点 Docker Swarm 上使用 [Google Drive](/drive/) 卷。

你需要先在每个 Swarm 节点上安装 Docker 和 FUSE、创建插件目录并安装 rclone 插件。然后[设置 Swarm](https://docs.docker.com/engine/swarm/swarm-mode/)。

Google Drive 卷需要访问令牌，可以通过 Web 浏览器进行设置，并由 rclone 定期续期。托管式插件无法运行浏览器，因此我们将使用类似于[在无头机器上设置 rclone](/remote_setup/) 的技术。

在*另一台*配备 *Web 浏览器* 和图形用户界面的机器上运行 [rclone config](/commands/rclone_config_create/)。创建 [Google Drive 远程存储](/drive/#standard-options)。完成后，将生成的 `rclone.conf` 传输到 Swarm 集群，并保存为 `/var/lib/docker-plugins/rclone/config/rclone.conf` 到*每个*节点上。默认情况下，此位置仅 root 用户可访问，因此你需要相应的权限。生成的配置如下所示：

```ini
[gdrive]
type = drive
scope = drive
drive_id = 1234567...
root_folder_id = 0Abcd...
token = {"access_token":...}
```

现在创建名为 `example.yml` 的文件，包含如下 Swarm 堆栈描述：

```yaml
version: '3'
services:
  heimdall:
    image: linuxserver/heimdall:latest
    ports: [8080:80]
    volumes: [configdata:/config]
volumes:
  configdata:
    driver: rclone
    driver_opts:
      remote: 'gdrive:heimdall'
      allow_other: 'true'
      vfs_cache_mode: full
      poll_interval: 0
```

然后运行堆栈：

```console
docker stack deploy example -c ./example.yml
```

几秒钟后，Docker 将把解析后的堆栈描述分发到集群，在端口 *8080* 上创建 `example_heimdall` 服务，在一个或多个集群节点上运行服务容器，并向节点主机上的 rclone 插件请求 `example_configdata` 卷。你可以使用以下命令确认结果：

```console
docker service ls
docker service ps example_heimdall
docker volume ls
```

在浏览器中访问 `http://cluster.host.address:8080` 来使用该服务。完成后使用 `docker stack remove example` 停止它。请注意，在集群节点上按需创建的 `example_configdata` 卷不会随堆栈自动删除，而是保留供将来复用。你可以在每个节点上手动执行 `docker volume remove example_configdata` 命令来删除它们。

## 通过 CLI 创建卷

可以使用 [docker volume create](https://docs.docker.com/engine/reference/commandline/volume_create/) 创建卷。以下是几个示例：

```console
docker volume create vol1 -d rclone -o remote=storj: -o vfs-cache-mode=full
docker volume create vol2 -d rclone -o remote=:storj,access_grant=xxx:heimdall
docker volume create vol3 -d rclone -o type=storj -o path=heimdall -o storj-access-grant=xxx -o poll-interval=0
```

注意 `-d rclone` 标志告诉 Docker 从 rclone 驱动请求卷。即使你安装托管驱动时使用了全名 `rclone/docker-volume-rclone`，这也有效，因为你提供了 `--alias rclone` 选项。

可以这样查看卷：

```console
docker volume list
docker volume inspect vol1
```

## 卷配置

Rclone 标志和卷选项通过 `docker volume create` 命令的 `-o` 标志设置。它们包括后端特定参数以及挂载和 *VFS* 选项。此外还有一些特殊的 `-o` 选项：`remote`、`fs`、`type`、`path`、`mount-type` 和 `persist`。

`remote` 指定配置文件中已有的远程存储名称，带尾随冒号，可选地带有远程路径。完整语法参见 [rclone 文档](/docs/#syntax-of-remote-paths)。此选项可以使用别名 `fs`，以避免与 *crypt* 或 *alias* 等后端的 *remote* 参数混淆。

`remote=:backend:dir/subdir` 语法可用于创建[即时（无配置）远程存储](/docs/#backend-path-to-dir)，而 `type` 和 `path` 选项为此提供了更简单的替代方案。使用两个拆分选项

```text
-o type=backend -o path=dir/subdir
```

等效于组合语法

```text
-o remote=:backend:dir/subdir
```

但在脚本中参数化更为方便。`path` 部分是可选的。

[挂载和 VFS 选项](/commands/rclone_serve_docker/#options) 以及[后端参数](/flags/#backend) 的命名方式与其对应的命令行标志相同，但不含 `--` CLI 前缀。你也可以在选项名称中使用下划线代替连字符。例如，`--vfs-cache-mode full` 变为 `-o vfs-cache-mode=full` 或 `-o vfs_cache_mode=full`。无值的布尔 CLI 标志将获得 `true` 值，例如 `--allow-other` 变为 `-o allow-other=true` 或 `-o allow_other=true`。

请注意，你只能为挂载的 `remote` 的后端类型直接引用的后端提供参数。如果这是 *alias*、*chunker* 或 *crypt* 等封装后端，则无法为所引用的远程存储或后端提供选项。此限制由 rclone 连接字符串解析器施加。唯一的变通方法是向插件提供 `rclone.conf` 或配置插件参数（见下文）。

## 特殊卷选项

`mount-type` 决定挂载方式，通常可以是 `mount`、`cmount` 或 `mount2` 之一。此选项可以使用别名 `mount_type`。需要注意的是，托管式 rclone Docker 插件目前不支持 `cmount` 方法，而 `mount2` 很少需要。此选项默认为第一个找到的方法，通常是 `mount`，因此你一般不需要使用它。

`persist` 是一个保留的布尔（true/false）选项。将来它将允许在插件的 `rclone.conf` 文件中持久化即时远程存储。

## 连接字符串

`remote` 值可以通过[连接字符串](/docs/#connection-strings) 进行扩展，作为提供后端参数的替代方式。这等效于 `-o` 后端选项，但有一个*语法差异*：在连接字符串内部，参数名必须去掉后端前缀，但在 `-o param=value` 数组中必须保留。例如，比较以下选项数组

```text
-o remote=:sftp:/home -o sftp-host=localhost
```

与等效的连接字符串：

```text
-o remote=:sftp,host=localhost:/home
```

此差异存在的原因是 `-o key=val` 标志选项不仅包含后端参数，还包含挂载/VFS 标志以及其他可能的设置。同时它还允许区分 `remote` 选项与 `crypt-remote`（或类似命名的后端参数），并且可以说由于更清晰的值替换方式而简化了脚本编写。

## 配合 Swarm 或 Compose 使用

*Docker Swarm* 和 *Docker Compose* 都使用 [YAML](http://yaml.org/spec/1.2/spec.html) 格式的文本文件来描述容器组（堆栈）、它们的属性、网络和卷。*Compose* 使用 [compose v2](https://docs.docker.com/compose/compose-file/compose-file-v2/#volume-configuration-reference) 格式，*Swarm* 使用 [compose v3](https://docs.docker.com/compose/compose-file/compose-file-v3/#volume-configuration-reference) 格式。它们大部分相似，差异在 [Docker 文档](https://docs.docker.com/compose/compose-file/compose-versioning/#upgrading)中有说明。

卷由顶级 `volumes:` 节点的子项描述。每个子项以其卷名命名，至少需要两个元素：不言自明的 `driver: rclone` 值和 `driver_opts:` 结构，后者与 `-o key=val` CLI 标志作用相同：

```yaml
volumes:
  volume_name_1:
    driver: rclone
    driver_opts:
      remote: 'gdrive:'
      allow_other: 'true'
      vfs_cache_mode: full
      token: '{"type": "borrower", "expires": "2021-12-31"}'
      poll_interval: 0
```

注意几个重要细节：

- YAML 更倾向于在选项名称中使用 `_` 而不是 `-`。
- YAML 对单引号和双引号一视同仁。简单字符串和整数可以不加引号。
- 布尔值必须加引号，如 `'true'` 或 `"false"`，因为这两个词是 YAML 的保留字。
- 文件系统字符串使用 `remote`（或 `fs`）作为键名。通常可以省略引号，但如果字符串以冒号结尾，你**必须**加引号，如 `remote: "storage_box:"`。
- YAML 对值中的花括号非常敏感，因为这实际上是另一种[键/值映射语法](http://yaml.org/spec/1.2/spec.html#id2790832)。例如，JSON 访问令牌通常包含双引号和花括号，因此你必须用单引号将其括起来。

## 作为托管插件安装

Docker 守护进程可以从镜像仓库安装插件并以托管方式运行。我们在 [Docker Hub](https://hub.docker.com) 上维护 [docker-volume-rclone](https://hub.docker.com/p/rclone/docker-volume-rclone/) 插件镜像。

Rclone 卷插件要求 **Docker Engine >= 19.03.15**

在安装插件之前，主机上必须存在两个目录。请注意，插件**不会**自动创建它们。默认情况下，它们必须在主机上的以下位置存在（不过你可以调整路径）：

- `/var/lib/docker-plugins/rclone/config` 用于存放 `rclone.conf` 配置文件，即使为空且配置文件不存在也**必须**存在。
- `/var/lib/docker-plugins/rclone/cache` 用于存放插件状态文件以及可选的 VFS 缓存。

你可以使用以下命令以默认设置[安装托管插件](https://docs.docker.com/engine/reference/commandline/plugin_install/)：

```console
docker plugin install rclone/docker-volume-rclone:amd64 --grant-all-permissions --alias rclone
```

镜像规范中冒号后面的 `:amd64` 部分称为*标签*。通常你会希望安装适合你架构的最新插件。在这种情况下，标签只需指定架构名，如上面的 `amd64`。目前可用的插件架构如下：

- `amd64`
- `arm64`
- `arm-v7`

有时你可能需要特定版本的插件，而不是最新版。此时应使用 `:架构-版本` 格式的镜像标签。例如，要在 `arm64` 架构上安装 `v1.56.2` 版本的插件，你应使用标签 `arm64-1.56.2`（注意去掉了 `v`），因此完整的镜像规范为 `rclone/docker-volume-rclone:arm64-1.56.2`。

我们还提供了 `latest` 插件标签，但由于截至撰写本文时 Docker 不支持多架构插件，此标签目前是 **`amd64` 的别名**。按照惯例，`latest` 标签是默认的，可以省略，因此 `rclone/docker-volume-rclone:latest` 和 `rclone/docker-volume-rclone` 都指向 `amd64` 平台的最新插件版本。

此外，`amd64` 部分也可以从带版本号的 rclone 插件标签中省略。例如，rclone 镜像引用 `rclone/docker-volume-rclone:amd64-1.56.2` 可以简写为 `rclone/docker-volume-rclone:1.56.2`。但是，对于非 Intel 架构，你仍须使用完整标签，因为 `amd64` 或 `latest` 将无法启动。

托管插件实际上是一个运行在与普通 Docker 容器分开的命名空间中的特殊容器。它在内部运行 `rclone serve docker` 命令。配置和缓存目录在启动时被绑定挂载到容器中。Docker 守护进程连接到该命令在容器内创建的 Unix 套接字。该命令按需在内部创建远程挂载，然后 Docker 机制通过内核挂载命名空间将其传播并绑定挂载到请求的用户容器中。

你可以在插件禁用（未使用）后调整一些插件设置，例如：

```console
docker plugin disable rclone
docker plugin set rclone RCLONE_VERBOSE=2 config=/etc/rclone args="--vfs-cache-mode=writes --allow-other"
docker plugin enable rclone
docker plugin inspect rclone
```

请注意，如果 Docker 拒绝禁用插件，你需要找到并删除所有与之关联的活动卷以及使用这些卷的容器和 Swarm 服务。这相当繁琐，因此请提前仔细规划。

你可以调整以下设置：`args`、`config`、`cache`、`HTTP_PROXY`、`HTTPS_PROXY`、`NO_PROXY` 和 `RCLONE_VERBOSE`。保持各 Swarm 集群节点上的插件设置同步是*你*的责任。

`args` 设置 `rclone serve docker` 命令的命令行参数（默认为*无*）。参数应以空格分隔，因此你通常需要在 [docker plugin set](https://docs.docker.com/engine/reference/commandline/plugin_set/) 命令行上将它们放在引号中。支持 [serve docker 标志](/commands/rclone_serve_docker/#options) 和[通用 rclone 标志](/flags/)，包括将作为卷创建默认值使用的后端参数。请注意，如果 `args` 值为空，插件将失败（由于 [此 Docker 缺陷](https://github.com/moby/moby/blob/v20.10.7/plugin/v2/plugin.go#L195)）。可使用 `args="-v"` 作为变通方法。

`config=/host/dir` 设置配置目录的替代主机位置。插件将在此处查找 `rclone.conf`。配置文件不存在不是错误，但目录必须存在。请注意，插件可能会定期重写配置文件，例如在续期存储访问令牌时。请记住这一点，尽量避免插件与主机上可能同时尝试更改配置的其他 rclone 实例之间的竞争，以免导致 `rclone.conf` 损坏。你还可以在此目录中放置 SFTP 远程存储的私钥文件等内容。只需注意它会被绑定挂载到插件容器内的预定义路径 `/data/config`。例如，如果你的密钥文件在主机上名为 `sftp-box1.key`，则相应的卷配置选项应为 `-o sftp-key-file=/data/config/sftp-box1.key`。

`cache=/host/dir` 设置 *缓存* 目录的替代主机位置。插件将在此处保存 VFS 缓存。同时它将在此目录中创建和维护 `docker-plugin.state` 文件。当插件重启或重新安装时，它将在此文件中查找以重建之前存在的卷。但是，重启后这些卷不会重新挂载到使用它们的容器中。通常这不是问题，因为 Docker 守护进程通常会在故障、守护进程重启或主机重启后重启受影响的用户容器。

`RCLONE_VERBOSE` 设置插件的详细程度，从 `0`（仅错误，默认值）到 `2`（调试级别）。详细程度也可以通过 `args="-v [-v] ..."` 来调整。由于参数更通用，你很少需要此设置。插件输出默认会输入到本地主机上的 Docker 守护进程日志。日志条目在 Docker 日志中显示为*错误*，但在封装的消息字符串中保留了 rclone 分配的实际级别。

`HTTP_PROXY`、`HTTPS_PROXY`、`NO_PROXY` 用于自定义插件的代理设置。

你可以在安装插件时一次性设置自定义插件选项：

```console
docker plugin remove rclone
docker plugin install rclone/docker-volume-rclone:amd64 \
       --alias rclone --grant-all-permissions \
       args="-v --allow-other" config=/etc/rclone
docker plugin inspect rclone
```

## 健康检查

Docker 插件卷协议没有提供让插件通知 Docker 守护进程卷（不可）可用的方式。作为变通方法，你可以设置健康检查来验证挂载是否正常响应，例如：

```yaml
services:
  my_service:
    image: my_image
    healthcheck:
      test: ls /path/to/rclone/mount || exit 1
      interval: 1m
      timeout: 15s
      retries: 3
      start_period: 15s
```

## 在 Systemd 下运行插件

在大多数情况下，你应该优先使用托管模式。此外，macOS 和 Windows 不支持原生 Docker 插件。请在这些系统上使用托管模式。以下内容仅适用于 Linux。

首先，[安装 rclone](/install/)。你可以直接运行它（输入 `rclone serve docker` 并按回车）进行测试。

安装 *FUSE*：

```console
sudo apt-get -y install fuse
```

下载两个 systemd 配置文件：[docker-volume-rclone.service](https://raw.githubusercontent.com/rclone/rclone/master/contrib/docker-plugin/systemd/docker-volume-rclone.service) 和 [docker-volume-rclone.socket](https://raw.githubusercontent.com/rclone/rclone/master/contrib/docker-plugin/systemd/docker-volume-rclone.socket)。

将它们放到 `/etc/systemd/system/` 目录中：

```console
cp docker-volume-plugin.service /etc/systemd/system/
cp docker-volume-plugin.socket  /etc/systemd/system/
```

请注意，本节中的所有命令都必须以 *root* 身份运行，但为简洁起见我们省略了 `sudo` 前缀。
现在创建服务所需的目录：

```console
mkdir -p /var/lib/docker-volumes/rclone
mkdir -p /var/lib/docker-plugins/rclone/config
mkdir -p /var/lib/docker-plugins/rclone/cache
```

以套接字激活模式运行 Docker 插件服务：

```console
systemctl daemon-reload
systemctl start docker-volume-rclone.service
systemctl enable docker-volume-rclone.socket
systemctl start docker-volume-rclone.socket
systemctl restart docker
```

或者直接运行服务：

- 运行 `systemctl daemon-reload` 让 systemd 读取新配置
- 运行 `systemctl enable docker-volume-rclone.service` 使新服务在开机时自动启动
- 运行 `systemctl start docker-volume-rclone.service` 立即启动服务
- 运行 `systemctl restart docker` 重启 Docker 守护进程以检测新的插件套接字。请注意，在托管模式下不需要此步骤，因为 Docker 知晓插件状态变更。

这两种方法从用户角度来看是等效的，但我个人更倾向于套接字激活方式。

## 故障排除

你可以使用以下命令[查看托管插件的设置](https://docs.docker.com/engine/extend/#debugging-plugins)：

```console
docker plugin list
docker plugin inspect rclone
```

请注意，Docker（包括最新的 20.10.7）不会显示 `args` 的实际值，只显示默认值。

使用 `journalctl --unit docker` 可以在 Docker 守护进程日志中查看托管插件的输出。请注意，Docker 将插件行显示为*错误*，但它们的实际级别可以从封装的消息字符串中看出。

你通常会安装适合你平台的最新版本托管插件。使用以下命令打印实际安装的版本：

```console
PLUGID=$(docker plugin list --no-trunc | awk '/rclone/{print$1}')
sudo runc --root /run/docker/runtime-runc/plugins.moby exec $PLUGID rclone version
```

你甚至可以使用 `runc` 在插件容器内运行 shell：

```console
sudo runc --root /run/docker/runtime-runc/plugins.moby exec --tty $PLUGID bash
```

你还可以使用 curl 检查插件套接字连接：

```console
docker plugin list --no-trunc
PLUGID=123abc...
sudo curl -H Content-Type:application/json -XPOST -d {} --unix-socket /run/docker/plugins/$PLUGID/rclone.sock http://localhost/Plugin.Activate
```

不过这很少需要。

如果插件无法正常工作，并且在你尝试了上述方法进行诊断后仍无结果，作为最后的手段，你可以尝试清除插件状态。**请注意，所有现有的 rclone Docker 卷可能都需要重新创建。** 这可能是必要的，因为重新安装不会清除现有的状态文件以便于轻松恢复，如上所述。

```console
docker plugin disable rclone # disable the plugin to ensure no interference
sudo rm /var/lib/docker-plugins/rclone/cache/docker-plugin.state # removing the plugin state
docker plugin enable rclone # re-enable the plugin afterward
```

## 注意事项

最后我想提一下*更新卷设置时的注意事项*。Docker CLI 没有专门的命令如 `docker volume update`。你可能会想在现有卷上使用带有更新选项的 `docker volume create`，但这里有个陷阱：该命令不会执行任何操作，甚至不会返回错误。我希望 Docker 维护者有朝一日能修复此问题。在此期间，请注意你必须先删除卷，然后才能使用新设置重新创建：

```console
docker volume remove my_vol
docker volume create my_vol -d rclone -o opt1=new_val1 ...
```

并验证设置确实已更新：

```console
docker volume list
docker volume inspect my_vol
```

如果 Docker 拒绝删除卷，你需要找到使用它的容器或 Swarm 服务并先停止它们。
