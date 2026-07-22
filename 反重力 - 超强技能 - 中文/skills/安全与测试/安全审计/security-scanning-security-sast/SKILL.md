---
name: security-scanning-security-sast
description: '静态应用安全测试（SAST），用于跨多种语言和框架的代码漏洞分析。触发词：SAST、静态安全测试、代码漏洞分析、安全扫描、代码安全、漏洞检测、安全测试'
risk: unknown
source: community
date_added: '2026-02-27'
---
# SAST 安全插件

静态应用安全测试（SAST），用于跨多种语言、框架和安全模式的综合代码漏洞检测。

## 功能特性

- **多语言 SAST**：Python、JavaScript/TypeScript、Java、Ruby、PHP、Go、Rust
- **工具集成**：Bandit、Semgrep、ESLint Security、SonarQube、CodeQL、PMD、SpotBugs、Brakeman、gosec、cargo-clippy
- **漏洞模式**：SQL 注入、XSS、硬编码密钥、路径遍历、IDOR、CSRF、不安全的反序列化
- **框架分析**：Django、Flask、React、Express、Spring Boot、Rails、Laravel
- **自定义规则编写**：为组织特定安全策略开发 Semgrep 模式

## 使用场景

用于代码审查安全分析、注入漏洞、硬编码密钥、框架特定模式、自定义安全策略执行、部署前验证、遗留代码评估以及合规性检查（OWASP、PCI-DSS、SOC2）。

**专用工具**：使用 `security-secrets.md` 进行高级凭证扫描，使用 `security-owasp.md` 进行 Top 10 映射，使用 `security-api.md` 测试 REST/GraphQL 端点。

## 不适用场景

- 只需要运行时测试或渗透测试
- 无法访问源代码或构建输出
- 环境禁止使用第三方扫描工具

## 使用说明

1. 识别要扫描的语言、框架和范围。
2. 选择 SAST 工具并为代码库配置规则。
3. 在 CI 或本地使用可重现的设置运行扫描。
4. 分类发现结果，按严重性优先排序，并提出修复建议。

## 安全注意事项

- 未经批准，避免将专有代码上传到外部服务。
- 启用自动修复或阻止发布前需要审查。

## SAST 工具选择

### Python：Bandit

```bash
# 安装与扫描
pip install bandit
bandit -r . -f json -o bandit-report.json
bandit -r . -ll -ii -f json  # 仅高危/严重
```

**配置**：`.bandit`
```yaml
exclude_dirs: ['/tests/', '/venv/', '/.tox/', '/build/']
tests: [B201, B301, B302, B303, B304, B305, B307, B308, B312, B323, B324, B501, B502, B506, B602, B608]
skips: [B101]
```

### JavaScript/TypeScript：ESLint Security

```bash
npm install --save-dev eslint @eslint/plugin-security eslint-plugin-no-secrets
eslint . --ext .js,.jsx,.ts,.tsx --format json > eslint-security.json
```

**配置**：`.eslintrc-security.json`
```json
{
  "plugins": ["@eslint/plugin-security", "eslint-plugin-no-secrets"],
  "extends": ["plugin:security/recommended"],
  "rules": {
    "security/detect-object-injection": "error",
    "security/detect-non-literal-fs-filename": "error",
    "security/detect-eval-with-expression": "error",
    "security/detect-pseudo-random-prng": "error",
    "no-secrets/no-secrets": "error"
  }
}
```

### 多语言：Semgrep

```bash
pip install semgrep
semgrep --config=auto --json --output=semgrep-report.json
semgrep --config=p/security-audit --json
semgrep --config=p/owasp-top-ten --json
semgrep ci --config=auto  # CI 模式
```

**自定义规则**：`.semgrep.yml`
```yaml
rules:
  - id: sql-injection-format-string
    pattern: cursor.execute("... %s ..." % $VAR)
    message: 通过字符串格式化进行 SQL 注入
    severity: ERROR
    languages: [python]
    metadata:
      cwe: "CWE-89"
      owasp: "A03:2021-Injection"

  - id: dangerous-innerHTML
    pattern: $ELEM.innerHTML = $VAR
    message: 通过 innerHTML 赋值进行 XSS 攻击
    severity: ERROR
    languages: [javascript, typescript]
    metadata:
      cwe: "CWE-79"

  - id: hardcoded-aws-credentials
    patterns:
      - pattern: $KEY = "AKIA..."
      - metavariable-regex:
          metavariable: $KEY
          regex: "(aws_access_key_id|AWS_ACCESS_KEY_ID)"
    message: 检测到硬编码的 AWS 凭证
    severity: ERROR
    languages: [python, javascript, java]

  - id: path-traversal-open
    patterns:
      - pattern: open($PATH, ...)
      - pattern-not: open(os.path.join(SAFE_DIR, ...), ...)
      - metavariable-pattern:
          metavariable: $PATH
          patterns:
            - pattern: $REQ.get(...)
    message: 通过用户输入进行路径遍历
    severity: ERROR
    languages: [python]

  - id: command-injection
    patterns:
      - pattern-either:
          - pattern: os.system($CMD)
          - pattern: subprocess.call($CMD, shell=True)
      - metavariable-pattern:
          metavariable: $CMD
          patterns:
            - pattern-either:
                - pattern: $X + $Y
                - pattern: f"...{$VAR}..."
    message: 通过 shell=True 进行命令注入
    severity: ERROR
    languages: [python]
```

