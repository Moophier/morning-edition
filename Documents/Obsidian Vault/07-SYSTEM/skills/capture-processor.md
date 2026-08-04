# Skill: capture-processor (每日捕获处理器)

## Purpose
自动整理你每天捕捉的所有内容，按类型归档到正确位置。结合A股投资特点，对每条信息做投资相关分类。

## Trigger
运行命令：`opencode run "执行技能: capture-processor"`

## Process

### 第一步：读取今日捕捉
- 读取 `03-DAILY\[日期].md` 中的 Captures / 捕捉 / 今日记录 部分
- 如果没有捕捉内容：记录并停止
- 提取所有条目，不遗漏

### 第二步：读取CLAUDE.md
了解当前投资关注的标的和筛选标准，用于判断相关性

### 第三步：分类处理每个条目

**标的线索**（发现一个值得研究的股票）
→ 在 `01-KNOWLEDGE\stocks\` 创建笔记：`[股票名]-[代码].md`
→ 内容格式：
  - 首次发现日期
  - 初步吸引点（为什么关注）
  - 初步筛选指标（PE、分红等是否符合你的标准）
  - 下一步：需要查什么数据

**财务数据**（某个标的的新数据）
→ 找到该标的的笔记，更新财务数据部分
→ 记录数据来源和日期

**投资思考**（对某个标的或策略的想法）
→ 在 `01-KNOWLEDGE\insights\` 创建笔记
→ 格式：`[日期]-[简要描述].md`

**决策记录**（做了一个买入/卖出/继续观察的决定）
→ 在 `01-KNOWLEDGE\decisions\` 创建笔记
→ 格式：见decision-intelligence技能模板

**资料保存**（研报、公告、新闻等）
→ 存入 `05-RESOURCES\investment-research\[标的名]\`

**疑问待查**（需要进一步研究的问题）
→ 加入 `00-INBOX\research-questions.md`

### 第四步：更新CLAUDE.md
如果今日有新的标的发现，更新"Current Focus Areas"

### 第五步：生成处理报告
```
# 捕获处理报告 — [日期]
- 标的线索：N条 → 已创建笔记
- 数据更新：N条 → 已更新笔记
- 投资思考：N条 → 已归档
- 待查疑问：N条 → 已记录
```

保存到：`04-JARVIS-OUTPUTS\[日期]-processing.md`