---
name: wp-site-health-auditor
description: "将 WordPress Site Health 报告转换为按风险分层、备份优先的修复方案，并附带精确的 WP-CLI/PHP 代码片段。涉及站点健康、推荐改进或严重问题报告时使用。"
category: development
risk: critical
source: self
source_type: self
date_added: "2026-07-03"
author: whoisabhishekadhikari
tags: [wordpress, site-health, wp-cli, seo, performance, security, hardening]
tools: [claude, cursor, codex, gemini]
---

# WP 站点健康审计器

## 适用场景

- 用户粘贴了 WordPress 站点健康报告（`工具 > 站点健康`），可以是文本或截图
- 用户粘贴了原始站点健康调试信息（`工具 > 站点健康 > 信息`），并询问哪里出了问题
- 用户在 WordPress 站点场景下涉及"站点健康"、"推荐改进"或"严重问题"
- 用户希望基于该界面清理、加固或加速某个 WP 安装

将 WordPress 站点健康报告（严重问题 / 推荐改进 / 通过测试）转换为按风险分层的修复方案——然后执行安全的修复，剩余部分以精确命令或代码的形式交接。

## ⚠️ 安全须知 — 修改任何文件前必读

本技能会编辑 `wp-config.php`、`.htaccess` 以及等效于 `php.ini` 的设置，并删除插件与主题。这三类操作只要一次编辑失误就可能引发白屏死机或上传路径损坏。**即便只是一行变更，即便用户急于完成，也请勿跳过本节。**

**任何编辑或删除之前，按以下顺序操作：**
1. **备份即将修改的具体文件**，而不是只在"某处有个备份"：
   ```
   cp wp-config.php wp-config.php.bak-$(date +%Y%m%d-%H%M%S)
   cp .htaccess .htaccess.bak-$(date +%Y%m%d-%H%M%S)
   ```
   若无 shell 访问权限，请告知用户先通过 SFTP/主机文件管理器下载当前文件，并在他们确认已下载后再继续。
2. **确认存在完整的站点/数据库备份**，再删除任何插件或主题，或运行 `wp search-replace`。若用户没有备份但启用了备份插件（UpdraftPlus 等），请先触发一次备份：`wp updraftplus backup` 或该插件自身的 WP-CLI 命令，或告知用户点击"立即备份"并在确认完成后再继续。
3. **运行 `wp search-replace` 前必须先用 `--dry-run`**，并将演练输出展示给用户后再真正执行。该命令会原地重写数据库——错误的匹配模式可能损坏其触及的每张表中的序列化数据。
4. **编辑任何 PHP 文件后，重新加载站点前先进行语法检查**：
   ```
   php -l wp-config.php
   ```
   对于 `.htaccess` 的修改，若可用请运行 `apachectl configtest`，或立即访问站点检查。`wp-config.php` 中的一处语法错误会立刻让整个站点宕机。不要为省事跳过语法检查。
5. **每次只改一处，然后验证站点仍可访问**（首页 + wp-admin），再进行下一处修改。不要将多个 Tier 2 文件编辑合并为一次操作——一旦出问题，你需要知道是哪一处改动导致的。
6. **每次编辑同时提供精确的回滚命令**：
   ```
   cp wp-config.php.bak-<timestamp> wp-config.php
   ```
   即便一切正常也要声明——这多写一行，将来可能救一个惊慌失措的用户。

若用户说"直接做吧，跳过备份"——仍需在编辑流程中静默创建备份并告知用户已创建。绝对不要整体跳过步骤 1 或步骤 4；这两步在任何紧急情况下都不可妥协，因为失败模式（`wp-config.php` 损坏、站点宕机）的后果远比十秒钟的备份成本更严重。

## 概览

"站点健康"界面是诊断性的，而非处方性的。它告诉站长"有问题"（例如"应使用持久化对象缓存"），但不告诉"如何修复"，且混杂了一键安全项（停用插件）与需要主机层面修改（php.ini、对象缓存后端）的项目，甚至是纯信息项（SQL 服务器版本——无需操作）。本技能的作用就是把这些梳理清楚——并安全地处理。

## 阶段 1 — 解析报告

输入通常为以下之一：
- 从 `工具 > 站点健康`（状态选项卡）复制的纯文本
- 从 `工具 > 站点健康 > 信息`（调试数据导出）复制的纯文本
- 状态选项卡的截图
- WP-CLI 输出（`wp site-health check` 并非核心命令；需提前说明，不要杜撰——参见阶段 4）

严格按照 WordPress 的标签提取三类：
1. **严重问题**（红色）— 始终优先修复，每次动手前务必确认。
2. **推荐改进**（黄色）— 实际工作的主体；按下面的风险层级分类处理。
3. **通过测试**（绿色）— 跳过。除非用户要求，否则不要"修复"或重新验证通过项。不要在绿色项上生造问题——一个常见错误是把"SQL 服务器已为最新版"当作需要处理的事项。它不是。

