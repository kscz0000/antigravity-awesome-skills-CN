---
title: 在类上使用 DBOS 装饰器
impact: MEDIUM
impactDescription: 支持基于类实例的有状态工作流模式
tags: classes, dbos_class, instance, oop
---

## 在类上使用 DBOS 装饰器

DBOS 装饰器可用于类方法。工作流类必须继承自 `DBOSConfiguredInstance`。

**错误（缺少类设置）：**

```python
class MyService:
    def __init__(self, url):
        self.url = url

    @DBOS.workflow()  # 没有正确的设置将无法工作
    def fetch_data(self):
        return self.fetch()
```

**正确（正确的类设置）：**

```python
from dbos import DBOS, DBOSConfiguredInstance

@DBOS.dbos_class()
class URLFetcher(DBOSConfiguredInstance):
    def __init__(self, url: str):
        self.url = url
        # instance_name 必须唯一并传入 super()
        super().__init__(instance_name=url)

    @DBOS.workflow()
    def fetch_workflow(self):
        return self.fetch_url()

    @DBOS.step()
    def fetch_url(self):
        return requests.get(self.url).text

# 必须在 DBOS.launch() 之前实例化
example_fetcher = URLFetcher("https://example.com")
api_fetcher = URLFetcher("https://api.example.com")

if __name__ == "__main__":
    DBOS.launch()
    print(example_fetcher.fetch_workflow())
```

要求：
- 类必须使用 `@DBOS.dbos_class()` 装饰
- 类必须继承自 `DBOSConfiguredInstance`
- `instance_name` 必须唯一并通过 `super().__init__()` 传入
- 所有实例必须在 `DBOS.launch()` 之前创建

步骤可以添加到任何类上，而无需满足这些要求。

参考：[Python 类](https://docs.dbos.dev/python/tutorials/classes)
