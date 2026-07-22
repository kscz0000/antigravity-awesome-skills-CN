---
name: sankhya-dashboard-html-jsp-custom-best-pratices
description: "当用户询问使用HTML、JSP、Java和SQL创建或修复Sankhya仪表盘的模式、最佳实践、创建或修复时，应使用此技能。触发词：Sankhya仪表盘、HTML、JSP、Java、SQL、最佳实践、仪表盘创建、仪表盘修复、Sankhya BI、JSP模式。"
category: code
risk: safe
source: community
tags: [sankhya, dashboard, jsp, html, sql, best-practices]
date_added: "2026-03-10"
---

# sankhya-dashboard-html-jsp-custom-best-pratices

## 目的

提供一份综合指南，涵盖在Sankhya生态系统（JSP/HTML/Java）中创建和维护仪表盘、SQL查询、BI参数化和UI/UX的模式与最佳实践。

## 何时使用此技能

当出现以下情况时，应使用此技能：
- 用户询问“Sankhya最佳实践”或“Sankhya仪表盘最佳实践”。
- 用户提到“Sankhya仪表盘”或正在开发Sankhya BI仪表盘。
- 用户询问任何与“Sankhya”相关的内容。
- 用户希望创建或修改Sankhya仪表盘的代码文件。

## 核心能力

1. **代码生成与审查**：应用JSP/JSTL模式和服务端组织结构，以减少编译错误和渲染失败。
2. **视觉一致性**：使用预定义的CSS令牌，在BI组件中标准化视觉标识。
3. **数据库探索**：构建数据探索查询，以优化性能并正确映射Sankhya实体。
4. **BI构建指南**：在BI中使用HTML5组件流程，确保正确的渲染、响应性和导航。

## 模式

### 代码最佳实践
应用JSP/JSTL模式和服务端组织结构，以减少仪表盘/界面的编译错误、渲染失败和回归问题。

**实施指南**
- 在文件顶部声明必需的JSP指令和标签库。
- 强制设置`isELIgnored="false"`以启用渲染时的`${...}`表达式。
- 在Sankhya生态系统中，优先使用`core_rt`作为JSTL核心标签库。
- 避免在JSP中使用Java脚本片段；使用JSTL（`c:if`、`c:choose`、`c:forEach`）。
- 将业务逻辑模块化（分层/服务），避免耦合在单个文件中。
- 避免硬编码凭据、敏感URL和令牌。
- 建模UI的全局状态（数据、过滤器、排序、活动标签页），并在新加载前重置状态。
- 将显示偏好持久化到`localStorage`（列顺序和排序）。
- 为重量级标签页/模态框实现按需加载（懒加载），以减少初始加载时间。
- **参数防护**：始终通过`c:set`为URL参数定义默认值（回退值），以避免Sankhya Java服务器返回500错误。
- **分层分离（JSP vs JS）**：避免在`<script>`块中直接注入JSP标签。使用隐藏的HTML容器将数据传递给JavaScript，以保持代码编辑器的健康（IDE语法检查）。

> 下方的表名和字段名仅为示例，可能因实例实现而异。

```jsp
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" isELIgnored="false" %>
<%@ taglib prefix="snk" uri="/WEB-INF/tld/sankhyaUtil.tld" %>
<%@ taglib uri="http://java.sun.com/jstl/core_rt" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %>
<snk:load />
```

**仪表盘/小部件中的资源加载**
- 使用`contextPath` + `BASE_FOLDER`引用文件。
- 在次级层级（`openLevel`）中，保持绝对路径以避免解析中断。

```html
<script src="${pageContext.request.contextPath}/${BASE_FOLDER}/js/app.js"></script>
<link rel="stylesheet" href="${pageContext.request.contextPath}/${BASE_FOLDER}/css/style.css" />
```

**安全使用`snk:query`**
- 遍历`query.rows`（而非根对象）。
- 使用`empty query.rows`测试空结果。

