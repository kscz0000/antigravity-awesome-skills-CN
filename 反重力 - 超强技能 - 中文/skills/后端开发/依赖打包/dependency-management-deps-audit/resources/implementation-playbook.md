# 依赖审计与安全分析实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

## 指令

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
        Discover all dependencies across different package managers
        """
        dependencies = {}
        
        # NPM/Yarn dependencies
        if (self.project_path / 'package.json').exists():
            dependencies['npm'] = self._parse_npm_dependencies()
            
        # Python dependencies
        if (self.project_path / 'requirements.txt').exists():
            dependencies['python'] = self._parse_requirements_txt()
        elif (self.project_path / 'Pipfile').exists():
            dependencies['python'] = self._parse_pipfile()
        elif (self.project_path / 'pyproject.toml').exists():
            dependencies['python'] = self._parse_pyproject_toml()
            
        # Go dependencies
        if (self.project_path / 'go.mod').exists():
            dependencies['go'] = self._parse_go_mod()
            
        return dependencies
    
    def _parse_npm_dependencies(self):
        """
        Parse NPM package.json and lock files
        """
        with open(self.project_path / 'package.json', 'r') as f:
            package_json = json.load(f)
            
        deps = {}
        
        # Direct dependencies
        for dep_type in ['dependencies', 'devDependencies', 'peerDependencies']:
            if dep_type in package_json:
                for name, version in package_json[dep_type].items():
                    deps[name] = {
                        'version': version,
                        'type': dep_type,
                        'direct': True
                    }
        
        # Parse lock file for exact versions
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
    Build complete dependency tree including transitive dependencies
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
                # Circular dependency detected
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
            
            # Recursively add transitive dependencies
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

对照漏洞数据库检查依赖：

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
        Scan dependencies for known vulnerabilities
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
        Check specific package for vulnerabilities
        """
        if ecosystem == 'npm':
            return self._check_npm_vulnerabilities(name, version)
        elif ecosystem == 'pypi':
            return self._check_python_vulnerabilities(name, version)
        elif ecosystem == 'maven':
            return self._check_java_vulnerabilities(name, version)
            
    def _check_npm_vulnerabilities(self, name, version):
        """
        Check NPM package vulnerabilities
        """
        # Using npm audit API
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

**严重程度分析**
```python
def analyze_vulnerability_severity(vulnerabilities):
    """
    Analyze and prioritize vulnerabilities by severity
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
        
        # Calculate risk score
        base_score = severity_scores.get(severity, 0)
        
        # Adjust score based on factors
        if vuln.get('exploit_available', False):
            base_score *= 1.5
        if vuln.get('publicly_disclosed', True):
            base_score *= 1.2
        if 'remote_code_execution' in vuln.get('description', '').lower():
            base_score *= 2.0
            
        vuln['risk_score'] = base_score
        analysis['risk_score'] += base_score
        
        # Flag immediate action items
        if severity in ['critical', 'high'] or base_score > 8.0:
            analysis['immediate_action_required'].append({
                'package': vuln['package'],
                'severity': severity,
                'action': f"Update to {vuln['patched_versions']}"
            })
    
    # Sort by risk score
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
            'GPL-3.0': 'Copyleft - requires source code disclosure',
            'AGPL-3.0': 'Strong copyleft - network use requires source disclosure',
            'proprietary': 'Cannot be used without explicit license',
            'unknown': 'License unclear - legal review required'
        }
        
    def analyze_licenses(self, dependencies, project_license='MIT'):
        """
        Analyze license compatibility
        """
        issues = []
        license_summary = {}
        
        for package_name, package_info in dependencies.items():
            license_type = package_info.get('license', 'unknown')
            
            # Track license usage
            if license_type not in license_summary:
                license_summary[license_type] = []
            license_summary[license_type].append(package_name)
            
            # Check compatibility
            if not self._is_compatible(project_license, license_type):
                issues.append({
                    'package': package_name,
                    'license': license_type,
                    'issue': f'Incompatible with project license {project_license}',
                    'severity': 'high',
                    'recommendation': self._get_license_recommendation(
                        license_type,
                        project_license
                    )
                })
            
            # Check for restrictive licenses
            if license_type in self.license_restrictions:
                issues.append({
                    'package': package_name,
                    'license': license_type,
                    'issue': self.license_restrictions[license_type],
                    'severity': 'medium',
                    'recommendation': 'Review usage and ensure compliance'
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

### 概要
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

#### 高严重程度
1. **GPL-3.0 依赖**
   - 包: package1, package2, package3
   - 问题: GPL-3.0 与 MIT 许可证不兼容
   - 风险: 可能需要开源你的整个项目
   - 建议: 
     - 替换为 MIT/Apache 许可的替代方案
     - 或将项目许可证更改为 GPL-3.0

#### 中严重程度
2. **未知许可证**
   - 包: mystery-lib, old-package
   - 问题: 无法确定许可证兼容性
   - 风险: 潜在的法律风险
   - 建议:
     - 联系包维护者
     - 审查源代码中的许可证信息
     - 考虑替换为已知许可证的替代方案
```

