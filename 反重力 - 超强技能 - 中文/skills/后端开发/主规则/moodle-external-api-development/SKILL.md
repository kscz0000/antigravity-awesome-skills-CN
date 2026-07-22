---
name: moodle-external-api-development
description: "本技能指导你为 Moodle LMS 创建自定义外部 Web 服务 API，遵循 Moodle 的外部 API 框架和编码规范。当用户要求创建 Moodle 外部 API、Web 服务接口或 REST 端点时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Moodle 外部 API 开发

本技能指导你为 Moodle LMS 创建自定义外部 Web 服务 API，遵循 Moodle 的外部 API 框架和编码规范。

## 使用场景

- 为 Moodle 插件创建自定义 Web 服务
- 实现用于课程管理的 REST/AJAX 端点
- 构建用于测验操作、用户跟踪或报告的 API
- 将 Moodle 功能暴露给外部应用程序
- 使用 Moodle 开发移动应用后端

## 核心架构模式

Moodle 外部 API 遵循严格的三方法模式：

1. **`execute_parameters()`** - 定义输入参数结构
2. **`execute()`** - 包含业务逻辑
3. **`execute_returns()`** - 定义返回结构

## 分步实现

### 步骤 1：创建外部 API 类文件

**位置**：`/local/yourplugin/classes/external/your_api_name.php`

```php
<?php
namespace local_yourplugin\external;

defined('MOODLE_INTERNAL') || die();
require_once("$CFG->libdir/externallib.php");

use external_api;
use external_function_parameters;
use external_single_structure;
use external_value;

class your_api_name extends external_api {
    
    // Three required methods will go here
    
}
```

**要点**：
- 类必须继承 `external_api`
- 命名空间遵循：`local_pluginname\external` 或 `mod_modname\external`
- 包含安全检查：`defined('MOODLE_INTERNAL') || die();`
- 引入 externallib.php 以使用基类

### 步骤 2：定义输入参数

```php
public static function execute_parameters() {
    return new external_function_parameters([
        'userid' => new external_value(PARAM_INT, 'User ID', VALUE_REQUIRED),
        'courseid' => new external_value(PARAM_INT, 'Course ID', VALUE_REQUIRED),
        'options' => new external_single_structure([
            'includedetails' => new external_value(PARAM_BOOL, 'Include details', VALUE_DEFAULT, false),
            'limit' => new external_value(PARAM_INT, 'Result limit', VALUE_DEFAULT, 10)
        ], 'Options', VALUE_OPTIONAL)
    ]);
}
```

**常用参数类型**：
- `PARAM_INT` - 整数
- `PARAM_TEXT` - 纯文本（去除 HTML）
- `PARAM_RAW` - 原始文本（不做清理）
- `PARAM_BOOL` - 布尔值
- `PARAM_FLOAT` - 浮点数
- `PARAM_ALPHANUMEXT` - 含扩展字符的字母数字

**结构类型**：
- `external_value` - 单个值
- `external_single_structure` - 具有命名字段的对象
- `external_multiple_structure` - 项目数组

**值标志**：
- `VALUE_REQUIRED` - 必须提供该参数
- `VALUE_OPTIONAL` - 参数可选
- `VALUE_DEFAULT, defaultvalue` - 可选且有默认值

### 步骤 3：实现业务逻辑

```php
public static function execute($userid, $courseid, $options = []) {
    global $DB, $USER;

    // 1. Validate parameters
    $params = self::validate_parameters(self::execute_parameters(), [
        'userid' => $userid,
        'courseid' => $courseid,
        'options' => $options
    ]);

    // 2. Check permissions/capabilities
    $context = \context_course::instance($params['courseid']);
    self::validate_context($context);
    require_capability('moodle/course:view', $context);

    // 3. Verify user access
    if ($params['userid'] != $USER->id) {
        require_capability('moodle/course:viewhiddenactivities', $context);
    }

    // 4. Database operations
    $sql = "SELECT id, name, timecreated
            FROM {your_table}
            WHERE userid = :userid
              AND courseid = :courseid
            LIMIT :limit";
    
    $records = $DB->get_records_sql($sql, [
        'userid' => $params['userid'],
        'courseid' => $params['courseid'],
        'limit' => $params['options']['limit']
    ]);

    // 5. Process and return data
    $results = [];
    foreach ($records as $record) {
        $results[] = [
            'id' => $record->id,
            'name' => $record->name,
            'timestamp' => $record->timecreated
        ];
    }

    return [
        'items' => $results,
        'count' => count($results)
    ];
}
```

**关键步骤**：
1. **始终使用 `validate_parameters()` 验证参数**
2. **使用 `validate_context()` 检查上下文**
3. **使用 `require_capability()` 验证权限**
4. **使用参数化查询**防止 SQL 注入
5. **返回与返回定义匹配的结构化数据**

