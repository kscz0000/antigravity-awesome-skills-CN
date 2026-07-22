---
name: bazel-build-optimization
description: "优化大规模单体仓库的 Bazel 构建。涵盖配置 Bazel、实现远程执行以及优化企业级代码库的构建性能。当用户要求'优化Bazel构建'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Bazel 构建优化

大规模单体仓库中 Bazel 的生产级模式。

## 不适用场景

- 任务与 Bazel 构建优化无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 适用场景

- 为单体仓库配置 Bazel
- 配置远程缓存/远程执行
- 优化构建时间
- 编写自定义 Bazel 规则
- 调试构建问题
- 迁移到 Bazel

## 核心概念

### 1. Bazel 架构

```
workspace/
├── WORKSPACE.bazel       # External dependencies
├── .bazelrc              # Build configurations
├── .bazelversion         # Bazel version
├── BUILD.bazel           # Root build file
├── apps/
│   └── web/
│       └── BUILD.bazel
├── libs/
│   └── utils/
│       └── BUILD.bazel
└── tools/
    └── bazel/
        └── rules/
```

### 2. 关键概念

| 概念 | 描述 |
|------|------|
| **Target** | 可构建单元（库、二进制文件、测试） |
| **Package** | 包含 BUILD 文件的目录 |
| **Label** | 目标标识符 `//path/to:target` |
| **Rule** | 定义如何构建目标 |
| **Aspect** | 横切构建行为 |

## 模板

### 模板 1：WORKSPACE 配置

```python
# WORKSPACE.bazel
workspace(name = "myproject")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Rules for JavaScript/TypeScript
http_archive(
    name = "aspect_rules_js",
    sha256 = "...",
    strip_prefix = "rules_js-1.34.0",
    url = "https://github.com/aspect-build/rules_js/releases/download/v1.34.0/rules_js-v1.34.0.tar.gz",
)

load("@aspect_rules_js//js:repositories.bzl", "rules_js_dependencies")
rules_js_dependencies()

load("@rules_nodejs//nodejs:repositories.bzl", "nodejs_register_toolchains")
nodejs_register_toolchains(
    name = "nodejs",
    node_version = "20.9.0",
)

load("@aspect_rules_js//npm:repositories.bzl", "npm_translate_lock")
npm_translate_lock(
    name = "npm",
    pnpm_lock = "//:pnpm-lock.yaml",
    verify_node_modules_ignored = "//:.bazelignore",
)

load("@npm//:repositories.bzl", "npm_repositories")
npm_repositories()

# Rules for Python
http_archive(
    name = "rules_python",
    sha256 = "...",
    strip_prefix = "rules_python-0.27.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.27.0/rules_python-0.27.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")
py_repositories()
```

### 模板 2：.bazelrc 配置

```bash
# .bazelrc

# Build settings
build --enable_platform_specific_config
build --incompatible_enable_cc_toolchain_resolution
build --experimental_strict_conflict_checks

# Performance
build --jobs=auto
build --local_cpu_resources=HOST_CPUS*.75
build --local_ram_resources=HOST_RAM*.75

# Caching
build --disk_cache=~/.cache/bazel-disk
build --repository_cache=~/.cache/bazel-repo

# Remote caching (optional)
build:remote-cache --remote_cache=grpcs://cache.example.com
build:remote-cache --remote_upload_local_results=true
build:remote-cache --remote_timeout=3600

# Remote execution (optional)
build:remote-exec --remote_executor=grpcs://remote.example.com
build:remote-exec --remote_instance_name=projects/myproject/instances/default
build:remote-exec --jobs=500

# Platform configurations
build:linux --platforms=//platforms:linux_x86_64
build:macos --platforms=//platforms:macos_arm64

# CI configuration
build:ci --config=remote-cache
build:ci --build_metadata=ROLE=CI
build:ci --bes_results_url=https://results.example.com/invocation/
build:ci --bes_backend=grpcs://bes.example.com

# Test settings
test --test_output=errors
test --test_summary=detailed

# Coverage
coverage --combined_report=lcov
coverage --instrumentation_filter="//..."

# Convenience aliases
build:opt --compilation_mode=opt
build:dbg --compilation_mode=dbg

# Import user settings
try-import %workspace%/user.bazelrc
```

### 模板 3：TypeScript 库 BUILD

```python
# libs/utils/BUILD.bazel
load("@aspect_rules_ts//ts:defs.bzl", "ts_project")
load("@aspect_rules_js//js:defs.bzl", "js_library")
load("@npm//:defs.bzl", "npm_link_all_packages")

npm_link_all_packages(name = "node_modules")

ts_project(
    name = "utils_ts",
    srcs = glob(["src/**/*.ts"]),
    declaration = True,
    source_map = True,
    tsconfig = "//:tsconfig.json",
    deps = [
        ":node_modules/@types/node",
    ],
)

js_library(
    name = "utils",
    srcs = [":utils_ts"],
    visibility = ["//visibility:public"],
)

# Tests
load("@aspect_rules_jest//jest:defs.bzl", "jest_test")

jest_test(
    name = "utils_test",
    config = "//:jest.config.js",
    data = [
        ":utils",
        "//:node_modules/jest",
    ],
    node_modules = "//:node_modules",
)
```