若报告是截图，则在分类前逐字转写项目标题与类别标签（安全/性能/SEO/隐私）——不要改写 WordPress 自动生成的标题，因为它会在阶段 3 中用于匹配修复方案。

若用户没有粘贴报告而只是说"审计我的站点健康"，请让他们粘贴状态选项卡的文本（最快），而不是凭空猜测——站点健康结果因主机与配置而异，猜测只会浪费一轮。

## 阶段 2 — 风险分层分类

在任何操作之前，将每个未通过项归入以下三个层级之一。当非 Tier 1 项超过 3 个时，先向用户呈现分类表——不要默默开始停用插件。

**Tier 1 — 安全、可逆、可在 wp-admin 或 WP-CLI 中自动修复**
无数据丢失风险、无停机、完全可逆。在删除任何内容前，仍需按"安全须知"一节进行备份。一旦用户确认了项目清单，可直接修复。
- 移除未启用的插件/主题（它们并未运行，停用已经发生——这只是删除死代码）
- 在生产环境中关闭 `WP_DEBUG` 显示（关闭 `WP_DEBUG_DISPLAY`，而非 `WP_DEBUG`，若用户仍需记录日志）
- 开启搜索引擎索引 / 修正 robots 可见性开关
- 将站点副标题从"Just another WordPress site"修改为其他内容

**Tier 2 — 需要主机/服务器层面访问 — Claude 起草变更，用户或主机应用**
无法仅在 wp-admin 中修复；需要 php.ini、.htaccess、wp-config.php 或主机面板的访问权限。起草精确代码片段，说明放在哪里，提醒用户上述备份与语法检查步骤，并标注可能需要服务器重启或主机支持工单。
- 固定链接结构变更（迁移——若无重定向会破坏现有 URL；应用前需制定重定向方案并刷新 CDN/缓存）
- `post_max_size` < `upload_max_filesize` 不匹配
- 持久化对象缓存不可用（Redis/Memcached）
- 未检测到页面缓存
- PHP 版本/模块变更
- HTTPS/SSL 配置
- 因防火墙或安全插件屏蔽导致的 Loopback/REST API 失败

**Tier 3 — 信息性 / 取决于主机，无修复或无需修复**
仅作为信息项报告。不要尝试修复，除非直接被问及，否则不要建议修复方案。
- SQL 服务器版本已是最新时的提示
- "自动加载的选项可接受"等通过项相邻的信息
- "通过测试"中已为绿色的任何项

## 阶段 3 — 按项目的修复方案

将 WordPress 自动生成的项目标题（不区分大小写的子串匹配即可）与下面的方案匹配。每个方案都假定对应文件已经遵循"安全须知"一节。若某项在此处没有匹配，请明确说明，不要拼凑一个修复——站点健康项集会随 WP 核心版本变化，本列表并非穷尽（完整列表及较少见项目见 `references/catalog.md`）。

### 应移除未启用的插件 / 主题 — Tier 1
```
# confirm full site backup exists first (Safety step 2)
wp plugin list --status=inactive --field=name
wp plugin delete <plugin-slug>

wp theme list --status=inactive --field=name
wp theme delete <theme-slug>
```
若当前启用的主题为子主题，绝不要删除其父主题。若 Twenty Twenty-Five（或当前默认核心主题）是唯一的回退主题，也不要删除——WordPress 至少需要一个回退主题；建议即便不启用也保留一个打包自带的默认主题。
删除前务必与用户确认插件/主题的准确名称——"未启用"不等于"未使用"；有些插件是刻意停用作为预备回滚。

### post_max_size 小于 upload_max_filesize — Tier 2
这会破坏大文件上传（post 数据会在达到文件大小限制前就被截断）。修复方法是将 `post_max_size` 提升至 `>= upload_max_filesize`，通常会为表单开销预留余量。

设置位置（按以下优先级选择主机所支持的）：
1. 主机控制面板的 PHP 设置（cPanel "Select PHP Version" > Options、Plesk 等）——无需改代码，是最安全的选项，可完全跳过文件备份步骤。
2. `php.ini`（若用户拥有服务器访问权限）—— 先备份（`cp php.ini php.ini.bak-<timestamp>`）：
   ```ini
   upload_max_filesize = 64M
   post_max_size = 128M
   ```
3. `.htaccess`（仅适用于 Apache + mod_php，PHP-FPM/nginx 不适用）—— 先备份：
   ```apache
   php_value upload_max_filesize 64M
   php_value post_max_size 128M
   ```
   格式错误的 `.htaccess` 指令会引发整个站点 500。重新加载前若有 `apachectl configtest` 可用请运行，否则保存后立即检查线上站点。
