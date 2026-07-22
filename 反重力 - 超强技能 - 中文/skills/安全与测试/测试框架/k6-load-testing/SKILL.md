---
name: k6-load-testing
description: "全面的 k6 负载测试技能，覆盖 API、浏览器和可扩展性测试。编写真实负载场景、分析结果并集成 CI/CD。触发词：k6、负载测试、压力测试、性能测试、API测试、CI/CD集成、smoke test、load test、stress test、spike test、soak test"
category: testing
risk: safe
source: community
date_added: "2026-03-13"
author: Kairo Official
tags: [k6, load-testing, performance, api-testing, ci-cd]
tools: [claude, cursor, gemini]
---

# k6 负载测试

## 概述

k6 是一款现代化的、以开发者为中心的负载测试工具，帮助你为 HTTP API、WebSocket 端点和浏览器场景编写并执行性能测试。本技能提供全面指导，涵盖编写真实负载测试、配置测试场景（smoke、load、stress、spike、soak）、分析结果以及集成 CI/CD 流水线。

当你需要验证系统性能、识别瓶颈、确保 SLA 合规或在部署前捕获性能回归时，使用本技能。

---

## 何时使用本技能

- 需要对 HTTP API、WebSocket 端点或浏览器场景进行负载测试时
- 在 CI/CD 中设置性能回归测试时
- 分析系统在不同负载条件下的行为时
- 比较代码变更前后的性能差异时
- 验证 SLA 要求和性能预算时

---

## k6 基础

### 安装

```bash
# macOS
brew install k6

# Windows
choco install k6

# Linux
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

### 快速开始

```javascript
// simple-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  const res = http.get('https://httpbin.test.k6.io/get');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
```

运行命令：`k6 run simple-test.js`

---

## 测试配置

### 常用选项

```javascript
export const options = {
  // Virtual Users (concurrent users)
  vus: 100,
  
  // Test duration
  duration: '5m',
  
  // Or use stages for ramp-up/ramp-down
  stages: [
    { duration: '30s', target: 20 },   // Ramp up
    { duration: '1m', target: 100 },  // Stay at 100
    { duration: '30s', target: 0 },    // Ramp down
  ],
  
  // Thresholds (SLA)
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% requests < 500ms
    http_req_failed: ['rate<0.01'],     // Error rate < 1%
  },
  
  // Load zones (distributed testing)
  ext: {
    loadimpact: {
      name: 'My Load Test',
      distribution: {
        'amazon:us:ashburn': { weight: 50 },
        'amazon:eu: Dublin': { weight: 50 },
      },
    },
  },
};
```

### 测试类型

| 类型 | 适用场景 | 配置方式 |
|------|----------|----------|
| Smoke Test | 验证基本功能 | 低 VU 数（1-5），短时长 |
| Load Test | 正常预期负载 | 根据流量设定目标 VU 数 |
| Stress Test | 寻找系统极限 | 逐步加压超出容量 |
| Spike Test | 突发流量冲击 | 快速增减负载 |
| Soak Test | 长时间稳定性 | 延长测试时长 |

---

## HTTP 测试

### 基本请求

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export default function () {
  // GET request
  const getRes = http.get('https://api.example.com/users');
  
  check(getRes, {
    'GET succeeded': (r) => r.status === 200,
    'has users': (r) => r.json('data.length') > 0,
  });

  // POST request with JSON body
  const postRes = http.post('https://api.example.com/users', 
    JSON.stringify({ name: 'Test User', email: 'test@example.com' }),
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + __ENV.API_TOKEN,
      },
    }
  );
  
  check(postRes, {
    'POST succeeded': (r) => r.status === 201,
    'user created': (r) => r.json('id') !== undefined,
  });

  sleep(1);
}
```

### 请求链式调用

```javascript
import http from 'k6/http';
import { check } from 'k6';

export default function () {
  // Login and extract token
  const loginRes = http.post('https://api.example.com/login', 
    JSON.stringify({ email: 'test@example.com', password: 'password123' })
  );
  
  const token = loginRes.json('access_token');
  
  // Use token in subsequent requests
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
  
  const profileRes = http.get('https://api.example.com/profile', {
    headers: headers,
  });
  
  check(profileRes, {
    'profile loaded': (r) => r.status === 200,
  });
}
```

