# 提示词模板库

## 分类模板

### 情感分析
```
Classify the sentiment of the following text as Positive, Negative, or Neutral.

Text: {text}

Sentiment:
```

### 意图检测
```
Determine the user's intent from the following message.

Possible intents: {intent_list}

Message: {message}

Intent:
```

### 主题分类
```
Classify the following article into one of these categories: {categories}

Article:
{article}

Category:
```

## 提取模板

### 命名实体识别
```
Extract all named entities from the text and categorize them.

Text: {text}

Entities (JSON format):
{
  "persons": [],
  "organizations": [],
  "locations": [],
  "dates": []
}
```

### 结构化数据提取
```
Extract structured information from the job posting.

Job Posting:
{posting}

Extracted Information (JSON):
{
  "title": "",
  "company": "",
  "location": "",
  "salary_range": "",
  "requirements": [],
  "responsibilities": []
}
```

## 生成模板

### 邮件生成
```
Write a professional {email_type} email.

To: {recipient}
Context: {context}
Key points to include:
{key_points}

Email:
Subject:
Body:
```

### 代码生成
```
Generate {language} code for the following task:

Task: {task_description}

Requirements:
{requirements}

Include:
- Error handling
- Input validation
- Inline comments

Code:
```

### 创意写作
```
Write a {length}-word {style} story about {topic}.

Include these elements:
- {element_1}
- {element_2}
- {element_3}

Story:
```

## 转换模板

### 摘要
```
Summarize the following text in {num_sentences} sentences.

Text:
{text}

Summary:
```

### 带上下文的翻译
```
Translate the following {source_lang} text to {target_lang}.

Context: {context}
Tone: {tone}

Text: {text}

Translation:
```

### 格式转换
```
Convert the following {source_format} to {target_format}.

Input:
{input_data}

Output ({target_format}):
```

## 分析模板

### 代码审查
```
Review the following code for:
1. Bugs and errors
2. Performance issues
3. Security vulnerabilities
4. Best practice violations

Code:
{code}

Review:
```

### SWOT 分析
```
Conduct a SWOT analysis for: {subject}

Context: {context}

Analysis:
Strengths:
-

Weaknesses:
-

Opportunities:
-

Threats:
-
```

## 问答模板

### RAG 模板
```
Answer the question based on the provided context. If the context doesn't contain enough information, say so.

Context:
{context}

Question: {question}

Answer:
```

### 多轮问答
```
Previous conversation:
{conversation_history}

New question: {question}

Answer (continue naturally from conversation):
```

## 专用模板

### SQL 查询生成
```
Generate a SQL query for the following request.

Database schema:
{schema}

Request: {request}

SQL Query:
```

### 正则表达式模式创建
```
Create a regex pattern to match: {requirement}

Test cases that should match:
{positive_examples}

Test cases that should NOT match:
{negative_examples}

Regex pattern:
```

### API 文档
```
Generate API documentation for this function:

Code:
{function_code}

Documentation (follow {doc_format} format):
```

## 通过填写 {variables} 来使用这些模板
