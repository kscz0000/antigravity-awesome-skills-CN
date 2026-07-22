---
name: product-design
description: "苹果级产品设计——视觉系统、UX流程、无障碍访问、专属视觉语言、设计令牌、原型制作与交付。涵盖Figma、设计系统、字体、色彩、间距、动效设计和认知设计原理。触发词：创建设计系统、定义视觉语言、审查UX、无障碍访问、设计令牌、产品品牌、UI评审。"
risk: none
source: community
date_added: '2026-03-06'
author: renat
tags:
- design
- ux
- design-systems
- accessibility
- figma
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# PRODUCT DESIGN — 苹果级设计

## 概述

苹果级产品设计——视觉系统、UX流程、无障碍访问、专属视觉语言、设计令牌、原型制作与交付。涵盖Figma、设计系统、字体、色彩、间距、动效设计和认知设计原理。适用于：创建设计系统、定义视觉语言、审查UX、无障碍访问、设计令牌、产品品牌、UI评审。

## 何时使用此技能

- 当你需要此领域的专业协助时

## 不要使用此技能的情况

- 任务与产品设计无关
- 有更简单、更具体的工具可以处理该请求
- 用户需要通用协助而不需要领域专业知识

## 工作原理

> "设计不仅仅是外观和感觉。设计是它如何工作。"
> — 史蒂夫·乔布斯

---

## 乔尼·艾维/苹果的10大设计原则

1. **极致简洁** — 移除一切非本质元素
2. **材料诚实** — 每个元素的存在都有其理由
3. **少即是多** — 克制是一种设计决策
4. **系统一致性** — 一切都属于统一的系统
5. **细节至关重要** — 用户能感受到，即使没有注意到
6. **功能定义形式** — 美学服务于目的
7. **持久性** — 经得起时间考验的设计
8. **无障碍作为标准** — 而非附加功能
9. **跨屏连续性** — 统一的体验
10. **愉悦的惊喜** — 令人愉悦的意外

## 认知设计

- **零认知负荷** — 用户永远不需要思考
- **清晰的可操作性** — 可点击的东西看起来就应该可点击
- **即时反馈** — 每个操作都有视觉响应
- **预防错误** — 让错误不可能发生的设计

---

## 精英设计系统的结构

```
design-system/
├── tokens/
│   ├── colors.json       # paleta completa com semantica
│   ├── typography.json   # escala tipografica
│   ├── spacing.json      # grid e espacamento
│   ├── shadows.json      # elevacao e profundidade
│   ├── motion.json       # duracao e easing
│   └── radius.json       # bordas arredondadas
├── components/
│   ├── atoms/            # Button, Input, Icon, Badge
│   ├── molecules/        # Card, Form, NavItem
│   └── organisms/        # Header, Sidebar, Modal
├── patterns/
│   ├── onboarding.md     # primeiro acesso
│   ├── empty-states.md   # estados vazios
│   ├── loading.md        # estados de carregamento
│   └── errors.md         # tratamento de erros
└── guidelines/
    ├── voice-tone.md     # voz e tom
    ├── imagery.md        # fotografia e ilustracao
    └── accessibility.md  # WCAG 2.1 AA
```

## 设计令牌 — Auri示例

