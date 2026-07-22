---
name: aws-serverless
description: 构建生产级 AWS 无服务器应用的专业技能。涵盖 Lambda 函数、API Gateway、DynamoDB、SQS/SNS 事件驱动模式、SAM/CDK 部署和冷启动优化。触发词：AWS无服务器、Lambda开发、API Gateway、DynamoDB、SQS、SNS、SAM部署、CDK、冷启动优化、Serverless架构
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# AWS Serverless

构建生产级 AWS 无服务器应用的专业技能。涵盖 Lambda 函数、API Gateway、DynamoDB、SQS/SNS 事件驱动模式、SAM/CDK 部署和冷启动优化。

## 原则

- 合理配置内存和超时（优化前先测量）
- 为延迟敏感型工作负载最小化冷启动
- Java/.NET 函数使用 SnapStart
- 简单用例优先使用 HTTP API 而非 REST API
- 使用 DLQ 和重试机制设计容错
- 保持部署包小巧
- 使用环境变量进行配置
- 实现带关联 ID 的结构化日志

## 模式

### Lambda Handler 模式

具有错误处理的正确 Lambda 函数结构

**何时使用**：任何 Lambda 函数实现、API 处理器、事件处理器、定时任务

```javascript
// Node.js Lambda Handler
// handler.js

// 在 handler 外初始化（跨调用复用）
const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, GetCommand } = require('@aws-sdk/lib-dynamodb');

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

// Handler 函数
exports.handler = async (event, context) => {
  // 可选：不等待事件循环清空（Node.js）
  context.callbackWaitsForEmptyEventLoop = false;

  try {
    // 根据事件源解析输入
    const body = typeof event.body === 'string'
      ? JSON.parse(event.body)
      : event.body;

    // 业务逻辑
    const result = await processRequest(body);

    // 返回 API Gateway 兼容响应
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(result)
    };
  } catch (error) {
    console.error('Error:', JSON.stringify({
      error: error.message,
      stack: error.stack,
      requestId: context.awsRequestId
    }));

    return {
      statusCode: error.statusCode || 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        error: error.message || 'Internal server error'
      })
    };
  }
};

async function processRequest(data) {
  // 在此编写业务逻辑
  const result = await docClient.send(new GetCommand({
    TableName: process.env.TABLE_NAME,
    Key: { id: data.id }
  }));
  return result.Item;
}
```

```python
# Python Lambda Handler
# handler.py

import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

# 在 handler 外初始化（跨调用复用）
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    try:
        # 解析输入
        body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event.get('body', {})

        # 业务逻辑
        result = process_request(body)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }

    except ClientError as e:
        logger.error(f"DynamoDB error: {e.response['Error']['Message']}")
        return error_response(500, 'Database error')

    except json.JSONDecodeError:
        return error_response(400, 'Invalid JSON')

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return error_response(500, 'Internal server error')

def process_request(data):
    response = table.get_item(Key={'id': data['id']})
    return response.get('Item')

def error_response(status_code, message):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': message})
    }
```

### 最佳实践

- 在 handler 外初始化客户端（跨热调用复用）
- 始终返回正确的 API Gateway 响应格式
- 使用结构化 JSON 日志以便 CloudWatch Insights 查询
- 在错误日志中包含请求 ID 用于追踪

### API Gateway 集成模式

REST API 和 HTTP API 与 Lambda 集成

**何时使用**：构建 Lambda 支持的 REST API、需要 HTTP 端点

```yaml
# template.yaml (SAM)
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: nodejs20.x
    Timeout: 30
    MemorySize: 256
    Environment:
      Variables:
        TABLE_NAME: !Ref ItemsTable

Resources:
  # HTTP API（简单用例推荐）
  HttpApi:
    Type: AWS::Serverless::HttpApi
    Properties:
      StageName: prod
      CorsConfiguration:
        AllowOrigins:
          - "*"
        AllowMethods:
          - GET
          - POST
          - DELETE
        AllowHeaders:
          - "*"

  # Lambda 函数
  GetItemFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/get.handler
      Events:
        GetItem:
          Type: HttpApi
          Properties:
            ApiId: !Ref HttpApi
            Path: /items/{id}
            Method: GET
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref ItemsTable

  CreateItemFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/create.handler
      Events:
        CreateItem:
          Type: HttpApi
          Properties:
            ApiId: !Ref HttpApi
            Path: /items
            Method: POST
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref ItemsTable

  # DynamoDB 表
  ItemsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      BillingMode: PAY_PER_REQUEST

Outputs:
  ApiUrl:
    Value: !Sub "https://${HttpApi}.execute-api.${AWS::Region}.amazonaws.com/prod"
```

