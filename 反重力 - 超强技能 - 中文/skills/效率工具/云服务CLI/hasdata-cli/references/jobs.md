# 招聘参考

子命令：`indeed-listing`、`indeed-job`、`glassdoor-listing`、`glassdoor-job`。Indeed：5 积分。Glassdoor：10 积分。

`*-listing` 按查询/地点搜索；`*-job` 按 URL 或 ID 深入单条职位。

---

## indeed-listing

```bash
hasdata indeed-listing \
  --query "backend engineer" --location "Remote" \
  [--days-since-posted 7] [--job-type fulltime|parttime|contract|temporary|internship] \
  [--remote] [--page 1] \
  --raw | jq '.jobs[] | {title, company, location, posted, salary, url}'
```

其他值得知道的标志：
- `--salary-min N` / `--salary-max N`
- `--experience-level entry|mid|senior`
- `--sort relevance|date`
- `--country us|gb|ca|de|fr|...`

## indeed-job

```bash
hasdata indeed-job --url "https://www.indeed.com/viewjob?jk=..." --raw | jq .
```

也可以用 `--job-key JK`。返回完整描述、公司信息、福利、招聘洞察、相近职位。

## glassdoor-listing

```bash
hasdata glassdoor-listing --keyword "data scientist" --location "Boston" --raw \
  | jq '.jobs[] | {title, employer, salary_estimate, rating}'
```

Glassdoor 在每条结果里附带雇主评分和薪资预估。当用户同时关心雇主口碑和职位时用。

## glassdoor-job

```bash
hasdata glassdoor-job --url "https://www.glassdoor.com/Job/jobs.htm?...JV=..." --raw | jq .
```

返回完整职位以及雇主评分分布、最新评论、薪资预估区间、面试难度。

---

## 非显式用例

- **薪资谈判调研** ——`indeed-listing --query ROLE --location CITY`，然后 `jq '[.jobs[].salary | select(.)] | sort_by(.min)'` 在谈薪前构建一份站得住脚的区间。
- **"我该不该为这工作搬家？"** ——同一岗位在 3–5 个城市，对比薪资中位数与当地生活成本。
- **竞品招聘动态情报** ——`indeed-listing --query "company:NAME"`（或用 `glassdoor-listing` 按雇主过滤）返回近期招聘；能看出哪些团队在扩张、用什么技术栈、分布在哪些地点。
- **"是真招还是幽灵职位？"** ——`indeed-job --url X --raw | jq '.posted_at'`。超过 60 天未刷新的职位常常是幽灵职位。
- **按地区看技术栈流行度** ——`indeed-listing --query "Rust" --location "Berlin"` 对比 `--location "San Francisco"`，看绝对岗位数和薪资差。
- **职业转型调研** ——`indeed-listing --query "TARGET ROLE" --raw | jq -r '.jobs[].description'`，再用 LLM 总结最常要求的技能。揭示的是真实差距，而不是培训班宣传的差距。
- **雇主口碑深挖** ——`glassdoor-listing` 内联返回评分；`glassdoor-job` 返回最新评论和面试难度。投递或接受 offer 之前先看。
- **远程职位筛选** ——`indeed-listing` 加 `--remote` 只看完全远程的岗位；用 `--country gb` 等找到美国之外对远程友好的市场。
- **签证友好雇主识别** ——`indeed-listing --query "ROLE H1B sponsorship"` 或 `--query "ROLE relocation"`，提到这些关键词的 listing 更可能支持签证 transfer。
- **只看实习** ——`indeed-listing` 加 `--job-type internship` 用于早期职业搜索。
- **薪资带反推** ——Glassdoor 的 `salary_estimate` 是估算；用 5–10 条同城市同岗位的 Indeed 帖子交叉验证，自己算中位数更靠谱。
- **"谁正在离开 X 公司？"** ——`glassdoor-listing --keyword "previously at: COMPANY"` 是一种很宽泛的查询，但有时能挖到前员工描述自己转职的帖子。
- **比新闻更早发现裁员** ——某地区 `indeed-listing --query "ex-COMPANY"` 突然暴涨往往先于官宣。
- **谈薪准备——面试难度** ——`glassdoor-job --url X --raw | jq '.interview_difficulty, .interview_experiences[]'`，能看到过往候选人怎么评价这个流程。

## 常见模式

```bash
# Salary distribution for a role
hasdata indeed-listing --query "senior python developer" --location "New York, NY" \
  --raw | jq '[.jobs[].salary | select(. != null)] | unique'

# Compare same role on both platforms
for src in indeed-listing glassdoor-listing; do
  echo "=== $src ==="
  hasdata "$src" --query "platform engineer" --location "SF" --raw \
    | jq '.jobs[:5][] | {title, company: (.company // .employer), location}'
done
```

先用 Indeed 广撒网；要看雇主评分或面试难度再升级到 Glassdoor。