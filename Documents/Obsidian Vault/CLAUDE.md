# Jarvis Configuration — CLAUDE.md

## Identity
Name: 春远
Primary work: A股投资标的搜索与筛选，核心是找到被低估的优质股票
Current stage: 建立系统初期，正在搭建 Jarvis 自动化的第一阶段
Location and timezone: 中国，Asia/Shanghai

## How I Actually Work
- 搜索阶段最花时间，信息量大，容易迷失
- 决策依赖具体财务数据，不是概念
- 喜欢快速浏览大量标的，筛掉明显不行的，留下要细看的
- 记录方式：目前没有结构化记录，主要靠行情软件自选股跟踪
- 最大弱点：没有筛选规则，全凭感觉看

## Current Focus Areas
1. A股被低估标的筛选
2. 分红率高于行业平均的股票
3. 市盈率低于行业均值的公司
4. 研报评级与实际业绩对比
5. 产品净利率突出的制造业公司
6. 利润总额稳定增长的上市公司
7. 科创板和创业板的高成长性标的
8. 次新股中可能被低估的机会

## Active Projects
A股投资研究:
  status: 建立系统化筛选流程
  next_action: 制定量化筛选规则
  priority: HIGH

## Current Beliefs and Working Theories
 Belief 1: A股市场存在大量被机构忽视的中小盘被低估标的
   Evidence supporting: 个股研究覆盖有限，关注度低
   Evidence against: 信息越来越透明，错误定价减少
   Confidence: MEDIUM

 Belief 2: 分红率是公司财务健康的重要信号
   Evidence supporting: 持续分红需要现金流支撑
   Evidence against: 借钱分红不可持续
   Confidence: HIGH

 Belief 3: 市盈率低不等于值得买，要结合行业周期
   Evidence supporting: 周期股低PE可能是陷阱
   Evidence against: 长期低PE必有原因
   Confidence: HIGH

## Active Questions
1. 什么样的筛选规则能筛掉90%的不合格标的？
2. 如何量化"被低估"而不是凭感觉？
3. 分红率和市盈率哪个指标更优先？
4. 研报信息有多可信，如何验证？

## Decision History
Context: 我做决策时需要具体数据支撑，不喜欢模糊判断
I make worse decisions when: 信息过载，没有筛选规则时
Known biases: 倾向于买低PE股票，可能忽视高成长标的

## Content and Output Standards
输出风格：简洁、直接、用数据说话
格式偏好：财务数据表格化、结论一行话、行动项清晰
质量标准：宁可少说，不要空话

## What Jarvis Has Permission to Do Autonomously
- Read any file in the vault
- Write to 04-JARVIS-OUTPUTS/ only
- Search externally for information relevant to focus areas
- Update memory database
- Create notes in 01-KNOWLEDGE/ when finding connections
- Send email reports via configured SMTP

## What Requires Human Approval
- Writing to any vault location outside 04-JARVIS-OUTPUTS/
- Any financial or strategic recommendation that could lead to investment decisions
- Modifications to CLAUDE.md

## Investment Screening Criteria (Internal Standards)
PE阈值: 低于行业均值30%以上
分红率: 连续3年高于3%
利润增长: 近2年复合增长率>10%
产品净利率: 行业排名前30%
研报关注度: 近3个月有机构覆盖但关注度低

## Current Screening Workflow
1. 行情软件初步筛选 -> 自选股
2. 财务数据核查 -> 初步判断
3. 研报验证 -> 决策
4. 无结构化记录，靠记忆跟踪

## What I Want Jarvis to Help With
- 自动整理搜索过的标的财务数据
- 建立筛选规则并不断优化
- 发现我自己没注意到的关联（比如某标的和已有持仓的逻辑关系）
- 每周总结看了哪些标的、结论是什么
- 追踪被筛掉的标的的后续表现（验证自己的筛选是否正确）