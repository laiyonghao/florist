# Florist Thumbs（缩略图）

> 目标：用户上传的原图可能很大（例如头像、素材图），但站内展示通常很小。我们希望**按需**生成缩略图（不预生成多规格），并且让模板作者用一条 DSL 就能精确控制缩放/裁剪/格式/质量，同时把攻击面和资源消耗控制在可接受范围内。

## 你会得到什么

- **模板层一行搞定**：`{{ avatar_url|thumb('w72h72cc-q70jpg') }}`
- **按需生成 + 落盘缓存**：第一次访问生成并写入磁盘，后续直接命中。
- **可控且安全**：只允许白名单 URL 前缀映射到本地文件；限制尺寸、放大倍数、输出格式。
- **Fail-open**：任何异常都回退到原图 URL，不影响页面渲染（只是可能加载原图）。

对应实现位于：`florist.contrib.thumbs`。

---

## 快速启用（TL;DR）

1. 配置 `UPLOADED_PATH`
2. 配置 `THUMBS_SOURCE_PREFIXES`（URL 前缀白名单 → 本地目录映射）
3. 模板中使用：`{{ url|thumb('w72h72cc-q70jpg') }}`

## 架构概览（实现与数据流）

核心组件：

- `florist.contrib.thumbs.filter`：注册 Jinja filter `thumb`
- `florist.contrib.thumbs.generator.ensure_thumb()`：
  - URL → 本地文件路径解析（基于 `THUMBS_SOURCE_PREFIXES`）
  - 解析/规范化 DSL spec（`spec.py`）
  - 生成缓存 key（包含源文件指纹 + spec + 格式 + 质量）
  - 如缓存不存在：调用 `transform.py` 用 Pillow 生成文件
  - 返回缩略图 URL（`THUMBS_URL_PREFIX/<hash-path>.<ext>`）
- `florist.contrib.thumbs.blueprint`：提供 `/thumbs/<path>` 路由读取落盘文件，并设置强缓存 Header

数据流（最常见：模板渲染时生成 URL）：

1. 模板调用 `thumb`：`{{ src_url|thumb('w72h72cc-q70jpg') }}`
2. `thumb` → `ensure_thumb(src_url, spec)`
3. `ensure_thumb`：
   - 只对能映射到本地文件的 URL 生效（白名单前缀）
   - 落盘到 `THUMBS_CACHE_DIR` 或 `UPLOADED_PATH/_thumbs`
4. 返回 `'/thumbs/xx/yy/<sha>.jpg'` 给模板
5. 浏览器请求 `/thumbs/...`：由 Flask blueprint（开发场景）或 nginx/CDN（生产推荐）直接提供静态文件

---

## 使用方式（上游应用怎么接入）

### 1）启用与初始化

Florist 的 `florist.init(app)` 已经包含 thumbs 的初始化调用（并且 fail-open）：

- 在 `florist/__init__.py` 中会 `from .contrib.thumbs import init as thumbs_init` 并注册 filter + blueprint。

如果你的工程不是通过 `florist.init(app)` 初始化，也可以手动：

```python
from florist.contrib.thumbs import init as thumbs_init

thumbs_init(app)
```

### 2）必备配置：`UPLOADED_PATH` 与 `THUMBS_SOURCE_PREFIXES`

thumbs 只处理“能从 URL 映射回本地文件”的场景。

- `UPLOADED_PATH`：上传文件根目录（工程里通常已经有）
- `THUMBS_SOURCE_PREFIXES`：**URL 前缀 → 文件系统子目录** 映射白名单

示例（xhh）：

```python
# sites/xhh/settings.py
THUMBS_SOURCE_PREFIXES = {
    "/wx/avatars/": "avatars",  # /wx/avatars/<fn> -> UPLOADED_PATH/avatars/<fn>
    "/meterial/": "",           # /meterial/<path>  -> UPLOADED_PATH/<path>
}
```

安全说明：

- 若 URL 不在白名单前缀内：`thumb()` 会直接回退原 URL（不做任何计算）。
- 映射过程会拒绝 `..` 目录穿越，且要求最终解析后的 `fs_path` 必须在 `fs_base` 内。

### 3）模板中使用（Jinja filter）

常用示例：

```jinja2
<img src="{{ avatar_url|thumb('w72h72cc-q70jpg') }}" />
```

与 CDN/静态 digest 组合（xhh 的写法示例）：

```jinja2
<img src="{{ cdn_url(avatar_url|thumb('w72h72cc-q70jpg')) }}" />
```

可选参数：

- `alt`：当 thumb 内部抛异常时，返回 `alt`（默认仍是“回退原值”）

---

## DSL 规范（Spec）

spec 分两段：

- `几何段`（geometry）：决定尺寸/缩放/裁剪模式
- `存储段`（storage）：决定质量与输出格式

格式：

- `几何段-存储段`
- 若只写几何段：`w200h200cc`
- 若只写存储段：`-q70jpg`（不改尺寸，仅重新编码）

### 1）几何段

支持：

- `wNNN`：目标宽度
- `hNNN`：目标高度
- `sNNN`：按千分比缩放（`s500` == 0.5 倍，`s2000` == 2 倍）
- mode 后缀（仅对 `w/h` 生效）：
  - `c`：contain（等比缩放，放进目标框，可能留白）
  - `cc`：cover+crop（等比缩放铺满并居中裁剪，常用于头像）
  - `s`：stretch（非等比拉伸，谨慎使用）

默认规则（在 `spec.canonicalize_spec` 里实现）：

