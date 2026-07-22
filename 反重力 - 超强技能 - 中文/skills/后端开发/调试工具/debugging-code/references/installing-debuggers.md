# 安装调试适配器

`dap` 依赖语言专属的调试适配器（后端）。很多 IDE 已经自带——**安装前先检查**。

---

## Python — debugpy

**检查：** `python3 -m debugpy --version`

**安装：** `pip install debugpy`

**虚拟环境：** `dap` 通过 `$VIRTUAL_ENV` 自动识别激活的 venv。
在跑 `dap debug` 之前先激活 venv（`source .venv/bin/activate`），或者传 `--python /path/to/venv/bin/python` 覆盖。如果两个都不做，`dap` 会回退到 PATH 上的 `python3`——那个可能没装 `debugpy`，也可能是错的解释器版本。

---

## Go — Delve

**检查：** `dlv version`

**安装：**
- macOS：`brew install delve`（或 `go install github.com/go-delve/delve/cmd/dlv@latest`）
- Linux：`go install github.com/go-delve/delve/cmd/dlv@latest`

macOS 注意：你可能需要 `sudo DevToolsSecurity -enable` 才能拿到调试权限。

---

## Node.js / TypeScript — js-debug

`dap` 会从常见位置自动发现 js-debug：
- VS Code 扩展（`~/.vscode/extensions/`）
- Cursor 扩展（`~/.cursor/extensions/`）
- 独立安装（`~/.dap-cli/js-debug/`）

**检查：** 在上述路径中找 js-debug，或直接跑 `dap debug --backend js-debug script.js` —— 失败再按下面安装。

**独立安装**（仅在以上位置都找不到时）：
```bash
DAP_VER=$(curl -fsSL https://api.github.com/repos/microsoft/vscode-js-debug/releases/latest | grep -o '"tag_name":"[^"]*"' | cut -d'"' -f4) && \
mkdir -p ~/.dap-cli/js-debug && \
curl -fsSL "https://github.com/microsoft/vscode-js-debug/releases/download/${DAP_VER}/js-debug-dap-${DAP_VER}.tar.gz" | tar -xz -C ~/.dap-cli/js-debug
```

也支持**浏览器端 JavaScript 的 Chrome DevTools 调试**。

---

## Rust / C / C++ — lldb-dap

**检查：** `lldb-dap --version`

**安装：**
- macOS：`brew install llvm`（需要 v18+）
- Linux：`apt install lldb`（或你的发行版对应的命令）

Homebrew 安装完成后，确保 Homebrew 的 `llvm` bin 目录在你的 PATH 上（例如 `export PATH="$(brew --prefix llvm)/bin:$PATH"`）。

---

## 已知坑

- **macOS 上的 lldb-dap**：Xcode Command Line Tools 自带的版本（v17）缺 `dap` 需要的 `--connection` 参数。请改用 Homebrew 的 `llvm` 包（v18+）。