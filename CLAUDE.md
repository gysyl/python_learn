# CLAUDE.md - AI 助手协作指南

> 本文件定义 AI 助手（Claude Code）在本项目中的行为规范、代码风格和协作流程，确保 AI 生成的代码与项目标准保持一致。

最后更新：2026-01-13

---

## 📋 项目概述

**项目名称**：python_learn
**项目类型**：Python 学习与实战项目（自动化 / Web / 数据科学）
**开发环境**：Windows + WSL2 + Python 3.12 + uv
**包管理**：uv (pyproject.toml)

### 项目结构
```
python_learn/
├── automation/        # 自动化脚本（文件批处理、Excel、抓取）
├── web/              # Web 项目（Django/Flask）
├── data_science/     # 数据分析与机器学习
├── basics/           # Python 基础
├── concurrency/      # 并发编程
├── scraping/         # 网页抓取
├── douban_spider/    # Scrapy 爬虫项目
├── networking/       # 网络编程
├── oop/              # 面向对象编程
├── tools/            # 工具脚本
└── tests/            # 测试文件（各模块下）
```

---

## 🌐 语言偏好约定

### 核心原则
**代码注释和文档使用中文，其他代码元素使用英文**

### 具体规范

| 代码元素 | 语言 | 示例 |
|---------|------|------|
| 变量名 | 英文 | `user_count`, `is_valid` |
| 函数名 | 英文 | `calculate_total()`, `fetch_data()` |
| 类名 | 英文（PascalCase） | `UserManager`, `DatabaseHandler` |
| 常量 | 英文（UPPER_CASE） | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT` |
| 代码注释 | 中文 | `# 计算用户总数` |
| 文档字符串（docstring） | 中文 | `"""获取用户信息"""` |
| README/文档 | 中文 | 使用中文编写说明 |
| 日志消息 | 中文 | `logger.info("开始处理数据")` |
| 异常消息 | 中文 | `raise ValueError("参数不能为空")` |
| 测试描述 | 中文 | `def test_用户登录成功():` |

### 命名风格示例

```python
# ✅ 正确示例
def process_user_data(user_list: list[dict]) -> dict:
    """
    处理用户数据并返回统计信息

    Args:
        user_list: 用户列表，每个用户是包含 id 和 name 的字典

    Returns:
        包含统计信息的字典，如 {'total': 100, 'active': 80}
    """
    total_count = len(user_list)
    active_users = [u for u in user_list if u.get('is_active', False)]
    return {
        'total': total_count,
        'active': len(active_users)
    }

# ❌ 错误示例
def 处理用户数据(用户列表: list) -> dict:  # 函数名不应使用中文
    """Process user data"""  # 文档字符串应使用中文
    pass
```

---

## 🔧 环境管理

### ⚠️ 强制规则：必须使用 uv 管理依赖

**本项目使用 uv 作为统一的包管理器，取代传统的 pip/venv 工作流。**

#### 为什么使用 uv？

- 🚀 **速度**：比 pip 快 10-100 倍
- 🔒 **锁定**：`uv.lock` 确保跨环境的绝对一致性
- 📦 **统一**：集成了 python 版本管理、虚拟环境和包安装
- 🛡️ **兼容**：完全兼容 pip 接口，但在项目中优先使用 uv 原生命令

#### uv 使用规范

```bash
# 1. 初始化/同步环境（自动创建 .venv 并安装依赖）
uv sync

# 2. 激活虚拟环境
# WSL/Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\activate

# 3. 添加新依赖
uv add package_name

# 4. 运行命令（推荐使用 uv run，无需显式激活）
uv run python script.py
```

#### AI 助手必须遵守

✅ **始终检查 uv 环境状态：**
- 优先使用 `uv run` 执行脚本
- 修改依赖时使用 `uv add` 或 `uv remove`
- 确保 `uv.lock` 与 `pyproject.toml` 同步

❌ **禁止行为：**
- ❌ 直接使用 `pip install` 修改环境（除非临时测试）
- ❌ 手动修改 `requirements.txt`（应修改 `pyproject.toml`）

#### 验证环境

```bash
# 检查 uv 状态
uv version
# 检查依赖树
uv tree
```

#### 依赖管理

- 所有依赖必须记录在 `pyproject.toml` 中
- `uv.lock` 必须提交到版本控制


---

## 📝 代码风格规范

### 基础规范