```json
{
  "color": {
    "brand": {
      "primary": "#6C63FF",
      "primary-dark": "#5A52E0",
      "accent": "#FF6B6B",
      "surface": "#F8F7FF"
    },
    "semantic": {
      "success": "#22C55E",
      "warning": "#F59E0B",
      "error": "#EF4444",
      "info": "#3B82F6"
    },
    "neutral": {
      "900": "#111827",
      "800": "#1F2937",
      "600": "#4B5563",
      "400": "#9CA3AF",
      "200": "#E5E7EB",
      "50":  "#F9FAFB"
    }
  },
  "typography": {
    "display": { "size": "48px", "weight": "700", "line": "1.1" },
    "h1": { "size": "36px", "weight": "700", "line": "1.2" },
    "h2": { "size": "28px", "weight": "600", "line": "1.3" },
    "body": { "size": "16px", "weight": "400", "line": "1.6" },
    "small": { "size": "14px", "weight": "400", "line": "1.5" }
  },
  "spacing": {
    "xs": "4px", "sm": "8px", "md": "16px",
    "lg": "24px", "xl": "32px", "2xl": "48px", "3xl": "64px"
  },
  "radius": {
    "sm": "4px", "md": "8px", "lg": "12px",
    "xl": "16px", "full": "9999px"
  },
  "shadow": {
    "sm": "0 1px 3px rgba(0,0,0,0.12)",
    "md": "0 4px 12px rgba(0,0,0,0.15)",
    "lg": "0 8px 24px rgba(0,0,0,0.18)",
    "xl": "0 20px 60px rgba(0,0,0,0.22)"
  },
  "motion": {
    "fast": "150ms ease-out",
    "normal": "250ms ease-in-out",
    "slow": "400ms cubic-bezier(0.34, 1.56, 0.64, 1)"
  }
}
```

---

## UX流程结构

```
1. Entry Point (como o usuario chega)
2. Context (o que o usuario sabe/quer)
3. Action (o que o usuario faz)
4. Feedback (resposta imediata do sistema)
5. Outcome (o que o usuario conseguiu)
6. Next Step (o que vem depois naturalmente)
```

## 精英级引导流程（前5分钟）

```
Tela 1: Promessa — "O que voce vai conseguir"
  - Uma frase impactante
  - Uma imagem que mostra o resultado
  - CTA: "Comecar" (nao "Criar conta")

Tela 2: Acao imediata — primeiro valor antes de cadastro
  - Deixe o usuario experimentar algo real
  - Formulario minimo (email apenas)
  - Progresso visivel (1 de 3)

Tela 3: Personalizacao — "Me conte sobre voce"
  - Max 3 perguntas
  - Visual, nao texto
  - Pula disponivel sempre

Tela 4: Momento Aha — primeiro sucesso real
  - O usuario faz algo que funciona
  - Celebracao genuina (nao excessiva)
  - "Voce acabou de [acao de valor]"
```

## 令人愉悦的空状态

```
Nao mostre: "Nenhum item encontrado"
Mostre:
  - Ilustracao contextual
  - Mensagem de oportunidade: "Ainda nao ha [X]. Crie o primeiro!"
  - CTA primario
  - Talvez: dica de como comecar
```

---

## 语音UI的独特原则

1. **零视觉负荷** — 用户看不到任何东西（只能听到）
2. **轻松撤销** — "撤销"始终可用
3. **可选确认** — 仅用于不可逆操作
4. **响应多样性** — 永远不会重复同一句话
5. **沉默也可以** — 在询问是否需要帮助前暂停2秒

## 语音响应结构

```
[Hook opcional] + [Resposta core] + [Acao ou pergunta]

Ruim: "Desculpe, nao entendi o que voce disse. Pode repetir?"
Bom:  "Nao captei bem. Pode repetir de outro jeito?"

Ruim: "Claro! Posso ajudar com isso. A resposta para sua pergunta e..."
Bom:  "A resposta e: [resposta direta]"
```

## Auri交互脚本

```
Primeiro uso:
"Oi! Sou a Auri. Pode me perguntar qualquer coisa — de decisoes de negocio
a ideias criativas. Como posso ajudar hoje?"

Retorno (usuario ja conhecido):
"Bem-vindo de volta! Onde paramos foi em [topico]. Quer continuar?"

Nao entendeu:
"Nao peguei bem. Tenta de outro jeito?"

Encerramento:
"Qualquer coisa, e so chamar. Ate logo!"
```

---

## 建设性批评框架

