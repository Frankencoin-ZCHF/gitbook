---
description: Changing debt, collateral and the explicitly stored liquidation price.
---

# Adjusting a Position

The position owner can change its debt, collateral and liquidation price within the contract's limits. The [pinned source version](README.md#contract-versions) is the reference below. Historical screenshots illustrate the interface, not a current quote.

## Select the position

Connect the wallet that currently owns the position, which may differ from its creator if ownership was transferred. Open its management view from the application's positions list. Match the chain and position address, then read its collateral balance, gross debt, stored liquidation price, expiry and any cooldown or challenge. A newly proposed position can hold collateral without having minted any ZCHF.

<figure><img src="../.gitbook/assets/kuva (37).png" alt="Historical owned-position list"><figcaption><p>Historical position list.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/kuva (38).png" alt="Historical position adjustment fields"><figcaption><p>Historical adjustment form.</p></figcaption></figure>

## Minting and repayment

Choose whether you want to increase debt and receive ZCHF, or reduce debt using ZCHF from your wallet. For the combined `adjust(newMinted, newCollateral, newPrice)` operation, all three inputs are **target totals**, not amounts to add or subtract. For example, moving from 3,000 ZCHF of gross debt to 2,000 ZCHF sets `newMinted` to 2,000 ZCHF. A direct `mint` instead specifies the additional gross amount, while `repay` specifies the wallet amount paid. The interface's transaction preview should make that distinction clear.

To mint, choose the intended debt and check both collateral cover and available family capacity. The position must also be outside cooldown, unexpired, open and free of active challenges. Read the up-front fee, reserve contribution and resulting net ZCHF before submitting; an available capacity figure alone does not establish eligibility.

Two WETH at a stored liquidation price of 1,500 ZCHF per WETH support a gross debt of 3,000 ZCHF, subject to the other position limits. In the historical example, a 300 ZCHF reserve contribution and a 90 ZCHF up-front fee leave 2,610 ZCHF for the wallet. The fee is not returned on repayment. Reserve recovery depends on the assigned reserve remaining available.

<figure><img src="../.gitbook/assets/kuva (39).png" alt="Historical minting outcome"><figcaption><p>Historical minting outcome with gross debt and net wallet receipt.</p></figcaption></figure>

With an unimpaired 10% reserve, repaying 900 ZCHF plus the position's 100 ZCHF assigned reserve extinguishes 1,000 ZCHF of gross debt. Shared reserve losses can increase the wallet contribution. The transaction quote uses the position's actual state.

For a repayment, choose the gross debt you want to clear and obtain the required wallet contribution from that state. Supply ZCHF, not collateral or Swiss francs. Approve any required spender for the chosen operation, then submit the repayment or combined adjustment. Afterwards, confirm the debt reduction and wallet debit. Clearing debt does not itself withdraw the collateral.

## Adding or withdrawing collateral

To add collateral through `adjust`, set the target collateral balance above the current balance and authorise the position to transfer the difference. Leave the debt and price targets unchanged if you only intend to add collateral. More collateral increases the amount of debt the position can support at its existing price, but does not change that price.

To withdraw collateral, select the amount to remove or the lower target balance, depending on the operation. The remaining collateral at the stored price must still cover outstanding gross debt. Active challenges and cooldowns restrict withdrawals. In the pinned source, withdrawing below the minimum closes the position and requires zero debt; to exit completely, clear the debt and withdraw the remaining collateral when those conditions permit.

## Lowering the liquidation price

**Adding collateral alone does not change the stored liquidation price.** Lowering the challenge price requires an explicit price adjustment, whether through `adjustPrice(newPrice)` or a combined `adjust` operation that supplies a different price.

The new collateral value at the lower price must still cover outstanding gross debt. For example, 3,000 ZCHF of debt needs three WETH at a price of 1,000 ZCHF per WETH. If only two WETH remain, debt must first fall to at most 2,000 ZCHF to use that price. Active challenges and the position's state can restrict adjustments.

Choose one of those ways to make the lower price possible: add enough collateral, repay enough debt, or combine the two. Set the lower price explicitly as part of the same adjustment or in a later price transaction. Depositing the extra WETH alone leaves the old challenge price in place.

If an interface combines a collateral deposit with a price change, the transaction must include both. The confirmed position's `price`, collateral balance and minted debt show whether the intended adjustment occurred.

## Increasing the liquidation price

In the pinned source, increasing the liquidation price triggers a three-day minting cooldown. It permits a higher collateral-based minting amount only after that period and within the family limit. Lowering the price does not trigger that same price-increase cooldown.

Submit the price increase separately from any mint that depends on the higher price. The combined `adjust` operation processes minting before changing the price, so it cannot use the new higher price to cover that mint. After confirmation, read the new price and cooldown; once the cooldown has passed, obtain a fresh mint quote.

## Confirm the adjustment

After the transaction confirms, compare the recorded debt, collateral balance and price with your target totals. Check the wallet's received or spent ZCHF and collateral as well. If the transaction reverted, the intended adjustment did not take effect; read the current challenge, cooldown, capacity and collateral state before changing the inputs.