4. `.user.ini`（CGI/FastCGI 主机；非 mod_php）—— 先备份，在 WordPress 根目录创建或编辑 `.user.ini`：
   ```ini
   upload_max_filesize = 64M
   post_max_size = 128M
   ```
   ⚠️ **不要在 `wp-config.php` 中使用 `ini_set()` 设置这些指令**——`upload_max_filesize` 与 `post_max_size` 属于 `PHP_INI_PERDIR`，只能在请求开始前设置（php.ini、.htaccess、.user.ini）。`ini_set()` 调用对两者都会静默失败，问题不会被解决。

务必将 `post_max_size` 严格设置得大于 `upload_max_filesize`。在操作前先确认当前值（`wp cli info` 不显示这些——查看 `phpinfo()` 或主机面板），不要假设默认值。

### 应使用持久化对象缓存 — Tier 2
需要在服务器层面安装缓存后端（Redis 或 Memcached）——这不是仅靠插件凭空能创建的东西。
1. 与用户的主机确认是否提供 Redis 或 Memcached（许多托管 WP 主机自带其中之一）。
2. 若可用，安装一个 drop-in 客户端插件：Redis Object Cache 或 WP Redis（Redis），或 Memcached Object Cache（Memcached）。运行 `wp plugin install redis-cache --activate` 然后 `wp redis enable`。这会在 `wp-content/` 写入一个 `object-cache.php` drop-in——确认未覆盖现有 `object-cache.php`（先用 `ls wp-content/object-cache.php` 检查）；若已存在，启用前先备份。
3. 若不可用，这是托管层级限制——如实报告，不要试图伪造修复；在用户未主动要求时不要建议更换主机，只需将其标注为阻塞因素。

### 未检测到页面缓存 — Tier 2
1. 检查主机是否提供服务器级页面缓存（许多托管 WP 主机已启用，但可能未报告站点健康所检测的响应头——在安装冗余插件前值得与主机确认）。
2. 若没有，安装一个页面缓存插件（不要整套插件都装）—— WP Super Cache、W3 Total Cache 或主机推荐的一款。运行 `wp plugin install wp-super-cache --activate` 然后从其设置界面启用缓存（各缓存插件没有统一的可靠 WP-CLI 开关——需告知用户手动操作）。
3. 避免堆叠两个缓存插件；若一个已启用但未检测到，请在添加另一个之前检查该插件自身的状态页面。一些缓存插件还会向 `.htaccess` 写入规则——按"安全须知"先备份再启用。

### 站点未设置为输出调试信息 — 通常已通过；若未通过 — Tier 1
先备份 `wp-config.php`，编辑后进行语法检查：
```php
// wp-config.php
define( 'WP_DEBUG', false );         // set to true only while actively debugging
define( 'WP_DEBUG_DISPLAY', false ); // never show errors to visitors
define( 'WP_DEBUG_LOG', true );      // logs to wp-content/debug.log instead
```

### REST API / loopback 请求 / 后台更新失败 — Tier 2
通常是安全插件、防火墙或 `.htaccess` 规则阻止了内部请求。步骤：
1. 逐个临时停用安全/防火墙插件，每次停用后重新检查站点健康。
2. 检查主机层面的防火墙（Cloudflare、Sucuri、主机 WAF）是否阻止了站点对自身的访问。
3. 若失败项是后台更新，请验证 `wp-config.php` 没有为后台更新错误地设置 `define('DISALLOW_FILE_MODS', true)`。在移除/编辑该行前先备份。

### HTTPS 未完全启用 — Tier 2
```
wp option get siteurl
wp option get home
```
两者都必须为 `https://`。同时检查是否存在混合内容（在内容/主题中硬编码的 http://）。确认存在完整数据库备份，然后演练后再真正应用：
```
wp search-replace 'http://olddomain.com' 'https://olddomain.com' --dry-run
```
只有在用户审阅了演练输出并确认替换计数与匹配行看起来正确后，才移除 `--dry-run`。

## 阶段 4 — 不可凭空捏造的内容

- 截至本文撰写时，WordPress 核心中没有 `wp site-health` 这一 WP-CLI 命令——不要杜撰。修复通过上面具体的命令完成，而不是单一的 audit-and-fix CLI 调用。
- 没有用户（或重新运行站点健康）确认前，不要声称修复完成——尤其服务器层面变更（Tier 2）可能因主机限制而静默失败。
- 不要猜测 PHP/服务器值（当前的 `upload_max_filesize`、缓存后端可用性等）——询问或让用户检查 `phpinfo()` / 主机面板，不要假设常见的默认值已生效。
- 不要以任何理由跳过或缩减"安全须知"一节，包括"这只是个小改动"——文件损坏风险并不随编辑量线性变化；`wp-config.php` 中漏写一个分号与大改动一样致命。

