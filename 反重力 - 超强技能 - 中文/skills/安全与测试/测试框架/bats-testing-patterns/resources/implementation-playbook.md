# Bats 测试模式实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

## Bats 基础

### 什么是 Bats？

Bats（Bash 自动化测试系统）是一个符合 TAP（Test Anything Protocol）规范的 Shell 脚本测试框架，提供：
- 简洁自然的测试语法
- 兼容 CI 系统的 TAP 输出格式
- 夹具和 setup/teardown 支持
- 断言辅助函数
- 并行测试执行

### 安装

```bash
# macOS with Homebrew
brew install bats-core

# Ubuntu/Debian
git clone https://github.com/bats-core/bats-core.git
cd bats-core
./install.sh /usr/local

# From npm (Node.js)
npm install --global bats

# Verify installation
bats --version
```

### 文件结构

```
project/
├── bin/
│   ├── script.sh
│   └── helper.sh
├── tests/
│   ├── test_script.bats
│   ├── test_helper.sh
│   ├── fixtures/
│   │   ├── input.txt
│   │   └── expected_output.txt
│   └── helpers/
│       └── mocks.bash
└── README.md
```

## 基本测试结构

### 简单测试文件

```bash
#!/usr/bin/env bats

# Load test helper if present
load test_helper

# Setup runs before each test
setup() {
    export TMPDIR=$(mktemp -d)
}

# Teardown runs after each test
teardown() {
    rm -rf "$TMPDIR"
}

# Test: simple assertion
@test "Function returns 0 on success" {
    run my_function "input"
    [ "$status" -eq 0 ]
}

# Test: output verification
@test "Function outputs correct result" {
    run my_function "test"
    [ "$output" = "expected output" ]
}

# Test: error handling
@test "Function returns 1 on missing argument" {
    run my_function
    [ "$status" -eq 1 ]
}
```

## 断言模式

### 退出码断言

```bash
#!/usr/bin/env bats

@test "Command succeeds" {
    run true
    [ "$status" -eq 0 ]
}

@test "Command fails as expected" {
    run false
    [ "$status" -ne 0 ]
}

@test "Command returns specific exit code" {
    run my_function --invalid
    [ "$status" -eq 127 ]
}

@test "Can capture command result" {
    run echo "hello"
    [ $status -eq 0 ]
    [ "$output" = "hello" ]
}
```

### 输出断言

```bash
#!/usr/bin/env bats

@test "Output matches string" {
    result=$(echo "hello world")
    [ "$result" = "hello world" ]
}

@test "Output contains substring" {
    result=$(echo "hello world")
    [[ "$result" == *"world"* ]]
}

@test "Output matches pattern" {
    result=$(date +%Y)
    [[ "$result" =~ ^[0-9]{4}$ ]]
}

@test "Multi-line output" {
    run printf "line1\nline2\nline3"
    [ "$output" = "line1
line2
line3" ]
}

@test "Lines variable contains output" {
    run printf "line1\nline2\nline3"
    [ "${lines[0]}" = "line1" ]
    [ "${lines[1]}" = "line2" ]
    [ "${lines[2]}" = "line3" ]
}
```

### 文件断言

```bash
#!/usr/bin/env bats

@test "File is created" {
    [ ! -f "$TMPDIR/output.txt" ]
    my_function > "$TMPDIR/output.txt"
    [ -f "$TMPDIR/output.txt" ]
}

@test "File contents match expected" {
    my_function > "$TMPDIR/output.txt"
    [ "$(cat "$TMPDIR/output.txt")" = "expected content" ]
}

@test "File is readable" {
    touch "$TMPDIR/test.txt"
    [ -r "$TMPDIR/test.txt" ]
}

@test "File has correct permissions" {
    touch "$TMPDIR/test.txt"
    chmod 644 "$TMPDIR/test.txt"
    [ "$(stat -f %OLp "$TMPDIR/test.txt")" = "644" ]
}

@test "File size is correct" {
    echo -n "12345" > "$TMPDIR/test.txt"
    [ "$(wc -c < "$TMPDIR/test.txt")" -eq 5 ]
}
```

## Setup 和 Teardown 模式

### 基本 Setup 和 Teardown

```bash
#!/usr/bin/env bats

setup() {
    # Create test directory
    TEST_DIR=$(mktemp -d)
    export TEST_DIR

    # Source script under test
    source "${BATS_TEST_DIRNAME}/../bin/script.sh"
}

teardown() {
    # Clean up temporary directory
    rm -rf "$TEST_DIR"
}

@test "Test using TEST_DIR" {
    touch "$TEST_DIR/file.txt"
    [ -f "$TEST_DIR/file.txt" ]
}
```

