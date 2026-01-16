# Git Auto Push 使用示例

## 示例 1：基础用法

```
用户: 帮我提交推送

技能:
📋 检测到变更：
M  local_test.py

📝 生成的提交信息：
feat: 新增测试脚本

确认执行？(Y/n) > Y

✓ 添加文件成功
✓ 提交成功：commit abc1234
✓ 推送成功：origin/main
```

## 示例 2：多文件变更

```
用户: 提交并推送

技能:
📋 检测到变更：
M  automation/process.py
M  tests/test_process.py
A  automation/config.yaml

📝 生成的提交信息：
feat(automation): 添加配置文件支持并完善测试

确认执行？(Y/n) > Y

✓ 添加文件成功
✓ 提交成功：commit def5678
✓ 推送成功：origin/main
```

## 示例 3：Bug 修复

```
用户: 快速提交

技能:
📋 检测到变更：
M  utils/helper.py

📝 生成的提交信息：
fix(utils): 修复字符串处理函数的空值异常

确认执行？(Y/n) > Y

✓ 添加文件成功
✓ 提交成功：commit 9012abc
✓ 推送成功：origin/main
```

## 示例 4：无变更时

```
用户: 帮我提交

技能:
✓ 当前工作目录干净，无需提交
```
