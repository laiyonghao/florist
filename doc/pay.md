# florist.contrib.pay（支付）

`pay` 当前是占位模块（仓库内只有 README），目标覆盖微信支付、支付宝等能力。

> 代码位置：`florist/contrib/pay/`

---

## 快速启用（TL;DR）

当前模块还未落地为可用代码，暂时**不可直接启用**；此文档用于约束未来实现方向。

## 支付模块（理论）

一个可复用的支付模块通常包含：

- 统一的订单/支付单模型：金额、币种、状态机、过期时间
- 渠道适配：微信/支付宝/银行卡
- 回调与验签：notify webhook + 签名校验
- 幂等：同一支付回调重复投递不产生副作用
- 对账与审计：支付流水、退款流水、差异处理

---

## 当前状态

- 只有 README 占位，没有可用实现。

如果要落地，建议先定义：

1. `PaymentIntent`（支付意图）与 `PaymentTransaction`（支付流水）
2. 渠道接口：`create_payment()` / `verify_notify()` / `refund()`
3. 状态机：`created -> pending -> paid/failed/closed/refunded`
4. 与 `event` 模块联动：支付成功写入事件日志

---

## 代码入口

- `florist/contrib/pay/README.md`：方向说明（当前仅占位）

---

## 配置项

- 暂无（未来会引入渠道配置与密钥）

---

## TODO

- 定义支付意图/流水模型与状态机
- 渠道适配：微信/支付宝的 create/notify/verify/refund
- 幂等与对账

