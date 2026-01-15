# Git Auto Push 技能

> 一句话完成 `git add + commit + push` 的自动化技能

## 功能特性

- ✅ **自动检测变更** - 识别新增、修改、删除的文件
- ✅ **智能分析 diff** - 理解代码改动的实际内容
- ✅ **自动选择类型** - 根据变更特征自动选择 feat/fix/refactor 等
- ✅ **生成中文提交信息** - 符合规范的中文提交消息
- ✅ **安全可控** - 执行前展示提交信息供确认
- ✅ **一键推送** - 自动推送到远程仓库

## 使用方法

### 在 Claude Code 中使用

```
用户: 帮我提交推送
```

或者：

```
用户: 提交代码
用户: quick commit
用户: /git-auto-push
```

### 技能执行流程

```
1. 检查 Git 状态 → 获取待提交文件
2. 分析 Diff 内容 → 理解改动含义
3. 生成提交信息 → feat/fix/refactor 等
4. 展示确认界面 → 用户确认后执行
5. Git Add + Commit + Push
6. 返回执行结果
```

## 提交类型识别

| 变更特征 | 类型 | 示例 |
|---------|------|------|
| 新增功能/文件 | feat | `feat(utils): 新增计算函数` |
| 修复 bug | fix | `fix(auth): 修复登录超时问题` |
| 重构代码 | refactor | `refactor(user): 重构用户验证逻辑` |
| 文档更新 | docs | `docs(readme): 更新安装说明` |
| 代码格式调整 | style | `style: 统一代码缩进` |
| 性能优化 | perf | `perf(api): 优化数据库查询` |
| 测试相关 | test | `test(utils): 添加单元测试` |
| 构建/工具链 | chore | `chore: 更新依赖版本` |

## 目录结构

```
.git-auto-push/
├── SKILL.md              # 技能定义（核心文件）
├── README.md             # 使用说明
├── examples/             # 使用示例
│   └── basic-usage.md
├── resources/            # 资源文件
│   └── commit-types.md
└── scripts/              # 辅助脚本
    └── analyze_diff.py   # Diff 分析工具
```

## 测试技能

```bash
# 创建测试文件
echo "# 测试" > test_file.md

# 在 Claude Code 中执行
帮我提交推送

# 或使用技能名
/git-auto-push
```

## 安全保证

- ❌ 绝不使用 `--force` 强制推送
- ❌ 绝不修改 Git 配置
- ✅ 推送前先 commit 成功
- ✅ 执行前必须获得用户确认

## 许可

MIT License