- 只给 `w` 或只给 `h`：默认 `c`
- 同时给 `w`+`h`：默认 `cc`
- `sNNN`：不允许再带 mode（比例缩放不需要 mode）

示例：

- `w72h72cc`：强制输出 72×72，cover+crop
- `w320c`：宽 320，按比例缩放
- `h200`：高 200，按比例缩放
- `s500`：按 0.5 倍缩放

### 2）存储段

支持：

- `qNN`：质量 0..100（仅对 `jpg/webp` 默认有意义；png 仍会保存但不等价）
- `fmt`：输出格式（如 `jpg/png/webp`，也支持 `jpeg` 会归一化为 `jpg`）

示例：

- `q70jpg`
- `q85webp`
- `png`

默认规则：

- 若 spec 不指定 fmt：优先使用源文件扩展名（再不行默认 `jpg`）
- 若 spec 不指定 q：当输出为 `jpg/webp` 时使用 `THUMBS_DEFAULT_QUALITY`（默认 70）

最终组合示例：

- `w72h72cc-q70jpg`
- `w800c-webp`（不显式写 q，但 webp 会用默认质量）
- `-q70jpg`（只转码）

---

## 配置项（Florist 默认值）

Florist 在 `florist/settings.py` 里提供了默认配置：

- `THUMBS_ENABLED`：默认 `True`
- `THUMBS_URL_PREFIX`：默认 `/thumbs`
- `THUMBS_CACHE_DIR`：默认 `None`（走 `UPLOADED_PATH / THUMBS_CACHE_SUBDIR`）
- `THUMBS_CACHE_SUBDIR`：默认 `_thumbs`
- `THUMBS_ALLOWED_FORMATS`：默认 `('jpg','png','webp')`
- `THUMBS_DEFAULT_QUALITY`：默认 `70`
- `THUMBS_MAX_SCALE_UP`：默认 `2.0`（最多放大 2×，防止滥用放大）
- `THUMBS_MAX_DIMENSION`：默认 `8192`（绝对尺寸上限，防止超大内存消耗）
- `THUMBS_SOURCE_PREFIXES`：默认 `{}`（空表示不启用源映射：thumb 会全部回退原图）

---

## 代码入口

- `florist/contrib/thumbs/__init__.py`：`init(app)`（注册 filter + blueprint）
- `florist/contrib/thumbs/filter.py`：Jinja filter `thumb`
- `florist/contrib/thumbs/spec.py`：DSL 解析与 canonicalize
- `florist/contrib/thumbs/generator.py`：`ensure_thumb()`（落盘缓存与 URL 返回）
- `florist/contrib/thumbs/transform.py`：Pillow 处理（resize/crop/encode）
- `florist/contrib/thumbs/blueprint.py`：`/thumbs/<path>` 静态读取路由

---

## 缓存策略与命名

- 缓存 key 包含：
  - 源文件“指纹”：`st_size + st_mtime_ns`
  - canonical spec 字符串（`spec_to_string`）
  - 输出格式 `out_fmt`
  - 输出质量 `quality`
- 输出文件命名：对 key 做 sha256，落盘到 `aa/bb/<sha>.<ext>` 分片目录，避免单目录爆炸
- 并发：同一时刻可能重复生成（best-effort）；通过 `os.replace()` 原子替换最终文件

---

## 安全边界与注意事项

这套实现刻意做了“可控 + 安全”的取舍：

1. **只处理白名单来源**：通过 `THUMBS_SOURCE_PREFIXES` 限制可处理 URL。
2. **拒绝路径穿越**：URL 后缀中出现 `..` 直接拒绝。
3. **尺寸与放大限制**：`THUMBS_MAX_DIMENSION` + `THUMBS_MAX_SCALE_UP`。
4. **格式白名单**：只输出 `THUMBS_ALLOWED_FORMATS`。
5. **JPEG 白底**：输出 jpg 时如有透明通道，会用白底合成，避免黑底/异常。
6. **EXIF 方向修正**：`ImageOps.exif_transpose`，避免拍照图片旋转错误。
7. **Fail-open**：任何解析/生成异常返回原 URL（或者你给的 `alt`），不影响页面。

生产环境建议：

- `/thumbs` 静态文件最好由 nginx/CDN 直接服务。
- 定期清理缓存目录（例如按时间或按容量），避免磁盘无限增长。

---

## 直接在 Python 里调用（可选）

```python
from florist.contrib.thumbs.generator import ensure_thumb

thumb_url = ensure_thumb('/wx/avatars/avatar.png', 'w128h128cc-q70jpg')
# 返回 '/thumbs/<hash-path>.jpg' 或 None
```

返回 `None` 的常见原因：

- `THUMBS_ENABLED=False`
- `THUMBS_SOURCE_PREFIXES` 未配置或不匹配
- 源文件不存在
- spec 非法
- out_fmt 不在白名单

---

## 排错清单

当你发现页面仍在请求原图（说明 thumb 回退了）：

- 确认 `THUMBS_SOURCE_PREFIXES` 是否覆盖该 URL 前缀
- 确认 `UPLOADED_PATH` 与映射子目录真实存在并包含文件
- 确认输出格式在 `THUMBS_ALLOWED_FORMATS` 内（比如 `avif` 默认会被拒绝）
- 检查 spec 是否写错（例如 `s500cc` 会被拒绝；`s` 不允许 mode）
- 若是“路由 404”：确认 `_thumbs`（或 `THUMBS_CACHE_DIR`）内已经生成文件；以及 blueprint 是否注册

---

## TODO

- 观测：生成耗时、命中率、失败原因统计
- 滥用防护：对 spec 维度做更强的限流/缓存策略

