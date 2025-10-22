# Python 学习与实战（自动化 / Web / 数据科学）

你每天投入 2 小时，本仓库帮你用“项目化 + 练习驱动”的方式同时推进三条路线：自动化、Web、数据科学。按周循序渐进，并提供示例与依赖清单。

## 快速开始（Windows PowerShell）
- 创建并启用虚拟环境：
  - `python -m venv .venv`
  - `./.venv/Scripts/Activate.ps1`
- 选择方向后安装依赖（示例见各子目录的 `requirements.txt`）：
  - 自动化：`pip install -r automation/requirements.txt`
  - Web：`pip install -r web/requirements.txt`
  - 数据科学：`pip install -r data_science/requirements.txt`

## 仓库结构
- `automation/` 自动化脚本与练习（文件批处理、Excel、抓取等）
- `web/` Flask Web 入门与小项目
- `data_science/` 数据分析与机器学习练习（建议使用 Jupyter）
- `study_plan.md` 详细学习计划（每天 2 小时，四周）

## 使用建议
- 每次练习尽量写“可运行的小成果”，并记录学到的要点。
- 为脚本添加命令行参数与 README，形成可复用的工具。
- 数据科学方向尽量用 Notebook 记录过程与结论，并输出一页可视化报告。
- Web 方向在完成基本路由后加入表单验证、数据库与登录，再考虑部署。

## 下一步
- 打开 `study_plan.md` 按每日任务推进。
- 从 `automation/01_rename_files.py` 或 `web/app.py` 起步，跑通第一个示例。
- 如果你希望我为你定制更细的每日任务或评审代码，告诉我你的近期优先级（自动化 / Web / 数据科学）。