---
description: Legacy FPS, the underlying equity curve and a simplified economic model.
---

# 📈 Investing and Pool Shares

## Reserve Pool Shares

Frankencoin Pool Shares (FPS) represent the equity capital of the system. Net fees and liquidation results change that capital and the protocol's FPS price. Losses reduce it. FPS also accumulates time-weighted governance votes under the legacy rules.

This page describes **legacy FPS and the underlying Equity curve**, not an interchangeable FCS investment path. [FCS](fcs.md) wraps FPS one to one, but uses different voting and exit rules. The [migration guide](fcs-migration.md) covers FPS and WFPS.

## Usage

The [equity application](https://app.frankencoin.com/equity) provides investment interfaces. A transaction may be a protocol mint, redemption, wrap or secondary-market trade; these are distinct operations. Legacy FPS redemption burns FPS and returns ZCHF under the Equity curve. It requires the holder's **average holding duration of at least 90 days**, rather than an age attached to individual transferable tokens. Balance changes and vote destruction can affect that duration.

The following screenshots are historical FPS interface examples. Their prices, balances, routes and controls are not current quotes or FCS instructions.

<figure><img src=".gitbook/assets/kuva (44).png" alt="Historical FPS investment interface"><figcaption><p>Historical FPS entry and redemption view.</p></figcaption></figure>

A marginal FPS price does not determine the exact output of a finite purchase: fees and the curve also apply. WFPS is a separate wrapper, not another name for FCS.

<figure><img src=".gitbook/assets/kuva (45).png" alt="Historical FPS statistics"><figcaption><p>Historical FPS statistics, retaining the FPS unit and supply.</p></figcaption></figure>

| Metric | Meaning |
| --- | --- |
| FPS reference valuation | FPS supply multiplied by the underlying marginal FPS price |
| Total reserve | ZCHF held in the reserve, including minter reserve and equity |
| Equity capital | Reserve capital after the minter-reserve allocation |
| Minter reserve | Reserve attributed to outstanding positions, subject to loss sharing |
| Income and losses | Historical flows over the displayed period, not a future return |

An FPS statistic does not become an FCS statistic because an interface also offers FCS. See [reserve accounting](reserve.md).

## Economics

### Proportional Capital Valuation

The underlying curve is inspired by [The Continuous Capital Corporation](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4189472). For equity capital `K` in ZCHF and outstanding FPS supply `s`, its marginal reference valuation and price are:

```text
V(K) = 3 × K
p = 3 × K / s
```

For positive capital and supply, the continuous model gives the following change after adding net capital `ΔK`, before implementation fees and integer rounding:

```text
s_new = s × ((K + ΔK) / K)^(1/3)
p_new = p × ((K + ΔK) / K)^(2/3)
```

For example, equity of 1,000,000 ZCHF and supply of 10,000 FPS imply a marginal reference price of 300 ZCHF per FPS. This is not a guaranteed execution price. Finite transactions move along the curve; FCS ZCHF exits also apply the [wrapper's redemption discount](fcs.md#prices-and-redemption-discount). Secondary-market prices depend on trading liquidity and orders.

### Equilibrium

A simplified model considers 30,000,000 ZCHF of outstanding mints at 5% annual interest: gross annual borrowing income is 1,500,000 ZCHF. If investors require a 5% return, and if that income continues without expenses or losses, capitalising it gives a valuation of 30,000,000 ZCHF. The FPS curve reaches that reference valuation at 10,000,000 ZCHF of equity.

Savings changes the income available to equity holders:

```text
net equity income = borrowing income + other net income - savings expense - losses
savings expense = interest-bearing savings balance × applicable savings rate
```

For example, an average interest-bearing savings balance of 10,000,000 ZCHF at 2% costs 200,000 ZCHF a year. With the borrowing income above, no other income and no losses, net equity income is 1,300,000 ZCHF. At the same assumed 5% required return, that would support a model valuation of 26,000,000 ZCHF, not 30,000,000 ZCHF. Actual accrual timing, changing rates, referrals and losses affect realised flows. Referral fees divide savings interest between the user and referrer; they are not an extra payment on top of that gross interest.

The one-third equity relationship is therefore a model result under assumptions, not a reserve requirement enforced by the contracts. Borrowing to buy equity exposes the holder to fees, losses, price changes and redemption conditions; a spread between quoted rates is not a risk-free arbitrage. Nor does comparing FPS reference valuation with ZCHF supply uniquely reveal expected growth.

### Limits to Capital Efficiency

Lower equity means a smaller buffer before losses reach shared minter reserves. More equity provides a larger buffer but changes the returns available per share. Neither the curve nor a proposed equilibrium ensures a particular reserve ratio or market price.
