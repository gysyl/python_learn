# Skill: Auto Commit & Push (Chinese)

## Description
自动读取当前 Git 仓库的变更，生成高质量中文提交信息，并执行 git add、git commit、git push。  
结合“Auto Git Commit Message”技能使用，可实现全自动化提交流程。

## When to use
当用户：
- 输入“提交并推送”
- 输入“自动提交”
- 输入“帮我 push”
- 输入“自动生成提交并推送”
- 请求“一键提交”

## Behavior
### 1. 自动读取 Git 变更
调用 `scripts/get-diff.sh` 获取：
- staged diff
- unstaged diff
- 文件列表

### 2. 自动生成中文提交信息
调用“Auto Git Commit Message”技能，根据 diff 自动生成提交说明。

### 3. 自动执行 Git 操作
调用 `scripts/commit-and-push.sh`：
- `git add .`
- `git commit -m "<自动生成的中文提交信息>"`
- `git push`

### 4. 安全要求
- 如果没有变更，提示用户“没有可提交的内容”
- 如果 push 失败（如未设置远程），提示用户检查 Git 配置
- 如果用户要求英文提交信息，则生成双语版本

## Resources
- scripts/get-diff.sh
- scripts/commit-and-push.sh
- resources/commit-style-guide.md
- resources/keywords.json