```jsp
<snk:query var="qDados">
    SELECT CAB.NUNOTA, CAB.CODPARC
      FROM TGFCAB CAB
</snk:query>

<c:choose>
    <c:when test="${empty qDados.rows}">
        <span>无结果</span>
    </c:when>
    <c:otherwise>
        <c:forEach var="linha" items="${qDados.rows}">
            ${linha.NUNOTA}
        </c:forEach>
    </c:otherwise>
</c:choose>
```

**SQL查询前的参数净化**
- 标准化输入值。
- 在注入查询前移除引号（`"`和`&quot;`）。
- 定义安全的回退值以避免无效SQL。

```jsp
<c:set var="raw_codusu" value="${empty param.P_CODUSU ? '0' : param.P_CODUSU}" />
<c:set var="codusu_limpo" value="${fn:replace(raw_codusu, '\"', '')}" />
<c:set var="codusu_limpo" value="${fn:replace(codusu_limpo, '&quot;', '')}" />
<c:set var="codusu_seguro" value="${empty codusu_limpo ? '0' : codusu_limpo}" />

<snk:query var="qAcessos">
    SELECT CODUSU, NOMEUSU
      FROM TSIUSU
     WHERE CODUSU = :codusu_seguro
</snk:query>
```

**单一仪表盘中的界面状态与懒加载**
- 定义全局列表以便在KPI、图表、表格和模态框中复用。
- 为每个标签页保存加载标志，以避免不必要的重复查询。
- 在事务性更新后重新加载数据并恢复上下文（产品/标签页）。

```js
var dadosGlobais = [];
var produtoAtual = null;
var abaCarregada = {};

function abrirDetalhe(dado) {
  produtoAtual = dado;
  abaCarregada = {};
  trocarAba("estoque");
}

function trocarAba(aba) {
  if (aba === "estoque" && !abaCarregada.estoque) carregarAbaEstoque(produtoAtual.CODPROD);
  if (aba === "pedidos" && !abaCarregada.pedidos) carregarAbaPedidos(produtoAtual.CODPROD);
  if (aba === "parceiros" && !abaCarregada.parceiros) carregarAbaParceiros(produtoAtual.CODPROD);
}
```
**参数防护与分层分离示例**

```jsp
<%-- 1. 文件顶部的参数防护 --%>
<c:set var="v_salesagent" value="${empty param.SALESAGENT ? '0' : param.SALESAGENT}" />

<%-- 2. 用于数据的隐藏容器（JSP与JS分离） --%>
<div id="data-container" style="display:none;">
    [
    <c:forEach var="row" items="${qDados.rows}" varStatus="loop">
        { "id": ${row.ID}, "nome": "${fn:replace(row.NOME, '"', '\\"')}" }${!loop.last ? ',' : ''}
    </c:forEach>
    ]
</div>

<script>
    // 3. JS仅从容器读取数据
    const rawData = document.getElementById('data-container').textContent.trim();
    const myData = rawData ? JSON.parse(rawData) : [];
</script>
```

### 视觉标识（颜色）
在BI组件中标准化视觉标识，以确保HTML5小部件、表格和指标之间的一致性。

**UI/UX指南**
- 通过令牌（`--color-*`）定义调色板，以避免分散的颜色值。
- 优先确保文本与背景之间的最小对比度（操作可读性）。
- 保持视觉语义一致性：成功、警告、错误、中性。
- 必要时允许通过SQL数据（`BKCOLOR`、`FGCOLOR`）进行覆盖。
- 对于高阅读量的宽表格，使用粘性表头和固定列。
- 通过CSS类区分行状态（已批准、部分、历史、关键），以便快速操作阅读。

> 下方的表名和字段名仅为示例，可能因实例实现而异。