- **缩进**：使用 4 空格，禁止使用 Tab
- **行长**：每行最多 88 字符（Black 默认）
- **编码**：UTF-8
- **导入顺序**：标准库 → 第三方库 → 本地模块

```python
# 导入顺序示例
import os  # 标准库
import sys
from typing import Optional, List

import requests  # 第三方库
from django.db import models

from .utils import helper_function  # 本地模块
```

### 类型注解

- 所有函数必须添加类型注解
- 使用 `typing` 模块提供类型
- 复杂类型使用 `TypeAlias`

```python
from typing import Optional, List, Dict, TypeAlias

# 类型别名定义
UserId: TypeAlias = int
UserInfo: TypeAlias = Dict[str, str | int]

def get_user(user_id: UserId) -> Optional[UserInfo]:
    """根据用户 ID 获取用户信息"""
    # 实现逻辑
    pass
```

### 字符串格式化

- 优先使用 f-string
- 避免使用 `%` 格式化或 `str.format()`

```python
# ✅ 推荐
name = "张三"
greeting = f"你好，{name}！"

# ❌ 避免
greeting = "你好，%s！" % name
greeting = "你好，{}！".format(name)
```

### 错误处理

- 明确捕获异常类型
- 使用 `logging` 记录错误
- 禁止使用裸 `except:`

```python
import logging

logger = logging.getLogger(__name__)

def process_file(file_path: str) -> None:
    """处理文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        logger.error(f"文件未找到: {file_path}")
        raise
    except PermissionError:
        logger.error(f"权限不足，无法读取: {file_path}")
        raise
```

---

## 🏗️ 代码组织原则

### 函数设计

- **单一职责**：每个函数只做一件事
- **长度限制**：函数不超过 25 行（特殊情况除外）
- **参数限制**：参数不超过 5 个，多参数考虑使用对象

```python
# ✅ 良好的函数设计
def send_notification(
    user_id: int,
    message: str,
    channel: str = "email"
) -> bool:
    """
    发送通知给用户

    Args:
        user_id: 用户 ID
        message: 通知内容
        channel: 通知渠道（email/sms/push）

    Returns:
        是否发送成功
    """
    # 实现逻辑
    pass

# ❌ 需要重构的函数
def send_notification(user_id, message, channel, priority, retry, timeout, headers):  # 参数过多
    pass
```

### 模块组织

- 每个模块不超过 200 行
- 相关功能组织在同一个包中
- 共享工具放在 `common/` 或 `utils/` 目录

### 嵌套控制

- 嵌套深度不超过 3 层
- 使用早返回（early return）减少嵌套

```python
# ✅ 早返回模式
def validate_user(user: dict) -> bool:
    """验证用户数据"""
    if not user:
        return False
    if 'id' not in user:
        return False
    if 'name' not in user:
        return False
    return True

# ❌ 深层嵌套
def validate_user(user: dict) -> bool:
    if user:
        if 'id' in user:
            if 'name' in user:
                return True
    return False
```

---

## 🧪 测试规范

### 测试框架

- 使用 `pytest` 作为测试框架
- 测试文件命名：`test_*.py` 或 `*_test.py`
- 测试函数命名：`test_*` 或使用中文描述 `test_功能描述`

### 测试结构

```python
import pytest

def test_用户登录成功():
    """测试用户成功登录的场景"""
    # Arrange（准备）
    username = "test_user"
    password = "correct_password"

    # Act（执行）
    result = login(username, password)

    # Assert（断言）
    assert result is True
    assert result.user_id == 1

def test_用户登录失败_密码错误():
    """测试用户登录失败的场景"""
    # 测试逻辑
    pass
```

### 测试覆盖率

- 总体覆盖率目标：≥ 80%
- 核心模块覆盖率：≥ 90%
- 运行命令：
  ```bash
  # 运行测试
  pytest -q

  # 生成覆盖率报告
  pytest --cov=src --cov-report=term-missing
  ```

---

## 🔒 安全规范

### 敏感数据管理

- 禁止将密钥、密码等提交到代码仓库
- 使用环境变量或 `.env` 文件管理敏感信息
- `.env` 文件必须添加到 `.gitignore`

```python
# ✅ 正确做法
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
db_password = os.getenv('DB_PASSWORD')

# ❌ 错误做法
api_key = "sk-1234567890abcdef"  # 永远不要硬编码密钥
```

### 输入验证

- 对所有外部输入进行验证
- 文件路径、网络请求、用户输入都需要验证