### 参数化测试

```javascript
import http from 'k6/http';
import { check } from 'k6';

const usernames = ['user1', 'user2', 'user3', 'user4', 'user5'];

export default function () {
  // Use shared array with VU-specific index
  const username = usernames[__VU % usernames.length];
  
  const res = http.get(`https://api.example.com/users/${username}`);
  
  check(res, {
    'user found': (r) => r.status === 200,
  });
}
```

---

## 浏览器测试（k6 Browser）

```javascript
import { browser } from 'k6/browser';

export const options = {
  scenarios: {
    browser_test: {
      executor: 'constant-vus',
      vus: 5,
      duration: '30s',
      browser: {
        type: 'chromium',
      },
    },
  },
};

export default async function () {
  const page = await browser.newPage();
  
  try {
    await page.goto('https://example.com');
    
    const title = await page.title();
    console.log(`Page title: ${title}`);
    
    // Click and interact
    await page.click('button[data-testid="submit"]');
    
    // Wait for response
    await page.waitForSelector('.success-message');
    
  } finally {
    await page.close();
  }
}
```

安装浏览器支持：`k6 install chromium`

---

## WebSocket 测试

```javascript
import ws from 'k6/ws';
import { check } from 'k6';

export default function () {
  const url = 'wss://echo.websocket.org';
  
  ws.connect(url, {}, function (socket) {
    socket.on('open', () => {
      console.log('WebSocket connected');
      socket.send('Hello WebSocket');
    });
    
    socket.on('message', (data) => {
      console.log(`Received: ${data}`);
      check(data, {
        'echo received': (d) => d.includes('Hello'),
      });
    });
    
    socket.on('close', () => {
      console.log('WebSocket closed');
    });
    
    // Send periodic messages
    socket.setInterval(function () {
      socket.send('ping');
    }, 1000);
    
    // Close after 5 seconds
    socket.setTimeout(function () {
      socket.close();
    }, 5000);
  });
}
```

---

## 数据处理

### CSV 数据源

```javascript
import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

// Option 1: Load once, shared across VUs
const users = new SharedArray('users', function () {
  return open('./users.csv').split('\n').slice(1).map(line => {
    const [email, password] = line.split(',');
    return { email, password };
  });
});

export default function () {
  const user = users[__VU % users.length];
  
  const res = http.post('https://api.example.com/login',
    JSON.stringify({ email: user.email, password: user.password })
  );
  
  check(res, { 'login successful': (r) => r.status === 200 });
}
```

### JSON 数据源

```javascript
import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

const products = new SharedArray('products', function () {
  return JSON.parse(open('./products.json'));
});

export default function () {
  const product = products[Math.floor(Math.random() * products.length)];
  
  const res = http.get(`https://api.example.com/products/${product.id}`);
  
  check(res, { 'product found': (r) => r.status === 200 });
}
```

---

## 阈值与 SLA

### 基本阈值

```javascript
export const options = {
  vus: 50,
  duration: '2m',
  
  thresholds: {
    // Response time thresholds
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    
    // Error rate threshold
    http_req_failed: ['rate<0.01'],
    
    // Throughput threshold
    http_reqs: ['rate>100'],
  },
};
```

### 高级阈值

```javascript
export const options = {
  thresholds: {
    // Multiple thresholds on same metric
    http_req_duration: [
      'p(90)<300',   // 90th percentile < 300ms
      'p(95)<500',  // 95th percentile < 500ms
      'p(99)<1000', // 99th percentile < 1s
      'avg<200',    // average < 200ms
    ],
    
    // Custom metrics
    my_custom_metric: ['avg<100'],
    
    // Abort on threshold failure
    'http_req_duration{method:GET}': ['p(95)<300'],
  },
};
```

---

## 自定义指标

### 计数器

```javascript
import http from 'k6/http';
import { Counter, Trend, Rate, Gauge } from 'k6/metrics';

// Define custom metrics
const myCounter = new Counter('api_calls_total');
const responseTime = new Trend('response_time');
const errorRate = new Rate('error_rate');
const activeUsers = new Gauge('active_users');