### 带资源的 Setup

```bash
#!/usr/bin/env bats

setup() {
    # Create directory structure
    mkdir -p "$TMPDIR/data/input"
    mkdir -p "$TMPDIR/data/output"

    # Create test fixtures
    echo "line1" > "$TMPDIR/data/input/file1.txt"
    echo "line2" > "$TMPDIR/data/input/file2.txt"

    # Initialize environment
    export DATA_DIR="$TMPDIR/data"
    export INPUT_DIR="$DATA_DIR/input"
    export OUTPUT_DIR="$DATA_DIR/output"
}

teardown() {
    rm -rf "$TMPDIR/data"
}

@test "Processes input files" {
    run my_process_script "$INPUT_DIR" "$OUTPUT_DIR"
    [ "$status" -eq 0 ]
    [ -f "$OUTPUT_DIR/file1.txt" ]
}
```

### 全局 Setup/Teardown

```bash
#!/usr/bin/env bats

# Load shared setup from test_helper.sh
load test_helper

# setup_file runs once before all tests
setup_file() {
    export SHARED_RESOURCE=$(mktemp -d)
    echo "Expensive setup" > "$SHARED_RESOURCE/data.txt"
}

# teardown_file runs once after all tests
teardown_file() {
    rm -rf "$SHARED_RESOURCE"
}

@test "First test uses shared resource" {
    [ -f "$SHARED_RESOURCE/data.txt" ]
}

@test "Second test uses shared resource" {
    [ -d "$SHARED_RESOURCE" ]
}
```

## Mock 和 Stub 模式

### 函数 Mock

```bash
#!/usr/bin/env bats

# Mock external command
my_external_tool() {
    echo "mocked output"
    return 0
}

@test "Function uses mocked tool" {
    export -f my_external_tool
    run my_function
    [[ "$output" == *"mocked output"* ]]
}
```

### 命令 Stub

```bash
#!/usr/bin/env bats

setup() {
    # Create stub directory
    STUBS_DIR="$TMPDIR/stubs"
    mkdir -p "$STUBS_DIR"

    # Add to PATH
    export PATH="$STUBS_DIR:$PATH"
}

create_stub() {
    local cmd="$1"
    local output="$2"
    local code="${3:-0}"

    cat > "$STUBS_DIR/$cmd" <<EOF
#!/bin/bash
echo "$output"
exit $code
EOF
    chmod +x "$STUBS_DIR/$cmd"
}

@test "Function works with stubbed curl" {
    create_stub curl "{ \"status\": \"ok\" }" 0
    run my_api_function
    [ "$status" -eq 0 ]
}
```

### 变量 Stub

```bash
#!/usr/bin/env bats

@test "Function handles environment override" {
    export MY_SETTING="override_value"
    run my_function
    [ "$status" -eq 0 ]
    [[ "$output" == *"override_value"* ]]
}

@test "Function uses default when var unset" {
    unset MY_SETTING
    run my_function
    [ "$status" -eq 0 ]
    [[ "$output" == *"default"* ]]
}
```

## 夹具管理

### 使用夹具文件

```bash
#!/usr/bin/env bats

# Fixture directory: tests/fixtures/

setup() {
    FIXTURES_DIR="${BATS_TEST_DIRNAME}/fixtures"
    WORK_DIR=$(mktemp -d)
    export WORK_DIR
}

teardown() {
    rm -rf "$WORK_DIR"
}

@test "Process fixture file" {
    # Copy fixture to work directory
    cp "$FIXTURES_DIR/input.txt" "$WORK_DIR/input.txt"

    # Run function
    run my_process_function "$WORK_DIR/input.txt"

    # Compare output
    diff "$WORK_DIR/output.txt" "$FIXTURES_DIR/expected_output.txt"
}
```

### 动态夹具生成

```bash
#!/usr/bin/env bats

generate_fixture() {
    local lines="$1"
    local file="$2"

    for i in $(seq 1 "$lines"); do
        echo "Line $i content" >> "$file"
    done
}

@test "Handle large input file" {
    generate_fixture 1000 "$TMPDIR/large.txt"
    run my_function "$TMPDIR/large.txt"
    [ "$status" -eq 0 ]
    [ "$(wc -l < "$TMPDIR/large.txt")" -eq 1000 ]
}
```

## 高级模式

### 测试错误条件

