---
name: mailtrap-setting-up-sending-domain
description: 添加或验证 Mailtrap 发送域名，排查 DNS 传播问题，发布 SPF/DKIM/DMARC 记录，完成合规流程。触发词：Mailtrap 发送域名、域名验证、DNS 传播、SPF 记录、DKIM 记录、DMARC 记录、发送域名设置、域名合规、DNS 配置、Mailtrap 域名
risk: critical
source: community
date_added: "2026-06-19"
---

# 设置 Mailtrap 发送域名

## 概述

在正式发送之前，你必须添加并验证一个你控制的域名。Mailtrap 会在 **UI** 中显示该域名所需的 **每一条 DNS 记录**：请 **添加完整集合**（不要挑选）。DNS 验证通过后，如有要求，请完成 **合规** 步骤。

**子域名与根域名：** 添加你将在 From 地址中使用的 **精确** 主机名。如果你从 `notifications.mycompany.com` 发送，则添加该 **子域名** 作为发送域名——而不仅仅是 `mycompany.com`，除非你确实从根域名发送。

对于常见主机的逐步操作，请打开 [发送域名设置](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain.md)（Cloudflare、Route 53 等）中对应的指南，并结合实时 **UI** 值进行操作。

**相关技能：** `mailtrap-sending-emails`（域名就绪后使用）。

## 何时使用

- 新的 **发送域名** 设置、验证卡住或合规问题
- DNS 在 Cloudflare、AWS、Google、Namecheap、GoDaddy、DigitalOcean 等

## 何时不使用

- 仅使用沙盒测试而不需要自定义域名（参见 `mailtrap-testing-with-sandbox`）

## 授权

下面的发送域名 API 调用需要 `Authorization: Bearer $MAILTRAP_API_TOKEN` 以及路径中的 `$MAILTRAP_ACCOUNT_ID`。通过 `GET https://mailtrap.io/api/accounts` 获取 `$MAILTRAP_ACCOUNT_ID`，并将令牌存储在环境变量或密钥管理器中。

## 自动化设置（API 和 DNS 提供商）

在构建脚本或 AI 辅助自动化时优先使用此路径：

1. **通过 API 获取 DNS 记录和状态** — 使用发送域名 API：
  - `GET https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/sending_domains` — 列出域名
  - `GET https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/sending_domains/{sending_domain_id}` — 返回 `dns_records`（每条记录包含 `type`、`name`、`value` 和验证 `status`）以及 `dns_verified`。在发布 DNS 后轮询此接口。
2. **通过 API 创建域名** —
  - 当你的流程以编程方式配置域名时，使用 `POST https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/sending_domains` 并传入 `domain_name`。
3. **以编程方式发布 DNS** —
  - 使用 DNS 主机的 API（例如 [Cloudflare API](https://developers.cloudflare.com/api/)、AWS Route 53、Google Cloud DNS）或 IaC 在 DNS 主机上创建返回的记录。记录名称和值必须与 API 响应完全一致。

**人工回退方案：** 当 API 自动化不可用时，进入 **Sending Domains** > **Add domain** > 将值复制到注册商 **UI** > 点击 **Verify**。

## 工作流（摘要）

1. 进入 **Sending Domains** > **Add domain** 并输入域名。
2. 从 **UI** 或发送域名 API 获取所需记录；在 DNS 主机上 **按显示内容创建所有列出的记录**（名称、类型、值必须完全一致）。
3. 等待 DNS 传播。**如果验证持续待定**，使用 `dig`、`nslookup` 或在线 DNS 查询工具确认每条记录已公开可见，然后再次点击 **Verify**。
4. 在提示时完成 **合规** 流程。

产品操作指南：[发送域名设置](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain.md)。

## DNS 提供商指南（文档）

Mailtrap 为常见提供商发布了点击路径指南。打开与用户 DNS 主机匹配的页面，并结合实时 **UI** 记录进行操作：

- [Cloudflare](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/cloudflare.md)
- [AWS Route 53](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/aws-route-53.md)
- [Google Cloud DNS](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/google-cloud-dns.md)
- [Squarespace](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/squarespace.md)（包含原 Google Domains 迁移说明，如适用）
- [GoDaddy](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/godaddy.md)
- [Namecheap](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/namecheap.md)
- [DigitalOcean](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/digitalocean.md)

如果用户的提供商不在列表中，同样适用此规则：**将每条记录** 从 Mailtrap 复制到服务于 From 域名的 DNS 区域中。

## 重要 DNS 注意事项（代理 DNS）

如果你的 DNS 提供商 **代理** 记录（Cloudflare 上的橙色云朵，其他地方的类似 CDN/代理模式），则与验证相关的记录必须是 **DNS-only**（灰色云朵 / 非代理），除非 Mailtrap 文档明确允许代理——被代理的 CNAME 等记录通常会破坏 SPF/DKIM 验证。同样的约束适用于任何通过代理前置 DNS 的主机。

## 限制

- DNS 和合规界面可能会变更；在发布 DNS 之前，务必从 Mailtrap 复制当前的确切记录。
