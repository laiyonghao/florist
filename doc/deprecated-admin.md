# florist.contrib.deprecated-admin（已弃用的简易后台示例）

`deprecated-admin` 是一个早期的“手写后台登录/注册”示例 blueprint，当前建议视为历史遗留（deprecated）。

> 代码位置：`florist/contrib/deprecated-admin/`

---

## 快速启用（TL;DR）

不建议用于生产。

如果只是本地 demo：可以直接参考 `florist/contrib/deprecated-admin/__init__.py` 的 blueprint 写法，按需复制/改造到你自己的模块里。

注意：该示例与 florist 当前的管理后台体系（Flask-Admin）不是一套东西，避免混用。

## 做了什么（现有实现）

- `admin_bp`：一个 Flask Blueprint
- `User`：MongoEngine Document，字段包含 username / hashed_password / is_staff / first_name / last_name
- 路由：
  - `GET /`：登录页（`signin.html`）
  - `POST /register/`：注册
  - `POST /auth/`：鉴权
  - `GET /signout/`：退出
  - `GET /dashboard/`：示例 dashboard

模板：`templates/signin.html` 基于 Tailwind 表单样式。

---

## 为什么标记为 deprecated

这个模块的实现更像“原型 demo”，与 florist 当前更推荐的方案不一致：

- 未实现会话/持久登录（没有使用 Flask-Login / Flask-Security 等）
- `g.user` 仅在单次请求上下文有效
- 密码 hash 只是 sha256（没有 per-user salt、没有 password hashing 的专用算法/参数）

因此不建议在生产中使用。

---

## 推荐替代方案

- 若你需要用户体系与后台鉴权：优先用 `Flask-Security-Too`（florist 本身已依赖）或 Flask-Login。
- 若你只需要管理后台：优先使用 `florist.admin` + `florist.user` 提供的管理入口。

---

## 何时仍有价值

- 作为“快速 demo/教学样例”参考 blueprint + template 的组织方式
- 作为 Tailwind 登录页模板素材

---

## 代码入口

- `florist/contrib/deprecated-admin/__init__.py`：blueprint 与示例路由
- `florist/contrib/deprecated-admin/templates/`：登录页模板

---

## 配置项

- 暂无（仅 demo；真实项目建议切换到 Flask-Security-Too / Flask-Login）

---

## TODO

- （仅作练习）补齐 session/login、密码 hashing、CSRF 等