```python
import os
from pathlib import Path

def safe_read_file(file_path: str) -> str:
    """安全地读取文件"""
    # 验证路径
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 防止路径遍历攻击
    if not str(path).startswith(os.getcwd()):
        raise PermissionError("不允许访问父目录")

    return path.read_text(encoding='utf-8')
```

---

## 📚 文档规范

### 文档字符串（docstring）

- 使用 Google 风格的 docstring
- 包含功能描述、参数说明、返回值、异常

```python
def calculate_discount(
    original_price: float,
    discount_rate: float,
    user_level: int = 1
) -> float:
    """
    计算折扣后的价格

    Args:
        original_price: 原价
        discount_rate: 折扣率（0-1 之间）
        user_level: 用户等级，用于计算额外折扣

    Returns:
        折扣后的价格

    Raises:
        ValueError: 当折扣率不在 0-1 之间时

    Example:
        >>> calculate_discount(100, 0.8, 2)
        75.0
    """
    if not 0 <= discount_rate <= 1:
        raise ValueError("折扣率必须在 0-1 之间")
    return original_price * discount_rate * (1 - user_level * 0.05)
```

### README 规范

每个重要模块/项目应包含 README.md：

```markdown
# 模块名称

简要描述模块的功能和用途。

## 功能特性

- 特性 1
- 特性 2

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```python
import module
module.run()
```

## 注意事项

- 注意事项 1
- 注意事项 2
```

---

## 🔄 Git 工作流

### 提交消息规范（Conventional Commits）

格式：`<type>(scope): <subject>`

**类型（type）：**
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链

**示例：**
```bash
feat(auth): 添加用户登录失败重试机制
fix(database): 修复连接池泄漏问题
docs(readme): 更新安装说明
refactor(user): 重构用户验证逻辑
```

### 分支策略

- `main`: 稳定分支
- `dev`: 开发分支
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复分支

---

## 🤖 AI 助手协作指南

### AI 助手应该做什么

✅ **推荐行为：**
- 遵循本文件中定义的所有代码规范
- 使用中文编写注释和文档
- 使用英文命名变量、函数、类
- 在修改代码前先阅读相关文件
- 为生成的代码添加适当的文档字符串
- 考虑边界条件和错误处理
- 保持代码简洁，避免过度设计

❌ **避免行为：**
- 不要过度设计或添加不必要的抽象
- 不要在修复 bug 时重构无关代码
- 不要使用 emojis（除非明确要求）
- 不要跳过测试就声称功能完成
- 不要硬编码敏感信息
- 不要生成过长的函数（超过 25 行）

### 代码审查清单

AI 助手在提交代码前应检查：

- [ ] 代码注释使用中文
- [ ] 变量/函数名使用英文
- [ ] 添加了类型注解
- [ ] 包含文档字符串（中文）
- [ ] 处理了可能的异常
- [ ] 函数长度 ≤ 25 行
- [ ] 嵌套深度 ≤ 3 层
- [ ] 没有硬编码的敏感信息
- [ ] 使用 f-string 格式化字符串
- [ ] 导入顺序正确（标准库 → 第三方 → 本地）

### 常用命令参考
 
 ```bash
 # 激活虚拟环境（WSL）
 source .venv/bin/activate
 
 # 初始化/同步环境
 uv sync
 
 # 添加依赖
 uv add package_name
 
 # 运行测试
 uv run pytest -q
 
 # 运行特定测试
 uv run pytest tests/test_module.py::test_function
 
 # 生成覆盖率报告
 uv run pytest --cov=src --cov-report=term-missing
 
 # Django 运行服务器
 uv run python manage.py runserver
 
 # Django 数据库迁移
 uv run python manage.py makemigrations
 uv run python manage.py migrate
 ```

---

## 📖 学习资源

### 项目内文档

- `study_plan.md`: 详细学习计划（四周）
- `README.md`: 项目快速开始指南
- `.project-rules.yml`: 完整的项目规范（YAML 格式）

### 外部资源

- [Python 官方文档](https://docs.python.org/zh-cn/3/)
- [Django 官方文档](https://docs.djangoproject.com/zh-hans/)
- [pytest 文档](https://docs.pytest.org/)

---

## 📞 联系与反馈

如果在使用 AI 助手过程中遇到问题或有改进建议，请：
- 提交 issue 到项目仓库
- 更新本文件以完善协作指南

---

**版本历史：**

- v1.1 (2026-01-13): 新增虚拟环境强制使用规则
- v1.0 (2026-01-13): 初始版本，定义基础协作规范
