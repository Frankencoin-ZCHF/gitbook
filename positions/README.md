---
description: Minting Frankencoins against collateral, with version-specific borrowing terms.
---

# 🖨️ Collateralized Minting

A **position** holds a user's collateral and records the Frankencoins they have minted against it. It has one owner, initially its creator; ownership can be transferred. The owner can add collateral and mint within the position's price, collateral, time and capacity constraints.

Anyone can challenge a position when they believe the **market value of the collateral is below the stored liquidation price**, not the other way around. A challenge starts a [two-phase auction](auctions.md). Challengers must supply collateral of their own, which can be bought during the first phase. A challenge is not a risk-free price report. This mechanism replaces an external price oracle; it depends on participants being able and willing to challenge.

There are two entry paths:

* [Open a new position](open.md): an advanced-user proposal with configurable parameters and a veto period. The application provides a [creation route](https://app.frankencoin.com/mint/create).
* [Clone an existing position](clone.md): use an accepted position's terms, subject to available capacity and its expiry. This is usually the simpler path.

## Contract versions

The implementation matters. This guide distinguishes the newer `contracts/minting/` source from historical screenshots and legacy terms. The source references are pinned to commit `8b4c4ab67bb361b91d58c474b87f4608fc4c0566`:

* [Position.sol](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/minting/Position.sol)
* [MintingHub.sol](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/minting/MintingHub.sol)

The chain, position address and originating hub identify a deployed position; its verified code and transaction quote determine its terms. The pinned source describes a version, not every existing position. Existing positions do not automatically gain a newer implementation's terms.
