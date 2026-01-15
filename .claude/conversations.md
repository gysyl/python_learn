# Claude 对话记录

> 本文件记录与 Claude Code AI 助手的重要对话、决策和上下文，用于跨会话保持项目记忆。

---

## 📅 2026-01-13

### 🎯 项目初始化与规范制定

#### 背景
- 项目：python_learn（Python 学习与实战项目）
- 目标：建立 AI 助手协作规范，确保代码质量一致性

#### 决策记录

**1. 语言偏好约定**
- ✅ **代码注释和文档使用中文**
- ✅ **变量名、函数名、类名使用英文**
- ✅ 日志消息、异常消息使用中文
- 理由：符合中文开发者习惯，同时保持代码国际化

**2. 创建了两个 CLAUDE.md 文件**
- `CLAUDE.md`（项目级）：针对 python_learn 定制，包含完整规范
- `CLAUDE.template.md`（全局模板）：通用模板，可复用到其他项目

**3. AI 助手记忆方案**
- 建立对话记录系统（本文件）
- 通过项目文件实现跨会话"记忆"
- 每次对话后更新重要决策

#### 文件变更
- 新增：`CLAUDE.md` - 项目协作指南
- 新增：`CLAUDE.template.md` - 全局模板
- 新增：`.claude/conversations.md` - 本文件

#### 下一步计划
- [ ] 根据实际使用调整规范
- [ ] 记录重要的技术决策
- [ ] 定期更新对话历史

---

## 📅 2026-01-15

### 🎯 Claude Code Skills 深入学习

#### 背景
- 学习主题：Claude Code 的 Skills 功能
- 目标：理解 Skills 系统、与 Shell 脚本的区别、现成资源

#### 核心概念

**什么是 Skills？**
- Skills 是 Claude Code 的可扩展命令系统
- 类似于 CLI 的别名/脚本，但更强大
- 每个 Skill 是预定义的提示词模板
- 通过简短命令调用复杂工作流程

**Skills vs Shell 脚本对比**

| 维度 | Shell 脚本 | Claude Skills |
|------|-----------|---------------|
| 执行主体 | Shell 直接执行 | AI 解析后执行 |
| 确定性 | 完全确定 | 非确定性，AI 会调整 |
| 上下文感知 | 无 | 完全感知项目上下文 |
| 适用场景 | 简单、确定性操作 | 需要代码理解/灵活调整 |

**使用方式**
```bash
# 基本语法
/skill-name [arguments]

# 示例
/commit
/review-pr 123
```

**Skill 定义结构**
```
.claude/skills/
├── my-skill/
│   └── skill.md          # 定义文件（YAML frontmatter + 指令）
```

**skill.md 格式**
```markdown
---
description: "简短描述"
---

详细提示词内容...
变量可用：{{arg1}}, {{args}}, {{namedParam}}
```

#### 官方资源

**官方仓库**
- `anthropics/skills` - 官方公开仓库

**安装官方 Skills**
```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

**官方 Skills 分类**
- 文档处理：`docx`, `pdf`, `pptx`, `xlsx`
- 设计创意：`algorithmic-art`, `canvas-design`
- 开发工具：`frontend-design`, `mcp-builder`, `webapp-testing`
- 技能创建：`skill-creator`（交互式创建新 skill）

#### 社区资源

**精选列表**
- `travisvn/awesome-claude-skills` - 社区 skills 精选列表

**推荐社区 Skills**
- `obra/superpowers` - 20+ 实战技能库（TDD、调试、协作）
- `ios-simulator-skill` - iOS 应用自动化测试
- `playwright-skill` - 浏览器自动化
- `claude-d3js-skill` - D3.js 数据可视化

**安装 superpowers**
```bash
/plugin marketplace add obra/superpowers-marketplace
```

#### 安全注意事项

⚠️ **Skills 可以执行任意代码！**
- 只从可信来源安装
- 安装前先查看 `SKILL.md` 内容
- 检查仓库的 star 数和活跃度
- 企业环境应建立内部 skill 审核流程

#### 技术要点

**Progressive Disclosure 架构**
1. 元数据加载（~100 tokens）：扫描可用的 Skills
2. 完整指令（<5k tokens）：加载相关 Skills
3. 捆绑资源：按需加载文件和代码

**Skills 与其他工具对比**
- **Skills** - 可复用的流程知识
- **Prompts** - 一次性指令
- **Projects** - 工作空间内的持久背景
- **Subagents** - 具有特定权限的独立任务执行
- **MCP** - 外部数据/API 集成

#### 有用的链接
- 官方文档：https://code.claude.com/docs/en/skills
- 官方仓库：https://github.com/anthropics/skills
- 精选列表：https://github.com/travisvn/awesome-claude-skills

---

## 📅 [日期]

### 🎯 [对话主题]

#### 背景
- 项目状态：[描述]
- 遇到问题：[描述]
- 目标：[描述]

#### 决策记录
**1. [决策标题]**
- 选择：[方案/方案]
- 理由：[原因]
- 影响：[影响范围]

**2. [决策标题]**
- ...

#### 技术要点
- [技术点1]
- [技术点2]

#### 文件变更
- 新增/修改：[文件路径] - [变更说明]

#### 问题与解决
- **问题**：[描述]
- **解决方案**：[描述]
- **经验教训**：[描述]

#### 下一步计划
- [ ] [任务1]
- [ ] [任务2]

---

## 📊 项目重要信息

### 项目结构
```
python_learn/
├── automation/        # 自动化脚本
├── web/              # Web 项目（Django）
├── data_science/     # 数据科学
├── basics/           # Python 基础
├── concurrency/      # 并发编程
├── scraping/         # 网页抓取
├── douban_spider/    # Scrapy 爬虫
└── tools/            # 工具脚本
```

### 技术栈
- **语言**：Python 3.12
- **Web 框架**：Django, Flask
- **数据科学**：pandas, numpy, jupyter
- **爬虫**：scrapy, selenium, requests
- **测试**：pytest
- **环境**：Windows + WSL2 + venv

### 开发规范
- 代码风格：PEP 8
- 提交规范：Conventional Commits
- 文档语言：中文注释 + 英文代码
- 测试覆盖率：≥ 80%

### 重要文件
- `CLAUDE.md` - AI 协作指南（必读）
- `README.md` - 项目快速开始
- `study_plan.md` - 学习计划
- `.project-rules.yml` - 项目规范（YAML）
- `requirements.txt` - 依赖清单

---

## 🔄 会话使用指南

### 开始新对话时
1. AI 助手会自动读取：
   - `CLAUDE.md` - 了解项目规范
   - `.claude/conversations.md` - 了解历史决策
   - `README.md` - 了解项目概况

2. 更新对话记录：
   - 记录重要决策
   - 更新项目状态
   - 标注下一步计划

3. 保持记录简洁：
   - 只记录关键信息
   - 避免冗长描述
   - 使用结构化格式

---

**最后更新**：2026-01-15
