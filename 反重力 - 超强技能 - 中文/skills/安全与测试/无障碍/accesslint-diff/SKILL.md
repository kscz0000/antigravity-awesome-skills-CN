---
name: accesslint-diff
description: "对比线上页面的无障碍违规情况与基线——默认比较未提交的变更（基于 stash），或传入 --branch [<name>] 与某个分支对比。仅报告新增的违规、已修复的违规以及既有的违规数量。需要完整审计（不做 diff）请使用 `scan`。触发词：accesslint diff、无障碍 diff、可访问性对比、a11y diff、违规对比、分支对比、stash diff。"
risk: safe
source: "https://github.com/AccessLint/skills"
date_added: "2026-06-02"
---

默认分支：!`git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null | sed 's|.*/||' || echo main`

只报告变化的部分。只定位，不修复。如果 `$ARGUMENTS` 里没有 URL，向用户索取。

解析 `$ARGUMENTS`：若包含 `--branch <name>` 则去掉 → 进入分支模式。若 `--branch` 后没有值，使用上面的默认分支。剩余部分即为 URL。

## 何时使用
- 任务与下面的描述匹配时使用本技能：对比线上页面的无障碍违规情况与基线——默认比较未提交的变更（基于 stash），或传入 --branch [<name>] 与某个分支对比。仅报告新增的违规、已修复的违规以及既有的违规数量。需要完整审计（不做 diff）请使用 `scan`。

## 1. 审计

```bash
PORT=$(npx -y @accesslint/chrome@latest ensure | node -e 'process.stdin.on("data",d=>process.stdout.write(""+JSON.parse(d).port))')
```

**Stash 模式**（默认——未提交的变更）。先告知用户：_"正在以 diff 模式运行——会暂存你的改动以采集基线，然后恢复。工作区会完整还原。"_ 如果 `git stash push` 失败，提示并退出。

```bash
git stash push -u -m "accesslint-diff-baseline"
npx -y @accesslint/cli@latest "<url>" --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --update-snapshot
git stash pop && sleep 2
npx -y @accesslint/cli@latest "<url>" --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --format json
```

**分支模式**（`--branch <name>`）。先告知用户：_"正在与 `<name>` 对比——会切换到该分支采集基线，然后恢复。工作区会完整还原。"_

切换分支会触发重新构建，但不会触发浏览器刷新——CLI 每次都会打开新标签页，因此始终读取当前构建产物。用 `--wait-for "<selector>"` 把审计流程关进构建完成之后；不传的话，需提醒用户构建缓慢可能导致基线过期。

分支名要放进下面带引号的 `branch` 变量里；切勿把分支名当作 shell 语法直接粘贴或求值。

```bash
git diff --quiet && git diff --cached --quiet || git stash push -u -m "accesslint-diff-branch"
branch="<branch>"
git check-ref-format --branch "$branch" >/dev/null
case "$branch" in -*) echo "Refusing option-like branch name: $branch" >&2; exit 1 ;; esac
git rev-parse --verify --quiet "$branch^{commit}" >/dev/null
git switch "$branch"
npx -y @accesslint/cli@latest "<url>" --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --update-snapshot [--wait-for "<selector>"]
git switch - && git stash pop 2>/dev/null
npx -y @accesslint/cli@latest "<url>" --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --format json [--wait-for "<selector>"]
```

`--selector`、`--include-aaa` 必须传给**两次**运行。

## 2. 报告

```
Accessibility diff — http://localhost:3000/ vs main (94 rules, live DOM)
2 new · 1 fixed · 4 pre-existing hidden

New — Critical
- color-contrast — 2.1:1 (needs 4.5:1), #bbb on #fff
    where: main > p.subtitle   fix: darken to #767676
Fixed
- img-alt — <img src="old.jpg"> (no longer present)
```

每条新增违规给出：**where**（选择器原文 + 若有 `source` 则附 `file:line (symbol)`，禁止编造）、**evidence**（证据）、**fix**（机械式改动或标注 `NEEDS HUMAN`）。

不要直接编辑。要修复时：机械式改动先应用，再跑一次 `accesslint:diff` 验证；批量工作交给 `accesslint:audit`。

## 3. 清理

```bash
npx -y @accesslint/chrome@latest stop --all  # 如果 ensure 输出 "managed":false 则跳过
```

## 注意事项

- `ensure` 始终决定端口——禁止写死 9222。
- CLI 退出码 2 = URL 不合法或页面未加载；检查开发服务器。
- Stash 模式：`sleep 2` 能覆盖大多数 HMR 场景；若基线和当前结果看起来一样，加 `--wait-for "<selector>"`。
- 分支模式：没有 HMR——CLI 每次都开新标签页。`--wait-for` 是构建完成的关卡。
- 两次运行之间 DOM 大幅改动会造成选择器漂移——用 `accesslint:scan` 重跑以获得完整图景。

## 局限
- 仅在任务明确匹配上述范围时使用本技能。
- 不要把输出当成特定环境验证、测试或专家评审的替代。
- 所需输入、权限、安全边界或成功标准缺失时，停下来向用户确认。