```html
<style>
  :root {
    --color-bg: #F5F7FA;
    --color-surface: #FFFFFF;
    --color-text: #1F2937;
    --color-success: #1A7F37;
    --color-warning: #B26A00;
    --color-danger: #B42318;
    --color-accent: #0E5A8A;
  }

  .card {
    background: var(--color-surface);
    color: var(--color-text);
    border-radius: 8px;
    padding: 12px;
  }
</style>
```

```sql
SELECT
    V.CODMETA,
    V.VALOR_ATUAL,
    V.VALOR_META,
    CASE WHEN V.VALOR_ATUAL >= V.VALOR_META THEN '#1A7F37' ELSE '#B42318' END AS BKCOLOR,
    '#FFFFFF' AS FGCOLOR
FROM AD_DADOS_VENDA V
```

```html
<style>
  #tblDados thead th { position: sticky; top: 0; z-index: 4; }
  #tblDados .col-fixa-1 { position: sticky; left: 0; z-index: 3; }
  #tblDados .col-fixa-2 { position: sticky; left: var(--fix-col-1-width); z-index: 2; }
  .row-aprovacao td { background: #ffe8cc; color: #7a3a00; }
  .row-parcial td { background: #fff4c4; color: #5e4c00; }
</style>
```

### 查询与数据库探索
构建数据探索查询，重点关注性能、可读性和Sankhya实体的正确映射。

**探索最佳实践（DBExplorer）**
- 使用DBExplorer检查表、字段、索引、视图和存储过程。
- 遵守配置的返回限制（例如`DBEXPMAXROW`），以避免过载。
- 避免在包含大字段（BLOB/CLOB）的表中使用`SELECT *`。

**生态系统核心映射**
- 数据字典：`TDDTAB`、`TDDCAM`、`TDDOPC`、`TDDINS`、`TDDLIG`。
- 商业/财务：`TGFCAB`、`TGFITE`、`TGFTOP`、`TGFPAR`、`TGFPRO`、`TGFEST`、`TGFVAR`。
- 安全/访问：`TSIUSU`、`TSIGRU`、`TSIACI`、`TSIIMP`。

**推荐的SQL模式**
- 对于版本化的TOP，关联`CODTIPOPER`与更改日期（`DHTIPOPER`/`DHALTER`）。
- 对于可选过滤器，使用模式`(... = :P_PARAM OR :P_PARAM IS NULL)`。
- 始终参数化（避免用户输入的字面量）。

> 下方的表名和字段名仅为示例，可能因实例实现而异。

```sql
SELECT
    CAB.NUNOTA,
    CAB.CODPARC,
    CAB.DTNEG,
    ITE.SEQUENCIA,
    ITE.CODPROD,
    (ITE.VLRTOT - ITE.VLRDESC) AS VLR_LIQUIDO
FROM TGFCAB CAB
JOIN TGFITE ITE
  ON ITE.NUNOTA = CAB.NUNOTA
JOIN TGFTOP TOP
  ON TOP.CODTIPOPER = CAB.CODTIPOPER
 AND TOP.DHALTER   = CAB.DHTIPOPER
WHERE (CAB.CODPARC = :P_CODPARC OR :P_CODPARC IS NULL)
  AND (CAB.CODVEND = :P_CODVEND OR :P_CODVEND IS NULL)
```

```sql
SELECT
    U.CODUSU,
    U.NOMEUSU,
    G.NOMEGRUPO,
    A.CODREL,
    I.NOME AS DESCRICAO_RECURSO,
    A.CONS,
    A.ALTERA
FROM TSIUSU U
JOIN TSIGRU G ON G.CODGRUPO = U.CODGRUPO
JOIN TSIACI A ON A.CODGRUPO = U.CODGRUPO
JOIN TSIIMP I ON I.CODREL = A.CODREL
WHERE U.CODUSU = :P_CODUSU
ORDER BY I.NOME
```

### BI构建器指南
在BI中应用HTML5组件开发流程，以确保渲染、响应性和层级间的导航。

