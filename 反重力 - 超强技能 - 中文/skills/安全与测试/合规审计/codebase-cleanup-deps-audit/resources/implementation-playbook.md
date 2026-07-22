# 依赖审计与安全分析实施手册

本文档包含技能引用的详细模式、检查清单和代码示例。

## 使用说明

### 1. 依赖发现

扫描并清点所有项目依赖：

**多语言检测**
```python
import os
import json
import toml
import yaml
from pathlib import Path

class DependencyDiscovery:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.dependency_files = {
            'npm': ['package.json', 'package-lock.json', 'yarn.lock'],
            'python': ['requirements.txt', 'Pipfile', 'Pipfile.lock', 'pyproject.toml', 'poetry.lock'],
            'ruby': ['Gemfile', 'Gemfile.lock'],
            'java': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
            'go': ['go.mod', 'go.sum'],
            'rust': ['Cargo.toml', 'Cargo.lock'],
            'php': ['composer.json', 'composer.lock'],
            'dotnet': ['*.csproj', 'packages.config', 'project.json']
        }
        
    def discover_all_dependencies(self):
        """
        发现不同包管理器中的所有依赖
        """
        dependencies = {}
        
        # NPM/Yarn 依赖
        if (self.project_path / 'package.json').exists():
            dependencies['npm'] = self._parse_npm_dependencies()
            
        # Python 依赖
        if (self.project_path / 'requirements.txt').exists():
            dependencies['python'] = self._parse_requirements_txt()
        elif (self.project_path / 'Pipfile').exists():
            dependencies['python'] = self._parse_pipfile()
        elif (self.project_path / 'pyproject.toml').exists():
            dependencies['python'] = self._parse_pyproject_toml()
            
        # Go 依赖
        if (self.project_path / 'go.mod').exists():
            dependencies['go'] = self._parse_go_mod()
            
        return dependencies
    
    def _parse_npm_dependencies(self):
        """
        解析 NPM package.json 和 lock 文件
        """
        with open(self.project_path / 'package.json', 'r') as f:
            package_json = json.load(f)
            
        deps = {}
        
        # 直接依赖
        for dep_type in ['dependencies', 'devDependencies', 'peerDependencies']:
            if dep_type in package_json:
                for name, version in package_json[dep_type].items():
                    deps[name] = {
                        'version': version,
                        'type': dep_type,
                        'direct': True
                    }
        
        # 解析 lock 文件获取精确版本
        if (self.project_path / 'package-lock.json').exists():
            with open(self.project_path / 'package-lock.json', 'r') as f:
                lock_data = json.load(f)
                self._parse_npm_lock(lock_data, deps)
                
        return deps
```

**依赖树分析**
```python
def build_dependency_tree(dependencies):
    """
    构建包含传递依赖的完整依赖树
    """
    tree = {
        'root': {
            'name': 'project',
            'version': '1.0.0',
            'dependencies': {}
        }
    }
    
    def add_dependencies(node, deps, visited=None):
        if visited is None:
            visited = set()
            
        for dep_name, dep_info in deps.items():
            if dep_name in visited:
                # 检测到循环依赖
                node['dependencies'][dep_name] = {
                    'circular': True,
                    'version': dep_info['version']
                }
                continue
                
            visited.add(dep_name)
            
            node['dependencies'][dep_name] = {
                'version': dep_info['version'],
                'type': dep_info.get('type', 'runtime'),
                'dependencies': {}
            }
            
            # 递归添加传递依赖
            if 'dependencies' in dep_info:
                add_dependencies(
                    node['dependencies'][dep_name],
                    dep_info['dependencies'],
                    visited.copy()
                )
    
    add_dependencies(tree['root'], dependencies)
    return tree
```

### 2. 漏洞扫描

检查依赖是否存在于漏洞数据库中：

