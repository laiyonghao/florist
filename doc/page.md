# florist.contrib.page（页面结构引擎 / 低代码页面）

`page` 当前主要是方向性模块（仓库内只有 README 占位），目标是做一个“配置式页面生成”到“可视化搭建”的页面引擎。

> 代码位置：`florist/contrib/page/`

---

## 快速启用（TL;DR）

当前模块还未落地为可用代码，暂时**不可直接启用**；此文档用于约束未来实现方向。

## 目标（理论）

页面引擎通常要解决：

- 页面由哪些区块组成（header/hero/list/footer…）
- 每个区块的参数（标题、图片、按钮、数据源）
- 区块的渲染模板与样式
- 数据绑定（从 CMS/商品/活动等模块读取数据）

一般演进路径：

1. 配置式：用 JSON/YAML 描述页面结构
2. 可视化：拖拽区块、所见即所得
3. 组件市场：沉淀可复用 block

---

## 当前状态

- 仅 README 描述，没有可用代码。

建议落地的最小版本（MVP）：

- `Page` 模型：slug、title、layout_json
- `Block` registry：block_type → render 函数 / Jinja 模板
- 渲染入口：`render_page(slug)`
- 管理后台：编辑 JSON（后续再做可视化）

---

## 代码入口

- `florist/contrib/page/README.md`：方向说明（当前仅占位）

---

## 配置项

- 暂无

---

## TODO

- 最小 MVP：Page 模型 + layout_json + 渲染入口
- block registry：block_type 到模板/渲染函数的映射
- admin 编辑器：先 JSON，后可视化

