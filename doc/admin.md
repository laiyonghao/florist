# Admin（Flask-Admin）

Florist 通过 Flask-Admin 提供后台管理。

## 当前视图标题（category / name）

当你在 Flask-Admin 里使用 `category` 对菜单分组后，页面本体有时不够明显地提示“当前正在看的 ModelView”。

Florist 提供一个可选的标题条，在页面内容区（messages 下方、正文 `{% block body %}` 之前）展示：

- `{{ admin_view.category }} / {{ admin_view.name }}`（当 `category` 为空时只显示 `name`）

### 开关配置

默认开启。

- 开启（默认）：`FLORIST_ADMIN_SHOW_VIEW_TITLE = True`
- 关闭：`FLORIST_ADMIN_SHOW_VIEW_TITLE = False`

### 实现方式

- 通过在 florist 内提供模板覆盖 `admin/base.html`（bootstrap4 主题）实现。
- 在 `florist.admin.init(app, ...)` 中将 florist 的模板 loader 提前到 Jinja2 搜索顺序最前，从而优先于 Flask-Admin 自带模板。

文件位置：

- `florist/admin/templates/admin/base.html`
- `florist/admin/__init__.py`（安装模板 loader）
