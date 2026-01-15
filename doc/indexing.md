# florist.contrib.*（模块接入方式与索引）

这一页解释 florist 的 contrib 模块如何被上游应用启用，以及为什么 florist 把“可对外使用的功能”放到 `florist.contrib.*`。

---

## 快速启用（TL;DR）

- 管理后台扩展模块：把包名加入 `FLORIST_ADMIN_PACKAGES`（Florist 会自动 import `pkg.admin`）
- 像 `thumbs` 这种“模板/静态能力”：直接调用模块提供的 `init(app)`

## 约定：contrib 包是什么

- `florist.contrib.<name>`：可被上游项目“直接启用/复用”的功能模块。
- 常见形式：
  - 提供 `admin.py`：注册 Flask-Admin 的 views
  - 提供 blueprint：对外暴露路由
  - 提供 models：MongoEngine 数据模型

---

## 上游如何启用（核心机制）

Florist 管理后台初始化时会读取：

- `FLORIST_ADMIN_PACKAGES`：一个 Python import path 列表

并对每个包执行：

- `import_module(f'{pkg}.admin')`

因此：

- 只要 `florist.contrib.xxx/admin.py` 里有 `admin.add_view(...)` 之类的注册逻辑，上游把包加进配置即可生效。

示例：

```python
FLORIST_ADMIN_PACKAGES = (
    'florist.contrib.meterial',
    'florist.contrib.cms',
    'florist.contrib.event',
)
```

---

## thumbs 是个例外（但也遵循 contrib 约定）

`thumbs` 更多面向“模板层能力 + 静态文件缓存”，不依赖 admin 包机制：

- 初始化入口：`florist.contrib.thumbs.init(app)`
- 对外能力：Jinja filter `thumb` + `/thumbs` blueprint

（详见 `doc/thumbs.md`）

---

## 代码入口

- `florist/admin/__init__.py`：读取 `FLORIST_ADMIN_PACKAGES` 并 import `{pkg}.admin`
- `florist/contrib/*/admin.py`：各模块注册 Flask-Admin views 的入口
- `florist/contrib/thumbs/__init__.py`：thumbs 的 `init(app)`（非 admin 模式）

---

## 配置项

- `FLORIST_ADMIN_PACKAGES`：启用哪些 contrib 模块的 admin 扩展
- `FLORIST_ADMIN_URL` / `FLORIST_ADMIN_SITE_NAME`：管理后台基本信息
- `THUMBS_*`：缩略图模块配置（详见 thumbs 文档）

---

## TODO

- 为各 contrib 模块补齐更一致的“启用方式/配置项/代码入口”说明（目前以 doc 为准）

