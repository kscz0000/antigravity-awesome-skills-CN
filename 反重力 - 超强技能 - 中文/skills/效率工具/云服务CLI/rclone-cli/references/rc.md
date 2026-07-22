---
title: "Remote Control / API"
description: "使用 API 远程控制 rclone、rc 命令、HTTP 接口、异步任务、选项配置、VFS、mount、pprof 性能分析。rclone 远程控制、API 编程接口、rc 命令语法、HTTP 远程调用、异步作业管理、过滤器配置、VFS 缓存、调试性能。"
versionIntroduced: "v1.40"
---

> **官方文档：** [https://rclone.org/rc/](https://rclone.org/rc/)
# 使用 API 远程控制 rclone

如果 rclone 使用 `--rc` 参数启动，则会启动一个 HTTP 服务器，
该服务器可通过 API 远程控制 rclone。

你可以使用 [rc](#api-rc) 命令访问 API，
也可以[直接使用 HTTP](#api-http)。

如果只想运行一个远程控制，请参阅 [rcd](/commands/rclone_rcd/) 命令。

## 支持的参数

### --rc

启动 HTTP 服务器以监听远程请求的标志。

### --rc-addr=IP

绑定服务器的 IPaddress:Port 或 :Port。（默认 "localhost:5572"）。

### --rc-cert=KEY

SSL PEM 密钥（证书和 CA 证书的拼接）。

### --rc-client-ca=PATH

用于验证客户端的客户端证书颁发机构。

### --rc-htpasswd=PATH

htpasswd 文件 - 如果未提供则不进行身份验证。

### --rc-key=PATH

TLS PEM 私钥文件。

### --rc-max-header-bytes=VALUE

请求头的最大大小（默认 4096）。

### --rc-min-tls-version=VALUE

可接受的最低 TLS 版本。有效值为 "tls1.0"、
"tls1.1"、"tls1.2" 和 "tls1.3"（默认 "tls1.0"）。

### --rc-user=VALUE

用于身份验证的用户名。

### --rc-pass=VALUE

用于身份验证的密码。

### --rc-realm=VALUE

身份验证的域（默认 "rclone"）。

### --rc-server-read-timeout=DURATION

服务器读取数据的超时时间（默认 1h0m0s）。

### --rc-server-write-timeout=DURATION

服务器写入数据的超时时间（默认 1h0m0s）。

### --rc-serve

启用通过 HTTP 接口提供远程对象服务。这意味着
默认情况下可通过 `http://127.0.0.1:5572/` 访问对象，
因此你可以浏览 `http://127.0.0.1:5572/` 或 `http://127.0.0.1:5572/*`
以查看远程列表。可以使用此语法从远程请求对象
`http://127.0.0.1:5572/[remote:path]/path/to/object`

默认关闭。

### --rc-serve-no-modtime

设置此标志可跳过读取修改时间（可加快速度）。

默认关闭。

### --rc-files /path/to/directory

在 HTTP 服务器上提供服务的本地文件路径。

如果设置了此参数，rclone 将提供该目录中的文件。如果指定了
浏览器根目录，它还会在 Web 浏览器中打开根目录。这用于
为 rclone 函数实现基于浏览器的 GUI。

如果设置了 `--rc-user` 或 `--rc-pass`，则打开的 URL 将
采用 `http://user:pass@localhost/` 形式在 URL 中包含授权信息。

默认关闭。

### --rc-enable-metrics

在 `/metrics` 启用与 OpenMetrics/Prometheus 兼容的端点。
如果需要对指标进行更多控制（例如在不同端口或使用不同身份验证运行），
则可以改用 `--metrics-*` 标志启用端点。

默认关闭。

### --rc-web-gui

设置此标志可在与 rclone 相同的端口上提供默认 Web GUI。

默认关闭。

### --rc-allow-origin

为 rc 请求设置允许的 Access-Control-Allow-Origin。

如果 rclone 运行的 IP 与 web-gui 不同，则可与 --rc-web-gui 配合使用。

默认为 rc 正在运行的 IP 地址。

### --rc-web-fetch-url

设置用于获取 rclone-web-gui 文件的 URL。

默认 <https://api.github.com/repos/rclone/rclone-webui-react/releases/latest>。

### --rc-web-gui-update

设置此标志以从 rc-web-fetch-url 检查并更新 rclone-webui-react。

默认关闭。

### --rc-web-gui-force-update

设置此标志以从 rc-web-fetch-url 强制更新 rclone-webui-react。

默认关闭。

### --rc-web-gui-no-open-browser

设置此标志可在使用 web-gui 时禁用自动打开浏览器。

默认关闭。

### --rc-job-expire-duration=DURATION

使早于 DURATION 的已完成异步任务过期（默认 60s）。

### --rc-job-expire-interval=DURATION

检查已过期异步任务的间隔时长（默认 10s）。

### --rc-no-auth

默认情况下，rclone 将要求在 rc 接口上设置授权，
以便使用任何访问 rclone 远程的方法。例如 `operations/list`
被拒绝，因为它涉及创建远程，`sync/copy` 也是如此。

如果设置了此参数，则在服务器上使用这些方法不需要授权。
另一种方法是使用 `--rc-user` 和 `--rc-pass` 并在请求中使用这些凭据。

默认关闭。

### --rc-baseurl

URL 的前缀。

默认为根目录

### --rc-template

用户指定的模板。

## 通过 rclone rc 命令访问远程控制 {#api-rc}

Rclone 本身在其 `rclone rc` 命令中实现了远程控制协议。

你可以这样使用它：

```console
$ rclone rc rc/noop param1=one param2=two
{
    "param1": "one",
    "param2": "two"
}
```

如果远程在不同于默认 `http://localhost:5572/` 的 URL 上运行，
请使用 `--url` 选项指定它：

```console
rclone rc --url http://some.remote:1234/ rc/noop
```

或者，如果远程正在侦听 Unix 套接字，请改用 `--unix-socket` 选项：

```console
rclone rc --unix-socket /tmp/rclone.sock rc/noop
```

单独运行 `rclone rc`（不带任何命令）以查看已安装的远程控制命令的帮助。
请注意，这还需要连接到远程服务器。

## JSON 输入

`rclone rc` 还支持 `--json` 标志，可用于发送更复杂的输入参数。

```console
$ rclone rc --json '{ "p1": [1,"2",null,4], "p2": { "a":1, "b":2 } }' rc/noop
{
    "p1": [
        1,
        "2",
        null,
        4
    ],
    "p2": {
        "a": 1,
        "b": 2
    }
}
```

如果传递的参数是对象，则可以将其作为 JSON 字符串传递，
而不是使用 `--json` 标志，从而简化命令行。

```console
rclone rc operations/list fs=/tmp remote=test opt='{"showHash": true}'
```

而不是

```console
rclone rc operations/list --json '{"fs": "/tmp", "remote": "test", "opt": {"showHash": true}}'
```

## 特殊参数

rc 接口支持一些适用于**所有**命令的特殊参数。它们以 `_` 开头，
以表示它们是不同的。

### 使用 _async = true 运行异步任务

每次 rc 调用都被归类为一项任务，并被分配自己的 id。默认情况下，
任务在创建时或同步地立即执行。

如果在 rc 调用中提供了 `_async` 且值为 true，则它将
立即返回一个任务 id 和 execute id，并且该任务将在后台运行。
`job/status` 调用可用于获取后台任务的信息。
任务完成后最多可以查询 1 分钟。

建议使用 `_async` 标志运行可能长时间运行的任务，例如 `sync/sync`、
`sync/copy`、`sync/move`、`operations/purge`，以避免 HTTP 请求和
响应超时可能导致的任何问题。

使用 `_async` 标志启动任务：

```console
$ rclone rc --json '{ "p1": [1,"2",null,4], "p2": { "a":1, "b":2 }, "_async": true }' rc/noop
{
    "jobid": 2,
    "executeId": "d794c33c-463e-4acf-b911-f4b23e4f40b7"
}
```

`jobid` 是此 rclone 实例中任务的唯一标识符。
`executeId` 标识 rclone 进程实例，并在 rclone 重启后更改。
两者组合（`executeId`、`jobid`）可在 rclone 重启后唯一标识一项任务。

查询状态以查看任务是否已完成。有关这些返回参数含义的更多信息，
请参阅 `job/status` 调用。

```console
$ rclone rc --json '{ "jobid":2 }' job/status
{
    "duration": 0.000124163,
    "endTime": "2018-10-27T11:38:07.911245881+01:00",
    "error": "",
    "executeId": "d794c33c-463e-4acf-b911-f4b23e4f40b7",
    "finished": true,
    "id": 2,
    "output": {
        "_async": true,
        "p1": [
            1,
            "2",
            null,
            4
        ],
        "p2": {
            "a": 1,
            "b": 2
        }
    },
    "startTime": "2018-10-27T11:38:07.911121728+01:00",
    "success": true
}
```

`job/list` 可用于显示正在运行或最近完成的任务及其状态

```console
$ rclone rc job/list
{
    "executeId": "d794c33c-463e-4acf-b911-f4b23e4f40b7",
    "finished_ids": [
        1
    ],
    "jobids": [
        1,
        2
    ],
    "running_ids": [
        2
    ]
}
```

这表示：
- `executeId` - 当前 rclone 实例 ID（所有任务相同，重启后更改）
- `jobids` - 所有任务 ID 的数组（包括运行中和已完成的）
- `running_ids` - 当前正在运行的任务 ID 的数组
- `finished_ids` - 已完成的任务 ID 的数组

### 使用 _config 设置配置标志

如果希望仅为 rc 调用的持续时间设置配置（等同于全局标志），
请传入 `_config` 参数。

这应与 [options/get](#options-get) 返回的 `main` 键的格式相同。

```console
rclone rc --loopback options/get blocks=main
```

你可以使用此命令查看有关这些选项的更多帮助
（有关更多信息，请参阅[选项块部分](#option-blocks)）。

```console
rclone rc --loopback options/info blocks=main
```

例如，如果希望使用 `--checksum` 参数运行 sync，
则应在 JSON blob 中传递此参数。

```json
"_config":{"CheckSum": true}
```

如果使用 `rclone rc`，则可以这样传递

```console
rclone rc sync/sync ... _config='{"CheckSum": true}'
```

未设置的任何配置参数都将继承使用命令行标志或环境变量设置的全局默认值。

请注意，可以将某些值设置为字符串或整数 -
有关更多信息，请参阅[数据类型](#data-types)。以下是
以字符串或整数格式设置等同于 `--buffer-size` 的示例。

```json
"_config":{"BufferSize": "42M"}
"_config":{"BufferSize": 44040192}
```

如果希望检查 `_config` 分配是否正常工作，
则调用 `options/local` 将显示该值被设置为什么。

### 使用 _filter 设置过滤器标志

如果希望仅为 rc 调用的持续时间设置过滤器，
请传入 `_filter` 参数。

这应与 [options/get](#options-get) 返回的 `filter` 键的格式相同。

```console
rclone rc --loopback options/get blocks=filter
```

你可以使用此命令查看有关这些选项的更多帮助
（有关更多信息，请参阅[选项块部分](#option-blocks)）。

```console
rclone rc --loopback options/info blocks=filter
```

例如，如果希望使用这些标志运行 sync

```text
--max-size 1M --max-age 42s --include "a" --include "b"
```

你应在 JSON blob 中传递此参数。

```json
"_filter":{"MaxSize":"1M", "IncludeRule":["a","b"], "MaxAge":"42s"}
```

如果使用 `rclone rc`，则可以这样传递

```console
rclone rc ... _filter='{"MaxSize":"1M", "IncludeRule":["a","b"], "MaxAge":"42s"}'
```

未设置的任何过滤器参数都将继承使用命令行标志或环境变量设置的全局默认值。

请注意，可以将某些值设置为字符串或整数 -
有关更多信息，请参阅[数据类型](#data-types)。以下是
以字符串或整数格式设置等同于 `--buffer-size` 的示例。

```json
"_filter":{"MinSize": "42M"}
"_filter":{"MinSize": 44040192}
```

如果希望检查 `_filter` 分配是否正常工作，
则调用 `options/local` 将显示该值被设置为什么。

### 使用 _group = value 将操作分配到组

每次 rc 调用都有自己的统计组用于跟踪其指标。默认情况下，
分组由前缀 `job/` 和任务 id 组成的复合组名完成，
例如 `job/1`。

如果 `_group` 有值，则该请求的统计信息将在该值下分组。
这允许调用方在其自己的名称下对统计信息进行分组。

可以通过将 `group` 传递给 `core/stats` 来访问特定组的统计信息：

```console
$ rclone rc --json '{ "group": "job/1" }' core/stats
{
    "speed": 12345
    ...
}
```

## 数据类型 {#data-types}

当 API 返回类型时，这些类型大多是直接的
整数、字符串或布尔类型。

但是 [options/get](#options-get) 调用返回的某些类型，
以及 [options/set](#options-set) 调用、`vfsOpt`、`mountOpt`
和 `_config` 参数接受的某些类型。

- `Duration` - 这些以整数纳秒持续时间的形式返回。
  它们可以设置为整数，也可以使用时间字符串设置，例如 "5s"。
  有关更多信息，请参阅[选项部分](/docs/#options)。
- `Size` - 这些以整数字节数返回。它们可以设置为整数，
  也可以使用大小后缀字符串设置，例如 "10M"。
  有关更多信息，请参阅[选项部分](/docs/#options)。
- 枚举类型（例如 `CutoffMode`、`DumpFlags`、`LogLevel`、
  `VfsCacheMode` - 这些将以整数形式返回，并且可以设置为整数，
  但更方便的是可以设置为字符串，例如
  `CutoffMode` 的 "HARD" 或 `LogLevel` 的 "DEBUG"。
- `BandwidthSpec` - 这将以字符串形式设置和返回，例如 "1M"。

### 选项块 {#option-blocks}

可以使用 [options/info](#options-info) 调用（用于主要配置）和
[config/providers](#config-providers) 调用（用于后端配置）来
获取 rclone 配置选项的信息。这可用于构建用于显示和设置任何 rclone
选项的用户界面。

它们由 `Option` 块数组组成。这些具有以下
格式。每个块描述一个选项。

| Field | Type | Optional | Description |
|-------|------|----------|-------------|
| Name       | string     | N | name of the option in snake_case |
| FieldName  | string     | N | name of the field used in the rc - if blank use Name. May contain "." for nested fields. |
| Help       | string     | N | help, started with a single sentence on a single line |
| Groups     | string     | Y | groups this option belongs to - comma separated string for options classification |
| Provider   | string     | Y | set to filter on provider |
| Default    | any        | N | default value, if set (and not to nil or "") then Required does nothing |
| Value      | any        | N | value to be set by flags |
| Examples   | Examples   | Y | predefined values that can be selected from list (multiple-choice option) |
| ShortOpt   | string     | Y | the short command line option for this |
| Hide       | Visibility | N | if non zero, this option is hidden from the configurator or the command line |
| Required   | bool       | N | this option is required, meaning value cannot be empty unless there is a default |
| IsPassword | bool       | N | set if the option is a password |
| NoPrefix   | bool       | N | set if the option for this should not use the backend prefix |
| Advanced   | bool       | N | set if this is an advanced config option |
| Exclusive  | bool       | N | set if the answer can only be one of the examples (empty string allowed unless Required or Default is set) |
| Sensitive  | bool       | N | set if this option should be redacted when using `rclone config redacted` |

此示例可能是 `--log-level` 标志。请注意，选项的
`Name` 变为命令行标志，其中 `_` 替换为 `-`。

```json
{
    "Advanced": false,
    "Default": 5,
    "DefaultStr": "NOTICE",
    "Examples": [
        {
            "Help": "",
            "Value": "EMERGENCY"
        },
        {
            "Help": "",
            "Value": "ALERT"
        },
        ...
    ],
    "Exclusive": true,
    "FieldName": "LogLevel",
    "Groups": "Logging",
    "Help": "Log level DEBUG|INFO|NOTICE|ERROR",
    "Hide": 0,
    "IsPassword": false,
    "Name": "log_level",
    "NoPrefix": true,
    "Required": true,
    "Sensitive": false,
    "Type": "LogLevel",
    "Value": null,
    "ValueStr": "NOTICE"
},
```

请注意 `Help` 可能是由 `\n` 分隔的多行。第一行始终是一个短句，
这是运行 `rclone help flags` 时显示的句子。

## 指定要使用的远程

根据所使用的命令，使用 `fs=`、`srcFs=`、`dstFs=` 参数指定远程。

参数可以是字符串，如 rclone 的其余部分，例如
`s3:bucket/path` 或 `:sftp:/my/dir`。它们也可以指定为 JSON blob。

如果指定 JSON blob，它应该是将字符串映射到字符串的对象。
这些值将用于配置远程。可以设置 3 个特殊值：

- `type` - 设置为 `type` 以指定名为 `:type:` 的远程
- `_name` - 设置为 `name` 以指定名为 `name:` 的远程
- `_root` - 设置远程的根目录 - 可以为空

通常应设置 `_name` 或 `type` 之一。如果需要 `local` 后端，
则应将 `type` 设置为 `local`。如果未指定 `_root`，
则默认为远程的根目录。

例如，此 JSON 等同于 `remote:/tmp`

```json
{
    "_name": "remote",
    "_root": "/tmp"
}
```

而这等同于 `:sftp,host='example.com':/tmp`

```json
{
    "type": "sftp",
    "host": "example.com",
    "_root": "/tmp"
}
```

而这等同于 `/tmp/dir`

```json
{
    "type": "local",
    "_root": "/tmp/dir"
}
```

## 支持的命令
<!-- autogenerated start "- run make rcdocs - don't edit here" -->
### backend/command: 运行后端命令。 {#backend-command}

此调用接受以下参数：

- command - 包含命令名称的字符串
- fs - 远程名称字符串，例如 "drive:"
- arg - 后端命令的参数列表
- opt - 选项的字符串到字符串映射

返回：

- result - 后端命令的结果

示例：

    rclone rc backend/command command=noop fs=. -o echo=yes -o blue -a path1 -a path2

返回

```
{
	"result": {
		"arg": [
			"path1",
			"path2"
		],
		"name": "noop",
		"opt": {
			"blue": "",
			"echo": "yes"
		}
	}
}
```

请注意，这直接等同于使用此 "backend" 命令：

    rclone backend noop . -o echo=yes -o blue path1 path2

请注意，参数必须以 "-a" 标志为前缀

有关更多信息，请参阅 [backend](/commands/rclone_backend/) 命令。

**此调用需要身份验证。**

### cache/expire: 从缓存中清除远程 {#cache-expire}

从缓存后端清除远程。支持目录或文件。
参数：
  - remote = 远程的路径（必需）
  - withData = true/false 也删除缓存的数据（块）（可选）

例如

    rclone rc cache/expire remote=path/to/sub/folder/
    rclone rc cache/expire remote=/ withData=true

### cache/fetch: 获取文件块 {#cache-fetch}

确保指定的文件块已缓存在磁盘上。

chunks= 参数指定要检查的文件块。
它接受以逗号分隔的数组切片索引列表。
切片索引类似于 Python 切片：start[:end]

start 是从文件开头开始的 0 基块编号（含）以获取。
end 是从文件开头开始的 0 基块编号（不含）以获取。
两个值都可以为负，在这种情况下它们从文件
末尾开始计数。值 "-5:" 表示文件的最后 5 个块。

一些有效的示例是：
":5,-5:" -> 第一个和最后五个块
"0,-2" -> 第一个和倒数第二个块
"0:10" -> 头十个块

可以使用任何以 "file" 开头的键的参数来指定要获取的文件，例如

    rclone rc cache/fetch chunks=0 file=hello file2=home/goodbye

当在缓存之上使用 crypt 远程时，文件名会自动加密。

### cache/stats: 获取缓存统计信息 {#cache-stats}

显示缓存远程的统计信息。

### config/create: 为远程创建配置。 {#config-create}

此调用接受以下参数：

- name - 远程的名称
- parameters - \{ "key": "value" \} 对的映射
- type - 新远程的类型
- opt - 用于控制配置的字典
    - obscure - 声明密码是明文的且需要模糊处理
    - noObscure - 声明密码已经模糊处理且不需要模糊处理
    - noOutput - 不向 stdout 打印任何内容
    - nonInteractive - 不与用户交互，返回问题
    - continue - 使用答案继续配置过程
    - all - 询问所有配置问题而不仅仅是配置后的问题
    - state - 要重新启动的状态 - 与 continue 一起使用
    - result - 要重新启动的结果 - 与 continue 一起使用


有关上述内容的更多信息，请参阅 [config create](/commands/rclone_config_create/) 命令。

**此调用需要身份验证。**

### config/delete: 在配置文件中删除远程。 {#config-delete}

参数：

- name - 要删除的远程的名称

有关上述内容的更多信息，请参阅 [config delete](/commands/rclone_config_delete/) 命令。

**此调用需要身份验证。**

### config/dump: 转储配置文件。 {#config-dump}

返回一个 JSON 对象：
- key: value

其中键是远程名称，值是配置参数。

有关上述内容的更多信息，请参阅 [config dump](/commands/rclone_config_dump/) 命令。

**此调用需要身份验证。**

### config/get: 在配置文件中获取远程。 {#config-get}

参数：

- name - 要获取的远程的名称

有关上述内容的更多信息，请参阅 [config dump](/commands/rclone_config_dump/) 命令。

**此调用需要身份验证。**

### config/listremotes: 列出配置文件和环境中定义的远程。 {#config-listremotes}

返回
- remotes - 远程名称的数组

有关上述内容的更多信息，请参阅 [listremotes](/commands/rclone_listremotes/) 命令。

**此调用需要身份验证。**

### config/password: 为远程的配置文件设置密码。 {#config-password}

此调用接受以下参数：

- name - 远程的名称
- parameters - \{ "key": "value" \} 对的映射


有关上述内容的更多信息，请参阅 [config password](/commands/rclone_config_password/) 命令。

**此调用需要身份验证。**

### config/paths: 读取配置文件路径和其他重要路径。 {#config-paths}

返回具有以下键的 JSON 对象：

- config: 配置文件的路径
- cache: 缓存目录根目录的路径
- temp: 临时目录根目录的路径

例如

    {
        "cache": "/home/USER/.cache/rclone",
        "config": "/home/USER/.rclone.conf",
        "temp": "/tmp"
    }

有关上述内容的更多信息，请参阅 [config paths](/commands/rclone_config_paths/) 命令。

**此调用需要身份验证。**

### config/providers: 显示配置文件中提供程序的配置方式。 {#config-providers}

返回一个 JSON 对象：
- providers - 对象数组

有关上述内容的更多信息，请参阅 [config providers](/commands/rclone_config_providers/) 命令。

请注意，Options 块的格式与 "options/info" 返回的格式相同。
它们在 [option blocks](#option-blocks) 部分中描述。

**此调用需要身份验证。**

### config/setpath: 设置配置文件的路径 {#config-setpath}

参数：

- path - 要使用的配置文件的路径

**此调用需要身份验证。**

### config/unlock: 解锁配置文件。 {#config-unlock}

如果配置文件已锁定，则将其解锁。

参数：

- 'configPassword' - 用于解锁配置文件的密码

建议在进行此调用之前禁用 AskPassword

**此调用需要身份验证。**

### config/update: 更新远程的配置。 {#config-update}

此调用接受以下参数：

- name - 远程的名称
- parameters - \{ "key": "value" \} 对的映射
- opt - 用于控制配置的字典
    - obscure - 声明密码是明文的且需要模糊处理
    - noObscure - 声明密码已经模糊处理且不需要模糊处理
    - noOutput - 不向 stdout 打印任何内容
    - nonInteractive - 不与用户交互，返回问题
    - continue - 使用答案继续配置过程
    - all - 询问所有配置问题而不仅仅是配置后的问题
    - state - 要重新启动的状态 - 与 continue 一起使用
    - result - 要重新启动的结果 - 与 continue 一起使用


有关上述内容的更多信息，请参阅 [config update](/commands/rclone_config_update/) 命令。

**此调用需要身份验证。**

### core/bwlimit: 设置带宽限制。 {#core-bwlimit}

将带宽限制设置为传入的字符串。这应该是
单个带宽限制条目或一对 upload:download 带宽。

例如

    rclone rc core/bwlimit rate=off
    {
        "bytesPerSecond": -1,
        "bytesPerSecondTx": -1,
        "bytesPerSecondRx": -1,
        "rate": "off"
    }
    rclone rc core/bwlimit rate=1M
    {
        "bytesPerSecond": 1048576,
        "bytesPerSecondTx": 1048576,
        "bytesPerSecondRx": 1048576,
        "rate": "1M"
    }
    rclone rc core/bwlimit rate=1M:100k
    {
        "bytesPerSecond": 1048576,
        "bytesPerSecondTx": 1048576,
        "bytesPerSecondRx": 131072,
        "rate": "1M"
    }


如果未提供 rate 参数，则查询带宽

    rclone rc core/bwlimit
    {
        "bytesPerSecond": 1048576,
        "bytesPerSecondTx": 1048576,
        "bytesPerSecondRx": 1048576,
        "rate": "1M"
    }

参数的格式与传递给 --bwlimit 的格式完全相同，
只是只能指定一个带宽。

无论哪种情况，"rate" 都以人类可读的字符串形式返回，
"bytesPerSecond" 以数字形式返回。

### core/command: 通过 rc 运行 rclone 终端命令。 {#core-command}

此调用接受以下参数：

- command - 包含命令名称的字符串。
- arg - 后端命令的参数列表。
- opt - 选项的字符串到字符串映射。
- returnType - 之一（"COMBINED_OUTPUT"、"STREAM"、"STREAM_ONLY_STDOUT"、"STREAM_ONLY_STDERR"）。
    - 如果未设置，默认为 "COMBINED_OUTPUT"。
    - STREAM returnType 将把输出写入 HTTP 消息的正文。
    - COMBINED_OUTPUT 将把输出写入 "result" 参数。

返回：

- result - 后端命令的结果。
    - 仅在使用 returnType "COMBINED_OUTPUT" 时设置。
- error	 - 如果 rclone 以错误代码退出则设置。
- returnType - 之一（"COMBINED_OUTPUT"、"STREAM"、"STREAM_ONLY_STDOUT"、"STREAM_ONLY_STDERR"）。

示例：

    rclone rc core/command command=ls -a mydrive:/ -o max-depth=1
    rclone rc core/command -a ls -a mydrive:/ -o max-depth=1

返回：

```
{
	"error": false,
	"result": "<Raw command line output>"
}

OR
{
	"error": true,
	"result": "<Raw command line output>"
}

```

**此调用需要身份验证。**

### core/du: 返回本地附加磁盘的磁盘使用情况。 {#core-du}

这将返回作为 dir 传入的本地目录的磁盘使用情况。

如果未传入目录，则默认为由 --cache-dir 指向的目录。

- dir - 字符串（可选）

返回：

```
{
	"dir": "/",
	"info": {
		"Available": 361769115648,
		"Free": 361785892864,
		"Total": 982141468672
	}
}
```

### core/gc: 运行垃圾回收。 {#core-gc}

这会告诉 go 运行时执行垃圾回收。通常不需要调用它，
但对于调试内存问题很有用。

### core/group-list: 返回统计信息列表。 {#core-group-list}

这将返回当前内存中的统计组列表。

返回以下值：
```
{
	"groups":  an array of group names:
		[
			"group1",
			"group2",
			...
		]
}
```

### core/memstats: 返回内存统计信息 {#core-memstats}

这将返回正在运行的程序的内存统计信息。值的含义
在 go 文档中解释：https://golang.org/pkg/runtime/#MemStats

对大多数人来说最有趣的值是：

- HeapAlloc - 这是 rclone 实际正在使用的内存量
- HeapSys - 这是 rclone 从操作系统获得的内存量
- Sys - 这是从操作系统请求的内存总量
   - 它是虚拟内存，因此可能包括未使用的内存

### core/obscure: 模糊处理传入的字符串。 {#core-obscure}

传入明文字符串，rclone 将为配置文件模糊处理它：
- clear - 字符串

返回：

- obscured - 字符串

### core/pid: 返回当前进程的 PID {#core-pid}

这将返回当前进程的 PID。
对于停止 rclone 进程很有用。

### core/quit: 终止应用程序。 {#core-quit}

（可选）传入用于终止应用程序的退出代码：
- exitCode - int

### core/stats: 返回有关当前传输的统计信息。 {#core-stats}

这将返回所有可用的统计信息：

	rclone rc core/stats

如果未提供 group，则将返回所有组的汇总统计信息。

参数

- group - 统计组的名称（字符串，可选）
- short - 如果为 true 将不返回 transferring 和 checking 数组（布尔值，可选）

返回以下值：

```
{
	"bytes": total transferred bytes since the start of the group,
	"checks": number of files checked,
	"deletes" : number of files deleted,
	"elapsedTime": time in floating point seconds since rclone was started,
	"errors": number of errors,
	"eta": estimated time in seconds until the group completes,
	"fatalError": boolean whether there has been at least one fatal error,
	"lastError": last error string,
	"renames" : number of files renamed,
	"listed" : number of directory entries listed,
	"retryError": boolean showing whether there has been at least one non-NoRetryError,
        "serverSideCopies": number of server side copies done,
        "serverSideCopyBytes": number bytes server side copied,
        "serverSideMoves": number of server side moves done,
        "serverSideMoveBytes": number bytes server side moved,
	"speed": average speed in bytes per second since start of the group,
	"totalBytes": total number of bytes in the group,
	"totalChecks": total number of checks in the group,
	"totalTransfers": total number of transfers in the group,
	"transferTime" : total time spent on running jobs,
	"transfers": number of transferred files,
	"transferring": an array of currently active file transfers:
		[
			{
				"bytes": total transferred bytes for this file,
				"eta": estimated time in seconds until file transfer completion
				"name": name of the file,
				"percentage": progress of the file transfer in percent,
				"speed": average speed over the whole transfer in bytes per second,
				"speedAvg": current speed in bytes per second as an exponentially weighted moving average,
				"size": size of the file in bytes
			}
		],
	"checking": an array of names of currently active file checks
		[]
}
```
"transferring"、"checking" 和 "lastError" 的值仅在有数据时才赋值。
如果无法确定 eta，则 "eta" 的值为 null。

### core/stats-delete: 删除统计组。 {#core-stats-delete}

这将删除整个统计组。

参数

- group - 统计组的名称（字符串）

### core/stats-reset: 重置统计信息。 {#core-stats-reset}

这将清除所有统计信息或特定统计组的计数器、错误和已完成的传输（如果提供了 group）。

参数

- group - 统计组的名称（字符串）

### core/transferred: 返回有关已完成的传输的统计信息。 {#core-transferred}

这将返回有关已完成的传输的统计信息：

	rclone rc core/transferred

如果未提供 group，则将返回所有组的已完成的传输。

请注意，仅返回最近 100 个已完成的传输。

参数

- group - 统计组的名称（字符串）

返回以下值：
```
{
	"transferred":  an array of completed transfers (including failed ones):
		[
			{
				"name": name of the file,
				"size": size of the file in bytes,
				"bytes": total transferred bytes for this file,
				"checked": if the transfer is only checked (skipped, deleted),
				"what": the purpose of the transfer (transferring, deleting, checking, importing, hashing, merging, listing, moving, renaming),
				"timestamp": integer representing millisecond unix epoch,
				"error": string description of the error (empty if successful),
				"jobid": id of the job that this transfer belongs to
			}
		]
}
```

### core/version: 显示 rclone、Go 和操作系统的当前版本。 {#core-version}

这将显示 rclone、Go 和操作系统的当前版本：

- version - rclone 版本，例如 "v1.71.2"
- decomposed - 版本号表示为 [major, minor, patch]
- isGit - 布尔值 - 如果这是从 git 版本编译的则为 true
- isBeta - 布尔值 - 如果这是 beta 版本则为 true
- os - 根据 Go GOOS 使用的操作系统（例如 "linux"）
- osKernel - 操作系统内核版本（例如 "6.8.0-86-generic (x86_64)"）
- osVersion -  操作系统版本（例如 "ubuntu 24.04 (64 bit)"）
- osArch - 使用的 cpu 架构（例如 "arm64 (ARMv8 compatible)"）
- arch - 根据 Go GOARCH 使用的 cpu 架构（例如 "arm64"）
- goVersion - 使用的 Go 运行时版本（例如 "go1.25.0"）
- linking - rclone 可执行文件的类型（静态或动态）
- goTags - 空格分隔的构建标签或 "none"

### debug/set-block-profile-rate: 设置用于阻塞分析的 runtime.SetBlockProfileRate。 {#debug-set-block-profile-rate}

SetBlockProfileRate 控制阻塞配置文件中报告的 goroutine
阻塞事件的比例。分析器旨在每 rate 纳秒阻塞时间采样
平均一个阻塞事件。

要在配置文件中包含每个阻塞事件，请传递 rate = 1。
要完全关闭分析，请传递 rate <= 0。

调用此函数后，你可以使用它来查看阻塞配置文件：

    go tool pprof http://localhost:5572/debug/pprof/block

参数：

- rate - int

### debug/set-gc-percent: 调用 runtime/debug.SetGCPercent 设置垃圾收集目标百分比。 {#debug-set-gc-percent}

SetGCPercent 设置垃圾收集目标百分比：当新分配的数据与
上一次收集后剩余的实时数据之比达到此百分比时，
将触发收集。SetGCPercent 返回先前的设置。初始设置是
启动时 GOGC 环境变量的值，如果未设置该变量，则为 100。

为了维持内存限制，此设置可能会被有效降低。
负百分比会有效地禁用垃圾回收，除非达到内存限制。

有关更多详细信息，请参阅 https://pkg.go.dev/runtime/debug#SetMemoryLimit。

参数：

- gc-percent - int

### debug/set-mutex-profile-fraction: 设置用于互斥分析的 runtime.SetMutexProfileFraction。 {#debug-set-mutex-profile-fraction}

SetMutexProfileFraction 控制互斥锁竞争
事件中报告的比例。平均报告 1/rate 事件。返回先前的速率。

要完全关闭分析，请传递 rate 0。要仅读取当前
速率，请传递 rate < 0。（对于 n>1，采样的细节可能会更改。）

设置此参数后，你可以使用它来对互斥锁竞争进行概要分析：

    go tool pprof http://localhost:5572/debug/pprof/mutex

参数：

- rate - int

结果：

- previousRate - int

### debug/set-soft-memory-limit: 调用 runtime/debug.SetMemoryLimit 为运行时设置软内存限制。 {#debug-set-soft-memory-limit}

SetMemoryLimit 为运行时提供软内存限制。

运行时执行多个进程以尝试遵守此内存限制，包括
调整垃圾收集的频率和更积极地将内存返回到基础
系统。即使 GOGC=off（或执行了 SetGCPercent(-1)），
也将遵守此限制。

输入限制以字节为单位，包括所有已映射、已管理和未
由 Go 运行时释放的内存。值得注意的是，它不考虑 Go 二进制文件
使用的空间和 Go 外部的内存，例如由基础系统代表
进程管理的内存，或由同一进程内的非 Go 代码管理的内存。
排除的内存源示例包括：代表进程持有的 OS 内核内存、
C 代码分配的内存，以及由 syscall.Mmap 映射的内存
（因为它不是由 Go 运行时管理的）。

零限制或低于 Go 运行时使用的内存量的限制可能导致
垃圾收集器几乎连续运行。但是，应用程序可能仍然会取得进展。

Go 运行时始终遵守内存限制，因此要有效地禁用此行为，
请将限制设置得非常高。math.MaxInt64 是禁用限制的规范值，
但远大于底层系统上可用内存的值也完全可以。

有关详细指南，请参阅 https://go.dev/doc/gc-guide，
其中更详细地解释了软内存限制，以及各种常见的用例和场景。

SetMemoryLimit 返回先前设置的内存限制。负输入不会调整限制，
并允许检索当前设置的内存限制。

参数：

- mem-limit - int

### fscache/clear: 清除 Fs 缓存。 {#fscache-clear}

这将清除 fs 缓存。后端创建的远程在此处
被短暂缓存以使重复的 rc 调用更高效。

如果更改了后端的参数，则可能需要调用
此函数以在重新创建之前从缓存中清除现有的远程。

**此调用需要身份验证。**

### fscache/entries: 返回 fs 缓存中的条目数。 {#fscache-entries}

这将返回 fs 缓存中的条目数。

返回
- entries - 缓存中的项目数

**此调用需要身份验证。**

### job/batch: 并发运行一批 rclone rc 命令。 {#job-batch}

此调用接受以下参数：

- concurrency - int - 同时执行这么多命令。如果未设置，则默认为 `--transfers`。
- inputs - 命令的输入列表，带有额外的 `_path` 参数

```json
{
    "_path": "rc/path",
    "param1": "parameter for the path as documented",
    "param2": "parameter for the path as documented, etc",
}
```

在使用 rc 时，输入可以使用 `_async`、`_group`、`_config` 和 `_filter`（照常）。

返回：

- results - 命令结果列表，每个 inputs 中的一项对应一个条目。

例如：

```sh
rclone rc job/batch --json '{
  "inputs": [
    {
      "_path": "rc/noop",
      "parameter": "OK"
    },
    {
      "_path": "rc/error",
      "parameter": "BAD"
    }
  ]
}
'
```

产生结果：

```json
{
  "results": [
    {
      "parameter": "OK"
    },
    {
      "error": "arbitrary error on input map[parameter:BAD]",
      "input": {
        "parameter": "BAD"
      },
      "path": "rc/error",
      "status": 500
    }
  ]
}
```

**此调用需要身份验证。**

### job/list: 列出正在运行的任务的 ID {#job-list}

参数：无。

结果：

- executeId - 执行 rclone 的字符串 id（重启后会更改）
- jobids - 整型任务 id 的数组（每次重启时从 1 开始）
- runningIds - 正在运行的整型任务 id 的数组
- finishedIds - 已完成的整型任务 id 的数组

### job/status: 读取任务 ID 的状态 {#job-status}

参数：

- jobid - 任务的 id（整数）。

结果：

- finished - 布尔值
- duration - 任务运行的秒数
- endTime - 任务完成的时间（例如 "2018-10-26T18:50:20.528746884+01:00"）
- error - 任务的错误或空字符串表示无错误
- finished - 布尔值，指示任务是否已完成
- id - 如上所传入的
- executeId - rclone 实例 ID（重启后更改）；与 id 结合可唯一标识一个任务
- startTime - 任务开始的时间（例如 "2018-10-26T18:50:20.528336039+01:00"）
- success - 布尔值 - 成功为 true，否则为 false
- output - 任务的输出，如同同步调用时返回的一样
- progress - 与基础任务相关的进度输出

### job/stop: 停止正在运行的任务 {#job-stop}

参数：

- jobid - 任务的 id（整数）。

### job/stopgroup: 停止组中所有正在运行的任务 {#job-stopgroup}

参数：

- group - 组的名称（字符串）。

### mount/listmounts: 显示当前挂载点 {#mount-listmounts}

这将显示当前挂载的点，可用于执行卸载。

此调用不接受任何参数，并返回

- mountPoints: 当前挂载点列表

例如

    rclone rc mount/listmounts

**此调用需要身份验证。**

### mount/mount: 创建新的挂载点 {#mount-mount}

rclone 允许 Linux、FreeBSD、macOS 和 Windows 使用 FUSE
将任何 Rclone 的云存储系统挂载为文件系统。

如果未提供 mountType，则按以下顺序给出优先级：1. mount 2.cmount 3.mount2

此调用接受以下参数：

- fs - 要挂载的远程路径（必需）
- mountPoint: 本地计算机上的有效路径（必需）
- mountType: 值之一（mount、cmount、mount2）指定要使用的挂载实现
- mountOpt: 包含 Mount 选项的 JSON 对象。
- vfsOpt: 包含 VFS 选项的 JSON 对象。

示例：

```console
rclone rc mount/mount fs=mydrive: mountPoint=/home/<user>/mountPoint
rclone rc mount/mount fs=mydrive: mountPoint=/home/<user>/mountPoint mountType=mount
rclone rc mount/mount fs=TestDrive: mountPoint=/mnt/tmp vfsOpt='{"CacheMode": 2}' mountOpt='{"AllowOther": true}'
```

vfsOpt 如 options/get 中所述，可在运行时
在 "vfs" 部分中看到，mountOpt 可在 "mount" 部分中看到：

```console
rclone rc options/get
```

**此调用需要身份验证。**

### mount/types: 显示所有可能的挂载类型 {#mount-types}

这将显示所有可能的挂载类型并将它们作为列表返回。

此调用不接受任何参数，并返回

- mountTypes: 挂载类型列表

挂载类型是 "mount"、"mount2"、"cmount" 等字符串，
可以作为 mountType 参数传递给 mount/mount。

例如

    rclone rc mount/types

**此调用需要身份验证。**

### mount/unmount: 卸载所选的活动挂载 {#mount-unmount}

rclone 允许 Linux、FreeBSD、macOS 和 Windows 使用 FUSE
将任何 Rclone 的云存储系统挂载为文件系统。

此调用接受以下参数：

- mountPoint: 本地计算机上创建挂载的有效路径（必需）

示例：

    rclone rc mount/unmount mountPoint=/home/<user>/mountPoint

**此调用需要身份验证。**

### mount/unmountall: 卸载所有活动挂载 {#mount-unmountall}

rclone 允许 Linux、FreeBSD、macOS 和 Windows 使用 FUSE
将任何 Rclone 的云存储系统挂载为文件系统。

此调用不接受任何参数，如果卸载不成功则返回错误。

例如

    rclone rc mount/unmountall

**此调用需要身份验证。**

### operations/about: 返回远程上已使用的空间 {#operations-about}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"

结果与 rclone about --json 返回的结果相同

有关上述内容的更多信息，请参阅 [about](/commands/rclone_about/) 命令。

**此调用需要身份验证。**

### operations/check: 检查源和目标是否相同 {#operations-check}

检查源和目标中的文件是否匹配。它比较
大小和哈希并记录不匹配的文件的报告。
它不会更改源或目标。

此调用接受以下参数：

- srcFs - 远程名称字符串，例如源 "drive:"，本地文件系统为 "/"
- dstFs - 远程名称字符串，例如目标 "drive2:"，本地文件系统为 "/"
- download - 通过下载而不是使用哈希进行检查
- checkFileHash - 将 checkFileFs:checkFileRemote 视为具有给定类型哈希的 SUM 文件
- checkFileFs - 将 checkFileFs:checkFileRemote 视为具有给定类型哈希的 SUM 文件
- checkFileRemote - 将 checkFileFs:checkFileRemote 视为具有给定类型哈希的 SUM 文件
- oneWay -  仅单向检查，源文件必须存在于远程
- combined - 制作更改的综合报告（默认 false）
- missingOnSrc - 报告源中所有缺失的文件（默认 true）
- missingOnDst - 报告目标中所有缺失的文件（默认 true）
- match - 报告所有匹配的文件（默认 false）
- differ - 报告所有不匹配的文件（默认 true）
- error - 报告所有有错误（哈希或读取）的文件（默认 true）

如果提供 download 标志，它将从两个远程下载数据并
动态地相互检查。这对于不支持哈希的远程或
如果你真的想检查所有数据很有用。

如果提供 size-only 全局标志，它将仅比较大小而不是
哈希也是如此。使用它进行快速检查。

如果使用有效的哈希名称提供 checkFileHash 选项，
则 checkFileFs:checkFileRemote 必须指向 SUM 格式的文本文件。
这会将校验和文件视为源，将 dstFs 视为目标。
请注意，srcFs 未使用，在这种情况下不应提供。

返回：

- success - 如果没有错误则为 true，否则为 false
- status - 检查的文本摘要，OK 或文本字符串
- hashType - 检查中使用的哈希，可能会缺失
- combined - 更改的综合报告的字符串数组
- missingOnSrc - 源中所有缺失的文件的字符串数组
- missingOnDst - 目标中所有缺失的文件的字符串数组
- match - 所有匹配文件的字符串数组
- differ - 所有不匹配文件的字符串数组
- error - 所有有错误（哈希或读取）的文件的字符串数组

**此调用需要身份验证。**

### operations/cleanup: 删除远程或路径中的垃圾文件 {#operations-cleanup}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"

有关上述内容的更多信息，请参阅 [cleanup](/commands/rclone_cleanup/) 命令。

**此调用需要身份验证。**

### operations/copyfile: 将文件从源远程复制到目标远程 {#operations-copyfile}

此调用接受以下参数：

- srcFs - 远程名称字符串，例如源 "drive:"，本地文件系统为 "/"
- srcRemote - 该远程中的路径，例如源的 "file.txt"
- dstFs - 远程名称字符串，例如目标 "drive2:"，本地文件系统为 "/"
- dstRemote - 该远程中的路径，例如目标的 "file2.txt"

**此调用需要身份验证。**

### operations/copyurl: 将 URL 复制到对象 {#operations-copyurl}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "dir"
- url - 字符串，要从中读取的 URL
 - autoFilename - 布尔值，设置为 true 以从 url 检索目标文件名

有关上述内容的更多信息，请参阅 [copyurl](/commands/rclone_copyurl/) 命令。

**此调用需要身份验证。**

### operations/delete: 删除路径中的文件 {#operations-delete}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"

有关上述内容的更多信息，请参阅 [delete](/commands/rclone_delete/) 命令。

**此调用需要身份验证。**

### operations/deletefile: 删除所指向的单个文件 {#operations-deletefile}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "dir"

有关上述内容的更多信息，请参阅 [deletefile](/commands/rclone_deletefile/) 命令。

**此调用需要身份验证。**

### operations/fsinfo: 返回有关远程的信息 {#operations-fsinfo}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"

这将返回有关传入的远程的信息；

```
{
        // optional features and whether they are available or not
        "Features": {
                "About": true,
                "BucketBased": false,
                "BucketBasedRootOK": false,
                "CanHaveEmptyDirectories": true,
                "CaseInsensitive": false,
                "ChangeNotify": false,
                "CleanUp": false,
                "Command": true,
                "Copy": false,
                "DirCacheFlush": false,
                "DirMove": true,
                "Disconnect": false,
                "DuplicateFiles": false,
                "GetTier": false,
                "IsLocal": true,
                "ListR": false,
                "MergeDirs": false,
                "MetadataInfo": true,
                "Move": true,
                "OpenWriterAt": true,
                "PublicLink": false,
                "Purge": true,
                "PutStream": true,
                "PutUnchecked": false,
                "ReadMetadata": true,
                "ReadMimeType": false,
                "ServerSideAcrossConfigs": false,
                "SetTier": false,
                "SetWrapper": false,
                "Shutdown": false,
                "SlowHash": true,
                "SlowModTime": false,
                "UnWrap": false,
                "UserInfo": false,
                "UserMetadata": true,
                "WrapFs": false,
                "WriteMetadata": true,
                "WriteMimeType": false
        },
        // Names of hashes available
        "Hashes": [
                "md5",
                "sha1",
                "whirlpool",
                "crc32",
                "sha256",
                "dropbox",
                "mailru",
                "quickxor"
        ],
        "Name": "local",        // Name as created
        "Precision": 1,         // Precision of timestamps in ns
        "Root": "/",            // Path as created
        "String": "Local file system at /", // how the remote will appear in logs
        // Information about the system metadata for this backend
        "MetadataInfo": {
                "System": {
                        "atime": {
                                "Help": "Time of last access",
                                "Type": "RFC 3339",
                                "Example": "2006-01-02T15:04:05.999999999Z07:00"
                        },
                        "btime": {
                                "Help": "Time of file birth (creation)",
                                "Type": "RFC 3339",
                                "Example": "2006-01-02T15:04:05.999999999Z07:00"
                        },
                        "gid": {
                                "Help": "Group ID of owner",
                                "Type": "decimal number",
                                "Example": "500"
                        },
                        "mode": {
                                "Help": "File type and mode",
                                "Type": "octal, unix style",
                                "Example": "0100664"
                        },
                        "mtime": {
                                "Help": "Time of last modification",
                                "Type": "RFC 3339",
                                "Example": "2006-01-02T15:04:05.999999999Z07:00"
                        },
                        "rdev": {
                                "Help": "Device ID (if special file)",
                                "Type": "hexadecimal",
                                "Example": "1abc"
                        },
                        "uid": {
                                "Help": "User ID of owner",
                                "Type": "decimal number",
                                "Example": "500"
                        }
                },
                "Help": "Textual help string\n"
        }
}
```

此命令没有等效的命令行，因此请改用：

    rclone rc --loopback operations/fsinfo fs=remote:

### operations/hashsum: 为路径中的所有对象生成哈希和文件。 {#operations-hashsum}

使用指定的哈希为路径中的所有对象生成哈希文件。
输出格式与标准 md5sum/sha1sum 工具相同。

此调用接受以下参数：

- fs - 远程名称字符串，例如源 "drive:"，本地文件系统为 "/"
    - 这可以指向一个文件，并且只会在列表中返回该文件。
- hashType - 要使用的哈希类型
- download - 通过下载而不是使用哈希进行检查（布尔值）
- base64 - 以 base64 而不是十六进制输出哈希（布尔值）

如果提供 download 标志，它将从远程下载数据并
动态创建哈希。这对于不支持给定哈希的远程或
如果你真的想检查所有数据很有用。

请注意，如果你希望提供检查文件以根据当前文件检查哈希，
则应使用 operations/check 而不是 operations/hashsum。

返回：

- hashsum - 哈希的字符串数组
- hashType - 使用的哈希类型

示例：

    $ rclone rc --loopback operations/hashsum fs=bin hashType=MD5 download=true base64=true
    {
        "hashType": "md5",
        "hashsum": [
            "WTSVLpuiXyJO_kGzJerRLg==  backend-versions.sh",
            "v1b_OlWCJO9LtNq3EIKkNQ==  bisect-go-rclone.sh",
            "VHbmHzHh4taXzgag8BAIKQ==  bisect-rclone.sh",
        ]
    }

有关上述内容的更多信息，请参阅 [hashsum](/commands/rclone_hashsum/) 命令。

**此调用需要身份验证。**

### operations/hashsumfile: 为单个文件生成哈希。 {#operations-hashsumfile}

使用指定的哈希为单个文件生成哈希。

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "file.txt"
- hashType - 要使用的哈希类型
- download - 通过下载而不是使用哈希进行检查（布尔值）
- base64 - 以 base64 而不是十六进制输出哈希（布尔值）

如果提供 download 标志，它将从远程下载数据并
动态创建哈希。这对于不支持给定哈希的远程或
如果你真的想读取所有数据很有用。

返回：

- hash - 文件的哈希
- hashType - 使用的哈希类型

示例：

    $ rclone rc --loopback operations/hashsumfile fs=/ remote=/bin/bash hashType=MD5 download=true base64=true
    {
        "hashType": "md5",
        "hash": "MDMw-fG2YXs7Uz5Nz-H68A=="
    }

有关上述内容的更多信息，请参阅 [hashsum](/commands/rclone_hashsum/) 命令。

**此调用需要身份验证。**

### operations/list: 以 JSON 格式列出给定的远程和路径 {#operations-list}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "dir"
- opt - 用于控制列表的字典（可选）
    - recurse - 如果设置则递归目录
    - noModTime - 如果设置则返回修改时间
    - showEncrypted -  如果设置则显示解密后的名称
    - showOrigIDs - 如果设置则显示每个项目的 ID（如果已知）
    - showHash - 如果设置则返回哈希字典
    - noMimeType - 如果设置则不显示 mime 类型
    - dirsOnly - 如果设置则仅显示目录
    - filesOnly - 如果设置则仅显示文件
    - metadata - 如果设置则还返回对象的元数据
    - hashTypes - 如果设置了 showHash 则显示的哈希类型的字符串数组

返回：

- list
    - 这是 lsjson 命令中描述的对象数组

有关上述内容和示例的更多信息，请参阅 [lsjson](/commands/rclone_lsjson/) 命令。

**此调用需要身份验证。**

### operations/mkdir: 创建目标目录或容器 {#operations-mkdir}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "dir"

有关上述内容的更多信息，请参阅 [mkdir](/commands/rclone_mkdir/) 命令。

**此调用需要身份验证。**

### operations/movefile: 将文件从源远程移动到目标远程 {#operations-movefile}

此调用接受以下参数：

- srcFs - 远程名称字符串，例如源 "drive:"，本地文件系统为 "/"
- srcRemote - 该远程中的路径，例如源的 "file.txt"
- dstFs - 远程名称字符串，例如目标 "drive2:"，本地文件系统为 "/"
- dstRemote - 该远程中的路径，例如目标的 "file2.txt"

**此调用需要身份验证。**

### operations/publiclink: 创建或检索给定文件或文件夹的公共链接。 {#operations-publiclink}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "dir"
- unlink - 布尔值 - 如果设置则删除链接而不是添加（可选）
- expire - 字符串 - 链接的过期时间，例如 "1d"（可选）

返回：

- url - 资源的 URL

有关上述内容的更多信息，请参阅 [link](/commands/rclone_link/) 命令。

**此调用需要身份验证。**

### operations/purge: 删除目录或容器及其所有内容 {#operations-purge}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "dir"

有关上述内容的更多信息，请参阅 [purge](/commands/rclone_purge/) 命令。

**此调用需要身份验证。**

### operations/rmdir: 删除空目录或容器 {#operations-rmdir}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "dir"

有关上述内容的更多信息，请参阅 [rmdir](/commands/rclone_rmdir/) 命令。

**此调用需要身份验证。**

### operations/rmdirs: 删除路径中的所有空目录 {#operations-rmdirs}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "dir"
- leaveRoot - 布尔值，设置为 true 则不删除根目录

有关上述内容的更多信息，请参阅 [rmdirs](/commands/rclone_rmdirs/) 命令。

**此调用需要身份验证。**

### operations/settier: 更改路径中所有文件的存储层或类 {#operations-settier}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"

有关上述内容的更多信息，请参阅 [settier](/commands/rclone_settier/) 命令。

**此调用需要身份验证。**

### operations/settierfile: 更改所指向的单个文件的存储层或类 {#operations-settierfile}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "dir"

**此调用需要身份验证。**

### operations/size: 计算远程中的字节数和文件数 {#operations-size}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:path/to/dir"

返回：

- count - 文件数
- bytes - 这些文件中的字节数

有关上述内容的更多信息，请参阅 [size](/commands/rclone_size/) 命令。

**此调用需要身份验证。**

### operations/stat: 提供有关提供的文件或目录的信息 {#operations-stat}

此调用接受以下参数

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "dir"
- opt - 用于控制列表的字典（可选）
    - 请参阅 operations/list 了解选项

结果是

- item - lsjson 命令中描述的对象。如果未找到则为 null。

请注意，如果你只对文件感兴趣，那么
在选项中设置 filesOnly 标志会更有效。

有关上述内容和示例的更多信息，请参阅 [lsjson](/commands/rclone_lsjson/) 命令。

**此调用需要身份验证。**

### operations/uploadfile: 使用 multiform/form-data 上传文件 {#operations-uploadfile}

此调用接受以下参数：

- fs - 远程名称字符串，例如 "drive:"
- remote - 该远程中的路径，例如 "dir"
- body 中的每个部分表示要上传的文件

**此调用需要身份验证。**

### options/blocks: 列出所有选项块 {#options-blocks}

返回：
- options - 选项块名称的列表

### options/get: 获取所有全局选项 {#options-get}

返回一个对象，其中键是选项块名称，值是具有当前选项值的对象。

参数：

- blocks: 要包含的以逗号分隔的块的可选字符串
    - 如果缺失或为 ""，则全部包含

请注意，这些是不受 _config 和 _filter 参数使用影响的全局选项。
如果你希望读取 _config 或 _filter 中设置的参数，请使用 options/local。

这将显示 rclone 中选项的内部名称，
这些名称应该很容易地映射到外部选项，只有少数例外。

### options/info: 获取有关所有全局选项的信息 {#options-info}

返回一个对象，其中键是选项块名称，值是包含有关每个选项的信息的对象数组。

参数：

- blocks: 要包含的以逗号分隔的块的可选字符串
    - 如果缺失或为 ""，则全部包含

这些对象的格式与 "config/providers" 返回的格式相同。
它们在 [option blocks](#option-blocks) 部分中描述。

### options/local: 获取此调用的当前活动配置 {#options-local}

返回一个具有键 "config" 和 "filter" 的对象。
"config" 键包含本地配置，"filter" 键包含
本地过滤器。

请注意，这些是特定于此 rc 调用的本地选项。
如果未提供 _config，则它们将是全局选项。
"_filter" 也是如此。

此调用主要用于查看 _config 和 _filter 传递
是否正常工作。

这将显示 rclone 中选项的内部名称，
这些名称应该很容易地映射到外部选项，只有少数例外。

### options/set: 设置一个选项 {#options-set}

参数：

- 选项块名称包含一个对象，其中
  - key: value

根据需要重复。

仅提供你希望更改的选项。如果某个选项未知
将被静默忽略。并非所有选项都会在以这种方式更改时生效。

例如：

这将设置 DEBUG 级别日志（-vv）（这些可以按数字或字符串设置）

    rclone rc options/set --json '{"main": {"LogLevel": "DEBUG"}}'
    rclone rc options/set --json '{"main": {"LogLevel": 8}}'

而这将设置 INFO 级别日志（-v）

    rclone rc options/set --json '{"main": {"LogLevel": "INFO"}}'

而这将设置 NOTICE 级别日志（普通不带 -v）

    rclone rc options/set --json '{"main": {"LogLevel": "NOTICE"}}'

### pluginsctl/addPlugin: 使用 url 添加插件 {#pluginsctl-addPlugin}

用于将插件添加到 webgui。

此调用接受以下参数：

- url - 托管插件的 github 仓库的 http url（http://github.com/rclone/rclone-webui-react）。

示例：

   rclone rc pluginsctl/addPlugin

**此调用需要身份验证。**

### pluginsctl/getPluginsForType: 按类型条件获取插件 {#pluginsctl-getPluginsForType}

这将按 mime 类型显示所有可能的插件。

此调用接受以下参数：

- type - 已加载插件支持的 mime 类型（例如 video/mp4、audio/mp3）。
- pluginType - 根据插件的类型过滤插件（例如 DASHBOARD、FILE_HANDLER、TERMINAL）。

返回：

- loadedPlugins - 当前生产插件的列表。
- testPlugins - 临时加载的开发插件的列表，通常在不同的服务器上运行。

示例：

   rclone rc pluginsctl/getPluginsForType type=video/mp4

**此调用需要身份验证。**

### pluginsctl/listPlugins: 获取当前加载的插件列表 {#pluginsctl-listPlugins}

这允许你获取当前启用的插件及其详细信息。

此调用不接受任何参数，并返回：

- loadedPlugins - 当前生产插件的列表。
- testPlugins - 临时加载的开发插件的列表，通常在不同的服务器上运行。

例如

   rclone rc pluginsctl/listPlugins

**此调用需要身份验证。**

### pluginsctl/listTestPlugins: 显示当前加载的测试插件 {#pluginsctl-listTestPlugins}

允许列出插件包 package.json 中 rclone.test 设置为 true 的测试插件。

此调用不接受任何参数，并返回：

- loadedTestPlugins - 当前可用的测试插件的列表。

例如

    rclone rc pluginsctl/listTestPlugins

**此调用需要身份验证。**

### pluginsctl/removePlugin: 移除已加载的插件 {#pluginsctl-removePlugin}

这允许你使用其名称移除插件。

此调用接受参数：

- name - 插件的名称，格式为 `author`/`plugin_name`。

例如

   rclone rc pluginsctl/removePlugin name=rclone/video-plugin

**此调用需要身份验证。**

### pluginsctl/removeTestPlugin: 移除测试插件 {#pluginsctl-removeTestPlugin}

这允许你使用其名称移除插件。

此调用接受以下参数：

- name - 插件的名称，格式为 `author`/`plugin_name`。

示例：

    rclone rc pluginsctl/removeTestPlugin name=rclone/rclone-webui-react

**此调用需要身份验证。**

### rc/error: 这将返回一个错误 {#rc-error}

这将返回一个错误，其中输入是其错误字符串的一部分。
对于测试错误处理很有用。

### rc/fatal: 这将返回致命错误 {#rc-fatal}

这将返回一个错误，其中输入是其错误字符串的一部分。
对于测试错误处理很有用。

### rc/list: 列出所有已注册的远程控制命令 {#rc-list}

这将以 JSON 映射的形式列出所有已注册的远程控制命令。
在命令响应中。

### rc/noop: 将输入回显到输出参数 {#rc-noop}

这会将输入参数回显到输出参数，用于测试
目的。它可用于检查 rclone 是否仍处于活动状态并检查
参数传递是否正常工作。

### rc/noopauth: 将输入回显到需要授权的输出参数 {#rc-noopauth}

这会将输入参数回显到输出参数，用于测试
目的。它可用于检查 rclone 是否仍处于活动状态并检查
参数传递是否正常工作。

**此调用需要身份验证。**

### rc/panic: 这将通过 panic 返回错误 {#rc-panic}

这将返回一个错误，其中输入是其错误字符串的一部分。
对于测试错误处理很有用。

### serve/list: 显示正在运行的服务器 {#serve-list}

显示正在运行的服务器及其 ID。

此调用不接受任何参数，并返回

- list: 正在运行的 serve 命令的列表

每个列表元素将具有

- id: 服务器的 ID
- addr: 服务器正在运行的地址
- params: 用于启动服务器的参数

例如

    rclone rc serve/list

返回

```json
{
    "list": [
        {
            "addr": "[::]:4321",
            "id": "nfs-ffc2a4e5",
            "params": {
                "fs": "remote:",
                "opt": {
                    "ListenAddr": ":4321"
                },
                "type": "nfs",
                "vfsOpt": {
                    "CacheMode": "full"
                }
            }
        }
    ]
}
```

**此调用需要身份验证。**

### serve/start: 创建新服务器 {#serve-start}

使用指定的参数创建新服务器。

此调用接受以下参数：

- `type` - 服务器类型：`http`、`webdav`、`ftp`、``sftp`、`nfs` 等。
- `fs` - 要提供服务的远程存储路径
- `addr` - 运行服务器的 ip:port，例如 ":1234" 或 "localhost:1234"

其他参数如相关 [rclone serve](/commands/rclone_serve/) 命令行选项的文档中所述。
要将命令行选项转换为 rc 参数，请删除前导
`--` 并将 `-` 替换为 `_`，因此 `--vfs-cache-mode` 变为
`vfs_cache_mode`。请注意，全局参数必须使用
`_config` 和 `_filter` 设置，如上所述。

示例：

    rclone rc serve/start type=nfs fs=remote: addr=:4321 vfs_cache_mode=full
    rclone rc serve/start --json '{"type":"nfs","fs":"remote:","addr":":1234","vfs_cache_mode":"full"}'

这将给出回复

```json
{
    "addr": "[::]:4321", // Address the server was started on
    "id": "nfs-ecfc6852" // Unique identifier for the server instance
}
```

或者如果启动失败则返回错误。

使用 `serve/stop` 停止服务器，并使用 `serve/list` 列出正在运行的服务器。

**此调用需要身份验证。**

### serve/stop: 取消所选活动 serve 的服务 {#serve-stop}

通过 ID 停止正在运行的 `serve` 实例。

此调用接受以下参数：

- id: 由 serve/start 返回

如果成功，这将给出空响应，否则给出错误。

示例：

    rclone rc serve/stop id=12345

**此调用需要身份验证。**

### serve/stopall: 停止所有活动服务器 {#serve-stopall}

停止所有活动服务器。

这将停止所有活动服务器。

    rclone rc serve/stopall

**此调用需要身份验证。**

### serve/types: 显示所有可能的 serve 类型 {#serve-types}

这将显示所有可能的 serve 类型并将它们作为列表返回。

此调用不接受任何参数，并返回

- types: serve 类型的列表，例如 "nfs"、"sftp" 等

serve 类型是 "serve"、"serve2"、"cserve" 等字符串，并且可以
作为 serveType 参数传递给 serve/start。

例如

    rclone rc serve/types

返回

```json
{
    "types": [
        "http",
        "sftp",
        "nfs"
    ]
}
```

**此调用需要身份验证。**

### sync/bisync: 在两个路径之间执行双向同步。 {#sync-bisync}

此调用接受以下参数

- path1 - 远程目录字符串，例如 `drive:path1`
- path2 - 远程目录字符串，例如 `drive:path2`
- dryRun - 干运行模式
- resync - 执行 resync 运行
- checkAccess - 如果在两个文件系统上找不到 RCLONE_TEST 文件则中止
- checkFilename - checkAccess 的文件名（默认：RCLONE_TEST）
- maxDelete - 如果已删除文件的百分比超过此阈值则中止同步
  （默认：50）
- force - 绕过 maxDelete 安全检查并运行同步
- checkSync - 默认为 `true`，`false` 禁用最终列表的比较，
              `only` 将跳过同步，仅比较上次运行的列表
- createEmptySrcDirs - 同步空目录的创建和删除。
			  （与 --remove-empty-dirs 不兼容）
- removeEmptyDirs - 在最终清理步骤中删除空目录
- filtersFile - 从文件读取过滤模式
- ignoreListingChecksum - 不使用校验和进行列表
- resilient - 允许将来在某些不太严重的错误后重试运行，而不需要 resync。
- workdir - 历史文件的服务器目录（默认：`~/.cache/rclone/bisync`）
- backupdir1 - Path1 的 --backup-dir。必须是同一远程上不重叠的路径。
- backupdir2 - Path2 的 --backup-dir。必须是同一远程上不重叠的路径。
- noCleanup - 保留工作文件

请参阅 [bisync 命令帮助](https://rclone.org/commands/rclone_bisync/)
和 [完整 bisync 描述](https://rclone.org/bisync/) 了解更多信息。

**此调用需要身份验证。**

### sync/copy: 将目录从源远程复制到目标远程 {#sync-copy}

此调用接受以下参数：

- srcFs - 远程名称字符串，例如源的 "drive:src"
- dstFs - 远程名称字符串，例如目标的 "drive:dst"
- createEmptySrcDirs - 如果设置，则在目标上创建空的 src 目录


有关上述内容的更多信息，请参阅 [copy](/commands/rclone_copy/) 命令。

**此调用需要身份验证。**

### sync/move: 将目录从源远程移动到目标远程 {#sync-move}

此调用接受以下参数：

- srcFs - 远程名称字符串，例如源的 "drive:src"
- dstFs - 远程名称字符串，例如目标的 "drive:dst"
- createEmptySrcDirs - 如果设置，则在目标上创建空的 src 目录
- deleteEmptySrcDirs - 如果设置，则删除空的 src 目录


有关上述内容的更多信息，请参阅 [move](/commands/rclone_move/) 命令。

**此调用需要身份验证。**

### sync/sync: 将目录从源远程同步到目标远程 {#sync-sync}

此调用接受以下参数：

- srcFs - 远程名称字符串，例如源的 "drive:src"
- dstFs - 远程名称字符串，例如目标的 "drive:dst"
- createEmptySrcDirs - 如果设置，则在目标上创建空的 src 目录


有关上述内容的更多信息，请参阅 [sync](/commands/rclone_sync/) 命令。

**此调用需要身份验证。**

### vfs/forget: 忘记目录缓存中的文件或目录。 {#vfs-forget}

这将忘记目录缓存中的路径，导致它们在
需要时从远程重新读取。

如果未传入任何路径，则它将忘记目录缓存中的所有路径。

    rclone rc vfs/forget

否则将文件或目录作为 file=path 或 dir=path 传入。任何
以 file 开头的参数键将忘记该文件，任何
以 dir 开头的参数键将忘记该目录，例如

    rclone rc vfs/forget file=hello file2=goodbye dir=home/junk

此命令接受 "fs" 参数。如果未提供此参数
并且如果只有一个 VFS 在用，那么将使用该 VFS。
如果有多个 VFS 在用，那么必须提供 "fs" 参数。

### vfs/list: 列出活动的 VFS。 {#vfs-list}

这将列出活动的 VFS。

它在键 "vfses" 下返回一个列表，其中值是可以作为 "fs" 参数
传递给其他 VFS 命令的 VFS 名称。

### vfs/poll-interval: 获取 poll-interval 选项的状态或更新其值。 {#vfs-poll-interval}

如果未给出任何参数，则返回 poll-interval 设置的当前状态。

当设置 interval=duration 参数时，poll-interval 值
被更新，并且轮询函数会收到通知。
设置 interval=0 禁用 poll-interval。

    rclone rc vfs/poll-interval interval=5m

timeout=duration 参数可用于指定等待
当前轮询函数应用新值的时间。
如果 timeout 小于或等于 0（默认值），则无限期等待。

仅当未达到 timeout 时，新的 poll-interval 值才会生效。

如果 poll-interval 被暂时更新或禁用，某些更改
可能不会被轮询函数拾取，具体取决于
使用的远程。

此命令接受 "fs" 参数。如果未提供此参数
并且如果只有一个 VFS 在用，那么将使用该 VFS。
如果有多个 VFS 在用，那么必须提供 "fs" 参数。

### vfs/queue: VFS 的队列信息。 {#vfs-queue}

这将返回所选 VFS 的上传队列信息。

仅当 `--vfs-cache-mode` > off 时才有用。如果在
`--vfs-cache-mode` 为 off 时调用它，它将返回一个空结果。

    {
        "queue": // an array of files queued for upload
        [
            {
                "name":      "file",   // string: name (full path) of the file,
                "id":        123,      // integer: id of this item in the queue,
                "size":      79,       // integer: size of the file in bytes
                "expiry":    1.5       // float: time until file is eligible for transfer, lowest goes first
                "tries":     1,        // integer: number of times we have tried to upload
                "delay":     5.0,      // float: seconds between upload attempts
                "uploading": false,    // boolean: true if item is being uploaded
            },
       ],
    }

`expiry` 时间是文件符合上传条件的浮动秒数时间。
这可能是负数。由于 rclone 一次只能传输 `--transfers` 个文件，
只有最低的 `--transfers` 个 expiry 时间的 `uploading` 才为 `true`。
所以可能会有 expiry 时间为负的文件，其 `uploading` 为 `false`。


此命令接受 "fs" 参数。如果未提供此参数
并且如果只有一个 VFS 在用，那么将使用该 VFS。
如果有多个 VFS 在用，那么必须提供 "fs" 参数。

### vfs/queue-set-expiry: 为排队等待上传的项目设置过期时间。 {#vfs-queue-set-expiry}

使用此选项可调整上传队列中项目的 `expiry` 时间。
在使用此调用之前，你需要使用 `vfs/queue` 读取项目的 `id`。

然后，你可以将 `expiry` 设置为从现在起表示秒数的浮动点数，
表示该项目符合上传条件的时间。如果希望该项目
尽快上传，请将其设置为较大的负数（例如
-1000000000）。如果希望项目的上传被延迟
很长时间，请将其设置为较大的正数。

设置已开始上传的项目的 `expiry` 将无效 - 该项目将继续被上传。

如果使用 `--vfs-cache-mode` off 调用，或者
未找到传入的 `id`，则将返回错误。

此调用接受以下参数

- `fs` - 选择正在使用的 VFS（可选）
- `id` - 从 `vfs/queue` 返回的数字 ID
- `expiry` - 作为浮动秒数的新过期时间
- `relative` - 如果设置，则 expiry 将被视为相对于当前 expiry（可选，布尔值）

成功时返回空结果，或返回错误。


此命令接受 "fs" 参数。如果未提供此参数
并且如果只有一个 VFS 在用，那么将使用该 VFS。
如果有多个 VFS 在用，那么必须提供 "fs" 参数。

### vfs/refresh: 刷新目录缓存。 {#vfs-refresh}

这将读取指定路径的目录并刷新目录缓存。

如果未传入任何路径，则将刷新根目录。

    rclone rc vfs/refresh

否则将目录作为 dir=path 传入。任何以 dir 开头的参数键
将刷新该目录，例如

    rclone rc vfs/refresh dir=home/junk dir2=data/misc

如果给出 recursive=true 参数，则将刷新整个目录树。
如果启用，此刷新将使用 --fast-list。

此命令接受 "fs" 参数。如果未提供此参数
并且如果只有一个 VFS 在用，那么将使用该 VFS。
如果有多个 VFS 在用，那么必须提供 "fs" 参数。

### vfs/stats: VFS 的统计信息。 {#vfs-stats}

这将返回所选 VFS 的统计信息。

    {
        // Status of the disk cache - only present if --vfs-cache-mode > off
        "diskCache": {
            "bytesUsed": 0,
            "erroredFiles": 0,
            "files": 0,
            "hashType": 1,
            "outOfSpace": false,
            "path": "/home/user/.cache/rclone/vfs/local/mnt/a",
            "pathMeta": "/home/user/.cache/rclone/vfsMeta/local/mnt/a",
            "uploadsInProgress": 0,
            "uploadsQueued": 0
        },
        "fs": "/mnt/a",
        "inUse": 1,
        // Status of the in memory metadata cache
        "metadataCache": {
            "dirs": 1,
            "files": 0
        },
        // Options as returned by options/get
        "opt": {
            "CacheMaxAge": 3600000000000,
            // ...
            "WriteWait": 1000000000
        }
    }


此命令接受 "fs" 参数。如果未提供此参数
并且如果只有一个 VFS 在用，那么将使用该 VFS。
如果有多个 VFS 在用，那么必须提供 "fs" 参数。

<!-- autogenerated stop -->

## 通过 HTTP 访问远程控制 {#api-http}

Rclone 实现了一个简单的基于 HTTP 的协议。

每个端点都接受一个 JSON 对象，并返回一个 JSON 对象或
错误。JSON 对象本质上是字符串名称到
值的映射。

所有调用必须使用 POST 发出。

输入对象可以使用 URL 参数、POST 参数提供，或者通过提供
"Content-Type: application/json" 和 JSON blob 在 body 中提供。
下面有使用 `curl` 的示例。

响应将是响应 body 中的 JSON blob。这
格式化为合理的人类可读。

### 错误返回

如果发生错误，则会有 HTTP 错误状态（例如 500），
响应的 body 将包含 JSON 编码的错误对象，例如

```json
{
    "error": "Expecting string value for key \"remote\" (was float64)",
    "input": {
        "fs": "/tmp",
        "remote": 3
    },
    "status": 400,
    "path": "operations/rmdir"
}
```

错误响应中的键是：

- error - 错误字符串
- input - 调用的输入参数
- status - HTTP 状态代码
- path - 调用的路径

### CORS

服务器实现基本的 CORS 支持，并允许所有来源。
对预检 OPTIONS 请求的响应将回显请求的
"Access-Control-Request-Headers"。

### 仅使用 URL 参数的 POST

```console
curl -X POST 'http://localhost:5572/rc/noop?potato=1&sausage=2'
```

响应

```json
{
    "potato": "1",
    "sausage": "2"
}
```

以下是错误响应的样子：

```console
curl -X POST 'http://localhost:5572/rc/error?potato=1&sausage=2'
```

```json
{
    "error": "arbitrary error on input map[potato:1 sausage:2]",
    "input": {
        "potato": "1",
        "sausage": "2"
    }
}
```

请注意，除非使用 `-f` 选项，否则 curl 不会向 shell 返回错误

```console
$ curl -f -X POST 'http://localhost:5572/rc/error?potato=1&sausage=2'
curl: (22) The requested URL returned error: 400 Bad Request
$ echo $?
22
```

### 使用带有表单的 POST

```console
curl --data "potato=1" --data "sausage=2" http://localhost:5572/rc/noop
```

响应

```json
{
    "potato": "1",
    "sausage": "2"
}
```

请注意，你也可以将这些与 URL 参数结合使用，其中 POST
参数优先。

```console
curl --data "potato=1" --data "sausage=2" "http://localhost:5572/rc/noop?rutabaga=3&sausage=4"
```

响应

```json
{
    "potato": "1",
    "rutabaga": "3",
    "sausage": "4"
}

```

### 使用带有 JSON blob 的 POST

```console
curl -H "Content-Type: application/json" -X POST -d '{"potato":2,"sausage":1}' http://localhost:5572/rc/noop
```

响应

```json
{
    "password": "xyz",
    "username": "xyz"
}
```

如果需要，也可以将其与 URL 参数结合使用。JSON
blob 优先。

```console
curl -H "Content-Type: application/json" -X POST -d '{"potato":2,"sausage":1}' 'http://localhost:5572/rc/noop?rutabaga=3&potato=4'
```

```json
{
    "potato": 2,
    "rutabaga": "3",
    "sausage": 1
}
```

## 使用 pprof 调试 rclone

如果使用 `--rc` 标志，则还将在同一端口上启用 go 分析工具的使用。

要使用这些工具，请先[安装 go](https://golang.org/doc/install)。

### 调试内存使用

要分析 rclone 的内存使用，可以运行：

```console
go tool pprof -web http://localhost:5572/debug/pprof/heap
```

这应在你的浏览器中打开一个页面，显示什么正在使用什么
内存。

你还可以使用 `-text` 标志生成文本摘要

```console
$ go tool pprof -text http://localhost:5572/debug/pprof/heap
Showing nodes accounting for 1537.03kB, 100% of 1537.03kB total
      flat  flat%   sum%        cum   cum%
 1024.03kB 66.62% 66.62%  1024.03kB 66.62%  github.com/rclone/rclone/vendor/golang.org/x/net/http2/hpack.addDecoderNode
     513kB 33.38%   100%      513kB 33.38%  net/http.newBufioWriterSize
         0     0%   100%  1024.03kB 66.62%  github.com/rclone/rclone/cmd/all.init
         0     0%   100%  1024.03kB 66.62%  github.com/rclone/rclone/cmd/serve.init
         0     0%   100%  1024.03kB 66.62%  github.com/rclone/rclone/cmd/serve/restic.init
         0     0%   100%  1024.03kB 66.62%  github.com/rclone/rclone/vendor/golang.org/x/net/http2.init
         0     0%   100%  1024.03kB 66.62%  github.com/rclone/rclone/vendor/golang.org/x/net/http2/hpack.init
         0     0%   100%  1024.03kB 66.62%  github.com/rclone/rclone/vendor/golang.org/x/net/http2/hpack.init.0
         0     0%   100%  1024.03kB 66.62%  main.init
         0     0%   100%      513kB 33.38%  net/http.(*conn).readRequest
         0     0%   100%      513kB 33.38%  net/http.(*conn).serve
         0     0%   100%  1024.03kB 66.62%  runtime.main
```

### 调试 go routine 泄漏

内存泄漏通常是由 go routine 泄漏造成的，这些泄漏使本应
被垃圾回收的内存保持活动状态。

使用以下方法查看所有活动的 go routine

```console
curl http://localhost:5572/debug/pprof/goroutine?debug=1
```

或者在你的浏览器中转到 <http://localhost:5572/debug/pprof/goroutine?debug=1>。

### 其他可查看的配置文件

你可以在 <http://localhost:5572/debug/pprof/> 看到可用配置文件的摘要。

以下是使用其中一些的方法：

- 内存：`go tool pprof http://localhost:5572/debug/pprof/heap`
- Go routine：`curl http://localhost:5572/debug/pprof/goroutine?debug=1`
- 30 秒 CPU 配置文件：`go tool pprof http://localhost:5572/debug/pprof/profile`
- 5 秒执行跟踪：`wget http://localhost:5572/debug/pprof/trace?seconds=5`
- Goroutine 阻塞配置文件
  - 首先启用：`rclone rc debug/set-block-profile-rate rate=1`（[文档](#debug-set-block-profile-rate)）
  - `go tool pprof http://localhost:5572/debug/pprof/block`
- 互斥锁竞争：
  - 首先启用：`rclone rc debug/set-mutex-profile-fraction rate=1`（[文档](#debug-set-mutex-profile-fraction)）
  - `go tool pprof http://localhost:5572/debug/pprof/mutex`

请参阅 [net/http/pprof 文档](https://golang.org/pkg/net/http/pprof/)
了解有关如何使用分析工具的更多信息，有关一般概述，
请参阅 [Go 团队关于分析 go 程序的博客文章](https://blog.golang.org/profiling-go-programs)。

分析钩子是[零开销，除非它被使用](https://stackoverflow.com/q/26545159/164234)。