```bash
#!/usr/bin/env bats

@test "Function fails with missing file" {
    run my_function "/nonexistent/file.txt"
    [ "$status" -ne 0 ]
    [[ "$output" == *"not found"* ]]
}

@test "Function fails with invalid input" {
    run my_function ""
    [ "$status" -ne 0 ]
}

@test "Function fails with permission denied" {
    touch "$TMPDIR/readonly.txt"
    chmod 000 "$TMPDIR/readonly.txt"
    run my_function "$TMPDIR/readonly.txt"
    [ "$status" -ne 0 ]
    chmod 644 "$TMPDIR/readonly.txt"  # Cleanup
}

@test "Function provides helpful error message" {
    run my_function --invalid-option
    [ "$status" -ne 0 ]
    [[ "$output" == *"Usage:"* ]]
}
```

### 测试依赖项

```bash
#!/usr/bin/env bats

setup() {
    # Check for required tools
    if ! command -v jq &>/dev/null; then
        skip "jq is not installed"
    fi

    export SCRIPT="${BATS_TEST_DIRNAME}/../bin/script.sh"
}

@test "JSON parsing works" {
    skip_if ! command -v jq &>/dev/null
    run my_json_parser '{"key": "value"}'
    [ "$status" -eq 0 ]
}
```

### 测试 Shell 兼容性

```bash
#!/usr/bin/env bats

@test "Script works in bash" {
    bash "${BATS_TEST_DIRNAME}/../bin/script.sh" arg1
}

@test "Script works in sh (POSIX)" {
    sh "${BATS_TEST_DIRNAME}/../bin/script.sh" arg1
}

@test "Script works in dash" {
    if command -v dash &>/dev/null; then
        dash "${BATS_TEST_DIRNAME}/../bin/script.sh" arg1
    else
        skip "dash not installed"
    fi
}
```

### 并行执行

```bash
#!/usr/bin/env bats

@test "Multiple independent operations" {
    run bash -c 'for i in {1..10}; do
        my_operation "$i" &
    done
    wait'
    [ "$status" -eq 0 ]
}

@test "Concurrent file operations" {
    for i in {1..5}; do
        my_function "$TMPDIR/file$i" &
    done
    wait
    [ -f "$TMPDIR/file1" ]
    [ -f "$TMPDIR/file5" ]
}
```

## 测试辅助函数模式

### test_helper.sh

```bash
#!/usr/bin/env bash

# Source script under test
export SCRIPT_DIR="${BATS_TEST_DIRNAME%/*}/bin"

# Common test utilities
assert_file_exists() {
    if [ ! -f "$1" ]; then
        echo "Expected file to exist: $1"
        return 1
    fi
}

assert_file_equals() {
    local file="$1"
    local expected="$2"

    if [ ! -f "$file" ]; then
        echo "File does not exist: $file"
        return 1
    fi

    local actual=$(cat "$file")
    if [ "$actual" != "$expected" ]; then
        echo "File contents do not match"
        echo "Expected: $expected"
        echo "Actual: $actual"
        return 1
    fi
}

# Create temporary test directory
setup_test_dir() {
    export TEST_DIR=$(mktemp -d)
}

cleanup_test_dir() {
    rm -rf "$TEST_DIR"
}
```

## 与 CI/CD 集成

### GitHub Actions 工作流

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Install Bats
        run: |
          npm install --global bats

      - name: Run Tests
        run: |
          bats tests/*.bats

      - name: Run Tests with Tap Reporter
        run: |
          bats tests/*.bats --tap | tee test_output.tap
```

### Makefile 集成

```makefile
.PHONY: test test-verbose test-tap

test:
	bats tests/*.bats

test-verbose:
	bats tests/*.bats --verbose

test-tap:
	bats tests/*.bats --tap

test-parallel:
	bats tests/*.bats --parallel 4

coverage: test
	# Optional: Generate coverage reports
```

## 最佳实践

1. **每个测试只测一件事** — 单一职责原则
2. **使用描述性测试名称** — 清楚说明正在测试什么
3. **测试后清理** — 始终在 teardown 中删除临时文件
4. **同时测试成功和失败路径** — 不要只测正常路径
5. **Mock 外部依赖** — 隔离被测单元
6. **对复杂数据使用夹具** — 使测试更可读
7. **在 CI/CD 中运行测试** — 尽早发现回归
8. **跨 Shell 方言测试** — 确保可移植性
9. **保持测试快速** — 尽可能并行运行
10. **记录复杂的测试设置** — 解释不寻常的模式

## 资源

- **Bats GitHub**: https://github.com/bats-core/bats-core
- **Bats 文档**: https://bats-core.readthedocs.io/
- **TAP 协议**: https://testanything.org/
- **测试驱动开发**: https://en.wikipedia.org/wiki/Test-driven_development