### 4. 过时依赖

识别并优先处理依赖更新：

**版本分析**
```python
def analyze_outdated_dependencies(dependencies):
    """
    Check for outdated dependencies
    """
    outdated = []
    
    for package_name, package_info in dependencies.items():
        current_version = package_info['version']
        latest_version = fetch_latest_version(package_name, package_info['ecosystem'])
        
        if is_outdated(current_version, latest_version):
            # Calculate how outdated
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
    Prioritize updates based on multiple factors
    """
    for dep in outdated_deps:
        score = 0
        
        # Security updates get highest priority
        if dep.get('has_security_fix', False):
            score += 100
            
        # Major version updates
        if dep['type'] == 'major':
            score += 20
        elif dep['type'] == 'minor':
            score += 10
        else:
            score += 5
            
        # Age factor
        if dep['age_days'] > 365:
            score += 30
        elif dep['age_days'] > 180:
            score += 20
        elif dep['age_days'] > 90:
            score += 10
            
        # Number of releases behind
        score += min(dep['releases_behind'] * 2, 20)
        
        dep['priority_score'] = score
        dep['priority'] = 'critical' if score > 80 else 'high' if score > 50 else 'medium'
    
    return sorted(outdated_deps, key=lambda x: x['priority_score'], reverse=True)
```

### 5. 依赖体积分析

分析包体积影响：

**Bundle Size 影响**
```javascript
// Analyze NPM package sizes
const analyzeBundleSize = async (dependencies) => {
    const sizeAnalysis = {
        totalSize: 0,
        totalGzipped: 0,
        packages: [],
        recommendations: []
    };
    
    for (const [packageName, info] of Object.entries(dependencies)) {
        try {
            // Fetch package stats
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
            
            // Size recommendations
            if (data.size > 1000000) { // 1MB
                sizeAnalysis.recommendations.push({
                    package: packageName,
                    issue: 'Large bundle size',
                    size: `${(data.size / 1024 / 1024).toFixed(2)} MB`,
                    suggestion: 'Consider lighter alternatives or lazy loading'
                });
            }
        } catch (error) {
            console.error(`Failed to analyze ${packageName}:`, error);
        }
    }
    
    // Sort by size
    sizeAnalysis.packages.sort((a, b) => b.size - a.size);
    
    // Add top offenders
    sizeAnalysis.topOffenders = sizeAnalysis.packages.slice(0, 10);
    
    return sizeAnalysis;
};
```

### 6. 供应链安全

检查依赖劫持和抢注攻击：

**供应链检查**
```python
def check_supply_chain_security(dependencies):
    """
    Perform supply chain security checks
    """
    security_issues = []
    
    for package_name, package_info in dependencies.items():
        # Check for typosquatting
        typo_check = check_typosquatting(package_name)
        if typo_check['suspicious']:
            security_issues.append({
                'type': 'typosquatting',
                'package': package_name,
                'severity': 'high',
                'similar_to': typo_check['similar_packages'],
                'recommendation': 'Verify package name spelling'
            })
        
        # Check maintainer changes
        maintainer_check = check_maintainer_changes(package_name)
        if maintainer_check['recent_changes']:
            security_issues.append({
                'type': 'maintainer_change',
                'package': package_name,
                'severity': 'medium',
                'details': maintainer_check['changes'],
                'recommendation': 'Review recent package changes'
            })
        
        # Check for suspicious patterns
        if contains_suspicious_patterns(package_info):
            security_issues.append({
                'type': 'suspicious_behavior',
                'package': package_name,
                'severity': 'high',
                'patterns': package_info['suspicious_patterns'],
                'recommendation': 'Audit package source code'
            })
    
    return security_issues

def check_typosquatting(package_name):
    """
    Check if package name might be typosquatting
    """
    common_packages = [
        'react', 'express', 'lodash', 'axios', 'webpack',
        'babel', 'jest', 'typescript', 'eslint', 'prettier'
    ]
    
    for legit_package in common_packages:
        distance = levenshtein_distance(package_name.lower(), legit_package)
        if 0 < distance <= 2:  # Close but not exact match
            return {
                'suspicious': True,
                'similar_packages': [legit_package],
                'distance': distance
            }
    
    return {'suspicious': False}
```

