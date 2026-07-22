# 评估模板

用于评估/基准测试基础设施的模板。

仅限高级 profile。仅当用户明确请求智能体评估、回归基准、技能评分或评估框架时，才加载此参考。不要将 `harness/eval` 创建为默认核心 harness 的一部分。

## 评估任务 JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "category", "difficulty", "prompt"],
  "properties": {
    "id": {
      "type": "string",
      "description": "唯一任务标识符，例如 'file_ops_001'"
    },
    "category": {
      "type": "string",
      "enum": ["file_ops", "code_gen", "debugging", "refactoring"],
      "description": "任务类别用于分组"
    },
    "difficulty": {
      "type": "string",
      "enum": ["easy", "medium", "hard"],
      "description": "任务难度级别"
    },
    "description": {
      "type": "string",
      "description": "人类可读的任务描述"
    },
    "prompt": {
      "type": "string",
      "description": "发送给智能体的用户提示"
    },
    "init_files": {
      "type": "object",
      "additionalProperties": { "type": "string" },
      "description": "运行前要创建的文件（路径 -> 内容）"
    },
    "expected_files": {
      "type": "object",
      "additionalProperties": { "$ref": "#/definitions/FileExpectation" },
      "description": "执行后期望的文件状态"
    },
    "expected_commands": {
      "type": "array",
      "items": { "type": "string" },
      "description": "应该已执行的命令"
    },
    "max_turns": {
      "type": "integer",
      "description": "允许的最大对话轮数"
    },
    "max_tokens": {
      "type": "integer",
      "description": "允许的最大 token 数"
    },
    "timeout": {
      "type": "string",
      "description": "超时持续时间，例如 '30s'、'2m'"
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "用于过滤的标签"
    }
  },
  "definitions": {
    "FileExpectation": {
      "type": "object",
      "properties": {
        "must_exist": { "type": "boolean" },
        "must_not_exist": { "type": "boolean" },
        "must_contain": {
          "type": "array",
          "items": { "type": "string" },
          "description": "必须匹配的正则表达式模式"
        },
        "must_not_contain": {
          "type": "array",
          "items": { "type": "string" },
          "description": "不得匹配的正则表达式模式"
        }
      }
    }
  }
}
```

## 示例评估任务

### 文件操作

```json
{
  "id": "file_ops_001",
  "category": "file_ops",
  "difficulty": "easy",
  "description": "Create a simple Go hello world",
  "prompt": "Create hello.go with a main function that prints 'Hello, World!'",
  "expected_files": {
    "hello.go": {
      "must_exist": true,
      "must_contain": ["package main", "func main", "Hello, World"]
    }
  },
  "max_turns": 3,
  "timeout": "30s",
  "tags": ["go", "create"]
}
```

### 代码生成

```json
{
  "id": "code_gen_001",
  "category": "code_gen",
  "difficulty": "medium",
  "description": "Generate function with error handling",
  "prompt": "Create a Go function ReadJSON that reads a JSON file into a struct",
  "expected_files": {
    "json_reader.go": {
      "must_exist": true,
      "must_contain": ["func ReadJSON", "json.Unmarshal", "error"]
    }
  },
  "max_turns": 5,
  "timeout": "60s",
  "tags": ["go", "function", "json"]
}
```

### 调试

```json
{
  "id": "debug_001",
  "category": "debugging",
  "difficulty": "medium",
  "description": "Fix nil pointer dereference",
  "prompt": "Fix the nil pointer bug in buggy.go",
  "init_files": {
    "buggy.go": "package main\n\nfunc main() {\n\tvar s *string\n\tprintln(*s)\n}"
  },
  "expected_files": {
    "buggy.go": {
      "must_exist": true,
      "must_not_contain": ["println(\\*s)"]
    }
  },
  "max_turns": 4,
  "timeout": "45s",
  "tags": ["go", "nil-check", "bug"]
}
```

### 重构

```json
{
  "id": "refactor_001",
  "category": "refactoring",
  "difficulty": "medium",
  "description": "Extract duplicated validation logic",
  "prompt": "Extract the duplicated validation in handler.go into a validate function",
  "init_files": {
    "handler.go": "package main\n\nfunc handleA(s string) error {\n\tif s == \"\" { return fmt.Errorf(\"empty\") }\n\tif len(s) > 100 { return fmt.Errorf(\"too long\") }\n\treturn nil\n}\n\nfunc handleB(s string) error {\n\tif s == \"\" { return fmt.Errorf(\"empty\") }\n\tif len(s) > 100 { return fmt.Errorf(\"too long\") }\n\treturn nil\n}"
  },
  "expected_files": {
    "handler.go": {
      "must_exist": true,
      "must_contain": ["func validate"]
    }
  },
  "max_turns": 5,
  "timeout": "60s",
  "tags": ["go", "extract-function"]
}
```

## 评估框架代码

```go
// harness/eval/framework.go
package eval

import (
	"encoding/json"
	"os"
	"path/filepath"
	"regexp"
	"time"
)

