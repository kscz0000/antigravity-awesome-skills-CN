# GDPR 数据处理实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# GDPR 数据处理

GDPR合规数据处理、同意管理和隐私控制的实用实施指南。

## 使用本技能的场景

- 构建处理欧盟个人数据的系统
- 实施同意管理
- 处理数据主体请求（DSR）
- 开展GDPR合规审查
- 设计隐私优先架构
- 创建数据处理协议

## 核心概念

### 1. 个人数据类别

| 类别 | 示例 | 保护级别 |
|----------|----------|------------------|
| **基本** | 姓名、邮箱、电话 | 标准 |
| **敏感（第9条）** | 健康、宗教、种族 | 明确同意 |
| **刑事（第10条）** | 定罪、犯罪 | 官方授权 |
| **儿童** | 16岁以下数据 | 家长同意 |

### 2. 处理的法律依据

```
第6条 - 合法依据:
├── 同意：自由给予、具体、知情
├── 合同：履行合同所必需
├── 法律义务：法律要求
├── 重要利益：保护某人生命
├── 公共利益：官方职能
└── 合法利益：与权利平衡
```

### 3. 数据主体权利

```
访问权（第15条）      ─┐
更正权（第16条）       │
删除权（第17条）       │ 必须在1个月内
限制处理权（第18条）   │ 响应
可携带权（第20条）     │
反对权（第21条）      ─┘
```

## 实施模式

### 模式1：同意管理

```javascript
// Consent data model
const consentSchema = {
  userId: String,
  consents: [{
    purpose: String,         // 'marketing', 'analytics', etc.
    granted: Boolean,
    timestamp: Date,
    source: String,          // 'web_form', 'api', etc.
    version: String,         // Privacy policy version
    ipAddress: String,       // For proof
    userAgent: String        // For proof
  }],
  auditLog: [{
    action: String,          // 'granted', 'withdrawn', 'updated'
    purpose: String,
    timestamp: Date,
    source: String
  }]
};

// Consent service
class ConsentManager {
  async recordConsent(userId, purpose, granted, metadata) {
    const consent = {
      purpose,
      granted,
      timestamp: new Date(),
      source: metadata.source,
      version: await this.getCurrentPolicyVersion(),
      ipAddress: metadata.ipAddress,
      userAgent: metadata.userAgent
    };

    // Store consent
    await this.db.consents.updateOne(
      { userId },
      {
        $push: {
          consents: consent,
          auditLog: {
            action: granted ? 'granted' : 'withdrawn',
            purpose,
            timestamp: consent.timestamp,
            source: metadata.source
          }
        }
      },
      { upsert: true }
    );

    // Emit event for downstream systems
    await this.eventBus.emit('consent.changed', {
      userId,
      purpose,
      granted,
      timestamp: consent.timestamp
    });
  }

  async hasConsent(userId, purpose) {
    const record = await this.db.consents.findOne({ userId });
    if (!record) return false;

    const latestConsent = record.consents
      .filter(c => c.purpose === purpose)
      .sort((a, b) => b.timestamp - a.timestamp)[0];

    return latestConsent?.granted === true;
  }

  async getConsentHistory(userId) {
    const record = await this.db.consents.findOne({ userId });
    return record?.auditLog || [];
  }
}
```

```html
<!-- GDPR-compliant consent UI -->
<div class="consent-banner" role="dialog" aria-labelledby="consent-title">
  <h2 id="consent-title">Cookie Preferences</h2>

  <p>We use cookies to improve your experience. Select your preferences below.</p>

  <form id="consent-form">
    <!-- Necessary - always on, no consent needed -->
    <div class="consent-category">
      <input type="checkbox" id="necessary" checked disabled>
      <label for="necessary">
        <strong>Necessary</strong>
        <span>Required for the website to function. Cannot be disabled.</span>
      </label>
    </div>

    <!-- Analytics - requires consent -->
    <div class="consent-category">
      <input type="checkbox" id="analytics" name="analytics">
      <label for="analytics">
        <strong>Analytics</strong>
        <span>Help us understand how you use our site.</span>
      </label>
    </div>

    <!-- Marketing - requires consent -->
    <div class="consent-category">
      <input type="checkbox" id="marketing" name="marketing">
      <label for="marketing">
        <strong>Marketing</strong>
        <span>Personalized ads based on your interests.</span>
      </label>
    </div>

    <div class="consent-actions">
      <button type="button" id="accept-all">Accept All</button>
      <button type="button" id="reject-all">Reject All</button>
      <button type="submit">Save Preferences</button>
    </div>

    <p class="consent-links">
      <a href="/privacy-policy">Privacy Policy</a> |
      <a href="/cookie-policy">Cookie Policy</a>
    </p>
  </form>
</div>
```

