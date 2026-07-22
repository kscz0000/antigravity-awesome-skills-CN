---
title: "Oracle Object Storage 挂载"
description: "Oracle Object Storage 挂载教程"
---

> **官方文档：** [https://rclone.org/oracleobjectstorage/](https://rclone.org/oracleobjectstorage/)
# Mount Buckets and Expose via NFS 教程

本操作手册展示如何使用 rclone 工具将 *Oracle Object Storage* 存储桶
[挂载](/commands/rclone_mount/) 为 OCI 计算实例上的本地文件系统。

你还将学习如何将 rclone 挂载导出为 NFS 挂载，以便其他 NFS 客户端可以访问它们。

使用模式：

NFS 客户端 --> NFS 服务器 --> RClone 挂载 --> OCI Object Storage

## 步骤 1：安装 Rclone

在 Oracle Linux 8 中，可以从
[OL8_Developer](https://yum.oracle.com/repo/OracleLinux/OL8/developer/x86_64/index.html)
Yum 仓库安装 Rclone。如果尚未启用该仓库，请先启用。

```console
[opc@base-inst-boot ~]$ sudo yum-config-manager --enable ol8_developer
[opc@base-inst-boot ~]$ sudo yum install -y rclone
[opc@base-inst-boot ~]$ sudo yum install -y fuse
# rclone will prefer fuse3 if available
[opc@base-inst-boot ~]$ sudo yum install -y fuse3
[opc@base-inst-boot ~]$ yum info rclone
Last metadata expiration check: 0:01:58 ago on Fri 07 Apr 2023 05:53:43 PM GMT.
Installed Packages
Name                : rclone
Version             : 1.62.2
Release             : 1.0.1.el8
Architecture        : x86_64
Size                : 67 M
Source              : rclone-1.62.2-1.0.1.el8.src.rpm
Repository          : @System
From repo           : ol8_developer
Summary             : rsync for cloud storage
URL                 : http://rclone.org/
License             : MIT
Description         : Rclone is a command line program to sync files and directories to and from various cloud services.
```

要将其作为挂载助手运行，应将 rclone 二进制文件符号链接到 /sbin/mount.rclone，
以及可选的 /usr/bin/rclonefs，例如 `ln -s /usr/bin/rclone /sbin/mount.rclone`。
rclone 会自动检测并适当转换命令行参数。

```console
ln -s /usr/bin/rclone /sbin/mount.rclone
```

## 步骤 2：配置 Rclone 配置文件

假设你要使用实例主体（instance principal）提供者作为与对象存储服务认证的方式，
从 OCI 计算实例访问 3 个存储桶。

- namespace-a, bucket-a,
- namespace-b, bucket-b,
- namespace-c, bucket-c

Rclone 配置文件需要包含 3 个远程节，上述 3 个存储桶各一个。
在 rclone 程序可读的可达位置创建配置文件。

```console
[opc@base-inst-boot ~]$ mkdir -p /etc/rclone
[opc@base-inst-boot ~]$ sudo touch /etc/rclone/rclone.conf


# add below contents to /etc/rclone/rclone.conf
[opc@base-inst-boot ~]$ cat /etc/rclone/rclone.conf


[ossa]
type = oracleobjectstorage
provider = instance_principal_auth
namespace = namespace-a
compartment = ocid1.compartment.oc1..aaaaaaaa...compartment-a
region = us-ashburn-1

[ossb]
type = oracleobjectstorage
provider = instance_principal_auth
namespace = namespace-b
compartment = ocid1.compartment.oc1..aaaaaaaa...compartment-b
region = us-ashburn-1


[ossc]
type = oracleobjectstorage
provider = instance_principal_auth
namespace = namespace-c
compartment = ocid1.compartment.oc1..aaaaaaaa...compartment-c
region = us-ashburn-1

# List remotes
[opc@base-inst-boot ~]$ rclone --config /etc/rclone/rclone.conf listremotes
ossa:
ossb:
ossc:

# Now please ensure you do not see below errors while listing the bucket,
# i.e you should fix the settings to see if namespace, compartment, bucket name are all correct.
# and you must have a dynamic group policy to allow the instance to use object-family in compartment.

[opc@base-inst-boot ~]$ rclone --config /etc/rclone/rclone.conf ls ossa:
2023/04/07 19:09:21 Failed to ls: Error returned by ObjectStorage Service. Http Status Code: 404. Error Code: NamespaceNotFound. Opc request id: iad-1:kVVAb0knsVXDvu9aHUGHRs3gSNBOFO2_334B6co82LrPMWo2lM5PuBKNxJOTmZsS. Message: You do not have authorization to perform this request, or the requested resource could not be found.
Operation Name: ListBuckets
Timestamp: 2023-04-07 19:09:21 +0000 GMT
Client Version: Oracle-GoSDK/65.32.0
Request Endpoint: GET https://objectstorage.us-ashburn-1.oraclecloud.com/n/namespace-a/b?compartmentId=ocid1.compartment.oc1..aaaaaaaa...compartment-a
Troubleshooting Tips: See https://docs.oracle.com/iaas/Content/API/References/apierrors.htm#apierrors_404__404_namespacenotfound for more information about resolving this error.
Also see https://docs.oracle.com/iaas/api/#/en/objectstorage/20160918/Bucket/ListBuckets for details on this operation's requirements.
To get more info on the failing request, you can set OCI_GO_SDK_DEBUG env var to info or higher level to log the request/response details.
If you are unable to resolve this ObjectStorage issue, please contact Oracle support and provide them this full error message.
[opc@base-inst-boot ~]$

```

## 步骤 3：配置动态组和添加 IAM 策略

正如人类用户通过 USER-PRINCIPAL 标识身份一样，每个 OCI 计算实例也是一个
通过 INSTANCE-PRINCIPAL 标识的机器人用户。实例主体密钥由 rclone/with-oci-sdk
从实例元数据自动获取，用于调用对象存储。

与[用户组](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managinggroups.htm)类似，
[实例组](https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingdynamicgroups.htm)
在 IAM 中称为动态组（dynamic-group）。

创建一个名为 rclone-dynamic-group 的动态组，使 OCI 计算实例成为该组的成员。
以下规则表示属于 compartment a...c 的所有实例都是此动态组的成员。

```console
any {instance.compartment.id = '<compartment_ocid_a>',
     instance.compartment.id = '<compartment_ocid_b>',
     instance.compartment.id = '<compartment_ocid_c>'
    }
```

现在你已有动态组，需要添加策略来定义该动态组的权限。
在本例中，我们希望该动态组能访问 object-storage，因此现在创建策略。

```text
allow dynamic-group rclone-dynamic-group to manage object-family in compartment compartment-a
allow dynamic-group rclone-dynamic-group to manage object-family in compartment compartment-b
allow dynamic-group rclone-dynamic-group to manage object-family in compartment compartment-c
```

添加策略后，确保 rclone 能列出存储桶中的文件。如果不能，请排查之前的配置。
请注意，身份策略最多可能需要一分钟才能生效。

## 步骤 4：配置挂载文件夹

假设你要挂载 3 个存储桶：bucket-a、bucket-b、bucket-c，
分别挂载到 /opt/mnt/bucket-a、/opt/mnt/bucket-b、/opt/mnt/bucket-c。

创建挂载文件夹并将其所有权设置为所需的用户和组。

```console
[opc@base-inst-boot ~]$ sudo mkdir /opt/mnt
[opc@base-inst-boot ~]$ sudo chown -R opc:adm /opt/mnt
```

为每个挂载路径设置所需的用户、组、其他人的 chmod 权限。

```console
[opc@base-inst-boot ~]$ sudo chmod 764 /opt/mnt
[opc@base-inst-boot ~]$ ls -al /opt/mnt/
total 0
drwxrw-r--. 2 opc adm 6 Apr 7 18:01 .
drwxr-xr-x. 10 root root 179 Apr 7 18:01 ..

[opc@base-inst-boot ~]$ mkdir -p /opt/mnt/bucket-a
[opc@base-inst-boot ~]$ mkdir -p /opt/mnt/bucket-b
[opc@base-inst-boot ~]$ mkdir -p /opt/mnt/bucket-c

[opc@base-inst-boot ~]$ ls -al /opt/mnt
total 0
drwxrw-r--. 5 opc adm 54 Apr 7 18:17 .
drwxr-xr-x. 10 root root 179 Apr 7 18:01 ..
drwxrwxr-x. 2 opc opc 6 Apr 7 18:17 bucket-a
drwxrwxr-x. 2 opc opc 6 Apr 7 18:17 bucket-b
drwxrwxr-x. 2 opc opc 6 Apr 7 18:17 bucket-c
```

## 步骤 5：确定要使用的 Rclone 挂载 CLI 配置选项

请完整阅读 [rclone mount](https://rclone.org/commands/rclone_mount/) 页面，
以真正理解挂载及其标志、rclone
[虚拟文件系统](https://rclone.org/commands/rclone_mount/#vfs-virtual-file-system)
模式设置，以及如何有效使用它们来实现所需的读写一致性。

本地文件系统期望 100% 可靠，而云存储系统离 100% 可靠还差很远。
对象存储可能抛出多种错误，如 429、503、404 等。
rclone sync/copy 命令通过大量重试来应对这些问题。
然而 rclone mount 无法以相同方式使用重试，除非在本地保存上传副本。
请查看 VFS 文件缓存以获取使挂载更可靠的解决方案。

首先了解 rclone 挂载标志和一些用于排查的全局标志。

```console
rclone mount \
    ossa:bucket-a \                     # Remote:bucket-name
    /opt/mnt/bucket-a \                 # Local mount folder
    --config /etc/rclone/rclone.conf \  # Path to rclone config file
    --allow-non-empty \                 # Allow mounting over a non-empty directory
    --dir-perms 0770 \                  # Directory permissions (default 0777)
    --file-perms 0660 \                 # File permissions (default 0666)
    --allow-other \                     # Allow access to other users
    --umask 0117  \                     # sets (660) rw-rw---- as permissions for the mount using the umask
    --transfers 8 \                     # default 4, can be set to adjust the number of parallel uploads of modified files to remote from the cache
    --tpslimit 50  \                    # Limit HTTP transactions per second to this. A transaction is roughly defined as an API call;
                                        # its exact meaning will depend on the backend. For HTTP based backends it is an HTTP PUT/GET/POST/etc and its response
    --cache-dir /tmp/rclone/cache       # Directory rclone will use for caching.
    --dir-cache-time 5m \               # Time to cache directory entries for (default 5m0s)
    --vfs-cache-mode writes \           # Cache mode off|minimal|writes|full (default off), writes gives the maximum compatibility like a local disk
    --vfs-cache-max-age 20m \           # Max age of objects in the cache (default 1h0m0s)
    --vfs-cache-max-size 10G \          # Max total size of objects in the cache (default off)
    --vfs-cache-poll-interval 1m \      # Interval to poll the cache for stale objects (default 1m0s)
    --vfs-write-back 5s   \             # Time to writeback files after last use when using cache (default 5s).
                                        # Note that files are written back to the remote only when they are closed and
                                        # if they haven't been accessed for --vfs-write-back seconds. If rclone is quit or
                                        # dies with files that haven't been uploaded, these will be uploaded next time rclone is run with the same flags.
    --vfs-fast-fingerprint              # Use fast (less accurate) fingerprints for change detection.
    --log-level ERROR \                            # log level, can be DEBUG, INFO, ERROR
    --log-file /var/log/rclone/oosa-bucket-a.log   # rclone application log
```

### --vfs-cache-mode writes

在此模式下，仅以读方式打开的文件仍直接从远程读取，
仅写和读/写文件会先缓冲到磁盘。此模式应支持所有正常的文件系统操作。
如果上传失败，将以指数增长的间隔重试，最长间隔为 1 分钟。

推荐使用 writes 的 VFS 缓存模式，以便应用程序能以最大兼容性
将远程存储当成本地磁盘使用。写入完成、文件关闭后，
经过 vfs-write-back 时长后文件会上传到后端远程。
如果 rclone 退出或崩溃时有文件尚未上传，
下次以相同标志运行 rclone 时这些文件将被上传。

### --tpslimit float

将每秒事务数限制为该数值。默认为 0，表示不限制每秒事务数。

事务大致定义为一次 API 调用；其确切含义取决于后端。
对于基于 HTTP 的后端，它是一次 HTTP PUT/GET/POST 等请求及其响应。
对于 FTP/SFTP，它是一次 TCP 往返事务。

例如，要将 rclone 限制为每秒 10 个事务，使用 --tpslimit 10，
或每 2 秒 1 个事务，使用 --tpslimit 0.5。

当 rclone 的每秒事务数导致云存储提供商出现问题
（例如被封禁、被限速或被节流）时使用此选项。

这对 rclone mount 控制使用它的应用程序的行为非常有用。
假设 Object Storage 每个租户大约允许 100 tps，
为安全起见，建议将其设为 50（根据各区域实际情况调整）。

### --vfs-fast-fingerprint

如果使用 --vfs-fast-fingerprint 标志，rclone 将不包含
慢操作来生成指纹。这使指纹精度略低但速度更快，
能改善缓存文件的打开时间。如果在 local、s3、object storage
或 swift 后端上运行 vfs 缓存，推荐使用此标志。

VFS 的各部分使用指纹来判断本地文件副本相对于远程文件是否已更改。
指纹由以下内容构成：

- 大小
- 修改时间
- 哈希值（在对象上可用时）

## 步骤 6：挂载选项，选择以下任一方式

### 步骤 6a：作为服务守护进程运行：为 Rclone 挂载配置 FSTAB 条目

在 /etc/fstab 中添加此条目：

```text
ossa:bucket-a /opt/mnt/bucket-a rclone rw,umask=0117,nofail,_netdev,args2env,config=/etc/rclone/rclone.conf,uid=1000,gid=4,
file_perms=0760,dir_perms=0760,allow_other,vfs_cache_mode=writes,cache_dir=/tmp/rclone/cache 0 0
```

重要提示：请注意在 fstab 条目中，参数使用下划线而非短横线，
例如：vfs_cache_mode=writes 而非 vfs-cache-mode=writes。
Rclone 在挂载助手模式下会将 -o 参数按逗号分割，将 `_` 替换为 `-`，
并在前面加上 `--` 以获得命令行标志。包含逗号或空格的选项
可以用单引号或双引号包裹。内部同类引号应双写转义。

然后运行 sudo mount -av

```console
[opc@base-inst-boot ~]$ sudo mount -av
/                    : ignored
/boot                : already mounted
/boot/efi            : already mounted
/var/oled            : already mounted
/dev/shm             : already mounted
none                 : ignored
/opt/mnt/bucket-a    : already mounted   # This is the bucket mounted information, running mount -av again and again is idempotent.
```

## 步骤 6b：作为服务守护进程运行：为 Rclone 挂载配置 systemd 条目

如果你熟悉配置 systemd 单元文件，也可以将每个 rclone 挂载
配置为 systemd 单元文件。
Git 搜索中的各种示例：<https://github.com/search?l=Shell&q=rclone+unit&type=Code>

```console
tee "/etc/systemd/system/rclonebucketa.service" > /dev/null <<EOF
[Unit]
Description=RCloneMounting
After=multi-user.target
[Service]
Type=simple
User=0
Group=0
ExecStart=/bin/bash /etc/rclone/scripts/bucket-a.sh
ExecStop=/bin/fusermount -uz /opt/mnt/bucket-a
TimeoutStopSec=20
KillMode=process
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
EOF
```

## 步骤 7：可选：挂载保姆脚本，用于弹性恢复，从进程崩溃中恢复

有时 rclone 进程崩溃，挂载点处于悬空状态——显示已挂载但 rclone 挂载进程已消失。
要清理挂载点，可以运行以下命令强制卸载。

```console
sudo fusermount -uz /opt/mnt/bucket-a
```

还可以运行 rclone_mount_nanny 脚本，它通过卸载后重新自动挂载来检测和清理挂载错误。

/etc/rclone/scripts/rclone_nanny_script.sh 的内容

```sh
#!/usr/bin/env bash
erroneous_list=$(df 2>&1 | grep -i 'Transport endpoint is not connected' | awk '{print ""$2"" }' | tr -d \:)
rclone_list=$(findmnt -t fuse.rclone -n 2>&1 | awk '{print ""$1"" }' | tr -d \:)
IFS=$'\n'; set -f
intersection=$(comm -12 <(printf '%s\n' "$erroneous_list" | sort) <(printf '%s\n' "$rclone_list" | sort))
for directory in $intersection
do
    echo "$directory is being fixed."
    sudo fusermount -uz "$directory"
done
sudo mount -av
```

用于幂等地添加 Cron 作业，每 5 分钟看护一次挂载路径的脚本

```sh
echo "Creating rclone nanny cron job."
croncmd="/etc/rclone/scripts/rclone_nanny_script.sh"
cronjob="*/5 * * * * $croncmd"
# idempotency - adds rclone_nanny cronjob only if absent.
( crontab -l | grep -v -F "$croncmd" || : ; echo "$cronjob" ) | crontab -
echo "Finished creating rclone nanny cron job."
```

确保 crontab 已添加，以便上述保姆脚本每 5 分钟运行一次。

```console
[opc@base-inst-boot ~]$ sudo crontab -l
*/5 * * * * /etc/rclone/scripts/rclone_nanny_script.sh
[opc@base-inst-boot ~]$
```

## 步骤 8：可选：配置 NFS 服务器以访问 rclone 的挂载点

假设你想将 rclone 挂载路径 /opt/mnt/bucket-a 作为 NFS 服务器导出，
以便其他客户端通过 NFS 客户端访问。

### 步骤 8a：配置 NFS 服务器

安装 NFS 工具

```console
sudo yum install -y nfs-utils
```

在 rclone 挂载所在的同一机器上通过 NFS 服务器导出所需目录，
确保 NFS 服务具有读取该目录的所需权限。
如果以 root 运行则肯定有权限，但如果以单独用户运行，
则需确保该用户拥有必要的所需特权。

```sh
# this gives opc user and adm (administrators group) ownership to the path, so any user belonging to adm group will be able to access the files.
[opc@tools ~]$ sudo chown -R opc:adm /opt/mnt/bucket-a/
[opc@tools ~]$ sudo chmod 764 /opt/mnt/bucket-a/

# Not export the mount path of rclone for exposing via nfs server
# There are various nfs export options that you should keep per desired usage.
# Syntax is
# <path> <allowed-ipaddr>(<option>)
[opc@tools ~]$ cat /etc/exports
/opt/mnt/bucket-a *(fsid=1,rw)


# Restart NFS server
[opc@tools ~]$ sudo systemctl restart nfs-server


# Show Export paths
[opc@tools ~]$ showmount -e
Export list for tools:
/opt/mnt/bucket-a *

# Know the port NFS server is running as, in this case it's listening on port 2049
[opc@tools ~]$ sudo rpcinfo -p | grep nfs
100003 3 tcp 2049 nfs
100003 4 tcp 2049 nfs
100227 3 tcp 2049 nfs_acl

# Allow NFS service via firewall
[opc@tools ~]$ sudo firewall-cmd --add-service=nfs --permanent
Warning: ALREADY_ENABLED: nfs
success
[opc@tools ~]$ sudo firewall-cmd --reload
success
[opc@tools ~]$

# Check status of NFS service
[opc@tools ~]$ sudo systemctl status nfs-server.service
● nfs-server.service - NFS server and services
   Loaded: loaded (/usr/lib/systemd/system/nfs-server.service; enabled; vendor preset: disabled)
   Active: active (exited) since Wed 2023-04-19 17:59:58 GMT; 13min ago
  Process: 2833741 ExecStopPost=/usr/sbin/exportfs -f (code=exited, status=0/SUCCESS)
  Process: 2833740 ExecStopPost=/usr/sbin/exportfs -au (code=exited, status=0/SUCCESS)
  Process: 2833737 ExecStop=/usr/sbin/rpc.nfsd 0 (code=exited, status=0/SUCCESS)
  Process: 2833766 ExecStart=/bin/sh -c if systemctl -q is-active gssproxy; then systemctl reload gssproxy ; fi (code=exit>
  Process: 2833756 ExecStart=/usr/sbin/rpc.nfsd (code=exited, status=0/SUCCESS)
  Process: 2833754 ExecStartPre=/usr/sbin/exportfs -r (code=exited, status=0/SUCCESS)
 Main PID: 2833766 (code=exited, status=0/SUCCESS)
    Tasks: 0 (limit: 48514)
   Memory: 0B
   CGroup: /system.slice/nfs-server.service

Apr 19 17:59:58 tools systemd[1]: Starting NFS server and services...
Apr 19 17:59:58 tools systemd[1]: Started NFS server and services.
```

### 步骤 8b：配置 NFS 客户端

现在从另一台客户端机器连接到 NFS 服务器，确保客户端机器
可以通过 TCP 端口 2049 访问 NFS 服务器机器，
确保子网网络 ACL 允许从所需源 IP 范围到目标 2049 端口的流量。

在客户端机器上挂载外部 NFS

```sh
# Install nfs-utils
[opc@base-inst-boot ~]$ sudo yum install -y nfs-utils

# In /etc/fstab, add the below entry
[opc@base-inst-boot ~]$ cat /etc/fstab | grep nfs
<ProvideYourIPAddress>:/opt/mnt/bucket-a /opt/mnt/buckert-a nfs rw 0 0

# remount so that newly added path gets mounted.
[opc@base-inst-boot ~]$ sudo mount -av
/ : ignored
/boot : already mounted
/boot/efi : already mounted
/var/oled : already mounted
/dev/shm : already mounted
/home/opc/share_drive/bucketa: already mounted
/opt/mnt/bucket-a: successfully mounted # this is the NFS mount
```

### 步骤 8c：测试连接

```sh
# List files to test connection
[opc@base-inst-boot ~]$ ls -al /opt/mnt/bucket-a
total 1
drw-rw----. 1 opc adm 0 Apr 18 17:28 .
drwxrw-r--. 7 opc adm 85 Apr 18 17:36 ..
drw-rw----. 1 opc adm 0 Apr 18 17:29 FILES
-rw-rw----. 1 opc adm 15 Apr 18 18:13 nfs.txt
```