```javascript
// src/handlers/get.js
const { getItem } = require('../lib/dynamodb');

exports.handler = async (event) => {
  const id = event.pathParameters?.id;

  if (!id) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Missing id parameter' })
    };
  }

  const item = await getItem(id);

  if (!item) {
    return {
      statusCode: 404,
      body: JSON.stringify({ error: 'Item not found' })
    };
  }

  return {
    statusCode: 200,
    body: JSON.stringify(item)
  };
};
```

### 项目结构

project/
├── template.yaml      # SAM 模板
├── src/
│   ├── handlers/
│   │   ├── get.js
│   │   ├── create.js
│   │   └── delete.js
│   └── lib/
│       └── dynamodb.js
└── events/
    └── event.json     # 测试事件

### API 对比

- Http_api:
  - 更低延迟（~10ms）
  - 更低成本（便宜 50-70%）
  - 更简单，功能更少
  - 最适合：大多数 REST API
- Rest_api:
  - 更多功能（缓存、请求验证、WAF）
  - 使用计划和 API 密钥
  - 请求/响应转换
  - 最适合：复杂 API、企业功能

### 事件驱动 SQS 模式

Lambda 由 SQS 触发，实现可靠的异步处理

**何时使用**：解耦的异步处理、需要重试逻辑和 DLQ、批量处理消息

```yaml
# template.yaml
Resources:
  ProcessorFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/processor.handler
      Events:
        SQSEvent:
          Type: SQS
          Properties:
            Queue: !GetAtt ProcessingQueue.Arn
            BatchSize: 10
            FunctionResponseTypes:
              - ReportBatchItemFailures  # 部分批处理失败处理

  ProcessingQueue:
    Type: AWS::SQS::Queue
    Properties:
      VisibilityTimeout: 180  # 6倍 Lambda 超时
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
        maxReceiveCount: 3

  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      MessageRetentionPeriod: 1209600  # 14 天
```

```javascript
// src/handlers/processor.js
exports.handler = async (event) => {
  const batchItemFailures = [];

  for (const record of event.Records) {
    try {
      const body = JSON.parse(record.body);
      await processMessage(body);
    } catch (error) {
      console.error(`Failed to process message ${record.messageId}:`, error);
      // 标记此项目失败（将被重试）
      batchItemFailures.push({
        itemIdentifier: record.messageId
      });
    }
  }

  // 返回失败项目以重试
  return { batchItemFailures };
};

async function processMessage(message) {
  // 你的处理逻辑
  console.log('Processing:', message);

  // 模拟工作
  await saveToDatabase(message);
}
```

```python
# Python 版本
import json
import logging

logger = logging.getLogger()

def handler(event, context):
    batch_item_failures = []

    for record in event['Records']:
        try:
            body = json.loads(record['body'])
            process_message(body)
        except Exception as e:
            logger.error(f"Failed to process {record['messageId']}: {e}")
            batch_item_failures.append({
                'itemIdentifier': record['messageId']
            })

    return {'batchItemFailures': batch_item_failures}
```

### 最佳实践

- 将 VisibilityTimeout 设置为 Lambda 超时的 6 倍
- 使用 ReportBatchItemFailures 处理部分批处理失败
- 始终配置 DLQ 处理毒消息
- 幂等处理消息

### DynamoDB Streams 模式

使用 Lambda 响应 DynamoDB 表变更

**何时使用**：实时响应数据变更、跨区域复制、审计日志、通知

