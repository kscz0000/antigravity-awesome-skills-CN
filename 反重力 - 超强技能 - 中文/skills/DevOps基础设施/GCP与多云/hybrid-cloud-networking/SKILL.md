---
name: hybrid-cloud-networking
description: "使用 VPN、Direct Connect 和 ExpressRoute 配置本地与云环境之间的安全高性能网络连接。当用户要求'混合云网络'、'本地连接云'、'VPN配置'、'Direct Connect'、'ExpressRoute'、'混合云组网'、'本地数据中心上云'时使用。"
risk: safe
source: community
date_added: "2026-02-27"
---

# 混合云网络

使用 VPN、Direct Connect 和 ExpressRoute 配置本地与云环境之间的安全高性能网络连接。

## 不适用场景

- 任务与混合云网络无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可执行的步骤和验证方法
- 如需详细示例，打开 `resources/implementation-playbook.md`

## 目的

在本地数据中心与云服务商（AWS、Azure、GCP）之间建立安全可靠的网络连接。

## 使用场景

- 本地连接到云
- 数据中心扩展到云
- 实现混合云双活架构
- 满足合规要求
- 逐步迁移上云

## 连接方案

### AWS 连接

#### 1. Site-to-Site VPN
- 基于互联网的 IPSec VPN
- 每条隧道最高 1.25 Gbps
- 适合中等带宽，成本较低
- 延迟较高，依赖互联网

```hcl
resource "aws_vpn_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "main-vpn-gateway"
  }
}

resource "aws_customer_gateway" "main" {
  bgp_asn    = 65000
  ip_address = "203.0.113.1"
  type       = "ipsec.1"
}

resource "aws_vpn_connection" "main" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.main.id
  type                = "ipsec.1"
  static_routes_only  = false
}
```

#### 2. AWS Direct Connect
- 专用网络连接
- 1 Gbps 至 100 Gbps
- 延迟低，带宽稳定
- 费用较高，需要部署时间

**参考：** 见 `references/direct-connect.md`

### Azure 连接

#### 1. Site-to-Site VPN
```hcl
resource "azurerm_virtual_network_gateway" "vpn" {
  name                = "vpn-gateway"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  type     = "Vpn"
  vpn_type = "RouteBased"
  sku      = "VpnGw1"

  ip_configuration {
    name                          = "vnetGatewayConfig"
    public_ip_address_id          = azurerm_public_ip.vpn.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway.id
  }
}
```

#### 2. Azure ExpressRoute
- 通过连接提供商的私有连接
- 最高 100 Gbps
- 低延迟，高可靠性
- 高级版支持全球连通

### GCP 连接

#### 1. Cloud VPN
- IPSec VPN（经典版或 HA VPN）
- HA VPN：99.99% SLA
- 每条隧道最高 3 Gbps

#### 2. Cloud Interconnect
- 专用互联（10 Gbps、100 Gbps）
- 合作伙伴互联（50 Mbps 至 50 Gbps）
- 延迟低于 VPN

## 混合网络架构

### 架构1：中心辐射型
```
On-Premises Datacenter
         ↓
    VPN/Direct Connect
         ↓
    Transit Gateway (AWS) / vWAN (Azure)
         ↓
    ├─ Production VPC/VNet
    ├─ Staging VPC/VNet
    └─ Development VPC/VNet
```

### 架构2：多区域混合
```
On-Premises
    ├─ Direct Connect → us-east-1
    └─ Direct Connect → us-west-2
            ↓
        Cross-Region Peering
```

### 架构3：多云混合
```
On-Premises Datacenter
    ├─ Direct Connect → AWS
    ├─ ExpressRoute → Azure
    └─ Interconnect → GCP
```

## 路由配置

### BGP 配置
```
On-Premises Router:
- AS Number: 65000
- Advertise: 10.0.0.0/8

Cloud Router:
- AS Number: 64512 (AWS), 65515 (Azure)
- Advertise: Cloud VPC/VNet CIDRs
```

### 路由传播
- 在路由表上启用路由传播
- 使用 BGP 实现动态路由
- 实施路由过滤
- 监控路由通告

## 安全最佳实践

1. **优先使用私有连接**（Direct Connect/ExpressRoute）
2. **VPN 隧道启用加密**
3. **使用 VPC 端点**避免流量经互联网路由
4. **配置网络 ACL**和安全组
5. **启用 VPC Flow Logs**进行监控
6. **部署 DDoS 防护**
7. **使用 PrivateLink/Private Endpoints**
8. **用 CloudWatch/Monitor**监控连接状态
9. **实现冗余**（双隧道）
10. **定期安全审计**

## 高可用

### 双 VPN 隧道
```hcl
resource "aws_vpn_connection" "primary" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.primary.id
  type                = "ipsec.1"
}

resource "aws_vpn_connection" "secondary" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.secondary.id
  type                = "ipsec.1"
}
```

### 双活配置
- 从不同位置建立多条连接
- 使用 BGP 自动故障切换
- 等价多路径（ECMP）路由
- 监控所有连接的健康状态

## 监控与排障

### 关键指标
- 隧道状态（up/down）
- 出入流量字节数
- 丢包率
- 延迟
- BGP 会话状态

### 排障命令
```bash
# AWS VPN
aws ec2 describe-vpn-connections
aws ec2 get-vpn-connection-telemetry

# Azure VPN
az network vpn-connection show
az network vpn-connection show-device-config-script
```

## 成本优化

1. **按流量选择合适的连接规格**
2. **低带宽负载使用 VPN**
3. **合并流量**减少连接数
4. **降低数据传输**费用
5. **高带宽场景使用 Direct Connect**
6. **部署缓存**减少流量

## 参考文件

- `references/vpn-setup.md` - VPN 配置指南
- `references/direct-connect.md` - Direct Connect 配置指南

## 相关技能

- `multi-cloud-architecture` - 架构决策
- `terraform-module-library` - IaC 实现

## 限制
- 仅在任务明确符合上述范围时使用本技能
- 输出内容不能替代针对具体环境的验证、测试或专家评审
- 如缺少必要输入、权限、安全边界或成功标准，应停止并请求澄清