**结构与发布**
- 将组件打包为`.zip`文件，以`index.html`作为主入口。
- 将静态资源组织在`assets/`目录中（CSS、JS、库、图片）。
- 根据需要使用XML/设计；当存在服务端预处理时，考虑使用JSP作为入口。

**数据流与参数**
- 根据复杂度定义SQL变量或BeanShell。
- 使用参数转换前缀：
  - `:` 用于标准绑定。
  - `:#` 用于字面替换（谨慎评估和验证）。
  - `:@` 用于`LIKE`等场景中的文本字面量。
- 对于广泛的多列表参数，使用`/*inCollection*/`。

> 下方的表名和字段名仅为示例，可能因实例实现而异。

```sql
SELECT
    C.CODCID,
    C.NOMECID,
    C.UF
FROM AD_TABELA_EXEMPLO C
WHERE /*inCollection*/ C.CODCID IN :P_CODCID /*inCollection*/
```

**响应性与生命周期**
- 当全局过滤器更改时，编程重新渲染。
- 避免在注入内容中完全依赖`DOMContentLoaded`。
- 应用异步初始化以确保元素可用。

```html
<script>
  function renderizarComponente(dados) {
    // 使用接收到的数据更新DOM、图表和KPI
  }

  function iniciar() {
    const dadosIniciais = window.snkBIData || [];
    renderizarComponente(dadosIniciais);
  }

  setTimeout(iniciar, 300);
</script>
```

**下钻与事件**
- 建模独立的层级（宏观 → 微观），使用显式参数。
- 避免在后续层级中出现空容器。
- 在层级之间使用上下文继承，以保留过滤器和导航。
- 实现点击操作以更新详情，并使用上下文键打开原生界面。

**多层导航（openLevel与上下文契约）**
- 在配置中定义层级常量（`NIVEL_RESUMO`、`NIVEL_DETALHE`、`NIVEL_ITEM`），以避免松散的字符串耦合。
- 将`openLevel`封装到按导航路由专用的函数中（例如：按销售人员打开详情，按合作伙伴打开项目）。
- 在层级之间传递上下文参数，使用显式契约（`ARG_*`用于键，`P_*`用于过滤器/时间段）。
- 在导航前验证`openLevel`和必需参数的可用性。
- 当上下文不允许打开层级时，在控制台/UI中应用错误回退。

```js
var cfg = window.DASH_CONFIG || {};
var NIVEL_DETALHE = cfg.NIVEL_DETALHE || "NIVEL_B";
var NIVEL_ITEM = cfg.NIVEL_ITEM || "NIVEL_C";

function abrirNivelDetalhe(codigoEntidade) {
  if (!codigoEntidade || typeof openLevel !== "function") return;
  openLevel(NIVEL_DETALHE, {
    ARG_CODENT: parseInt(codigoEntidade, 10),
    P_PERIODO_INI: cfg.P_PERIODO_INI || "",
    P_PERIODO_FIN: cfg.P_PERIODO_FIN || "",
    P_CODMETA: cfg.P_CODMETA || ""
  });
}

function abrirNivelItem(codigoEntidadeFilha) {
  if (!codigoEntidadeFilha || typeof openLevel !== "function") return;
  openLevel(NIVEL_ITEM, {
    ARG_CODENT_FILHA: parseInt(codigoEntidadeFilha, 10),
    P_PERIODO_INI: cfg.P_PERIODO_INI || "",
    P_PERIODO_FIN: cfg.P_PERIODO_FIN || "",
    P_CODMETA: cfg.P_CODMETA || ""
  });
}
```

**基于范围的访问安全与锁定**
- 在聚合数据前，通过用户-元/范围关系限制任何层级查询。
- 将安全谓词集中到`WHERE`子句构建函数中，以便在KPI、网格和图表中复用。
- 优先使用会话变量（`CODUSU_LOG`或等效的登录用户函数），以避免用户参数欺骗。
- 当关键参数缺失时（例如：时间段、目标、下钻实体），阻止加载。