### 步骤 4：定义返回结构

```php
public static function execute_returns() {
    return new external_single_structure([
        'items' => new external_multiple_structure(
            new external_single_structure([
                'id' => new external_value(PARAM_INT, 'Item ID'),
                'name' => new external_value(PARAM_TEXT, 'Item name'),
                'timestamp' => new external_value(PARAM_INT, 'Creation time')
            ])
        ),
        'count' => new external_value(PARAM_INT, 'Total items')
    ]);
}
```

**返回结构规则**：
- 必须与 `execute()` 的返回完全匹配
- 使用适当的参数类型
- 为每个字段添加描述文档
- 允许嵌套结构

### 步骤 5：注册服务

**位置**：`/local/yourplugin/db/services.php`

```php
<?php
defined('MOODLE_INTERNAL') || die();

$functions = [
    'local_yourplugin_your_api_name' => [
        'classname'   => 'local_yourplugin\external\your_api_name',
        'methodname'  => 'execute',
        'classpath'   => 'local/yourplugin/classes/external/your_api_name.php',
        'description' => 'Brief description of what this API does',
        'type'        => 'read',  // or 'write'
        'ajax'        => true,
        'capabilities'=> 'moodle/course:view', // comma-separated if multiple
        'services'    => [MOODLE_OFFICIAL_MOBILE_SERVICE] // Optional
    ],
];

$services = [
    'Your Plugin Web Service' => [
        'functions' => [
            'local_yourplugin_your_api_name'
        ],
        'restrictedusers' => 0,
        'enabled' => 1
    ]
];
```

**服务注册键**：
- `classname` - 完整命名空间的类名
- `methodname` - 始终为 'execute'
- `type` - 'read'（SELECT）或 'write'（INSERT/UPDATE/DELETE）
- `ajax` - 设为 true 以启用 AJAX/REST 访问
- `capabilities` - 所需的 Moodle 权限
- `services` - 可选的服务包

### 步骤 6：实现错误处理与日志记录

```php
private static function log_debug($message) {
    global $CFG;
    $logdir = $CFG->dataroot . '/local_yourplugin';
    if (!file_exists($logdir)) {
        mkdir($logdir, 0777, true);
    }
    $debuglog = $logdir . '/api_debug.log';
    $timestamp = date('Y-m-d H:i:s');
    file_put_contents($debuglog, "[$timestamp] $message\n", FILE_APPEND | LOCK_EX);
}

public static function execute($userid, $courseid) {
    global $DB;

    try {
        self::log_debug("API called: userid=$userid, courseid=$courseid");
        
        // Validate parameters
        $params = self::validate_parameters(self::execute_parameters(), [
            'userid' => $userid,
            'courseid' => $courseid
        ]);

        // Your logic here
        
        self::log_debug("API completed successfully");
        return $result;

    } catch (\invalid_parameter_exception $e) {
        self::log_debug("Parameter validation failed: " . $e->getMessage());
        throw $e;
    } catch (\moodle_exception $e) {
        self::log_debug("Moodle exception: " . $e->getMessage());
        throw $e;
    } catch (\Exception $e) {
        // Log detailed error info
        $lastsql = method_exists($DB, 'get_last_sql') ? $DB->get_last_sql() : '[N/A]';
        self::log_debug("Fatal error: " . $e->getMessage());
        self::log_debug("Last SQL: " . $lastsql);
        self::log_debug("Stack trace: " . $e->getTraceAsString());
        throw $e;
    }
}
```

**错误处理最佳实践**：
- 用 try-catch 块包裹逻辑
- 记录带时间戳和上下文的错误日志
- 在数据库错误时捕获 SQL 查询
- 保留堆栈跟踪用于调试
- 记录日志后重新抛出异常

## 高级模式

### 复杂数据库操作

```php
// Transaction example
$transaction = $DB->start_delegated_transaction();

try {
    // Insert record
    $recordid = $DB->insert_record('your_table', $dataobject);
    
    // Update related records
    $DB->set_field('another_table', 'status', 1, ['recordid' => $recordid]);
    
    // Commit transaction
    $transaction->allow_commit();
} catch (\Exception $e) {
    $transaction->rollback($e);
    throw $e;
}
```

### 操作课程模块

