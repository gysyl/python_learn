# Skill: Auto Commit & Push (Chinese)

自动读取当前 Git 仓库的变更，生成高质量中文提交信息，并执行 git add、git commit、git push。

## When to use

当用户说：
- "提交并推送"
- "自动提交"
- "帮我 push"
- "自动生成提交并推送"
- "一键提交"

## What it does

1. **检查git状态** - 获取当前工作目录的git变更
2. **分析变更** - 识别新增、修改、删除的文件
3. **生成提交信息** - 根据变更自动生成中文提交说明
4. **执行git操作** - 自动执行 `git add .`、`git commit`、`git push`
5. **反馈结果** - 告知用户提交是否成功

## Example

User: "提交并推送"