> 下方的表名和字段名仅为示例，可能因实例实现而异。

```sql
SELECT
    M.CODMETA,
    M.CODENTIDADE,
    SUM(M.VLRPREV) AS VLR_PREV,
    SUM(M.VLRREAL) AS VLR_REAL
FROM AD_DADOS_META M
WHERE M.CODMETA = :P_CODMETA
  AND M.DTREF BETWEEN TO_DATE(:P_PERIODO_INI, 'DD/MM/YYYY')
                  AND TO_DATE(:P_PERIODO_FIN, 'DD/MM/YYYY')
  AND EXISTS (
      SELECT 1
      FROM AD_META_USUARIO_LIB L
      WHERE L.CODMETA = M.CODMETA
        AND L.CODUSU = STP_GET_CODUSULOGADO
  )
GROUP BY M.CODMETA, M.CODENTIDADE
```

**带展开/折叠的层级网格**
- 构建`filhosPorPai`映射和`nosExpandidos`状态，以实现树的增量渲染。
- 将高层级的非分析节点初始化为展开状态，以改善初始阅读。
- 在折叠的节点中，显示分析后代的聚合数据，以在不展开整棵树的情况下保持上下文。
- 在表头提供“全部展开”和“全部折叠”的快捷操作。
- 在文本过滤器中，包含找到节点的祖先节点，以保持层级可追溯性。

```js
var filhosPorPai = {};
var nosExpandidos = {};

function alternarNo(codNo) {
  var id = String(codNo);
  nosExpandidos[id] = !nosExpandidos[id];
  renderizarGrid();
}

function obterVisiveis(raiz) {
  var lista = [];
  function visitar(pai) {
    (filhosPorPai[pai] || []).forEach(function (no) {
      lista.push(no);
      if (nosExpandidos[String(no.CODNO)]) visitar(String(no.CODNO));
    });
  }
  visitar(String(raiz || ""));
  return lista;
}
```

**加载弹性**
- 将主要加载与补充加载（例如月度实际值）分离，不因次要故障阻塞主视图。
- 按组件处理数据缺失（`vazio`），而不破坏整个布局。
- 在重新创建图表实例前销毁旧实例，以避免内存泄漏和视觉重叠。
- 仅在打开对应标签页/视图时加载次要面板（按需加载）。

**层级内导航（单一JSP）**
- 将单一JSP视为导航外壳：主表格 + 详情模态框 + 内部标签页 + 辅助模态框。
- 在不切换Sankhya层级的情况下链接点击：KPI → 列表模态框，图表 → 表格过滤器，表格行 → 详情。
- 在详情中应用操作快捷方式，以在主键上下文中打开原生注册表。
- 通过点击遮罩层关闭模态框，以减少使用摩擦。

```js
function abrirTelaNativa(resourceIdBase64, pkObj) {
  var pk = btoa(JSON.stringify(pkObj));
  top.location.href = "/mge/system.jsp#app/" + resourceIdBase64 + "/" + pk + "&pk-refresh=" + Date.now();
}

function onKpiClick(lista) {
  abrirModalLista("Itens selecionados", "Navegação por atalho", lista);
}

function onGraficoClick(grupo) {
  filtrarTabelaPorGrupo(grupo);
}
```

**界面操作反馈**
- 在每个面板中显示明确的加载、空状态和错误状态。
- 在更新操作中，禁用确认按钮直到`executeQuery`返回。
- 成功后，重新加载数据并恢复先前的上下文（产品和活动标签页）。

**内部安全变量**
- 利用会话变量实现行级安全（`CODUSU_LOG`、`CODGRU_LOG`、`CODVEN_LOG`）。
- 在构建可视化前，按用户上下文限制数据。

## 局限性
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为替代环境特定的验证、测试或专家评审。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。