**CVE 数据库检查**
```python
import requests
from datetime import datetime

class VulnerabilityScanner:
    def __init__(self):
        self.vulnerability_apis = {
            'npm': 'https://registry.npmjs.org/-/npm/v1/security/advisories/bulk',
            'pypi': 'https://pypi.org/pypi/{package}/json',
            'rubygems': 'https://rubygems.org/api/v1/gems/{package}.json',
            'maven': 'https://ossindex.sonatype.org/api/v3/component-report'
        }
        
    def scan_vulnerabilities(self, dependencies):
        """
        扫描依赖中的已知漏洞
        """
        vulnerabilities = []
        
        for package_name, package_info in dependencies.items():
            vulns = self._check_package_vulnerabilities(
                package_name,
                package_info['version'],
                package_info.get('ecosystem', 'npm')
            )
            
            if vulns:
                vulnerabilities.extend(vulns)
                
        return self._analyze_vulnerabilities(vulnerabilities)
    
    def _check_package_vulnerabilities(self, name, version, ecosystem):
        """
        检查特定包的漏洞
        """
        if ecosystem == 'npm':
            return self._check_npm_vulnerabilities(name, version)
        elif ecosystem == 'pypi':
            return self._check_python_vulnerabilities(name, version)
        elif ecosystem == 'maven':
            return self._check_java_vulnerabilities(name, version)
            
    def _check_npm_vulnerabilities(self, name, version):
        """
        检查 NPM 包漏洞
        """
        # 使用 npm audit API
        response = requests.post(
            'https://registry.npmjs.org/-/npm/v1/security/advisories/bulk',
            json={name: [version]}
        )
        
        vulnerabilities = []
        if response.status_code == 200:
            data = response.json()
            if name in data:
                for advisory in data[name]:
                    vulnerabilities.append({
                        'package': name,
                        'version': version,
                        'severity': advisory['severity'],
                        'title': advisory['title'],
                        'cve': advisory.get('cves', []),
                        'description': advisory['overview'],
                        'recommendation': advisory['recommendation'],
                        'patched_versions': advisory['patched_versions'],
                        'published': advisory['created']
                    })
                    
        return vulnerabilities
```

**严重性分析**
```python
def analyze_vulnerability_severity(vulnerabilities):
    """
    按严重性分析和优先排序漏洞
    """
    severity_scores = {
        'critical': 9.0,
        'high': 7.0,
        'moderate': 4.0,
        'low': 1.0
    }
    
    analysis = {
        'total': len(vulnerabilities),
        'by_severity': {
            'critical': [],
            'high': [],
            'moderate': [],
            'low': []
        },
        'risk_score': 0,
        'immediate_action_required': []
    }
    
    for vuln in vulnerabilities:
        severity = vuln['severity'].lower()
        analysis['by_severity'][severity].append(vuln)
        
        # 计算风险分数
        base_score = severity_scores.get(severity, 0)
        
        # 根据因素调整分数
        if vuln.get('exploit_available', False):
            base_score *= 1.5
        if vuln.get('publicly_disclosed', True):
            base_score *= 1.2
        if 'remote_code_execution' in vuln.get('description', '').lower():
            base_score *= 2.0
            
        vuln['risk_score'] = base_score
        analysis['risk_score'] += base_score
        
        # 标记需要立即处理的项目
        if severity in ['critical', 'high'] or base_score > 8.0:
            analysis['immediate_action_required'].append({
                'package': vuln['package'],
                'severity': severity,
                'action': f"更新到 {vuln['patched_versions']}"
            })
    
    # 按风险分数排序
    for severity in analysis['by_severity']:
        analysis['by_severity'][severity].sort(
            key=lambda x: x.get('risk_score', 0),
            reverse=True
        )
    
    return analysis
```

### 3. 许可证合规

分析依赖许可证的兼容性：