### 7. 自动修复

生成自动修复脚本：

**更新脚本**
```bash
#!/bin/bash
# Auto-update dependencies with security fixes

echo "🔒 Security Update Script"
echo "========================"

# NPM/Yarn updates
if [ -f "package.json" ]; then
    echo "📦 Updating NPM dependencies..."
    
    # Audit and auto-fix
    npm audit fix --force
    
    # Update specific vulnerable packages
    npm update package1@^2.0.0 package2@~3.1.0
    
    # Run tests
    npm test
    
    if [ $? -eq 0 ]; then
        echo "✅ NPM updates successful"
    else
        echo "❌ Tests failed, reverting..."
        git checkout package-lock.json
    fi
fi

# Python updates
if [ -f "requirements.txt" ]; then
    echo "🐍 Updating Python dependencies..."
    
    # Create backup
    cp requirements.txt requirements.txt.backup
    
    # Update vulnerable packages
    pip-compile --upgrade-package package1 --upgrade-package package2
    
    # Test installation
    pip install -r requirements.txt --dry-run
    
    if [ $? -eq 0 ]; then
        echo "✅ Python updates successful"
    else
        echo "❌ Update failed, reverting..."
        mv requirements.txt.backup requirements.txt
    fi
fi
```

**Pull Request 生成**
```python
def generate_dependency_update_pr(updates):
    """
    Generate PR with dependency updates
    """
    pr_body = f"""
## 🔒 依赖安全更新

本 PR 更新 {len(updates)} 个依赖，以解决安全漏洞和过时包问题。

### 安全修复 ({sum(1 for u in updates if u['has_security'])})

| 包 | 当前版本 | 更新版本 | 严重程度 | CVE |
|---------|---------|---------|----------|-----|
"""
    
    for update in updates:
        if update['has_security']:
            pr_body += f"| {update['package']} | {update['current']} | {update['target']} | {update['severity']} | {', '.join(update['cves'])} |\n"
    
    pr_body += """

### 其他更新

| 包 | 当前版本 | 更新版本 | 类型 | 时长 |
|---------|---------|---------|------|-----|
"""
    
    for update in updates:
        if not update['has_security']:
            pr_body += f"| {update['package']} | {update['current']} | {update['target']} | {update['type']} | {update['age_days']} 天 |\n"
    
    pr_body += """

### 测试
- [ ] 所有测试通过
- [ ] 未发现破坏性变更
- [ ] 已审查包体积影响

### 审查清单
- [ ] 安全漏洞已处理
- [ ] 许可证合规性已维护
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

### 8. 监控与告警

设置持续依赖监控：

**GitHub Actions 工作流**
```yaml
name: Dependency Audit

on:
  schedule:
    - cron: '0 0 * * *'  # Daily
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
          echo "::error::Found $(jq '.vulnerabilities.total' npm-audit.json) vulnerabilities"
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
              title: `🚨 ${critical} critical vulnerabilities found`,
              body: 'Dependency audit found critical vulnerabilities. See workflow run for details.',
              labels: ['security', 'dependencies', 'critical']
            });
          }
```

## 输出格式

1. **执行摘要**: 高层风险评估和行动项
2. **漏洞报告**: 详细的 CVE 分析及严重程度评级
3. **许可证合规**: 兼容性矩阵和法律风险
4. **更新建议**: 带工作量估算的优先级列表
5. **供应链分析**: 抢注和劫持风险
6. **修复脚本**: 自动更新命令和 PR 生成
7. **体积影响报告**: 包体积分析和优化建议
8. **监控设置**: 用于持续扫描的 CI/CD 集成

专注于提供可操作的洞察，帮助维护安全、合规、高效的依赖管理。