```yaml
# template.yaml
Resources:
  ItemsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: items
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      BillingMode: PAY_PER_REQUEST
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES

  StreamProcessorFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/stream.handler
      Events:
        Stream:
          Type: DynamoDB
          Properties:
            Stream: !GetAtt ItemsTable.StreamArn
            StartingPosition: TRIM_HORIZON
            BatchSize: 100
            MaximumRetryAttempts: 3
            DestinationConfig:
              OnFailure:
                Destination: !GetAtt StreamDLQ.Arn

  StreamDLQ:
    Type: AWS::SQS::Queue
```

```javascript
// src/handlers/stream.js
exports.handler = async (event) => {
  for (const record of event.Records) {
    const eventName = record.eventName;  // INSERT, MODIFY, REMOVE

    // 将 DynamoDB 格式转换为普通 JS 对象
    const newImage = record.dynamodb.NewImage
      ? unmarshall(record.dynamodb.NewImage)
      : null;
    const oldImage = record.dynamodb.OldImage
      ? unmarshall(record.dynamodb.OldImage)
      : null;

    console.log(`${eventName}: `, { newImage, oldImage });

    switch (eventName) {
      case 'INSERT':
        await handleInsert(newImage);
        break;
      case 'MODIFY':
        await handleModify(oldImage, newImage);
        break;
      case 'REMOVE':
        await handleRemove(oldImage);
        break;
    }
  }
};

// 使用 AWS SDK v3 unmarshall
const { unmarshall } = require('@aws-sdk/util-dynamodb');
```

### Stream 视图类型

- KEYS_ONLY: 仅键属性
- NEW_IMAGE: 修改后
- OLD_IMAGE: 修改前
- NEW_AND_OLD_IMAGES: 修改前后都有

### 冷启动优化模式

最小化 Lambda 冷启动延迟

**何时使用**：延迟敏感型应用、面向用户的 API、高流量函数

## 1. 优化包大小

```javascript
// 使用模块化 AWS SDK v3 导入
// 好 - 只导入需要的部分
const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, GetCommand } = require('@aws-sdk/lib-dynamodb');

// 坏 - 导入整个 SDK
const AWS = require('aws-sdk');  // 不要这样做！
```

## 2. 使用 SnapStart（Java/.NET）

```yaml
# template.yaml
Resources:
  JavaFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: com.example.Handler::handleRequest
      Runtime: java21
      SnapStart:
        ApplyOn: PublishedVersions  # 启用 SnapStart
      AutoPublishAlias: live
```

## 3. 合理配置内存

```yaml
# 更多内存 = 更多 CPU = 更快初始化
Resources:
  FastFunction:
    Type: AWS::Serverless::Function
    Properties:
      MemorySize: 1024  # 1GB 获得完整 vCPU
      Timeout: 30
```

## 4. 预置并发（必要时）

```yaml
Resources:
  CriticalFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/critical.handler
      AutoPublishAlias: live

  ProvisionedConcurrency:
    Type: AWS::Lambda::ProvisionedConcurrencyConfig
    Properties:
      FunctionName: !Ref CriticalFunction
      Qualifier: live
      ProvisionedConcurrentExecutions: 5
```

## 5. 保持初始化轻量

```python
# 好 - 延迟初始化
_table = None

def get_table():
    global _table
    if _table is None:
        dynamodb = boto3.resource('dynamodb')
        _table = dynamodb.Table(os.environ['TABLE_NAME'])
    return _table

def handler(event, context):
    table = get_table()  # 仅在首次使用时初始化
    # ...
```

### 优化优先级

- 1: 减小包大小（影响最大）
- 2: Java/.NET 使用 SnapStart
- 3: 增加内存以加快初始化
- 4: 延迟重型导入
- 5: 预置并发（最后手段）

### SAM 本地开发模式

使用 SAM CLI 进行本地测试和调试

**何时使用**：本地开发和测试、调试 Lambda 函数、本地测试 API Gateway

```bash
# 安装 SAM CLI
pip install aws-sam-cli

# 初始化新项目
sam init --runtime nodejs20.x --name my-api

# 构建项目
sam build

# 本地运行
sam local start-api

# 调用单个函数
sam local invoke GetItemFunction --event events/get.json

# 本地调试（Node.js 配合 VS Code）
sam local invoke --debug-port 5858 GetItemFunction

# 部署
sam deploy --guided
```