**许可证检测**
```python
class LicenseAnalyzer:
    def __init__(self):
        self.license_compatibility = {
            'MIT': ['MIT', 'BSD', 'Apache-2.0', 'ISC'],
            'Apache-2.0': ['Apache-2.0', 'MIT', 'BSD'],
            'GPL-3.0': ['GPL-3.0', 'GPL-2.0'],
            'BSD-3-Clause': ['BSD-3-Clause', 'MIT', 'Apache-2.0'],
            'proprietary': []
        }
        
        self.license_restrictions = {
            'GPL-3.0': 'Copyleft - 需要公开源代码',
            'AGPL-3.0': '强 Copyleft - 网络使用需要公开源代码',
            'proprietary': '未经明确许可不得使用',
            'unknown': '许可证不明确 - 需要法务审查'
        }
        
    def analyze_licenses(self, dependencies, project_license='MIT'):
        """
        分析许可证兼容性
        """
        issues = []
        license_summary = {}
        
        for package_name, package_info in dependencies.items():
            license_type = package_info.get('license', 'unknown')
            
            # 跟踪许可证使用情况
            if license_type not in license_summary:
                license_summary[license_type] = []
            license_summary[license_type].append(package_name)
            
            # 检查兼容性
            if not self._is_compatible(project_license, license_type):
                issues.append({
                    'package': package_name,
                    'license': license_type,
                    'issue': f'与项目许可证 {project_license} 不兼容',
                    'severity': 'high',
                    'recommendation': self._get_license_recommendation(
                        license_type,
                        project_license
                    )
                })
            
            # 检查限制性许可证
            if license_type in self.license_restrictions:
                issues.append({
                    'package': package_name,
                    'license': license_type,
                    'issue': self.license_restrictions[license_type],
                    'severity': 'medium',
                    'recommendation': '审查使用情况并确保合规'
                })
        
        return {
            'summary': license_summary,
            'issues': issues,
            'compliance_status': 'FAIL' if issues else 'PASS'
        }
```

**许可证报告**
```markdown
## 许可证合规报告

### 摘要
- **项目许可证**: MIT
- **依赖总数**: 245
- **许可证问题**: 3
- **合规状态**: ⚠️ 需要审查

### 许可证分布
| 许可证 | 数量 | 包 |
|---------|-------|----------|
| MIT | 180 | express, lodash, ... |
| Apache-2.0 | 45 | aws-sdk, ... |
| BSD-3-Clause | 15 | ... |
| GPL-3.0 | 3 | [问题] package1, package2, package3 |
| Unknown | 2 | [问题] mystery-lib, old-package |

### 合规问题

#### 高严重性
1. **GPL-3.0 依赖**
   - 包: package1, package2, package3
   - 问题: GPL-3.0 与 MIT 许可证不兼容
   - 风险: 可能需要开源整个项目
   - 建议: 
     - 用 MIT/Apache 许可的替代品替换
     - 或将项目许可证改为 GPL-3.0

#### 中等严重性
2. **未知许可证**
   - 包: mystery-lib, old-package
   - 问题: 无法确定许可证兼容性
   - 风险: 潜在法律风险
   - 建议:
     - 联系包维护者
     - 审查源代码中的许可证信息
     - 考虑用已知替代品替换
```

### 4. 过时依赖

识别并优先处理依赖更新：

**版本分析**
```python
def analyze_outdated_dependencies(dependencies):
    """
    检查过时的依赖
    """
    outdated = []
    
    for package_name, package_info in dependencies.items():
        current_version = package_info['version']
        latest_version = fetch_latest_version(package_name, package_info['ecosystem'])
        
        if is_outdated(current_version, latest_version):
            # 计算落后程度
            version_diff = calculate_version_difference(current_version, latest_version)
            
            outdated.append({
                'package': package_name,
                'current': current_version,
                'latest': latest_version,
                'type': version_diff['type'],  # major, minor, patch
                'releases_behind': version_diff['count'],
                'age_days': get_version_age(package_name, current_version),
                'breaking_changes': version_diff['type'] == 'major',
                'update_effort': estimate_update_effort(version_diff),
                'changelog': fetch_changelog(package_name, current_version, latest_version)
            })
    
    return prioritize_updates(outdated)

def prioritize_updates(outdated_deps):
    """
    基于多个因素优先排序更新
    """
    for dep in outdated_deps:
        score = 0
        
        # 安全更新获得最高优先级
        if dep.get('has_security_fix', False):
            score += 100
            
        # 主版本更新
        if dep['type'] == 'major':
            score += 20
        elif dep['type'] == 'minor':
            score += 10
        else:
            score += 5
            
        # 时间因素
        if dep['age_days'] > 365:
            score += 30
        elif dep['age_days'] > 180:
            score += 20
        elif dep['age_days'] > 90:
            score += 10
            
        # 落后版本数量
        score += min(dep['releases_behind'] * 2, 20)
        
        dep['priority_score'] = score
        dep['priority'] = 'critical' if score > 80 else 'high' if score > 50 else 'medium'
    
    return sorted(outdated_deps, key=lambda x: x['priority_score'], reverse=True)
```

### 5. 依赖大小分析