```php
// Create course module
$moduleid = $DB->get_field('modules', 'id', ['name' => 'quiz'], MUST_EXIST);

$cm = new \stdClass();
$cm->course = $courseid;
$cm->module = $moduleid;
$cm->instance = 0; // Will be updated after activity creation
$cm->visible = 1;
$cm->groupmode = 0;
$cmid = add_course_module($cm);

// Create activity instance (e.g., quiz)
$quiz = new \stdClass();
$quiz->course = $courseid;
$quiz->name = 'My Quiz';
$quiz->coursemodule = $cmid;
// ... other quiz fields ...

$quizid = quiz_add_instance($quiz, null);

// Update course module with instance ID
$DB->set_field('course_modules', 'instance', $quizid, ['id' => $cmid]);
course_add_cm_to_section($courseid, $cmid, 0);
```

### 访问限制（分组/可用性）

```php
// Restrict activity to specific user via group
$groupname = 'activity_' . $activityid . '_user_' . $userid;

// Create or get group
if (!$groupid = $DB->get_field('groups', 'id', ['courseid' => $courseid, 'name' => $groupname])) {
    $groupdata = (object)[
        'courseid' => $courseid,
        'name' => $groupname,
        'timecreated' => time(),
        'timemodified' => time()
    ];
    $groupid = $DB->insert_record('groups', $groupdata);
}

// Add user to group
if (!$DB->record_exists('groups_members', ['groupid' => $groupid, 'userid' => $userid])) {
    $DB->insert_record('groups_members', (object)[
        'groupid' => $groupid,
        'userid' => $userid,
        'timeadded' => time()
    ]);
}

// Set availability condition
$restriction = [
    'op' => '&',
    'show' => false,
    'c' => [
        [
            'type' => 'group',
            'id' => $groupid
        ]
    ],
    'showc' => [false]
];

$DB->set_field('course_modules', 'availability', json_encode($restriction), ['id' => $cmid]);
```

### 使用标签随机选题

```php
private static function get_random_questions($categoryid, $tagname, $limit) {
    global $DB;
    
    $sql = "SELECT q.id
            FROM {question} q
            INNER JOIN {question_versions} qv ON qv.questionid = q.id
            INNER JOIN {question_bank_entries} qbe ON qbe.id = qv.questionbankentryid
            INNER JOIN {question_categories} qc ON qc.id = qbe.questioncategoryid
            JOIN {tag_instance} ti ON ti.itemid = q.id
            JOIN {tag} t ON t.id = ti.tagid
            WHERE LOWER(t.name) = :tagname
              AND qc.id = :categoryid
              AND ti.itemtype = 'question'
              AND q.qtype = 'multichoice'";
    
    $qids = $DB->get_fieldset_sql($sql, [
        'categoryid' => $categoryid,
        'tagname' => strtolower($tagname)
    ]);
    
    shuffle($qids);
    return array_slice($qids, 0, $limit);
}
```

## 测试你的 API

### 1. 通过 Moodle Web 服务测试客户端

1. 启用 Web 服务：**站点管理 > 高级功能**
2. 启用 REST 协议：**站点管理 > 插件 > Web 服务 > 管理协议**
3. 创建服务：**站点管理 > 服务器 > Web 服务 > 外部服务**
4. 测试函数：**站点管理 > 开发 > Web 服务测试客户端**

### 2. 通过 curl

```bash
# Get token first
curl -X POST "https://yourmoodle.com/login/token.php" \
  -d "username=admin" \
  -d "password=yourpassword" \
  -d "service=moodle_mobile_app"

# Call your API
curl -X POST "https://yourmoodle.com/webservice/rest/server.php" \
  -d "wstoken=YOUR_TOKEN" \
  -d "wsfunction=local_yourplugin_your_api_name" \
  -d "moodlewsrestformat=json" \
  -d "userid=2" \
  -d "courseid=3"
```

### 3. 通过 JavaScript (AJAX)

```javascript
require(['core/ajax'], function(ajax) {
    var promises = ajax.call([{
        methodname: 'local_yourplugin_your_api_name',
        args: {
            userid: 2,
            courseid: 3
        }
    }]);

    promises[0].done(function(response) {
        console.log('Success:', response);
    }).fail(function(error) {
        console.error('Error:', error);
    });
});
```

## 常见问题与解决方案

### 1. "Function not found" 错误
**解决方案**：
- 清除缓存：**站点管理 > 开发 > 清除所有缓存**
- 验证 services.php 中的函数名是否完全匹配
- 检查命名空间和类名是否正确

### 2. "Invalid parameter value detected"
**解决方案**：
- 确保参数类型在定义和使用之间匹配
- 检查必需参数与可选参数
- 验证嵌套结构定义

### 3. SQL 注入漏洞
**解决方案**：
- 始终使用占位符参数（`:paramname`）
- 永远不要将用户输入拼接到 SQL 字符串中
- 使用 Moodle 的数据库方法：`get_record()`、`get_records()` 等