### 其他语言工具

**Java**：`mvn spotbugs:check`
**Ruby**：`brakeman -o report.json -f json`
**Go**：`gosec -fmt=json -out=gosec.json ./...`
**Rust**：`cargo clippy -- -W clippy::unwrap_used`

## 漏洞模式

### SQL 注入

**漏洞**：在 SQL 查询中使用用户输入进行字符串格式化/拼接

**安全**：
```python
# 参数化查询
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
User.objects.filter(id=user_id)  # ORM
```

### 跨站脚本（XSS）

**漏洞**：直接操作 HTML 且未清理用户输入（innerHTML、outerHTML、document.write）

**安全**：
```javascript
// 使用 textContent 显示纯文本
element.textContent = userInput;

// React 自动转义
<div>{userInput}</div>

// 需要 HTML 时进行清理
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 硬编码密钥

**漏洞**：在源代码中硬编码 API 密钥、密码、令牌

**安全**：
```python
import os
API_KEY = os.environ.get('API_KEY')
PASSWORD = os.getenv('DB_PASSWORD')
```

### 路径遍历

**漏洞**：使用未清理的用户输入打开文件

**安全**：
```python
import os
ALLOWED_DIR = '/var/www/uploads'
file_name = request.args.get('file')
file_path = os.path.join(ALLOWED_DIR, file_name)
file_path = os.path.realpath(file_path)
if not file_path.startswith(os.path.realpath(ALLOWED_DIR)):
    raise ValueError("Invalid file path")
with open(file_path, 'r') as f:
    content = f.read()
```

### 不安全的反序列化

**漏洞**：对不可信数据使用 pickle.loads()、yaml.load()

**安全**：
```python
import json
data = json.loads(user_input)  # 安全
import yaml
config = yaml.safe_load(user_input)  # 安全
```

### 命令注入

**漏洞**：使用 os.system() 或 subprocess 且 shell=True 和用户输入

**安全**：
```python
subprocess.run(['ping', '-c', '4', user_input])  # 数组参数
import shlex
safe_input = shlex.quote(user_input)  # 输入验证
```

### 不安全的随机数

**漏洞**：在安全关键操作中使用 random 模块

**安全**：
```python
import secrets
token = secrets.token_hex(16)
session_id = secrets.token_urlsafe(32)
```

## 框架安全

### Django

**漏洞**：@csrf_exempt、DEBUG=True、弱 SECRET_KEY、缺少安全中间件

**安全**：
```python
# settings.py
DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
```

### Flask

**漏洞**：debug=True、弱 secret_key、CORS 通配符

**安全**：
```python
import os
from flask_talisman import Talisman

app.secret_key = os.environ.get('FLASK_SECRET_KEY')
Talisman(app, force_https=True)
CORS(app, origins=['https://example.com'])
```

### Express.js

**漏洞**：缺少 helmet、CORS 通配符、无速率限制

**安全**：
```javascript
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

app.use(helmet());
app.use(cors({ origin: 'https://example.com' }));
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));
```

## 多语言扫描器实现

```python
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SASTFinding:
    tool: str
    severity: str
    category: str
    title: str
    description: str
    file_path: str
    line_number: int
    cwe: str
    owasp: str
    confidence: str

