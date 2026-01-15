# florist.contrib.event（事件模式）

`event` 是 florist 的“事件日志/行为流”模块：把各种业务动作统一抽象成事件（什么时候、谁、做了什么、对什么对象、附加信息）。

> 代码位置：`florist/contrib/event/`

---

## 快速启用（TL;DR）

1. 配置 `FLORIST_ADMIN_PACKAGES` 包含 `florist.contrib.event`（获得后台日志视图）
2. 业务代码里写入 `EventLog`（行为/审计/运营统计）

## 事件模式（理论）

一个事件通常可表示为：

- `occurred_at`：发生时间
- `subject`：主体（谁）
- `predicate`：动作（做了什么）
- `object`：客体（对什么）
- `ext_info`：扩展信息（补充上下文，例如来源、渠道、金额、UA 等）

好处：

- 不同业务（收藏、评论、加购、支付、关注……）可以共享同一种“记录与查询”模式
- 更容易做审计、风控、运营统计、用户行为时间线

---

## 现有实现（代码导读）

### 1）模型：`EventLog`

- 文件：`florist/contrib/event/models.py`
- 字段：
  - `occurred_at: DateTimeField`
  - `subject: ReferenceField(User)`（引用 `florist.user.models.User`）
  - `predicate: StringField`
  - `object: GenericReferenceField`（可引用不同类型的 Document）
  - `ext_info: DictField`

索引（meta.indexes）：

- `('predicate', 'subject')`
- `('predicate', 'object')`
- `('predicate', 'occurred_at')`
- `('subject', 'occurred_at')`
- `('object', 'occurred_at')`

这些索引覆盖典型查询：

- “某用户做过哪些动作？”
- “某动作最近发生的事件？”
- “某对象相关的事件流（如某商品被加购/下单）？”

### 2）管理后台：只读日志视图

- 文件：`florist/contrib/event/admin.py`
- `EventLogModelView`：
  - `can_create/can_edit/can_delete = False`：禁止后台手工改日志
  - `can_view_details = True`：可看详情
  - `column_filters`：支持按 predicate/subject/occurred_at 过滤

---

## 如何启用（上游应用）

把包加入 `FLORIST_ADMIN_PACKAGES` 即可获得后台日志视图：

```python
FLORIST_ADMIN_PACKAGES = (
    'florist.contrib.event',
)
```

---

## 如何写入事件（建议方式）

当前模块没有封装 helper（比如 `log_event()`），上游可以直接创建 `EventLog`：

```python
from datetime import datetime
from florist.contrib.event.models import EventLog

EventLog(
    occurred_at=datetime.utcnow(),
    subject=user,
    predicate='favorite',
    object=article,
    ext_info={'source': 'web'},
).save()

---

## 代码入口

- `florist/contrib/event/models.py`：`EventLog`
- `florist/contrib/event/admin.py`：`EventLogModelView`（只读）

---

## 配置项

- `FLORIST_ADMIN_PACKAGES`：是否启用后台日志视图

---

## TODO

- 增加 helper：例如 `log_event(subject, predicate, object, ext_info=None)`
- 事件规范化：对 `predicate`、对象类型建立统一约束与字典
- 高写入场景的归档/TTL 策略
```

建议约定：

- `predicate` 采用稳定的短字符串（如 `favorite`/`unfavorite`/`comment`/`pay`）
- `ext_info` 仅存必要字段，避免把大对象塞进去

---

## 注意事项

- `GenericReferenceField` 灵活但也带来“对象类型多样”的复杂度，后续若做聚合统计，建议对 `predicate` 与对象类型做统一规范。
- 事件日志属于高写入表，生产环境建议：
  - 控制 ext_info 大小
  - 做归档/TTL（如按月归档）

