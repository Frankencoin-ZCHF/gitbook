---
description: Changing debt, collateral and the explicitly stored liquidation price.
---

# Adjusting a Position

The position owner can change its debt, collateral and liquidation price within the contract's limits. The [pinned source version](README.md#contract-versions) is the reference below. Historical screenshots illustrate the interface, not a current quote.

## Select the position

Connect the wallet that currently owns the position, which may differ from its creator if ownership was transferred. Open its management view from the application's positions list.

<figure><img src="../.gitbook/assets/kuva (37).png" alt="Historical owned-position list"><figcaption><p>Historical position list.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/kuva (38).png" alt="Historical position adjustment fields"><figcaption><p>Historical adjustment form.</p></figcaption></figure>

## Minting and repayment

Two WETH at a stored liquidation price of 1,500 ZCHF per WETH support a gross debt of 3,000 ZCHF, subject to the other position limits. In the historical example, a 300 ZCHF reserve contribution and a 90 ZCHF up-front fee leave 2,610 ZCHF for the wallet. The fee is not returned on repayment. Reserve recovery depends on the assigned reserve remaining available.

<figure><img src="../.gitbook/assets/kuva (39).png" alt="Historical minting outcome"><figcaption><p>Historical minting outcome with gross debt and net wallet receipt.</p></figcaption></figure>

With an unimpaired 10% reserve, repaying 900 ZCHF plus the position's 100 ZCHF assigned reserve extinguishes 1,000 ZCHF of gross debt. Shared reserve losses can increase the wallet contribution. The transaction quote uses the position's actual state.

## Lowering the liquidation price

**Adding collateral alone does not change the stored liquidation price.** Lowering the challenge price requires an explicit price adjustment, whether through `adjustPrice(newPrice)` or a combined `adjust` operation that supplies a different price.

The new collateral value at the lower price must still cover outstanding gross debt. For example, 3,000 ZCHF of debt needs three WETH at a price of 1,000 ZCHF per WETH. If only two WETH remain, debt must first fall to at most 2,000 ZCHF to use that price. Active challenges and the position's state can restrict adjustments.

If an interface combines a collateral deposit with a price change, the transaction must include both. The confirmed position's `price`, collateral balance and minted debt show whether the intended adjustment occurred.

## Increasing the liquidation price

In the pinned source, increasing the liquidation price triggers a three-day minting cooldown. It permits a higher collateral-based minting amount only after that period and within the family limit. Lowering the price does not trigger that same price-increase cooldown.