### 模式2：数据主体访问请求（DSAR）

```python
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class DSARHandler:
    """Handle Data Subject Access Requests."""

    RESPONSE_DEADLINE_DAYS = 30
    EXTENSION_ALLOWED_DAYS = 60  # For complex requests

    def __init__(self, data_sources: List['DataSource']):
        self.data_sources = data_sources

    async def submit_request(
        self,
        request_type: str,  # 'access', 'erasure', 'rectification', 'portability'
        user_id: str,
        verified: bool,
        details: Optional[Dict] = None
    ) -> str:
        """Submit a new DSAR."""
        request = {
            'id': self.generate_request_id(),
            'type': request_type,
            'user_id': user_id,
            'status': 'pending_verification' if not verified else 'processing',
            'submitted_at': datetime.utcnow(),
            'deadline': datetime.utcnow() + timedelta(days=self.RESPONSE_DEADLINE_DAYS),
            'details': details or {},
            'audit_log': [{
                'action': 'submitted',
                'timestamp': datetime.utcnow(),
                'details': 'Request received'
            }]
        }

        await self.db.dsar_requests.insert_one(request)
        await self.notify_dpo(request)

        return request['id']

    async def process_access_request(self, request_id: str) -> Dict:
        """Process a data access request."""
        request = await self.get_request(request_id)

        if request['type'] != 'access':
            raise ValueError("Not an access request")

        # Collect data from all sources
        user_data = {}
        for source in self.data_sources:
            try:
                data = await source.get_user_data(request['user_id'])
                user_data[source.name] = data
            except Exception as e:
                user_data[source.name] = {'error': str(e)}

        # Format response
        response = {
            'request_id': request_id,
            'generated_at': datetime.utcnow().isoformat(),
            'data_categories': list(user_data.keys()),
            'data': user_data,
            'retention_info': await self.get_retention_info(),
            'processing_purposes': await self.get_processing_purposes(),
            'third_party_recipients': await self.get_recipients()
        }

        # Update request status
        await self.update_request(request_id, 'completed', response)

        return response

    async def process_erasure_request(self, request_id: str) -> Dict:
        """Process a right to erasure request."""
        request = await self.get_request(request_id)

        if request['type'] != 'erasure':
            raise ValueError("Not an erasure request")

        results = {}
        exceptions = []

        for source in self.data_sources:
            try:
                # Check for legal exceptions
                can_delete, reason = await source.can_delete(request['user_id'])

                if can_delete:
                    await source.delete_user_data(request['user_id'])
                    results[source.name] = 'deleted'
                else:
                    exceptions.append({
                        'source': source.name,
                        'reason': reason  # e.g., 'legal retention requirement'
                    })
                    results[source.name] = f'retained: {reason}'
            except Exception as e:
                results[source.name] = f'error: {str(e)}'

        response = {
            'request_id': request_id,
            'completed_at': datetime.utcnow().isoformat(),
            'results': results,
            'exceptions': exceptions
        }

        await self.update_request(request_id, 'completed', response)

        return response

    async def process_portability_request(self, request_id: str) -> bytes:
        """Generate portable data export."""
        request = await self.get_request(request_id)
        user_data = await self.process_access_request(request_id)

        # Convert to machine-readable format (JSON)
        portable_data = {
            'export_date': datetime.utcnow().isoformat(),
            'format_version': '1.0',
            'data': user_data['data']
        }

        return json.dumps(portable_data, indent=2, default=str).encode()
```

### 模式3：数据保留

