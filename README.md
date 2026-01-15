# Florist

种花家，基于Flask的一个web dev实验，准备用来写一本关于Flask项目工程化开发的书。

## 文档

- 文档索引：`doc/doc.md`
- 缩略图（Thumbs）：`doc/thumbs.md`

## 目标

基于 Flask+MongoDB 打造一个快速开发方案，达到开发官网、小店、博客只需要写几十行代码就可以，开发复杂网站六成功能开箱即用的程度。

## 使用的库

仅列出项目内直接 `import` 的

* Flask
* Flask-Mongoengine
  * Mongoengine
* Flask-Admin
* Flask-Security-Too
* Flask-WTForms
  * WTForms
* Flask-CKEditor
* Pillow（缩略图/图片处理）
* flaskfilemanager

> 说明：历史上曾尝试过 Flask-thumbnails，但目前 florist 内置了更可控的缩略图实现（见 `florist.contrib.thumbs`）。

## 功能模块

1. meterial: 素材管理
2. facet: 片面模式
3. event: 事件模式
4. cms: 内容管理
5. shop: 店铺功能
6. pay: 支付功能
7. page: 低代码页面开发
8. config: 配置
9. thumbs: 缩略图（按需生成 + 落盘缓存，Jinja filter）

## 状态

项目初始期，重度开发中，未进入稳定期前请勿用以生产。