export default function () {
  const res = http.get('https://api.example.com/data');
  
  // Increment counter
  myCounter.add(1);
  
  // Add to trend (for percentiles)
  responseTime.add(res.timings.duration);
  
  // Track error rate
  errorRate.add(res.status !== 200);
  
  // Set gauge value
  activeUsers.add(__VU);
  
  // Tagged metrics
  const taggedRes = http.get('https://api.example.com/users', {
    tags: { endpoint: 'users', env: 'prod' },
  });
}
```

---

## CI/CD 集成

### GitHub Actions

```yaml
# .github/workflows/load-test.yml
name: Load Tests

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup k6
        uses: grafana/k6-action@v0.2.0
        
      - name: Run load test
        env:
          API_TOKEN: ${{ secrets.API_TOKEN }}
        run: k6 run --out json=results.json load-test.js
        
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: results.json
          
      - name: Check thresholds
        if: failure()
        run: |
          echo "Load test failed thresholds!"
          exit 1
```

### GitLab CI

```yaml
# .gitlab-ci.yml
load_test:
  image: grafana/k6:latest
  script:
    - k6 run load-test.js
  artifacts:
    when: always
    paths:
      - results.json
    reports:
      junit: results.xml
```

---

## 结果分析

### 内置报告

```bash
# Text summary
k6 run load-test.js

# JSON output for parsing
k6 run --out json=results.json load-test.js

# InfluxDB + Grafana
k6 run --out influxdb=http://localhost:8086/k6 load-test.js

# Prometheus remote write
k6 run --out prometheus=localhost:9090/k6 load-test.js

# Cloud results
k6 run --out cloud load-test.js
```

### 解读结果

| 指标 | 说明 | 良好 | 警告 | 异常 |
|------|------|------|------|------|
| http_req_duration (p95) | 95% 响应时间 | < 300ms | 300-500ms | > 500ms |
| http_req_failed | 错误率 | < 0.1% | 0.1-1% | > 1% |
| http_reqs | 请求/秒 | 达到目标 | 接近上限 | 达到上限 |
| vus | 虚拟用户数 | 稳定 | 逐步增长 | 意外激增 |

---

## 示例

### 示例 1：基本 API 负载测试

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '2m',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}
```

### 示例 2：带认证和数据参数化的测试

```javascript
import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

const users = new SharedArray('users', function () {
  return JSON.parse(open('./users.json'));
});

export default function () {
  const user = users[__VU % users.length];
  
  const loginRes = http.post('https://api.example.com/login',
    JSON.stringify({ email: user.email, password: user.password })
  );
  
  const token = loginRes.json('access_token');
  
  const headers = { 'Authorization': `Bearer ${token}` };
  const res = http.get('https://api.example.com/profile', { headers });
  
  check(res, { 'profile loaded': (r) => r.status === 200 });
}
```

---

## 最佳实践

- **从 smoke test 开始**：先以 1-5 个 VU 验证测试可运行，再逐步扩量
- **使用真实数据**：用真实用户数据和行为进行参数化
- **设定有意义的阈值**：与你的 SLA 和业务需求对齐
- **预热系统**：在 stages 中包含爬升时间
- **监控外部依赖**：不仅追踪你的 API，还要关注下游服务
- **善用标签**：为请求打标签以便精细分析（`tags: { endpoint: 'users' }`）
- **保持测试聚焦**：每个场景一个测试文件，清晰明了

---

## 常见陷阱

- **问题**：测试本地通过但 CI 中失败
  **解决**：确保 CI 环境具有相近的资源和网络条件

- **问题**：多次运行结果不一致
  **解决**：排查外部依赖、随机数据或测试数据污染

- **问题**：k6 内存不足
  **解决**：大数据集使用 `SharedArray`，减少 VU 数，或使用 `--max-memory` 参数

- **问题**：阈值过于严格
  **解决**：先放宽阈值，再根据历史数据逐步收紧

---

## 相关技能

- `@performance-engineer` — 更广泛的性能优化
- `@api-testing-observability-api-mock` — 测试期间的 API 模拟
- `@application-performance-performance-optimization` — 性能优化

---

## 更多资源

- [k6 文档](https://k6.io/docs/)
- [k6 示例](https://github.com/grafana/k6/tree/master/examples)
- [k6 负载测试指南](https://k6.io/guides/)
- [k6 Cloud](https://k6.io/cloud/)

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 当缺少必要输入、权限、安全边界或成功标准时，停下来请求澄清。