```python
from datetime import datetime, timedelta
from enum import Enum

class RetentionBasis(Enum):
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligation"
    LEGITIMATE_INTEREST = "legitimate_interest"

class DataRetentionPolicy:
    """Define and enforce data retention policies."""

    POLICIES = {
        'user_account': {
            'retention_period_days': 365 * 3,  # 3 years after last activity
            'basis': RetentionBasis.CONTRACT,
            'trigger': 'last_activity_date',
            'archive_before_delete': True
        },
        'transaction_records': {
            'retention_period_days': 365 * 7,  # 7 years for tax
            'basis': RetentionBasis.LEGAL_OBLIGATION,
            'trigger': 'transaction_date',
            'archive_before_delete': True,
            'legal_reference': 'Tax regulations require 7 year retention'
        },
        'marketing_consent': {
            'retention_period_days': 365 * 2,  # 2 years
            'basis': RetentionBasis.CONSENT,
            'trigger': 'consent_date',
            'archive_before_delete': False
        },
        'support_tickets': {
            'retention_period_days': 365 * 2,
            'basis': RetentionBasis.LEGITIMATE_INTEREST,
            'trigger': 'ticket_closed_date',
            'archive_before_delete': True
        },
        'analytics_data': {
            'retention_period_days': 365,  # 1 year
            'basis': RetentionBasis.CONSENT,
            'trigger': 'collection_date',
            'archive_before_delete': False,
            'anonymize_instead': True
        }
    }

    async def apply_retention_policies(self):
        """Run retention policy enforcement."""
        for data_type, policy in self.POLICIES.items():
            cutoff_date = datetime.utcnow() - timedelta(
                days=policy['retention_period_days']
            )

            if policy.get('anonymize_instead'):
                await self.anonymize_old_data(data_type, cutoff_date)
            else:
                if policy.get('archive_before_delete'):
                    await self.archive_data(data_type, cutoff_date)
                await self.delete_old_data(data_type, cutoff_date)

            await self.log_retention_action(data_type, cutoff_date)

    async def anonymize_old_data(self, data_type: str, before_date: datetime):
        """Anonymize data instead of deleting."""
        # Example: Replace identifying fields with hashes
        if data_type == 'analytics_data':
            await self.db.analytics.update_many(
                {'collection_date': {'$lt': before_date}},
                {'$set': {
                    'user_id': None,
                    'ip_address': None,
                    'device_id': None,
                    'anonymized': True,
                    'anonymized_date': datetime.utcnow()
                }}
            )
```

### 模式4：隐私设计

```python
class PrivacyFirstDataModel:
    """Example of privacy-by-design data model."""

    # Separate PII from behavioral data
    user_profile_schema = {
        'user_id': str,  # UUID, not sequential
        'email_hash': str,  # Hashed for lookups
        'created_at': datetime,
        # Minimal data collection
        'preferences': {
            'language': str,
            'timezone': str
        }
    }

    # Encrypted at rest
    user_pii_schema = {
        'user_id': str,
        'email': str,  # Encrypted
        'name': str,   # Encrypted
        'phone': str,  # Encrypted (optional)
        'address': dict,  # Encrypted (optional)
        'encryption_key_id': str
    }

    # Pseudonymized behavioral data
    analytics_schema = {
        'session_id': str,  # Not linked to user_id
        'pseudonym_id': str,  # Rotating pseudonym
        'events': list,
        'device_category': str,  # Generalized, not specific
        'country': str,  # Not city-level
    }

class DataMinimization:
    """Implement data minimization principles."""

    @staticmethod
    def collect_only_needed(form_data: dict, purpose: str) -> dict:
        """Filter form data to only fields needed for purpose."""
        REQUIRED_FIELDS = {
            'account_creation': ['email', 'password'],
            'newsletter': ['email'],
            'purchase': ['email', 'name', 'address', 'payment'],
            'support': ['email', 'message']
        }

        allowed = REQUIRED_FIELDS.get(purpose, [])
        return {k: v for k, v in form_data.items() if k in allowed}

    @staticmethod
    def generalize_location(ip_address: str) -> str:
        """Generalize IP to country level only."""
        import geoip2.database
        reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
        try:
            response = reader.country(ip_address)
            return response.country.iso_code
        except:
            return 'UNKNOWN'
```

### 模式5：数据泄露通知

