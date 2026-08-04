# Skill: decision-intelligence (决策智能系统)

## Purpose
结构化投资决策，并在预定时间回顾过去决策的有效性。

## Trigger
两部分：

**A部分：结构化新决策**
当你在 vault 中创建包含"decision"的文件名时自动触发
运行命令：`opencode run "执行技能: decision-intelligence --part A"`

**B部分：回顾过去决策**
每周一9AM
运行命令：`opencode run "执行技能: decision-intelligence --part B"`

---

## Part A: 结构化决策

### 读取
- 原始决策内容（来自 inbox）
- CLAUDE.md 了解当前背景
- 记忆库中任何相关的过往决策

### 生成结构化决策笔记
```
---
type: decision
date: [日期]
status: active
review_date: [建议的回顾日期，基于决策风险]
stock_code: [股票代码，如果相关]
stock_name: [股票名称]
decision_type: [买入/卖出/继续观察/止损/其他]
---

# 决策：[主题]

## 决定是什么
[清晰具体的陈述]

## 真正的原因
[实际推理，不是事后找的理由]

## 被拒绝的替代方案
[桌上还有什么，为什么选了当前这个]

## 关键假设
[这个决策所依赖的最重要假设，必须为真才成立]

## 预期结果
[具体可观察的结果]

## 预警信号
[如何 early know 如果这个决策出问题]

## 回顾日期
[何时需要检查决策有效性]
```

保存到：`01-KNOWLEDGE\decisions\[日期]-[标的]-[决策类型].md`
归档原始 inbox 文件

---

## Part B: 回顾决策

### 读取
- 所有状态为 active 的决策笔记
- 找出所有 review_date 在今天之前的决策

### 对每个到期决策
- 读取 vault 中关于该标的的最新信息
- 对比关键假设和当前证据

### 评估结果
- **VALID（有效）**：假设仍然成立，决策看起来正确
- **CHALLENGED（受挑战）**：新证据使假设复杂化
- **INVALIDATED（失效）**：证据明显反驳假设

### 生成回顾
```
# 决策回顾：[标的]

原始决策：[[决策笔记链接]]

当时假设：[关键假设]

当前证据：[vault中有什么]

状态：[VALID / CHALLENGED / INVALIDATED]

建议行动：[保持/修订/反转 — 具体理由]
```

保存到：`04-JARVIS-OUTPUTS\reviews\[日期]-decision-review.md`