分析包大小影响：

**包大小影响**
```javascript
// 分析 NPM 包大小
const analyzeBundleSize = async (dependencies) => {
    const sizeAnalysis = {
        totalSize: 0,
        totalGzipped: 0,
        packages: [],
        recommendations: []
    };
    
    for (const [packageName, info] of Object.entries(dependencies)) {
        try {
            // 获取包统计信息
            const response = await fetch(
                `https://bundlephobia.com/api/size?package=${packageName}@${info.version}`
            );
            const data = await response.json();
            
            const packageSize = {
                name: packageName,
                version: info.version,
                size: data.size,
                gzip: data.gzip,
                dependencyCount: data.dependencyCount,
                hasJSNext: data.hasJSNext,
                hasSideEffects: data.hasSideEffects
            };
            
            sizeAnalysis.packages.push(packageSize);
            sizeAnalysis.totalSize += data.size;
            sizeAnalysis.totalGzipped += data.gzip;
            
            // 大小建议
            if (data.size > 1000000) { // 1MB
                sizeAnalysis.recommendations.push({
                    package: packageName,
                    issue: '包体积过大',
                    size: `${(data.size / 1024 / 1024).toFixed(2)} MB`,
                    suggestion: '考虑使用更轻量的替代品或懒加载'
                });
            }
        } catch (error) {
            console.error(`分析 ${packageName} 失败:`, error);
        }
    }
    
    // 按大小排序
    sizeAnalysis.packages.sort((a, b) => b.size - a.size);
    
    // 添加主要问题包
    sizeAnalysis.topOffenders = sizeAnalysis.packages.slice(0, 10);
    
    return sizeAnalysis;
};
```

### 6. 供应链安全

检查依赖劫持和拼写错误攻击：

**供应链检查**
```python
def check_supply_chain_security(dependencies):
    """
    执行供应链安全检查
    """
    security_issues = []
    
    for package_name, package_info in dependencies.items():
        # 检查拼写错误攻击
        typo_check = check_typosquatting(package_name)
        if typo_check['suspicious']:
            security_issues.append({
                'type': 'typosquatting',
                'package': package_name,
                'severity': 'high',
                'similar_to': typo_check['similar_packages'],
                'recommendation': '验证包名称拼写'
            })
        
        # 检查维护者变更
        maintainer_check = check_maintainer_changes(package_name)
        if maintainer_check['recent_changes']:
            security_issues.append({
                'type': 'maintainer_change',
                'package': package_name,
                'severity': 'medium',
                'details': maintainer_check['changes'],
                'recommendation': '审查最近的包变更'
            })
        
        # 检查可疑模式
        if contains_suspicious_patterns(package_info):
            security_issues.append({
                'type': 'suspicious_behavior',
                'package': package_name,
                'severity': 'high',
                'patterns': package_info['suspicious_patterns'],
                'recommendation': '审计包源代码'
            })
    
    return security_issues

def check_typosquatting(package_name):
    """
    检查包名是否可能是拼写错误攻击
    """
    common_packages = [
        'react', 'express', 'lodash', 'axios', 'webpack',
        'babel', 'jest', 'typescript', 'eslint', 'prettier'
    ]
    
    for legit_package in common_packages:
        distance = levenshtein_distance(package_name.lower(), legit_package)
        if 0 < distance <= 2:  # 接近但不完全匹配
            return {
                'suspicious': True,
                'similar_packages': [legit_package],
                'distance': distance
            }
    
    return {'suspicious': False}
```

### 7. 自动化修复

生成自动化修复：

**更新脚本**
```bash
#!/bin/bash
# 自动更新带有安全修复的依赖

echo "🔒 安全更新脚本"
echo "========================"

# NPM/Yarn 更新
if [ -f "package.json" ]; then
    echo "📦 更新 NPM 依赖..."
    
    # 审计并自动修复
    npm audit fix --force
    
    # 更新特定有漏洞的包
    npm update package1@^2.0.0 package2@~3.1.0
    
    # 运行测试
    npm test
    
    if [ $? -eq 0 ]; then
        echo "✅ NPM 更新成功"
    else
        echo "❌ 测试失败，回滚..."
        git checkout package-lock.json
    fi
fi

