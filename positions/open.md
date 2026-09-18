---
description: Proposing a collateralised position and selecting its borrowing terms.
---

# Opening New Positions

A new position is an advanced-user proposal. The [creation page](https://app.frankencoin.com/mint/create) exposes the route; [cloning an accepted position](clone.md) reuses existing terms. The contract behaviour below refers to the [pinned minting sources](README.md#contract-versions). Screenshots show a historical interface, not current quotes.

<figure><img src="../.gitbook/assets/kuva (46).png" alt="Historical new-position button"><figcaption><p>Historical entry point for proposing a position.</p></figcaption></figure>

## Proposal terms

In the pinned source, opening a position costs 1,000 ZCHF and the initialisation period is at least three days. The fee is not returned after a veto. A qualified holder can veto the position during this period. [FCS governance](../governance.md#veto-process) explains the holder and underlying-contract qualification checks. Position creation is separate from the FCS minter-application rule of 1,200 ZCHF and 60 days.

<figure><img src="../.gitbook/assets/kuva (30).png" alt="Historical position proposal terms"><figcaption><p>Historical proposal form.</p></figcaption></figure>

## Interest and minting capacity

The newer `contracts/minting/Position.sol` calculates the annual rate as the **global borrowing rate plus the position's risk premium**, in ppm. The proposer selects the risk premium, not the global rate. Minting deducts a fee for the remaining term, using the applicable rate at the mint. The source uses a 365-day year and caps the fee fraction at 100%.

Older interfaces described a user-set annual interest rate. That description is not the complete rate formula for the pinned newer source.

The original position and its clones share a family minting limit. Available clone capacity changes with the family's outstanding minted amount and capacity reserved for the original position's collateral. It is not a permanent split of the remaining limit into independent clone allocations. The amount displayed before submission can change before execution.

<figure><img src="../.gitbook/assets/kuva (31).png" alt="Historical position financial terms"><figcaption><p>Historical financial terms; field names differ between versions.</p></figcaption></figure>

## Collateral and liquidation price

The collateral is identified by its chain and token address. Challengers need access to the same asset for the [auction mechanism](auctions.md). The [collateral discussion](https://github.com/Frankencoin-ZCHF/FrankenCoin/discussions/11) sets out selection considerations.

Initial collateral must meet the position's minimum. The liquidation price is an explicit stored parameter, not a live oracle value or automatically calculated debt-to-collateral ratio. A numerical example: two WETH at 2,500 ZCHF per WETH have a liquidation value of 5,000 ZCHF; 20 WETH at 250 ZCHF have the same value. These are examples, not quotes or universal minimum-value rules.

<figure><img src="../.gitbook/assets/kuva (33).png" alt="Historical collateral fields"><figcaption><p>Historical collateral selection.</p></figcaption></figure>

## Reserve and auction duration

The reserve contribution withholds part of the gross minted ZCHF. It absorbs losses under the [reserve rules](../reserve.md). Collateral volatility and auction duration affect how far sale proceeds can fall below the position's liquidation value.

<figure><img src="../.gitbook/assets/kuva (34).png" alt="Historical liquidation parameters"><figcaption><p>Historical reserve and auction-duration fields.</p></figcaption></figure>

## Submission and confirmation

Review the chain, hub, collateral address, rate components, expiry, reserve contribution, stored liquidation price and family limit. After proposal confirmation, the initialisation period must finish without a veto before minting becomes available. Opening a proposal is not itself a ZCHF mint. The [adjustment guide](adjust.md) describes minting and later changes.
