# WP 站点健康项目目录

较少见 WordPress 站点健康项的扩展列表，按类别组织。
主 `SKILL.md` 方案列表中的项目在此**不再重复**。

## 安全

### 密码需要更新 — Tier 1
存在弱密码或重复使用密码的用户。通知管理员，列出受影响用户：
```
wp user list --field=user_login | while read u; do echo "$u: $(wp user meta get "$u" session_tokens | wc -c)"; done
```
没有自动修复——管理员必须通过
`wp user reset-password <user>` 或"用户 > 个人资料"要求每位用户更新。

### 站点未使用持久连接（非对象缓存）— Tier 3
持久数据库连接（`mysqli.persist`）。纯粹信息项；
大多数共享主机禁用了此项，对标准 WP 安装没有性能负面影响。无需操作。

### 应检查文件权限 — Tier 2
`wp-config.php` 与 `/wp-content/` 目录权限。给出期望的权限：
```bash
find . -type f -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;
chmod 600 wp-config.php
chmod 400 .htaccess # if Apache; nginx ignores it
```
用户必须向主机确认文件系统是否支持这些权限
（部分托管 WP 主机锁定了权限）。

## 性能

### 发现大量自动加载的索引选项 — Tier 2
自动加载选项超过 1 MB。列出最大占用者：
```
SELECT option_name, LENGTH(option_value) AS size
FROM wp_options
WHERE autoload = 'yes'
ORDER BY size DESC
LIMIT 20;
```
若某个插件是来源，报告该插件名称。清理方式包括：
- `wp option delete <key>`（仅在确认该选项可安全删除时使用——
  需先与插件作者确认）。
- 禁用自动加载：`wp option update <key> <value> --autoload=no`。

### 无法处理计划维护任务（wp_cron）— Tier 2
已设置 `DISABLE_WP_CRON` 但没有系统 cron 在运行。可通过以下方式修复：
1. 设置真正的系统 cron 任务（推荐）：
   ```
   * * * * * wget -q -O - https://example.com/wp-cron.php
   ```
2. 从 `wp-config.php` 中移除 `define('DISABLE_WP_CRON', true);`

### 后台更新失败 — Tier 2
针对核心/插件/主题的自动后台更新。检查：
```
wp core check-update
wp plugin list --update=available
```
若 `DISALLOW_FILE_MODS` 为 true，则后台更新被阻止。
仅在用户明确希望自动更新时才覆盖：
```php
define('DISALLOW_FILE_MODS', false); // wp-config.php
```

## SEO

### llms.txt 生成未配置 — Tier 1
站点在域根缺少 `llms.txt` 文件。安装并激活支持此功能的 SEO 插件，
或在 wp-admin > SEO > 设置中手动创建该文件。
不是排名因素，但建议为 AI 爬虫的可发现性配置。

### 未检测到 XML 站点地图 — Tier 1
安装支持站点地图的 SEO 插件（Yoast、Rank Math 等）
或专用站点地图插件。在插件设置界面启用站点地图生成
（各插件没有可靠的统一 WP-CLI 开关）。

### 缺少社交预览图片 — Tier 2
未设置 Open Graph / Twitter Card meta 标签。需要主题集成
或 SEO 插件。若主题使用 `wp_head()`，可起草 OG meta 标签：
```php
add_action('wp_head', function () {
    if (has_post_thumbnail()) {
        echo '<meta property="og:image" content="' . esc_url(get_the_post_thumbnail_url()) . '" />';
    }
});
```

## 隐私

### 未设置隐私政策页面 — Tier 1
站点没有隐私政策页面。创建一个：
```
wp post create --post_type=page --post_title="Privacy Policy" --post_status=draft
```
然后在"设置 > 隐私"中指定，或通过：
```
wp option update wp_page_for_privacy_policy <page-id>
```

### 隐私政策页面已过时 — Tier 2
隐私政策页面创建于站点当前隐私指引生成日期之前。
在"工具 > 导出个人数据"中重新运行指引生成器
并更新页面内容。该操作无 WP-CLI 命令——需手动完成。

## 诊断 / 难以分类

### Xdebug 扩展的版本需求不匹配 — Tier 3
Xdebug 已加载但生产环境并不需要。若用户并非有意安装，
建议通过主机面板或 php.ini 移除：
```
; php.ini
; zend_extension=xdebug.so  (comment out or remove)
```

### 缺少 ZipArchive / gzinflate / BCMath / Imagick — Tier 2
缺少部分插件或 WordPress 自身所需的 PHP 扩展。
列出缺失的扩展并建议通过主机面板安装，或：
```
sudo apt install php-zip php-gd php-bcmath php-imagick
```
（命令因操作系统而异——根据用户环境起草相应命令。）

## 故意不收入本目录的项目

- **SQL Server 版本** — WP 核心已将其报告为通过或信息项；不存在用户操作。
- **活动主题为最新** — 已在站点健康中为绿色；无需操作。
- **有可用插件更新** — 由 `wp plugin update --all` 处理。