# Django 入门

## 安装依赖
- 激活虚拟环境：`./.venv/Scripts/Activate.ps1`
- 安装：`pip install -r web/requirements.txt`

## 运行开发服务器
- `python web/manage.py runserver`
- 浏览器访问：`http://127.0.0.1:8000/`

## 结构说明（最小骨架）
- `web/manage.py`：Django 管理命令入口
- `web/mysite/`：项目配置（settings/urls/asgi/wsgi）
- `web/core/`：示例应用（首页视图与路由）

## 下一步建议
- 新增模板与静态资源，改用模板渲染首页。
- 添加一个模型（如 `Task`）并通过 `admin` 后台管理。
- 按需引入 `djangorestframework` 提供 API。