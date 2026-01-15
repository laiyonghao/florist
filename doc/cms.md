# florist.contrib.cms（内容管理）

`cms` 是 florist 的内容管理模块，当前实现偏向“文章/图文内容”的最小闭环：

- 数据模型：`Article`（MongoEngine Document）
- 管理后台：基于 Flask-Admin 的 `ArticleView`，并集成 CKEditor 富文本编辑

> 代码位置：`florist/contrib/cms/`

---

## 快速启用（TL;DR）

1. 配置 `FLORIST_ADMIN_PACKAGES` 包含 `florist.contrib.cms`
2. 确保已初始化 florist admin（`florist.admin.init(app)` 或通过 `florist.init(app)`）
3. 可选：配合 `florist.contrib.meterial` 作为富文本图片上传/选择能力

## 功能定位（理论）

内容管理（CMS）的核心是：

- 用一个相对稳定的数据结构表达内容（标题、正文、内容类型、发布时间、更新时间）
- 提供可编辑、可预览、可发布的操作界面（通常是 admin）

florist 的 `cms` 目前只实现了“文章管理”这条主线，足够支撑：

- 站点公告/博客/图文页
- 与素材库（`meterial`）组合：富文本里插入图片

---

## 现有实现（代码导读）

### 1）模型：`Article`

- 文件：`florist/contrib/cms/models.py`
- 字段：
  - `title`：标题
  - `content`：正文（字符串）
  - `content_type`：`EnumField`（`rt` 富文本 / `md` Markdown），目前默认 `RichText`
  - `published_at`：发布时间
  - `updated_at`：更新时间（在 `save()` 里自动更新）

设计点：

- `save()` 重写用于维护 `updated_at`，避免上层忘记设置。

### 2）管理后台：`ArticleView`

- 文件：`florist/contrib/cms/admin.py`
- 关键点：
  - `form_overrides = dict(content=CKEditorField)`：把 `content` 字段替换成 CKEditor
  - `form_excluded_columns` 排除一些自动字段
  - `create_template/edit_template` 指向 `cms/templates/admin/*.html`（用于 CKEditor 相关定制）

依赖：

- `flask_ckeditor`：编辑器与字段
- `florist.admin`：`admin` 与 `ModelView`

---

## 如何启用（上游应用）

### 1）加入 Florist 管理后台包列表

在上游应用配置中增加：

```python
FLORIST_ADMIN_PACKAGES = (
    'florist.contrib.cms',
    # ...其他包
)
```

Florist 会在初始化 admin 时自动 import：`{pkg}.admin`，从而完成 view 注册。

### 2）CKEditor 与上传联动（常见组合）

如果你希望在 CMS 富文本里直接上传/选择图片，推荐同时启用 `florist.contrib.meterial` 并配置 CKEditor uploader：

- `CKEDITOR_FILE_BROWSER = 'flaskfilemanager.index'`
- `CKEDITOR_FILE_UPLOADER = 'meterialadmin.ckeditor_upload'`

（xhh 的配置就是这种组合）

---

## 代码入口

- `florist/contrib/cms/models.py`：`Article`
- `florist/contrib/cms/admin.py`：`ArticleView`（Flask-Admin + CKEditor）
- `florist/contrib/cms/templates/admin/`：admin 编辑页面模板

---

## 配置项

- `FLORIST_ADMIN_PACKAGES`：启用 admin view 注册
- `CKEDITOR_*`：CKEditor 的文件浏览/上传（建议配合 `meterial`）

---

## TODO

- 增加前台展示（public view）与渲染模板
- `content_type=Markdown` 的渲染与编辑体验
- 更完整的发布流程（草稿/发布/撤回）

---

## 注意事项

- `ContentTyep`（拼写）目前是 Enum 名称，功能不受影响，但后续若对外暴露 API，建议统一命名。
- 目前没有前台路由（public view）与渲染模板，CMS 主要用于“后台管理”。前台展示可由上游项目自行实现。

