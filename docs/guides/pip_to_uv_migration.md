# 从 pip 迁移到 uv 系统性指南

本指南详细说明了将 Python 项目从标准 pip 依赖管理迁移到 uv 的标准化流程，适用于 Windows、WSL 和 Linux 多环境协作场景。

## 1. 环境准备与工具安装

在开始迁移前，需确保所有开发环境（Windows/WSL/Linux）均已安装 uv 工具。

### 安装命令
- **Linux / WSL / macOS**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source $HOME/.local/bin/env
  ```
- **Windows (PowerShell)**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **验证安装**:
  ```bash
  uv --version
  ```

## 2. 项目迁移流程

对每个项目执行以下标准化迁移步骤：

### a. 备份与清理
在进行任何更改前，备份现有的依赖配置文件：
```bash
cp requirements.txt requirements.txt.bak
# 如果有 pyproject.toml 但未使用 uv
cp pyproject.toml pyproject.toml.bak
```
建议删除旧的虚拟环境以确保清洁迁移（可选但推荐）：
```bash
rm -rf .venv
```

### b. 初始化 uv 项目
如果项目尚未使用 `pyproject.toml`，建议通过 uv 初始化：
```bash
uv init
```
这将生成基础的 `pyproject.toml` 和 `.python-version` 文件。

### c. 依赖转换与安装
将 `requirements.txt` 中的依赖迁移到 `pyproject.toml` 并安装。

**方式一：自动导入（推荐）**
使用 `uv add` 逐步添加核心依赖，这会自动更新 `pyproject.toml` 并生成 `uv.lock`：
```bash
# 逐个添加（更精确控制版本约束）
uv add package_name

# 或者批量从 requirements.txt 读取（需要手动解析或脚本辅助，目前 uv add -r 支持正在开发中，建议手动整理核心依赖）
# 替代方案：直接使用 pip 接口安装但不生成 lock（不推荐用于最终状态）
# uv pip install -r requirements.txt
```

**方式二：保持 requirements.txt 模式（兼容旧流程）**
如果必须保留 `requirements.txt` 作为单一事实来源：
```bash
uv venv
uv pip install -r requirements.txt
```
*注意：此模式不会生成 `uv.lock`，无法享受 uv 的确定性锁定优势。*

**推荐目标状态**：
项目根目录应包含 `pyproject.toml` 和 `uv.lock`。

### d. 生成依赖锁定文件
确保执行一次全量锁定以生成 `uv.lock`：
```bash
uv lock
```
此文件应提交到版本控制系统中，以确保跨环境的一致性。

## 3. 跨环境一致性保障

### 依赖同步
在不同环境中拉取代码后，使用以下命令同步环境：
```bash
uv sync
```
该命令会根据 `uv.lock` 精确还原依赖环境。

### 系统级差异处理
对于包含系统级二进制依赖的包（如 `psycopg2`, `numpy` 等），uv 会自动根据当前平台（Windows/Linux）下载对应的预编译 wheel 包。
- 检查 `pyproject.toml` 中的 `[tool.uv]` 部分（如有）是否包含特定平台约束。
- 确保所有环境的 Python 主版本号一致（通过 `.python-version` 文件锁定）。

## 4. 迁移后验证

1.  **功能测试**：运行项目测试套件（`pytest`）确保核心功能正常。
2.  **性能对比**：观察依赖安装速度，uv 通常比 pip 快 10-100 倍。
3.  **环境检查**：
    ```bash
    uv pip list
    ```
    确认已安装的包列表与预期一致。

## 5. 常用命令速查

| 任务 | 旧 pip 命令 | 新 uv 命令 |
| :--- | :--- | :--- |
| 创建虚拟环境 | `python -m venv .venv` | `uv venv` |
| 激活环境 | `source .venv/bin/activate` | `source .venv/bin/activate` (或直接用 uv run) |
| 安装依赖 | `pip install -r requirements.txt` | `uv sync` (基于 lock) 或 `uv pip install` |
| 添加依赖 | `pip install pkg` + 手动更新文件 | `uv add pkg` |
| 移除依赖 | `pip uninstall pkg` + 手动更新文件 | `uv remove pkg` |
| 运行脚本 | `python script.py` | `uv run script.py` |

## 6. 回滚方案

如果迁移出现严重问题，可随时回滚：
1. 删除 `uv.lock` 和 `pyproject.toml`（如果是新生成的）。
2. 恢复 `requirements.txt.bak`。
3. 使用标准 pip 重新安装：`pip install -r requirements.txt`。