```json
// events/get.json (测试事件)
{
  "pathParameters": {
    "id": "123"
  },
  "httpMethod": "GET",
  "path": "/items/123"
}
```

```json
// .vscode/launch.json (用于调试)
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to SAM CLI",
      "type": "node",
      "request": "attach",
      "address": "localhost",
      "port": 5858,
      "localRoot": "${workspaceRoot}/src",
      "remoteRoot": "/var/task/src",
      "protocol": "inspector"
    }
  ]
}
```

### 常用命令

- Sam_build: 构建 Lambda 部署包
- Sam_local_start_api: 启动本地 API Gateway
- Sam_local_invoke: 调用单个函数
- Sam_deploy: 部署到 AWS
- Sam_logs: 追踪 CloudWatch 日志

### CDK Serverless 模式

使用 AWS CDK 实现基础设施即代码

**何时使用**：Lambda 之外的复杂基础设施、偏好编程语言而非 YAML、需要可复用构造

```typescript
// lib/api-stack.ts
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { Construct } from 'constructs';

export class ApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB 表
    const table = new dynamodb.Table(this, 'ItemsTable', {
      partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY, // 仅用于开发环境
    });

    // Lambda 函数
    const getItemFn = new lambda.Function(this, 'GetItemFunction', {
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: 'get.handler',
      code: lambda.Code.fromAsset('src/handlers'),
      environment: {
        TABLE_NAME: table.tableName,
      },
      memorySize: 256,
      timeout: cdk.Duration.seconds(30),
    });

    // 授予权限
    table.grantReadData(getItemFn);

    // API Gateway
    const api = new apigateway.RestApi(this, 'ItemsApi', {
      restApiName: 'Items Service',
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
      },
    });

    const items = api.root.addResource('items');
    const item = items.addResource('{id}');

    item.addMethod('GET', new apigateway.LambdaIntegration(getItemFn));

    // 输出 API URL
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: api.url,
    });
  }
}
```

```bash
# CDK 命令
npm install -g aws-cdk
cdk init app --language typescript
cdk synth    # 生成 CloudFormation
cdk diff     # 显示变更
cdk deploy   # 部署到 AWS
```

## 常见陷阱

### 冷启动 INIT 阶段现在计费（2025年8月）

严重程度：高

场景：在生产环境运行 Lambda 函数

症状：
Lambda 费用意外增加（高出 10-50%）。
账单包含函数初始化费用。
启动逻辑重的函数成本超出预期。

原因：
自 2025 年 8 月 1 日起，AWS 对 INIT 阶段的计费方式与调用时长相同。此前，冷启动初始化不计入完整时长。

这会影响以下函数：
- 重型依赖加载（大型包）
- 缓慢的初始化代码
- 频繁冷启动（低流量或并发配置差）

冷启动现在直接影响账单，而不仅仅是延迟。

推荐修复：

## 测量 INIT 阶段

```bash
# 检查 CloudWatch Logs 中的 INIT_REPORT
# 查找 Init Duration（毫秒）

# 示例日志行：
# INIT_REPORT Init Duration: 423.45 ms
```

## 减少 INIT 时长

```javascript
// 1. 最小化包大小
// 使用 tree shaking，排除开发依赖
// npm prune --production

// 2. 延迟加载重型依赖
let heavyLib = null;
function getHeavyLib() {
  if (!heavyLib) {
    heavyLib = require('heavy-library');
  }
  return heavyLib;
}

// 3. 使用 AWS SDK v3 模块化导入
const { S3Client } = require('@aws-sdk/client-s3');
// 不要：const AWS = require('aws-sdk');
```

## Java/.NET 使用 SnapStart

```yaml
Resources:
  JavaFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: java21
      SnapStart:
        ApplyOn: PublishedVersions
```

## 监控冷启动频率

```javascript
// 使用自定义指标追踪冷启动
let isColdStart = true;

exports.handler = async (event) => {
  if (isColdStart) {
    console.log('COLD_START');
    // 在此发送 CloudWatch 自定义指标
    isColdStart = false;
  }
  // ...
};
```

### Lambda 超时配置错误

严重程度：高

场景：运行 Lambda 函数，尤其是有外部调用时

