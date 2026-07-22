# Playwright Java – Page Object 模式

## 组件模式（可复用的子 Page Object）

对于重复出现的 UI 组件（导航栏、弹窗、表格），创建 Component 类：

```java
// 可复用的表格组件 — 传入定位器根节点
public class DataTable extends BasePage {
    private final Locator tableRoot;

    public DataTable(Page page, Locator tableRoot) {
        super(page);
        this.tableRoot = tableRoot;
    }

    public int getRowCount() {
        return tableRoot.locator("tbody tr").count();
    }

    public String getCellValue(int row, int col) {
        return tableRoot.locator("tbody tr")
                        .nth(row)
                        .locator("td")
                        .nth(col)
                        .innerText();
    }

    public void clickRowAction(int row, String actionLabel) {
        tableRoot.locator("tbody tr")
                 .nth(row)
                 .getByRole(AriaRole.BUTTON, new Locator.GetByRoleOptions().setName(actionLabel))
                 .click();
    }

    public DataTable sortByColumn(String columnHeader) {
        tableRoot.getByRole(AriaRole.COLUMNHEADER,
                new Locator.GetByRoleOptions().setName(columnHeader)).click();
        return this;
    }
}

// 在 Page Object 中使用：
public class UsersPage extends BasePage {
    public final DataTable usersTable;
    private final Locator searchInput;
    private final Locator addUserButton;

    public UsersPage(Page page) {
        super(page);
        usersTable    = new DataTable(page, page.locator("#users-table"));
        searchInput   = page.getByPlaceholder("Search users…");
        addUserButton = page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Add User"));
    }

    @Override protected String getUrl() { return "/admin/users"; }

    public UsersPage searchFor(String query) {
        searchInput.fill(query);
        searchInput.press("Enter");
        page.waitForResponse("**/api/users**", () -> {});
        return this;
    }
}
```

---

## 弹窗 / 对话框组件

```java
public class ConfirmDialog extends BasePage {
    private final Locator dialog;
    private final Locator confirmButton;
    private final Locator cancelButton;
    private final Locator titleText;

    public ConfirmDialog(Page page) {
        super(page);
        dialog        = page.getByRole(AriaRole.DIALOG);
        confirmButton = dialog.getByRole(AriaRole.BUTTON, new Locator.GetByRoleOptions().setName("Confirm"));
        cancelButton  = dialog.getByRole(AriaRole.BUTTON, new Locator.GetByRoleOptions().setName("Cancel"));
        titleText     = dialog.getByRole(AriaRole.HEADING);
    }

    public void waitForOpen() {
        dialog.waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.VISIBLE));
    }

    public void confirm() { confirmButton.click(); dialog.waitFor(
        new Locator.WaitForOptions().setState(WaitForSelectorState.HIDDEN)); }

    public void cancel()  { cancelButton.click(); }

    public String getTitle() { return titleText.innerText(); }

    @Override protected String getUrl() { return ""; }
}
```

---

## 导航链模式

页面方法应**返回下一个页面对象** — 导航操作永远不要返回 `void`：

```java
// 正确 — 支持流式链式调用
public DashboardPage loginAs(String email, String password) {
    fill(emailInput, email);
    fill(passwordInput, password);
    clickAndWaitForNav(submitButton);
    return new DashboardPage(page);
}

// 使用方式
DashboardPage dash = new LoginPage(page)
    .navigate()
    .loginAs("user@test.com", "secret")
    .navigateTo(OrdersPage::new)  // 辅助方法减少样板代码
    .filterByStatus("PENDING");
```

---

## 动态定位器

针对结构相同的列表项：

```java
// 通过标题定位卡片
public Locator getProductCard(String productName) {
    return page.locator(".product-card")
               .filter(new Locator.FilterOptions().setHasText(productName));
}

// 等待表格中出现特定行
public void waitForOrderRow(String orderId) {
    page.locator("tr[data-order-id='" + orderId + "']")
        .waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.VISIBLE)
                .setTimeout(15_000));
}
```

---

## 下拉框 / Select 处理

```java
// 原生 <select>
page.selectOption("#country-select", "India");

// 自定义下拉框（非原生）
public void selectCountry(String countryName) {
    page.getByLabel("Country").click();
    page.getByRole(AriaRole.LISTBOX)
        .getByText(countryName)
        .click();
}
```

---

## 文件上传

```java
// 标准文件输入
page.setInputFiles("#file-upload", Paths.get("src/test/resources/testdata/sample.pdf"));

// 拖拽上传区域
page.locator(".upload-zone").setInputFiles(Paths.get("src/test/resources/testdata/sample.pdf"));

// 多文件上传
page.setInputFiles("#file-upload", new Path[]{
    Paths.get("file1.png"),
    Paths.get("file2.png")
});
```

---

## 下载处理

```java
Download download = page.waitForDownload(() ->
    page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Export CSV")).click()
);
Path downloadedFile = download.path();
assertThat(downloadedFile.toFile()).exists();
```

---

## 悬停与工具提示验证

```java
page.getByTestId("info-icon").hover();
Locator tooltip = page.getByRole(AriaRole.TOOLTIP);
tooltip.waitFor();
assertThat(tooltip).hasText("This field is required");
```

---

## 等待策略（防抖）

```java
// 操作后等待 API 响应
page.waitForResponse(resp -> resp.url().contains("/api/search") && resp.status() == 200,
    () -> searchInput.fill("test"));

// 等待网络空闲（复杂渲染后使用）
page.waitForLoadState(LoadState.NETWORKIDLE);

// 等待元素数量稳定
Locator rows = page.locator("tbody tr");
rows.first().waitFor(); // 等待至少出现一个
assertThat(rows).hasCount(10);

// 轮询自定义条件
Assertions.assertDoesNotThrow(() -> {
    page.waitForCondition(() -> page.locator(".spinner").count() == 0);
});
```