type EvalTask struct {
	ID               string                      `json:"id"`
	Category         string                      `json:"category"`
	Difficulty       string                      `json:"difficulty"`
	Description      string                      `json:"description,omitempty"`
	Prompt           string                      `json:"prompt"`
	InitFiles        map[string]string           `json:"init_files,omitempty"`
	ExpectedFiles    map[string]FileExpectation  `json:"expected_files,omitempty"`
	ExpectedCommands []string                    `json:"expected_commands,omitempty"`
	MaxTurns         int                         `json:"max_turns,omitempty"`
	MaxTokens        int                         `json:"max_tokens,omitempty"`
	Timeout          time.Duration               `json:"timeout,omitempty"`
	Tags             []string                    `json:"tags,omitempty"`
}

type FileExpectation struct {
	MustExist      bool     `json:"must_exist"`
	MustNotExist   bool     `json:"must_not_exist,omitempty"`
	MustContain    []string `json:"must_contain,omitempty"`
	MustNotContain []string `json:"must_not_contain,omitempty"`
}

type Score struct {
	Correctness float64            `json:"correctness"`
	Efficiency  float64            `json:"efficiency"`
	Style       float64            `json:"style"`
	Overall     float64            `json:"overall"`
	Details     map[string]float64 `json:"details,omitempty"`
	Notes       []string           `json:"notes,omitempty"`
}

type EvalResult struct {
	TaskID    string        `json:"task_id"`
	Success   bool          `json:"success"`
	Score     Score         `json:"score"`
	Duration  time.Duration `json:"duration"`
	Error     string        `json:"error,omitempty"`
	Timestamp time.Time     `json:"timestamp"`
}

// LoadTask reads an eval task from JSON
func LoadTask(path string) (*EvalTask, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var task EvalTask
	return &task, json.Unmarshal(data, &task)
}

// LoadTasksFromDir loads all tasks from a directory
func LoadTasksFromDir(dir string) ([]EvalTask, error) {
	var tasks []EvalTask
	filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() || filepath.Ext(path) != ".json" {
			return nil
		}
		task, err := LoadTask(path)
		if err == nil {
			tasks = append(tasks, *task)
		}
		return nil
	})
	return tasks, nil
}

// ValidateFile checks if a file meets expectations
func ValidateFile(path string, exp FileExpectation) (bool, []string) {
	var issues []string

	_, err := os.Stat(path)
	exists := err == nil

	if exp.MustExist && !exists {
		issues = append(issues, "file must exist")
	}
	if exp.MustNotExist && exists {
		issues = append(issues, "file must not exist")
	}
	if !exists {
		return len(issues) == 0, issues
	}

	content, err := os.ReadFile(path)
	if err != nil {
		issues = append(issues, "cannot read file")
		return false, issues
	}

	for _, pattern := range exp.MustContain {
		if matched, _ := regexp.Match(pattern, content); !matched {
			issues = append(issues, "missing: "+pattern)
		}
	}
	for _, pattern := range exp.MustNotContain {
		if matched, _ := regexp.Match(pattern, content); matched {
			issues = append(issues, "forbidden: "+pattern)
		}
	}

	return len(issues) == 0, issues
}
```

## CLI 集成

```go
// cmd/eval/eval.go
package eval

import (
	"fmt"
	evalfw "your-module/harness/eval"
	"github.com/spf13/cobra"
)

func NewEvalCommand() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "eval",
		Short: "Run evaluation benchmarks",
	}
	cmd.AddCommand(newRunCmd())
	cmd.AddCommand(newListCmd())
	return cmd
}

func newRunCmd() *cobra.Command {
	var category, taskID, output string
	cmd := &cobra.Command{
		Use:   "run",
		Short: "Run eval tasks",
		RunE: func(cmd *cobra.Command, args []string) error {
			tasks, _ := evalfw.LoadTasksFromDir("harness/eval/datasets")
			fmt.Printf("Running %d tasks...\n", len(tasks))
			// Execute tasks and report
			return nil
		},
	}
	cmd.Flags().StringVar(&category, "category", "", "Filter by category")
	cmd.Flags().StringVar(&taskID, "task", "", "Run specific task")
	cmd.Flags().StringVar(&output, "output", "", "Export results to file")
	return cmd
}

func newListCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "list",
		Short: "List available eval tasks",
		RunE: func(cmd *cobra.Command, args []string) error {
			tasks, _ := evalfw.LoadTasksFromDir("harness/eval/datasets")
			fmt.Printf("%-20s %-15s %-10s\n", "ID", "Category", "Difficulty")
			for _, t := range tasks {
				fmt.Printf("%-20s %-15s %-10s\n", t.ID, t.Category, t.Difficulty)
			}
			return nil
		},
	}
}
```

## 报告格式

```go
type EvalReport struct {
	StartTime time.Time     `json:"start_time"`
	EndTime   time.Time     `json:"end_time"`
	Results   []EvalResult  `json:"results"`
	Summary   EvalSummary   `json:"summary"`
}

type EvalSummary struct {
	TotalTasks   int     `json:"total_tasks"`
	PassedTasks  int     `json:"passed_tasks"`
	FailedTasks  int     `json:"failed_tasks"`
	PassRate     float64 `json:"pass_rate"`
	AverageScore float64 `json:"average_score"`
}
```