症状：
函数意外超时。
日志中出现 "Task timed out after X seconds"。
部分处理无响应。
静默失败且未捕获错误。

原因：
Lambda 默认超时仅 3 秒。最大为 15 分钟。

常见超时原因：
- 默认超时对工作负载太短
- 下游服务响应时间超出预期
- VPC 内网络问题
- 无限循环或阻塞操作
- S3 下载文件比预期大

Lambda 在超时时终止，不会优雅关闭。

推荐修复：

## 设置合适的超时

```yaml
# template.yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Timeout: 30  # 秒（最大 900）
      # 设置为预期时长 + 缓冲
```

## 实现超时感知

```javascript
exports.handler = async (event, context) => {
  // 获取剩余时间
  const remainingTime = context.getRemainingTimeInMillis();

  // 如果时间不足，优雅失败
  if (remainingTime < 5000) {
    console.warn('Running low on time, aborting');
    throw new Error('Insufficient time remaining');
  }

  // 对于长时间操作，定期检查
  for (const item of items) {
    if (context.getRemainingTimeInMillis() < 10000) {
      // 保存进度并优雅退出
      await saveProgress(processedItems);
      throw new Error('Timeout approaching, saved progress');
    }
    await processItem(item);
  }
};
```

## 设置下游超时

```javascript
const axios = require('axios');

// 始终为 HTTP 调用设置超时
const response = await axios.get('https://api.example.com/data', {
  timeout: 5000  // 5 秒
});
```

### 内存不足（OOM）崩溃

严重程度：高

场景：Lambda 函数处理数据

症状：
函数突然停止且无错误。
CloudWatch 日志显示截断。
"Max Memory Used" 达到配置限制。
负载下行为不一致。

原因：
当 Lambda 超出内存分配时，AWS 强制终止运行时。这不会抛出可捕获的异常。

常见原因：
- 在内存中处理大文件
- 跨调用内存泄漏
- 缓冲整个响应体
- 重型库消耗过多内存

推荐修复：

## 增加内存分配

```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      MemorySize: 1024  # MB（128-10240）
      # 更多内存 = 更多 CPU
```

## 流式处理大数据

```javascript
// 坏 - 将整个文件加载到内存
const data = await s3.getObject(params).promise();
const content = data.Body.toString();

// 好 - 流式处理
const { S3Client, GetObjectCommand } = require('@aws-sdk/client-s3');
const s3 = new S3Client({});

const response = await s3.send(new GetObjectCommand(params));
const stream = response.Body;

// 分块处理流
for await (const chunk of stream) {
  await processChunk(chunk);
}
```

## 监控内存使用

```javascript
exports.handler = async (event, context) => {
  const used = process.memoryUsage();
  console.log('Memory:', {
    heapUsed: Math.round(used.heapUsed / 1024 / 1024) + 'MB',
    heapTotal: Math.round(used.heapTotal / 1024 / 1024) + 'MB'
  });
  // ...
};
```

## 使用 Lambda Power Tuning

```bash
# 找到最佳内存设置
# https://github.com/alexcasalboni/aws-lambda-power-tuning
```

### VPC 附加 Lambda 冷启动延迟

严重程度：中

场景：VPC 内的 Lambda 函数访问私有资源

症状：
极慢的冷启动（曾为 10+ 秒，现约 100ms）。
空闲期后首次调用超时。
VPC 内函数可用但比非 VPC 慢。

原因：
VPC 内的 Lambda 函数需要弹性网络接口（ENI）。AWS 通过 Hyperplane ENI 显著改善了此问题，但：

- VPC 内首次冷启动仍有开销
- NAT Gateway 问题可能导致超时
- 安全组配置错误阻止流量
- DNS 解析可能缓慢

推荐修复：

## 验证 VPC 配置

```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      VpcConfig:
        SecurityGroupIds:
          - !Ref LambdaSecurityGroup
        SubnetIds:
          - !Ref PrivateSubnet1
          - !Ref PrivateSubnet2  # 多可用区

  LambdaSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Lambda SG
      VpcId: !Ref VPC
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0  # 允许 HTTPS 出站
```

## 为 AWS 服务使用 VPC 端点

