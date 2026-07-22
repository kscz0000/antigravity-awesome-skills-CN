# 巴西商业委员会 — 拍卖师URL及采集状态

包含全部27个商业委员会及其拍卖师网站的参考表。
**最后更新：** 2026-02-25

| UF | 委员会 | 拍卖师URL | 方法 | 状态 |
|----|-------|---------------|--------|--------|
| SP | JUCESP | https://www.institucional.jucesp.sp.gov.br/tradutores-leiloeiros.html | httpx+BS4 | 定制 |
| RJ | JUCERJA | https://www.jucerja.rj.gov.br/AuxiliaresComercio/Leiloeiros | PLAYWRIGHT | 定制 |
| MG | JUCEMG | https://jucemg.mg.gov.br/pagina/139/leiloeiros-oficiais | httpx+BS4 | 定制 |
| ES | JUCEES | https://jucees.es.gov.br/leiloeiros | httpx+BS4 | 通用 |
| RS | JUCISRS | https://sistemas.jucisrs.rs.gov.br/leiloeiros/ | PLAYWRIGHT | 定制（旧域名：jucers.rs.gov.br 已废弃） |
| PR | JUCEPAR | https://www.juntacomercial.pr.gov.br/Pagina/LEILOEIROS-OFICIAIS | httpx+BS4 | 定制（从 jucepar.pr.gov.br 迁移） |
| SC | JUCESC | https://leiloeiros.jucesc.sc.gov.br/site/ | httpx+BS4 | 定制（专用子域名） |
| BA | JUCEB | https://www.ba.gov.br/juceb/home/matriculas-e-carteira-profissional/leiloeiros | httpx+BS4 | 定制（从 juceb.ba.gov.br 迁移） |
| PE | JUCEPE | https://portal.jucepe.pe.gov.br/leiloeiros | PLAYWRIGHT | 定制（SPA — 从 jucepe.pe.gov.br 迁移） |
| CE | JUCEC | https://www.jucec.ce.gov.br/leiloeiros/ | httpx+BS4 | 定制 |
| MA | JUCEMA | http://www.jucema.ma.gov.br/leiloeiros | httpx+多URL | 定制（尝试多个URL） |
| PI | JUCEPI | https://portal.pi.gov.br/jucepi/leiloeiro-oficial/ | httpx+BS4 | 定制（迁移至州门户） |
| RN | JUCERN | http://www.jucern.rn.gov.br/Conteudo.asp?TRAN=ITEM&TARG=8695&ACT=&PAGE=0&PARM=&LBL=Leiloeiros | httpx+BS4 | 定制（HTTP，查询字符串） |
| PB | JUCEP | https://jucep.pb.gov.br/contatos/leiloeiros | httpx+BS4 | 定制（域名迁移至 jucep.pb.gov.br） |
| AL | JUCEAL | http://www.juceal.al.gov.br/servicos/leiloeiros | httpx+BS4 | 定制（URL：/servicos/leiloeiros） |
| SE | JUCESE | https://jucese.se.gov.br/leiloeiros/ | httpx+BS4 | 通用 |
| DF | JUCIS-DF | https://jucis.df.gov.br/leiloeiros/ | httpx+BS4 | 定制 |
| GO | JUCEG | https://goias.gov.br/juceg/ | httpx+BS4 | 通用 |
| MT | JUCEMAT | https://www.jucemat.mt.gov.br/leiloeiros | httpx+BS4 | 通用 |
| MS | JUCEMS | https://www.jucems.ms.gov.br/empresas/controles-especiais/agentes-auxiliares/leiloeiros/ | httpx+BS4 | 通用（完整路径URL） |
| PA | JUCEPA | https://www.jucepa.pa.gov.br/node/171 | httpx+BS4 | 定制（Drupal节点ID） |
| AM | JUCEA | https://www.jucea.am.gov.br/leiloeiros/ | httpx+BS4 | 通用 |
| RO | JUCER | https://rondonia.ro.gov.br/jucer/lista-de-leiloeiros-oficiais/ | httpx+BS4 | 定制（迁移至州门户） |
| RR | JUCERR | https://jucerr.rr.gov.br/leiloeiros/ | httpx+BS4 | 通用 |
| AP | JUCAP | http://www.jucap.ap.gov.br/leiloeiros | httpx (verify=False) | 定制（TLS证书无效） |
| AC | JUCEAC | https://juceac.ac.gov.br/leiloeiro/ | httpx+BS4 | 定制（URL：/leiloeiro/ 单数形式） |
| TO | JUCETINS | https://www.to.gov.br/jucetins/leiloeiros/152aezl6blm0 | httpx+BS4 | 定制（旧域名：juceto.to.gov.br 已废弃） |

## 状态说明

- **定制**：针对页面格式编写的专用Scraper
- **通用**：使用 `GenericJuntaScraper` 自动检测表格/列表
- **PLAYWRIGHT**：需要JS渲染（无头浏览器）
- **不可用**：网站离线或无拍卖师页面（已记录在日志中）

## 已确认的域名迁移（2025-2026）

| 旧地址 | 新地址 | 委员会 |
|--------|------|-------|
| jucers.rs.gov.br | jucisrs.rs.gov.br + sistemas.jucisrs.rs.gov.br | JUCISRS（更名） |
| jucepar.pr.gov.br | juntacomercial.pr.gov.br | JUCEPAR |
| jucesc.sc.gov.br/index.php | leiloeiros.jucesc.sc.gov.br/site/ | JUCESC |
| juceb.ba.gov.br | ba.gov.br/juceb | JUCEB |
| jucepe.pe.gov.br | portal.jucepe.pe.gov.br | JUCEPE |
| jucepa.pa.gov.br/index.php | jucepa.pa.gov.br/node/171 | JUCEPA |
| jucepi.pi.gov.br | portal.pi.gov.br/jucepi | JUCEPI |
| jucepb.pb.gov.br | jucep.pb.gov.br | JUCEP（更名） |
| juceal.al.gov.br/leiloeiros | juceal.al.gov.br/servicos/leiloeiros | JUCEAL |
| jucer.ro.gov.br | rondonia.ro.gov.br/jucer | JUCER |
| juceac.ac.gov.br/leiloeiros | juceac.ac.gov.br/leiloeiro/ | JUCEAC |
| juceto.to.gov.br | to.gov.br/jucetins | JUCETINS（更名） |
| jucers.ms.gov.br/leiloeiros | jucems.ms.gov.br/empresas/controles-especiais/agentes-auxiliares/leiloeiros/ | JUCEMS |

## 备用数据源

如某个网站不可用，可检查：
- **DREI**：https://www.gov.br/empresas-e-negocios/pt-br/drei/tradutores-e-leiloeiros
- **BomValor**：https://osleiloeiros.bomvalor.com.br/
- **InnLei**：https://innlei.org.br/juntas-comerciais
- **FENAJU**：https://www.fenaju.org.br/federados

## 与Web-Scraper技能的集成

对于采集率低或网站有问题的州，`web_scraper_fallback.py` 会自动调用web-scraper技能进行智能补充提取。

执行：`python scripts/web_scraper_fallback.py --estado MA RN AP`

## 如何更新此文件

每次采集后，检查 `data/scraping_log.json`：
- 状态为 `VAZIO` 的州 → 调查URL是否变更
- 状态为 `ERRO` 的州 → 可能需要使用Playwright
- 必要时更新 `方法` 和 `URL` 列