### 4. 权限拒绝错误
**解决方案**：
- 在 execute() 中尽早调用 `self::validate_context($context)`
- 检查所需权限是否匹配用户的权限
- 验证用户在上下文中具有角色分配

### 5. 事务死锁
**解决方案**：
- 保持事务简短
- 始终在 finally 块中提交或回滚
- 避免嵌套事务

## 调试检查清单

- [ ] 检查 Moodle 调试模式：**站点管理 > 开发 > 调试**
- [ ] 查看 Web 服务日志：**站点管理 > 报告 > 日志**
- [ ] 检查 `$CFG->dataroot/local_yourplugin/` 中的自定义日志文件
- [ ] 使用 `$DB->set_debug(true)` 验证数据库查询
- [ ] 使用管理员用户测试以排除权限问题
- [ ] 清除浏览器缓存和 Moodle 缓存
- [ ] 检查服务器上的 PHP 错误日志

## 插件结构检查清单

```
local/yourplugin/
├── version.php                 # Plugin version and metadata
├── db/
│   ├── services.php           # External service definitions
│   └── access.php             # Capability definitions (optional)
├── classes/
│   └── external/
│       ├── your_api_name.php  # External API implementation
│       └── another_api.php    # Additional APIs
├── lang/
│   └── en/
│       └── local_yourplugin.php  # Language strings
└── tests/
    └── external_test.php      # Unit tests (optional but recommended)
```

## 实际实现示例

### 简单读取 API（获取测验尝试次数）

```php
<?php
namespace local_userlog\external;

defined('MOODLE_INTERNAL') || die();
require_once("$CFG->libdir/externallib.php");

use external_api;
use external_function_parameters;
use external_single_structure;
use external_value;

class get_quiz_attempts extends external_api {
    public static function execute_parameters() {
        return new external_function_parameters([
            'userid' => new external_value(PARAM_INT, 'User ID'),
            'courseid' => new external_value(PARAM_INT, 'Course ID')
        ]);
    }

    public static function execute($userid, $courseid) {
        global $DB;

        self::validate_parameters(self::execute_parameters(), [
            'userid' => $userid,
            'courseid' => $courseid
        ]);

        $sql = "SELECT COUNT(*) AS quiz_attempts
                FROM {quiz_attempts} qa
                JOIN {quiz} q ON qa.quiz = q.id
                WHERE qa.userid = :userid AND q.course = :courseid";

        $attempts = $DB->get_field_sql($sql, [
            'userid' => $userid,
            'courseid' => $courseid
        ]);

        return ['quiz_attempts' => (int)$attempts];
    }

    public static function execute_returns() {
        return new external_single_structure([
            'quiz_attempts' => new external_value(PARAM_INT, 'Total number of quiz attempts')
        ]);
    }
}
```

### 复杂写入 API（从分类创建测验）

参见附件 `create_quiz_from_categories.php`，其中包含完整的综合示例，涵盖：
- 多次数据库插入
- 课程模块创建
- 测验实例配置
- 使用标签随机选题
- 基于分组的访问限制
- 详细的错误日志记录
- 事务管理

## 快速参考：常用 Moodle 数据表

| 表名 | 用途 |
|------|------|
| `{user}` | 用户账户 |
| `{course}` | 课程 |
| `{course_modules}` | 课程中的活动实例 |
| `{modules}` | 可用的活动类型（测验、论坛等） |
| `{quiz}` | 测验配置 |
| `{quiz_attempts}` | 测验尝试记录 |
| `{question}` | 题库 |
| `{question_categories}` | 题目分类 |
| `{grade_items}` | 成绩册项目 |
| `{grade_grades}` | 学生成绩 |
| `{groups}` | 课程分组 |
| `{groups_members}` | 分组成员 |
| `{logstore_standard_log}` | 活动日志 |

## 扩展资源

- [Moodle 外部 API 文档](https://moodledev.io/docs/5.2/apis/subsystems/external/functions)
- [Moodle 编码规范](https://moodledev.io/general/development/policies/codingstyle)
- [Moodle 数据库 API](https://moodledev.io/docs/5.2/apis/core/dml)
- [Web 服务 API 文档](https://moodledev.io/docs/5.2/apis/subsystems/external)

## 准则

- 始终使用 `validate_parameters()` 验证输入参数
- 在操作前检查用户上下文和权限
- 使用参数化 SQL 查询（永远不要字符串拼接）
- 实现全面的错误处理和日志记录
- 遵循 Moodle 命名规范（小写、下划线）
- 清晰记录所有参数和返回值
- 使用不同的用户角色和权限进行测试
- 对写操作考虑事务安全性
- 服务注册更改后清除缓存
- 保持 API 方法专注且单一职责

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。