# Python 更新
if [ -f "requirements.txt" ]; then
    echo "🐍 更新 Python 依赖..."
    
    # 创建备份
    cp requirements.txt requirements.txt.backup
    
    # 更新有漏洞的包
    pip-compile --upgrade-package package1 --upgrade-package package2
    
    # 测试安装
    pip install -r requirements.txt --dry-run
    
    if [ $? -eq 0 ]; then
        echo "✅ Python 更新成功"
    else
        echo "❌ 更新失败，回滚..."
        mv requirements.txt.backup requirements.txt
    fi
fi
```

**Pull Request 生成**
```python
def generate_dependency_update_pr(updates):
    """
    生成带有依赖更新的 PR
    """
    pr_body = f"""
## 🔒 依赖安全更新

此 PR 更新了 {len(updates)} 个依赖，以解决安全漏洞和过时的包。

### 安全修复 ({sum(1 for u in updates if u['has_security'])})

| 包 | 当前版本 | 更新版本 | 严重性 | CVE |
|---------|---------|---------|----------|-----|
"""
    
    for update in updates:
        if update['has_security']:
            pr_body += f"| {update['package']} | {update['current']} | {update['target']} | {update['severity']} | {', '.join(update['cves'])} |\n"
    
    pr_body += """

### 其他更新

| 包 | 当前版本 | 更新版本 | 类型 | 时间 |
|---------|---------|---------|------|-----|
"""
    
    for update in updates:
        if not update['has_security']:
            pr_body += f"| {update['package']} | {update['current']} | {update['target']} | {update['type']} | {update['age_days']} 天 |\n"
    
    pr_body += """

### 测试
- [ ] 所有测试通过
- [ ] 未发现破坏性变更
- [ ] 已审查包大小影响

### 审查清单
- [ ] 已解决安全漏洞
- [ ] 已维护许可证合规
- [ ] 未添加意外依赖
- [ ] 已评估性能影响

cc @security-team
"""
    
    return {
        'title': f'chore(deps): 安全更新 {len(updates)} 个依赖',
        'body': pr_body,
        'branch': f'deps/security-update-{datetime.now().strftime("%Y%m%d")}',
        'labels': ['dependencies', 'security']
    }
```

### 8. 监控和告警

设置持续依赖监控：

**GitHub Actions 工作流**
```yaml
name: Dependency Audit

on:
  schedule:
    - cron: '0 0 * * *'  # 每日
  push:
    paths:
      - 'package*.json'
      - 'requirements.txt'
      - 'Gemfile*'
      - 'go.mod'
  workflow_dispatch:

jobs:
  security-audit:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run NPM Audit
      if: hashFiles('package.json')
      run: |
        npm audit --json > npm-audit.json
        if [ $(jq '.vulnerabilities.total' npm-audit.json) -gt 0 ]; then
          echo "::error::发现 $(jq '.vulnerabilities.total' npm-audit.json) 个漏洞"
          exit 1
        fi
    
    - name: Run Python Safety Check
      if: hashFiles('requirements.txt')
      run: |
        pip install safety
        safety check --json > safety-report.json
        
    - name: Check Licenses
      run: |
        npx license-checker --json > licenses.json
        python scripts/check_license_compliance.py
    
    - name: Create Issue for Critical Vulnerabilities
      if: failure()
      uses: actions/github-script@v6
      with:
        script: |
          const audit = require('./npm-audit.json');
          const critical = audit.vulnerabilities.critical;
          
          if (critical > 0) {
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `🚨 发现 ${critical} 个严重漏洞`,
              body: '依赖审计发现严重漏洞。详见工作流运行详情。',
              labels: ['security', 'dependencies', 'critical']
            });
          }
```

## 输出格式

1. **执行摘要**: 高层次风险评估和行动项目
2. **漏洞报告**: 带严重性评级的详细 CVE 分析
3. **许可证合规**: 兼容性矩阵和法律风险
4. **更新建议**: 带工作量估算的优先排序列表
5. **供应链分析**: 拼写错误攻击和劫持风险
6. **修复脚本**: 自动化更新命令和 PR 生成
7. **大小影响报告**: 包大小分析和优化技巧
8. **监控设置**: 持续扫描的 CI/CD 集成

重点关注可操作的洞察，帮助维护安全、合规和高效的依赖管理。
