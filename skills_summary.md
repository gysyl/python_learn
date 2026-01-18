# User 级别 Skills 功能总结

> 本文档总结了项目中所有 user 级别的技能及其主要功能

最后更新：2026-01-18

---

## 📊 技能概览

当前项目共有 **1 个** user 级别的技能：

| 技能名称 | 功能描述 | 主要用途 |
|---------|---------|---------|
| `git-auto-push` | Git 自动提交推送 | 一键完成 git add + commit + push |

---

## 🔧 技能详细说明

### 1. Git Auto Push

**技能标识：** `git-auto-push`

**功能描述：** 一句话完成 `git add + commit + push` 的自动化技能，自动分析 diff 并生成中文提交信息

#### 核心功能

- ✅ **自动检测变更** - 识别新增、修改、删除的文件
- ✅ **智能分析 diff** - 理解代码改动的实际内容
- ✅ **自动选择类型** - 根据变更特征自动选择 feat/fix/refactor 等
- ✅ **生成中文提交信息** - 符合规范的中文提交消息
- ✅ **安全可控** - 执行前展示提交信息供确认
- ✅ **一键推送** - 自动推送到远程仓库

#### 使用方法

在 Claude Code 中使用以下任一方式触发：

```
用户: 帮我提交推送
用户: 提交代码
用户: quick commit
用户: /git-auto-push
```

#### 执行流程

```
1. 检查 Git 状态 → 获取待提交文件
2. 分析 Diff 内容 → 理解改动含义
3. 生成提交信息 → feat/fix/refactor 等
4. 展示确认界面 → 用户确认后执行
5. Git Add + Commit + Push
6. 返回执行结果
```

#### 提交类型识别规则

| 变更特征 | 类型 | 示例提交信息 |
|---------|------|------------|
| 新增功能/文件 | feat | `feat(utils): 新增计算函数` |
| 修复 bug | fix | `fix(auth): 修复登录超时问题` |
| 重构代码 | refactor | `refactor(user): 重构用户验证逻辑` |
| 文档更新 | docs | `docs(readme): 更新安装说明` |
| 代码格式调整 | style | `style: 统一代码缩进` |
| 性能优化 | perf | `perf(api): 优化数据库查询` |
| 测试相关 | test | `test(utils): 添加单元测试` |
| 构建/工具链 | chore | `chore: 更新依赖版本` |

#### 提交信息格式

```
<type>(<scope>): <subject>

# 详细说明（可选）
<详细描述改动内容>
```

**示例：**
- `feat(auth): 添加用户登录失败重试机制`
- `fix(database): 修复连接池泄漏问题`
- `docs(readme): 更新安装说明`

#### 前置条件

- 当前目录必须是 Git 仓库
- 已配置远程仓库（origin）
- 有待提交的变更
- 已配置 Git 用户信息（git config user.name/email）

#### 安全保证

- ❌ 绝不使用 `--force` 或 `--force-with-lease` 强制推送
- ❌ 绝不修改 Git 配置
- ✅ 推送前先 commit 成功
- ✅ 执行前必须获得用户确认

#### 技能文件位置

```
.claude/skills/git-auto-push/
├── SKILL.md              # 技能定义（核心文件）
├── README.md             # 使用说明
├── examples/             # 使用示例
│   └── basic-usage.md
├── resources/            # 资源文件
│   └── commit-types.md
└── scripts/              # 辅助脚本
    └── analyze_diff.py   # Diff 分析工具
```

---

## 📝 使用示例

### 示例 1：新增功能提交

```bash
# 用户修改了 utils.py，新增了 calculate_tax() 函数
用户: 帮我提交推送

# 技能执行：
# 1. 检测到 utils.py 有变更
# 2. 分析 diff：新增税率计算函数
# 3. 生成提交信息：feat(utils): 新增税率计算函数
# 4. 展示给用户确认
# 5. 执行 git add → commit → push
# 6. 报告成功
```

### 示例 2：修复 bug 提交

```bash
# 用户修复了 auth.py 中的登录超时问题
用户: 提交代码

# 技能执行：
# 1. 检测到 auth.py 有变更
# 2. 分析 diff：修改了超时处理逻辑
# 3. 生成提交信息：fix(auth): 修复登录超时问题
# 4. 展示给用户确认
# 5. 执行 git add → commit → push
# 6. 报告成功
```

---

## 🎯 总结

当前项目中的 `git-auto-push` 技能主要用于简化日常开发的 Git 提交流程，通过智能分析代码变更，自动生成符合规范的中文提交信息，并一键完成提交和推送操作，大大提高了开发效率。

该技能特别适合：
- 日常开发的快速提交场景
- 需要保持提交信息规范的团队协作
- 希望减少重复性 Git 操作的开发者

---

**文档版本：** v1.0
**维护者：** 项目维护团队