```
1. OBSERVACAO: O que eu vejo (sem julgamento)
   "Noto que o botao principal esta no canto inferior direito"

2. PRINCIPIO: Qual principio esta sendo testado
   "Hierarquia visual e posicionamento de CTA primario"

3. IMPACTO: O que isso causa ao usuario
   "Usuarios que usam o polegar precisam esticar para alcanca-lo"

4. ALTERNATIVA: Sugestao construtiva
   "Considerar posicionar acima do fold, centralizado"

5. TRADE-OFF: O que se perde/ganha
   "Mais acessivel, mas perde area para conteudo"
```

## UI评审检查清单

- [ ] 清晰的视觉层次（眼睛知道该看哪里）
- [ ] 合适的对比度（WCAG AA：文本4.5:1）
- [ ] 最小触摸尺寸（移动端44x44px）
- [ ] 与设计系统的一致性
- [ ] 已定义的交互状态（hover/active/disabled/focus）
- [ ] 响应式设计（移动优先）
- [ ] 加载状态和空状态
- [ ] 有用的错误处理信息
- [ ] 无障碍访问（标签、ARIA角色、键盘导航）
- [ ] 感知性能（骨架屏、乐观UI）

---

## 视觉概念

Auri是**带有温暖人性的智能**。它不是机器人——而是一个存在。
视觉身份应该传达：平易近人的精致感。

## 主调色板

```
Roxo Auri:     #6C63FF  — identidade, inteligencia, inovacao
Rosa Auri:     #FF6B9D  — calor, empatia, humanidade
Branco Puro:   #FFFFFF  — clareza, espaco, respiro
Grafite Suave: #1A1A2E  — autoridade, profundidade, noite
```

## 字体设计

```
Display/Titulos: Inter (ou SF Pro para Apple) — Bold 700
Corpo de texto:  Inter Regular 400 — linha 1.6
Mono/Codigo:     JetBrains Mono — para elementos tecnicos
```

## Logo概念

```
Forma: Onda de audio estilizada formando a letra "A"
Cor: Gradiente roxo → rosa (esquerda para direita)
Espaco negativo: Sugestao de microfone ou ear
Versao dark/light: Ambas definidas
Tamanho minimo: 24px (icone), 120px (lockup completo)
```

---

## 设计工具栈

| 工具 | 用途 |
|------|------|
| Figma | UI设计、原型制作、交付 |
| FigJam | 用户旅程、工作坊、创意构思 |
| Zeroheight | 设计系统文档 |
| Lottie | 动画（从After Effects/Figma导出） |
| Mobbin | UI模式参考 |
| Screenlane | 真实UI灵感 |

## 设计冲刺流程（5天）

```
Segunda: Entender — pesquisa, user interviews, definir o problema
Terca:   Divergir — crazy 8s, sketches individuais, lightning demos
Quarta:  Decidir — vote, storyboard, decisao final
Quinta:  Prototipar — prototipo de alta fidelidade no Figma
Sexta:   Testar — 5 usuarios, insights, iterar
```

---

## 8. 命令

| 命令 | 作用 |
|------|------|
| `/design-critique` | 结构化的设计评审 |
| `/design-tokens` | 为项目生成设计令牌 |
| `/ux-flow` | 映射用户体验流程 |
| `/voice-ux` | 语音交互设计 |
| `/onboarding` | 创建引导流程 |
| `/design-system` | 构建完整的设计系统 |
| `/accessibility` | 无障碍访问审计 |
| `/visual-identity` | 定义产品视觉身份 |

## 最佳实践

- 提供清晰、具体的项目背景和需求
- 在应用到生产代码前审查所有建议
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于超出其领域专长的任务
- 在不了解具体上下文的情况下应用建议
- 没有提供足够的项目背景以进行准确分析

## 相关技能

- `analytics-product` - 增强分析的互补技能
- `growth-engine` - 增强分析的互补技能
- `monetization` - 增强分析的互补技能
- `product-inventor` - 增强分析的互补技能

## 限制条件
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来寻求澄清。