```yaml
# 避免通过 NAT Gateway 访问 AWS 服务
DynamoDBEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    ServiceName: !Sub com.amazonaws.${AWS::Region}.dynamodb
    VpcId: !Ref VPC
    RouteTableIds:
      - !Ref PrivateRouteTable
    VpcEndpointType: Gateway

S3Endpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    ServiceName: !Sub com.amazonaws.${AWS::Region}.s3
    VpcId: !Ref VPC
    VpcEndpointType: Gateway
```

## 仅在必要时使用 VPC

除非需要以下情况，否则不要将 Lambda 附加到 VPC：
- 访问 VPC 内的 RDS/ElastiCache
- 访问私有 EC2 实例
- 合规要求

大多数 AWS 服务可以在不使用 VPC 的情况下访问。

### Node.js 事件循环未清空

严重程度：中

场景：Node.js Lambda 函数有回调或定时器

症状：
函数耗时达到完整超时时长才返回。
逻辑已完成但仍出现 "Task timed out"。
空闲时间产生额外费用。

原因：
默认情况下，Lambda 等待 Node.js 事件循环为空后才返回。如果你有：
- 未解决的 setTimeout/setInterval
- 悬空的数据库连接
- 待处理的回调

Lambda 会等待直到超时，即使响应已准备好。

推荐修复：

## 告诉 Lambda 不要等待事件循环

```javascript
exports.handler = async (event, context) => {
  // 不等待事件循环清空
  context.callbackWaitsForEmptyEventLoop = false;

  // 你的代码
  const result = await processRequest(event);

  return {
    statusCode: 200,
    body: JSON.stringify(result)
  };
};
```

## 正确关闭连接

```javascript
// 对于数据库连接，使用连接池
// 或显式关闭连接

const mysql = require('mysql2/promise');

exports.handler = async (event, context) => {
  context.callbackWaitsForEmptyEventLoop = false;

  const connection = await mysql.createConnection({...});
  try {
    const [rows] = await connection.query('SELECT * FROM users');
    return { statusCode: 200, body: JSON.stringify(rows) };
  } finally {
    await connection.end();  // 始终关闭
  }
};
```

### API Gateway 负载大小限制

严重程度：中

场景：返回大响应或接收大请求

症状：
"413 Request Entity Too Large" 错误
"Execution failed due to configuration error: Malformed Lambda proxy response"
响应被截断或失败

原因：
API Gateway 有硬性负载限制：
- REST API: 10 MB 请求/响应
- HTTP API: 10 MB 请求/响应
- Lambda 本身: 6 MB 同步响应，256 KB 异步

超出这些限制会导致可能不明显的失败。

推荐修复：

## 对于大文件上传

```javascript
// 使用预签名 S3 URL 而非通过 API Gateway 传递

const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');

exports.handler = async (event) => {
  const s3 = new S3Client({});

  const command = new PutObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: `uploads/${Date.now()}.file`
  });

  const uploadUrl = await getSignedUrl(s3, command, { expiresIn: 300 });

  return {
    statusCode: 200,
    body: JSON.stringify({ uploadUrl })
  };
};
```

## 对于大响应

```javascript
// 存储到 S3，返回预签名下载 URL
exports.handler = async (event) => {
  const largeData = await generateLargeReport();

  await s3.send(new PutObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: `reports/${reportId}.json`,
    Body: JSON.stringify(largeData)
  }));

  const downloadUrl = await getSignedUrl(s3,
    new GetObjectCommand({
      Bucket: process.env.BUCKET_NAME,
      Key: `reports/${reportId}.json`
    }),
    { expiresIn: 3600 }
  );

  return {
    statusCode: 200,
    body: JSON.stringify({ downloadUrl })
  };
};
```

### 无限循环或递归调用

严重程度：高

场景：Lambda 由事件触发

症状：
成本失控。
几分钟内数千次调用。
CloudWatch 日志显示重复调用。
Lambda 写入触发它的源存储桶/表。

原因：
Lambda 可能意外触发自身：
- S3 触发器写回同一存储桶
- DynamoDB 触发器更新同一表
- SNS 发布到触发它的主题
- Step Functions 错误处理不当

