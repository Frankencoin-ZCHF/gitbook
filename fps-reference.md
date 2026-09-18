---
description: Underlying FPS identities, the Equity curve and legacy holder mechanics.
---

# Underlying FPS Reference

[Frankencoin Share Token (FCS)](pool-shares.md) is the canonical governance and share token. This page documents its underlying Frankencoin Pool Shares (FPS) and the legacy holder mechanics. It is a technical reference, not the starting point for acquiring FCS.

## Token identity and backing

The Equity contract holds the system's equity capital and issues FPS. Each FCS wraps one FPS, but the tokens have separate supplies, voting records and contract interfaces. The Ethereum [FPS address](https://etherscan.io/address/0x1bA26788dfDe592fec8bcB0Eaff472a42BE341B2) remains an FPS address. WFPS is an older wrapper, not another name for FCS.

The ChainSecurity report calls this underlying token `FPS1` and the FCS wrapper `FPS2`. Source identifiers and API routes retain these names; the [FCS version reference](fcs.md#version-and-terminology) identifies the reviewed commit. `/ecosystem/fps/info`, `/prices/erc20/fps` and `/analytics/fps/*` report underlying FPS data, not FCS supply or market prices.

## Proportional Capital Valuation

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

For example, equity of 1,000,000 ZCHF and supply of 10,000 FPS imply a marginal reference price of 300 ZCHF per FPS. This is not a guaranteed execution price. Finite transactions move along the curve; FCS ZCHF exits also apply the [redemption discount](fcs.md#prices-and-redemption-discount). Secondary-market prices depend on trading liquidity and orders. The [equity income model](pool-shares.md#equilibrium) relates fees, savings expense and losses to shared capital.

## Legacy votes and quorum

Legacy FPS votes grow with balance and average holding duration. For example, 10 FPS held for 730 days gives 7,300 FPS-days, compared with 7,000 FPS-days for 1,000 FPS held for seven days, before balance changes. A freshly borrowed balance carries no accumulated holding time. This legacy illustration does not apply the FCS `cap()` mechanism.

FPS retains its underlying 2% quorum and delegation mechanism. The applicable contract's quorum check determines eligibility, including fixed-point rounding at the boundary. FCS has a separate internal quorum and exercises underlying votes through its contract; it does not change every FPS holder's threshold to 1%.

Legacy `kamikaze` sacrifices the caller's votes to destroy the same number of votes at other addresses, affecting their redemption age too. While FCS is binding, permissionless `shoot(target)` invokes this mechanism against external FPS holders without burning their tokens. See [remaining outside the wrapper](fcs-migration.md#remaining-outside-the-wrapper).

## Direct FPS redemption

Legacy FPS redemption burns FPS and returns ZCHF under the Equity curve. It requires the holder's **average holding duration of at least 90 days**, rather than an age attached to individual transferable tokens. Balance changes and vote destruction can affect that duration. FPS remains transferable; a secondary-market sale is separate from redemption.

The FCS contract is itself an FPS holder. Its underlying age therefore matters for FCS ZCHF exits, but an individual FCS holder has no separate personal 90-day redemption wait. Unwrapping FCS returns FPS without carrying FCS voting age back into the legacy record. See [FCS exit eligibility](fcs.md#exit-paths-and-eligibility).

## Historical interface and metrics

The following screenshots are historical FPS interface examples. Their prices, balances, routes and controls are not current quotes or FCS instructions.

<figure><img src=".gitbook/assets/kuva (44).png" alt="Historical FPS investment interface"><figcaption><p>Historical FPS entry and redemption view.</p></figcaption></figure>

A marginal FPS price does not determine the exact output of a finite purchase: fees and the curve also apply.

<figure><img src=".gitbook/assets/kuva (45).png" alt="Historical FPS statistics"><figcaption><p>Historical FPS statistics, retaining the FPS unit and supply.</p></figcaption></figure>

| Metric | Meaning |
| --- | --- |
| FPS reference valuation | FPS supply multiplied by the underlying marginal FPS price |
| Total reserve | ZCHF held in the reserve, including minter reserve and equity |
| Equity capital | Reserve capital after the minter-reserve allocation |
| Minter reserve | Reserve attributed to outstanding positions, subject to loss sharing |
| Income and losses | Historical flows over the displayed period, not a future return |

An FPS statistic does not become an FCS statistic because an interface also offers FCS. See [reserve accounting](reserve.md), the [ecosystem API](api-docs/ecosystem.md) for underlying data and the [FCS API](api-docs/fcs.md) for share-specific fields.