## 阶段 5 — 输出格式

向用户提供：
1. **分类表**：项目 | 类别 | 层级 | 一行修复摘要
2. **Tier 1 修复**：直接执行（删除前需确认 + 备份），展示修改前/后
3. **Tier 2 修复**：精确代码片段 + 准确放置位置 + 备份命令 + 语法检查/验证命令 + 回滚命令 + 标注可能需要主机重启或支持工单；在用户确认站点仍可访问前不要标记为"完成"
4. **Tier 3 / 未识别项**：每项一行，仅作信息项
5. 建议在 Tier 1/2 变更后重新运行站点健康以确认黄色项清空。

保持整体响应易于扫读——这是一份工作清单，不是文章。使用上面的表格 + 简短的方案块，而非散文段落，除非用户要求对某项作更多说明。

## 示例

### 示例：站点健康报告"应使用持久化对象缓存"

1. 分类 → Tier 2（需要在服务器层面有 Redis/Memcached）
2. 让用户向主机确认 Redis 是否可用
3. 若是，运行：
   ```
   wp plugin install redis-cache --activate
   wp redis enable
   ```
4. 验证：`ls wp-content/object-cache.php` 文件存在
5. 重新运行站点健康，确认该项清空

### 示例：站点健康报告"站点未设置为输出调试信息"

1. 分类 → Tier 1（安全、可通过 wp-config.php 还原）
2. 备份 `wp-config.php`：
   ```
   cp wp-config.php wp-config.php.bak-$(date +%Y%m%d-%H%M%S)
   ```
3. 编辑并进行语法检查：
   ```php
   define( 'WP_DEBUG', false );
   define( 'WP_DEBUG_DISPLAY', false );
   ```
4. 验证 `php -l wp-config.php` 通过
5. 确认站点首页 + wp-admin 仍可访问

## 最佳实践

- ✅ 每次编辑前先备份具体文件——`cp` 只需几秒，恢复宕机站点却要数小时
- ✅ 每次只改一处，并在每次变更之间验证站点可访问
- ✅ 编辑 `wp-config.php` 后、重新加载站点前，务必运行 `php -l`
- ✅ 运行 `wp search-replace` 时先加 `--dry-run`，并将输出展示给用户
- ❌ 不要将多个 Tier 2 文件编辑合并为一次操作——你无法确定是哪一处改动让站点崩溃
- ❌ 不要跳过备份步骤，即便只是一行注释修改

## 参考

`references/catalog.md` — 较少见站点健康项的扩展列表（SEO 类项目如 llms.txt 生成、隐私类项目、较罕见的安全类项目），采用相同的层级分类，供包含上述未覆盖项目的报告使用。

## 常见陷阱

- **将每个黄色项都视为可操作** — 部分推荐改进（例如持久化对象缓存）属于主机层面，可能无法修复。始终按层级分类后再行动。
- **变更固定链接时没有重定向方案** — 在已收录的站点上切换到"文章名"会破坏所有现有 URL。务必先规划 301 重定向。
- **使用 `ini_set()` 设置上传限制** — `upload_max_filesize` 与 `post_max_size` 属于 `PHP_INI_PERDIR`；`ini_set()` 会静默失败。应改用 `php.ini`、`.htaccess` 或 `.user.ini`。
- **跳过 `wp search-replace` 的演练** — 错误的匹配模式可能损坏序列化数据。运行前必须加 `--dry-run`。
- **安装两个缓存插件** — 堆叠页面缓存插件会导致冲突与隐蔽 bug。若一个已启用但未检测到，应调试该插件而非再添加一个。

## 局限性

- 无法对线上站点自行执行任何操作——所有 WP-CLI/PHP 代码片段都需由用户或其主机运行；本技能对用户实际服务器没有 shell 访问权限。
- 无法验证当前 PHP/服务器值（上传限制、缓存后端可用性、HTTPS 状态）——依赖于用户在检查 `phpinfo()` 或其主机面板后回报的信息。
- 未涵盖多站点专属的站点健康变体或 WooCommerce 专属的健康检查；这两者会增加本技能方案列表未包含的额外项目。
- 项目目录（主文件 + `references/catalog.md`）反映了截至 2026 年中 WordPress 核心的站点健康检查——项目标题/措辞会随核心版本变化，因此未匹配项应报告为未匹配，而不是强行套用最接近的方案。
- 不能替代完整的安全审计或入侵扫描——站点健康标记的是配置层面的卫生问题，而非站点已被攻陷的迹象。

## 相关技能

- `@security-hardening` — 用于超越站点健康表层检查的深入 WordPress 安全审计
- `@wp-performance` — 用于在站点健康标记被解决后进行有针对性的性能优化