### 模板 4：Python 库 BUILD

```python
# libs/ml/BUILD.bazel
load("@rules_python//python:defs.bzl", "py_library", "py_test", "py_binary")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "ml",
    srcs = glob(["src/**/*.py"]),
    deps = [
        requirement("numpy"),
        requirement("pandas"),
        requirement("scikit-learn"),
        "//libs/utils:utils_py",
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "ml_test",
    srcs = glob(["tests/**/*.py"]),
    deps = [
        ":ml",
        requirement("pytest"),
    ],
    size = "medium",
    timeout = "moderate",
)

py_binary(
    name = "train",
    srcs = ["train.py"],
    deps = [":ml"],
    data = ["//data:training_data"],
)
```

### 模板 5：Docker 自定义规则

```python
# tools/bazel/rules/docker.bzl
def _docker_image_impl(ctx):
    dockerfile = ctx.file.dockerfile
    base_image = ctx.attr.base_image
    layers = ctx.files.layers

    # Build the image
    output = ctx.actions.declare_file(ctx.attr.name + ".tar")

    args = ctx.actions.args()
    args.add("--dockerfile", dockerfile)
    args.add("--output", output)
    args.add("--base", base_image)
    args.add_all("--layer", layers)

    ctx.actions.run(
        inputs = [dockerfile] + layers,
        outputs = [output],
        executable = ctx.executable._builder,
        arguments = [args],
        mnemonic = "DockerBuild",
        progress_message = "Building Docker image %s" % ctx.label,
    )

    return [DefaultInfo(files = depset([output]))]

docker_image = rule(
    implementation = _docker_image_impl,
    attrs = {
        "dockerfile": attr.label(
            allow_single_file = [".dockerfile", "Dockerfile"],
            mandatory = True,
        ),
        "base_image": attr.string(mandatory = True),
        "layers": attr.label_list(allow_files = True),
        "_builder": attr.label(
            default = "//tools/docker:builder",
            executable = True,
            cfg = "exec",
        ),
    },
)
```

### 模板 6：查询与依赖分析

```bash
# Find all dependencies of a target
bazel query "deps(//apps/web:web)"

# Find reverse dependencies (what depends on this)
bazel query "rdeps(//..., //libs/utils:utils)"

# Find all targets in a package
bazel query "//libs/..."

# Find changed targets since commit
bazel query "rdeps(//..., set($(git diff --name-only HEAD~1 | sed 's/.*/"&"/' | tr '\n' ' ')))"

# Generate dependency graph
bazel query "deps(//apps/web:web)" --output=graph | dot -Tpng > deps.png

# Find all test targets
bazel query "kind('.*_test', //...)"

# Find targets with specific tag
bazel query "attr(tags, 'integration', //...)"

# Compute build graph size
bazel query "deps(//...)" --output=package | wc -l
```

### 模板 7：远程执行配置

```python
# platforms/BUILD.bazel
platform(
    name = "linux_x86_64",
    constraint_values = [
        "@platforms//os:linux",
        "@platforms//cpu:x86_64",
    ],
    exec_properties = {
        "container-image": "docker://gcr.io/myproject/bazel-worker:latest",
        "OSFamily": "Linux",
    },
)

platform(
    name = "remote_linux",
    parents = [":linux_x86_64"],
    exec_properties = {
        "Pool": "default",
        "dockerNetwork": "standard",
    },
)

# toolchains/BUILD.bazel
toolchain(
    name = "cc_toolchain_linux",
    exec_compatible_with = [
        "@platforms//os:linux",
        "@platforms//cpu:x86_64",
    ],
    target_compatible_with = [
        "@platforms//os:linux",
        "@platforms//cpu:x86_64",
    ],
    toolchain = "@remotejdk11_linux//:jdk",
    toolchain_type = "@bazel_tools//tools/jdk:runtime_toolchain_type",
)
```

## 性能优化

```bash
# Profile build
bazel build //... --profile=profile.json
bazel analyze-profile profile.json

# Identify slow actions
bazel build //... --execution_log_json_file=exec_log.json

# Memory profiling
bazel build //... --memory_profile=memory.json

# Skip analysis cache
bazel build //... --notrack_incremental_state
```

## 最佳实践

### 推荐做法
- **使用细粒度目标** - 更好的缓存效果
- **锁定依赖版本** - 可复现的构建
- **启用远程缓存** - 共享构建产物
- **合理使用可见性** - 强制执行架构约束
- **每个目录编写 BUILD 文件** - 标准惯例

### 避免做法
- **不要用 glob 声明 deps** - 显式声明更好
- **不要提交 bazel-* 目录** - 添加到 .gitignore
- **不要跳过 WORKSPACE 配置** - 构建的基础
- **不要忽略构建警告** - 技术债务

## 资源

- [Bazel 文档](https://bazel.build/docs)
- [Bazel 远程执行](https://bazel.build/docs/remote-execution)
- [rules_js](https://github.com/aspect-build/rules_js)

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