class MultiLanguageSASTScanner:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.findings: List[SASTFinding] = []

    def detect_languages(self) -> List[str]:
        """自动检测语言"""
        languages = []
        indicators = {
            'python': ['*.py', 'requirements.txt'],
            'javascript': ['*.js', 'package.json'],
            'typescript': ['*.ts', 'tsconfig.json'],
            'java': ['*.java', 'pom.xml'],
            'ruby': ['*.rb', 'Gemfile'],
            'go': ['*.go', 'go.mod'],
            'rust': ['*.rs', 'Cargo.toml'],
        }
        for lang, patterns in indicators.items():
            for pattern in patterns:
                if list(self.project_path.glob(f'**/{pattern}')):
                    languages.append(lang)
                    break
        return languages

    def run_comprehensive_sast(self) -> Dict[str, Any]:
        """执行所有适用的 SAST 工具"""
        languages = self.detect_languages()

        scan_results = {
            'timestamp': datetime.now().isoformat(),
            'languages': languages,
            'tools_executed': [],
            'findings': []
        }

        self.run_semgrep_scan()
        scan_results['tools_executed'].append('semgrep')

        if 'python' in languages:
            self.run_bandit_scan()
            scan_results['tools_executed'].append('bandit')
        if 'javascript' in languages or 'typescript' in languages:
            self.run_eslint_security_scan()
            scan_results['tools_executed'].append('eslint-security')

        scan_results['findings'] = [vars(f) for f in self.findings]
        scan_results['summary'] = self.generate_summary()
        return scan_results

    def run_semgrep_scan(self):
        """运行 Semgrep"""
        for ruleset in ['auto', 'p/security-audit', 'p/owasp-top-ten']:
            try:
                result = subprocess.run([
                    'semgrep', '--config', ruleset, '--json', '--quiet',
                    str(self.project_path)
                ], capture_output=True, text=True, timeout=300)

                if result.stdout:
                    data = json.loads(result.stdout)
                    for f in data.get('results', []):
                        self.findings.append(SASTFinding(
                            tool='semgrep',
                            severity=f.get('extra', {}).get('severity', 'MEDIUM').upper(),
                            category='sast',
                            title=f.get('check_id', ''),
                            description=f.get('extra', {}).get('message', ''),
                            file_path=f.get('path', ''),
                            line_number=f.get('start', {}).get('line', 0),
                            cwe=f.get('extra', {}).get('metadata', {}).get('cwe', ''),
                            owasp=f.get('extra', {}).get('metadata', {}).get('owasp', ''),
                            confidence=f.get('extra', {}).get('metadata', {}).get('confidence', 'MEDIUM')
                        ))
            except Exception as e:
                print(f"Semgrep {ruleset} 失败: {e}")

    def generate_summary(self) -> Dict[str, Any]:
        """生成统计信息"""
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for f in self.findings:
            severity_counts[f.severity] = severity_counts.get(f.severity, 0) + 1

        return {
            'total_findings': len(self.findings),
            'severity_breakdown': severity_counts,
            'risk_score': self.calculate_risk_score(severity_counts)
        }

    def calculate_risk_score(self, severity_counts: Dict[str, int]) -> int:
        """风险评分 0-100"""
        weights = {'CRITICAL': 10, 'HIGH': 7, 'MEDIUM': 4, 'LOW': 1}
        total = sum(weights[s] * c for s, c in severity_counts.items())
        return min(100, int((total / 50) * 100))
```

## CI/CD 集成

### GitHub Actions

```yaml
name: SAST Scan
on:
  pull_request:
    branches: [main]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: 安装工具
        run: |
          pip install bandit semgrep
          npm install -g eslint @eslint/plugin-security

      - name: 运行扫描
        run: |
          bandit -r . -f json -o bandit.json || true
          semgrep --config=auto --json --output=semgrep.json || true

      - name: 上传报告
        uses: actions/upload-artifact@v3
        with:
          name: sast-reports
          path: |
            bandit.json
            semgrep.json
```

### GitLab CI

```yaml
sast:
  stage: test
  image: python:3.11
  script:
    - pip install bandit semgrep
    - bandit -r . -f json -o bandit.json || true
    - semgrep --config=auto --json --output=semgrep.json || true
  artifacts:
    reports:
      sast: bandit.json
```

## 最佳实践

1. **尽早且频繁运行** - 预提交钩子和 CI/CD
2. **组合多种工具** - 不同工具捕获不同漏洞
3. **调整误报** - 配置排除项和阈值
4. **优先处理发现** - 首先关注严重/高危
5. **框架感知扫描** - 使用特定规则集
6. **自定义规则** - 组织特定模式
7. **开发者培训** - 安全编码实践
8. **增量修复** - 逐步修复
9. **基线管理** - 跟踪已知问题
10. **定期更新** - 保持工具最新

## 相关工具

- **security-secrets.md** - 高级凭证检测
- **security-owasp.md** - OWASP Top 10 评估
- **security-api.md** - API 安全测试
- **security-scan.md** - 综合安全扫描

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。