推荐修复：

## 使用不同的存储桶/前缀

```yaml
# 带前缀过滤器的 S3 触发器
Events:
  S3Event:
    Type: S3
    Properties:
      Bucket: !Ref InputBucket
      Events: s3:ObjectCreated:*
      Filter:
        S3Key:
          Rules:
            - Name: prefix
              Value: uploads/  # 仅对 uploads/ 触发

# 输出到不同的存储桶或前缀
# OutputBucket 或 processed/ 前缀
```

## 添加幂等性检查

```javascript
exports.handler = async (event) => {
  for (const record of event.Records) {
    const key = record.s3.object.key;

    // 如果是已处理文件则跳过
    if (key.startsWith('processed/')) {
      console.log('Skipping already processed file:', key);
      continue;
    }

    // 处理并写入不同位置
    await processFile(key);
    await writeToS3(`processed/${key}`, result);
  }
};
```

## 设置预留并发作为熔断器

```yaml
Resources:
  RiskyFunction:
    Type: AWS::Serverless::Function
    Properties:
      ReservedConcurrentExecutions: 10  # 最多 10 个并行
      # 限制失控调用的波及范围
```

## 使用 CloudWatch 告警监控

```yaml
InvocationAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    MetricName: Invocations
    Namespace: AWS/Lambda
    Statistic: Sum
    Period: 60
    EvaluationPeriods: 1
    Threshold: 1000  # 超过 1000 次/分钟时告警
    ComparisonOperator: GreaterThanThreshold
```

## 验证检查

### 硬编码 AWS 凭证

严重程度：错误

AWS 凭证绝不能硬编码

消息：检测到硬编码的 AWS 访问密钥。使用 IAM 角色或环境变量。

### 源代码中的 AWS 密钥

严重程度：错误

密钥应使用 Secrets Manager 或环境变量

消息：硬编码的 AWS 密钥。使用 IAM 角色或 Secrets Manager。

### 过于宽松的 IAM 策略

严重程度：警告

避免在 Lambda IAM 角色中使用通配符权限

消息：过于宽松的 IAM 策略。使用最小权限原则。

### Lambda Handler 无错误处理

严重程度：警告

Lambda handler 应有 try/catch 以实现优雅错误处理

消息：Lambda handler 无错误处理。添加 try/catch。

### 缺少 callbackWaitsForEmptyEventLoop

严重程度：信息

Node.js handler 应设置 callbackWaitsForEmptyEventLoop

消息：考虑设置 context.callbackWaitsForEmptyEventLoop = false

### 默认内存配置

严重程度：信息

默认 128MB 对许多工作负载可能太低

消息：使用默认 128MB 内存。考虑增加以获得更好性能。

### 低超时配置

严重程度：警告

非常低的超时可能导致意外失败

消息：1-3 秒的超时可能太低。如果有外部调用请增加。

### 无死信队列配置

严重程度：警告

异步函数应有 DLQ 处理失败调用

消息：未配置 DLQ。为异步调用添加 DLQ。

### 导入完整 AWS SDK v2

严重程度：警告

从 AWS SDK v3 导入特定客户端以获得更小的包

消息：导入完整 AWS SDK。使用模块化 SDK v3 导入以获得更小的包。

### 硬编码 DynamoDB 表名

严重程度：警告

表名应来自环境变量

消息：硬编码表名。使用环境变量以提高可移植性。

## 协作

### 委派触发

- 用户需要 GCP 无服务器 -> gcp-cloud-run（容器用 Cloud Run，事件用 Cloud Functions）
- 用户需要 Azure 无服务器 -> azure-functions（Azure Functions、Logic Apps）
- 用户需要数据库设计 -> postgres-wizard（RDS 设计，或使用 DynamoDB 模式）
- 用户需要认证 -> auth-specialist（Cognito、API Gateway 授权器）
- 用户需要复杂工作流 -> workflow-automation（Step Functions、EventBridge）
- 用户需要 AI 集成 -> llm-architect（Lambda 调用 Bedrock 或外部 LLM）

## 何时使用
当请求明显匹配上述能力和模式时使用此技能。

## 限制
- 仅当任务明显匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
