# florist.contrib.meterial（素材管理）

`meterial`（历史拼写）提供“本地素材上传/管理/引用”的最小闭环，主要面向两类场景：

- 管理后台里上传、管理图片/文件（Flask-Admin FileAdmin）
- 富文本编辑器（CKEditor）里插入图片：提供上传接口与文件管理器

> 代码位置：`florist/contrib/meterial/`

---

## 快速启用（TL;DR）

1. 配置 `UPLOADED_PATH` 指向本地上传目录
2. 配置 `FLORIST_ADMIN_PACKAGES` 包含 `florist.contrib.meterial`
3. 若要在富文本里上传/选图：配置 `CKEDITOR_FILE_BROWSER` 与 `CKEDITOR_FILE_UPLOADER`

## 功能定位（理论）

素材系统通常需要解决：

- 文件的落盘/命名（避免重名、避免目录爆炸）
- 文件的管理界面（列表/删除/移动/搜索）
- 文件的访问控制与缓存策略（静态文件强缓存）
- 与富文本编辑器联动（上传、选择已有文件）

florist 的 `meterial` 当前选择“本地存储 + 强缓存 + 管理后台”的路径，并用 limiter 限制滥用。

---

## 现有实现（代码导读）

### 1）Flask-Admin FileAdmin

- 文件：`florist/contrib/meterial/admin.py`
- `admin.add_view(FileAdmin(...))`：把上传目录挂到 admin 里可管理
- 自定义 `_save_form_files()`：
  - 使用 sha256 对原文件名做 hash，减少冲突与泄漏原始名字

### 2）文件访问：`/meterial/<path:filename>`

- 通过 `@admin.app.route('/meterial/<path:filename>')` 提供文件访问
- 行为：
  - `send_from_directory(UPLOADED_PATH, filename)`
  - `Cache-Control: public, max-age=31536000, immutable`（强缓存 1 年）
  - 限流：`4/minute;40/day`，并以 `IP + path` 作为 key

### 3）CKEditor 上传接口：`/meterial/ckeditor_upload/`

- endpoint：`meterialadmin.ckeditor_upload`
- 仅允许图片扩展名：`jpg/gif/png/jpeg`
- 保存到 `UPLOADED_PATH` 根目录，并返回可访问 URL

### 4）文件管理器（flaskfilemanager）集成

- 初始化：`flaskfilemanager_init(admin.app, ...)`
- `custom_init_js_path`：用于相对路径等定制

---

## 如何启用（上游应用）

### 1）加入 Florist 管理后台包列表

```python
FLORIST_ADMIN_PACKAGES = (
    'florist.contrib.meterial',
)
```

### 2）配置上传目录

`meterial` 依赖：

- `UPLOADED_PATH`：本地上传根目录

### 3）与 CKEditor 联动（推荐）

```python
CKEDITOR_FILE_BROWSER = 'flaskfilemanager.index'
CKEDITOR_FILE_UPLOADER = 'meterialadmin.ckeditor_upload'
```

---

## 与 thumbs（缩略图）的关系

- `meterial` 负责“原文件上传与访问”（`/meterial/...`）
- `thumbs` 负责“基于原文件生成缩略图”（例如把 `/meterial/a.png` 生成 `/thumbs/...webp`）

要让 thumbs 能处理 meterial 的 URL，需要配置：

```python
FLORIST_THUMBS_SOURCE_PREFIXES = {
    '/meterial/': '',
}

---

## 代码入口

- `florist/contrib/meterial/admin.py`：Flask-Admin FileAdmin、上传与访问路由、flaskfilemanager 初始化
- `florist/contrib/meterial/static/`：filemanager init js

---

## 配置项

- `UPLOADED_PATH`：必需（保存上传文件，也用于 send_from_directory）
- `FLORIST_ADMIN_PACKAGES`：启用 admin view 与相关路由
- `CKEDITOR_FILE_BROWSER` / `CKEDITOR_FILE_UPLOADER`：CKEditor 集成
- `FLORIST_THUMBS_SOURCE_PREFIXES`：若希望缩略图支持 `/meterial/...` 源图

---

## TODO

- 上传安全增强：MIME/解码校验、大小限制、图片真实格式校验
- 文件命名与目录策略：当前 ckeditor_upload 直接用原始文件名保存（可能冲突）
- 鉴权/ACL：是否允许匿名访问 `/meterial/...` 取决于业务
```

---

## 安全与注意事项

- 当前上传接口只做了扩展名检查，生产环境建议进一步做：
  - MIME 类型校验
  - 图片解码校验（防 polyglot）
  - 限制文件大小
- `UPLOADED_PATH` 直接暴露给下载路由时，需要结合业务决定是否要鉴权。

