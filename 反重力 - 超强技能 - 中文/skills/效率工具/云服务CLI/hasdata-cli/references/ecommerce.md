# 电商参考

子命令：`amazon-search`、`amazon-product`、`amazon-seller`、`amazon-seller-products`、`shopify-products`、`shopify-collections`。每个 5 积分。

---

## amazon-search

```bash
hasdata amazon-search --q "wireless earbuds" [--domain amazon.com] --raw | jq '.results[]'
```

- `--q TEXT`（必填）
- `--domain amazon.com|amazon.co.uk|amazon.de|amazon.in|amazon.co.jp|amazon.fr|amazon.it|amazon.es|amazon.com.br|amazon.com.mx|amazon.ca|amazon.com.au`
- `--page N` ——分页
- `--sort featured|price-asc-rank|price-desc-rank|review-rank|date-desc-rank`
- `--node ID` ——限定到品类节点
- `--customer-reviews` ——仅含评论的商品

每条结果字段：`asin`、`title`、`price`、`link`、`image`、`rating`、`reviews_count`、`prime`。

## amazon-product

```bash
hasdata amazon-product --asin B08N5WRWNW [--domain amazon.com] --raw | jq .
```

- `--asin ASIN`（必填）
- `--domain` 同上
- `--include-reviews` ——附带首页评论
- `--include-html` ——除解析数据外返回原始 HTML

返回：title、price、availability、features、descriptions、variants、images、ratings、top reviews、A+ content。

## amazon-seller

```bash
hasdata amazon-seller --seller-id A1234567890ABC [--domain amazon.com] --raw
```

卖家资料：name、ratings、review count、returns policy、shipping policy、"About" content。

## amazon-seller-products

```bash
hasdata amazon-seller-products --seller-id A1234567890ABC [--domain amazon.com] [--page 1] --raw
```

某卖家全部商品的列表——适用于竞品分析或店铺全量抓取。

---

## shopify-products

```bash
hasdata shopify-products --url "https://store.example.com" [--page 1] --raw | jq '.products[]'
```

可作用于任意 Shopify 店铺（查询其公开的 `/products.json` 风格端点）。返回 title、vendor、product_type、variants[]（含价格、SKU、库存）、images、tags、handle。

## shopify-collections

```bash
hasdata shopify-collections --url "https://store.example.com" --raw | jq '.collections[]'
```

要深入某个集合，给 URL 追加 `/collections/SLUG`，或使用这里返回的 collection handle。

---

## 非显式用例

- **跨市场价格套利** ——同一 `--asin` 跨 `--domain amazon.com|amazon.co.uk|amazon.de` 展示货币标准化后的地区差价；对灰色市场转卖和跨境买家有用。
- **"这个商品还在售吗？"** ——`amazon-product --asin X --raw | jq '.availability'`。避免基于过时训练数据瞎答。
- **变体矩阵导出** ——`amazon-product --asin X --raw | jq '.variants[] | {asin, color, size, price}'` 返回完整颜色/尺寸/等全维度网格及当前价格。
- **假货链接识别** ——`amazon-search --q "BRAND PRODUCT" --raw`，再检查 `.results[].seller_name` 是否为非授权卖家；进一步用 `amazon-seller` 查其全部商品。
- **店铺目录** ——`amazon-seller-products --seller-id X --page 1..N` 翻页抓取卖家全部目录；适合竞品分析或对供应商做尽调。
- **"X 类目里卖得最好的是什么？"** ——`amazon-search --q "CATEGORY KEYWORD" --sort featured` 返回亚马逊官方排序（按评论加权用 `--sort review-rank`）。
- **Shopify 店铺线索增强** ——`shopify-products --url store.example.com --raw` 暴露 vendor 名称、tags、product types、SKU——对竞品产品线盘点有用。
- **库存检查** ——`shopify-products` 返回每个变体的 `available` 布尔值；可以驱动"到货通知"功能而不必爬购物车 UI。
- **降价监控** ——每天定时跑 `amazon-product --asin X`，把 `.price` 落盘；变化 > N% 时告警。
- **A/B 测试探测** ——同一 `--asin` 通过两个不同的 `--proxy-country`（若 `amazon-product` 不支持则改用 web-scraping 回退）有时会看到不同的价格/标题——因为有 A/B 测试。
- **礼品卡/优惠券挖掘** ——`google-shopping --q "PRODUCT"` 经常能找到亚马逊不展示的返点卖家。
- **情绪板用的商品图** ——`amazon-product --asin X --raw | jq -r '.images[]'` 返回的 CDN URL 可单独下载。
- **评论摘要对比** ——`amazon-product --asin X --include-reviews --raw | jq '.reviews[] | {rating, title, body}'` 不必爬评论页也能拿到快速情感样本。
- **为广告生成 Shopify 商品 feed** ——`shopify-products --url X --raw | jq -c '.products[] | {id, title, price: .variants[0].price, url: ("https://" + $store + "/products/" + .handle)}'`。

## 常见模式

```bash
# Price tracking — pull current price for a known ASIN
hasdata amazon-product --asin "$ASIN" --raw | jq '.price'

# Product discovery → details fan-out
hasdata amazon-search --q "$Q" --raw \
  | jq -r '.results[].asin' \
  | head -5 \
  | xargs -I{} hasdata amazon-product --asin {} --raw

# Compare across marketplaces
for d in amazon.com amazon.co.uk amazon.de; do
  echo "=== $d ==="
  hasdata amazon-product --asin "$ASIN" --domain "$d" --raw \
    | jq '{currency: .currency, price: .price}'
done
```