```python
from datetime import datetime
from enum import Enum

class BreachSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BreachNotificationHandler:
    """Handle GDPR breach notification requirements."""

    AUTHORITY_NOTIFICATION_HOURS = 72
    AFFECTED_NOTIFICATION_REQUIRED_SEVERITY = BreachSeverity.HIGH

    async def report_breach(
        self,
        description: str,
        data_types: List[str],
        affected_count: int,
        severity: BreachSeverity
    ) -> dict:
        """Report and handle a data breach."""
        breach = {
            'id': self.generate_breach_id(),
            'reported_at': datetime.utcnow(),
            'description': description,
            'data_types_affected': data_types,
            'affected_individuals_count': affected_count,
            'severity': severity.value,
            'status': 'investigating',
            'timeline': [{
                'event': 'breach_reported',
                'timestamp': datetime.utcnow(),
                'details': description
            }]
        }

        await self.db.breaches.insert_one(breach)

        # Immediate notifications
        await self.notify_dpo(breach)
        await self.notify_security_team(breach)

        # Authority notification required within 72 hours
        if self.requires_authority_notification(severity, data_types):
            breach['authority_notification_deadline'] = (
                datetime.utcnow() + timedelta(hours=self.AUTHORITY_NOTIFICATION_HOURS)
            )
            await self.schedule_authority_notification(breach)

        # Affected individuals notification
        if severity.value in [BreachSeverity.HIGH.value, BreachSeverity.CRITICAL.value]:
            await self.schedule_individual_notifications(breach)

        return breach

    def requires_authority_notification(
        self,
        severity: BreachSeverity,
        data_types: List[str]
    ) -> bool:
        """Determine if supervisory authority must be notified."""
        # Always notify for sensitive data
        sensitive_types = ['health', 'financial', 'credentials', 'biometric']
        if any(t in sensitive_types for t in data_types):
            return True

        # Notify for medium+ severity
        return severity in [BreachSeverity.MEDIUM, BreachSeverity.HIGH, BreachSeverity.CRITICAL]

    async def generate_authority_report(self, breach_id: str) -> dict:
        """Generate report for supervisory authority."""
        breach = await self.get_breach(breach_id)

        return {
            'organization': {
                'name': self.config.org_name,
                'contact': self.config.dpo_contact,
                'registration': self.config.registration_number
            },
            'breach': {
                'nature': breach['description'],
                'categories_affected': breach['data_types_affected'],
                'approximate_number_affected': breach['affected_individuals_count'],
                'likely_consequences': self.assess_consequences(breach),
                'measures_taken': await self.get_remediation_measures(breach_id),
                'measures_proposed': await self.get_proposed_measures(breach_id)
            },
            'timeline': breach['timeline'],
            'submitted_at': datetime.utcnow().isoformat()
        }
```

## 合规检查清单

```markdown
## GDPR 实施检查清单

### 法律依据
- [ ] 为每项处理活动记录法律依据
- [ ] 同意机制符合GDPR要求
- [ ] 完成合法利益评估

### 透明度
- [ ] 隐私政策清晰且易于访问
- [ ] 处理目的明确说明
- [ ] 数据保留期限已记录

### 数据主体权利
- [ ] 访问请求流程已实施
- [ ] 删除请求流程已实施
- [ ] 可携带性导出功能可用
- [ ] 更正流程可用
- [ ] 在30天期限内响应

### 安全
- [ ] 静态加密已实施
- [ ] 传输加密（TLS）
- [ ] 访问控制已到位
- [ ] 审计日志已启用

### 泄露响应
- [ ] 泄露检测机制
- [ ] 72小时通知流程
- [ ] 泄露文档系统

### 文档
- [ ] 处理活动记录（第30条）
- [ ] 数据保护影响评估
- [ ] 与供应商的数据处理协议
```

## 最佳实践

### 应做事项
- **最小化数据收集** - 只收集所需数据
- **记录一切** - 处理活动、法律依据
- **加密PII** - 静态和传输中
- **实施访问控制** - 按需知悉原则
- **定期审计** - 持续验证合规性

### 禁止事项
- **不要预先勾选同意框** - 必须是主动选择
- **不要捆绑同意** - 不同目的分开处理
- **不要无限期保留** - 定义并执行保留策略
- **不要忽视DSAR** - 需要30天响应
- **不要在没有保障措施的情况下传输** - 标准合同条款或充分性决定

## 资源

- [GDPR Full Text](https://gdpr-info.eu/)
- [ICO Guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
- [EDPB Guidelines](https://edpb.europa.eu/our-work-tools/general-guidance/gdpr-guidelines-recommendations-best-practices_en)
