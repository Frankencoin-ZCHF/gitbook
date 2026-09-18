---
description: Borrowing through an existing position's terms and available family capacity.
---

# Cloning Existing Positions

A clone reuses an accepted position's terms without a new collateral proposal. On the [mint page](https://app.frankencoin.com/mint), select a position for the intended collateral and inspect its available capacity, rate, reserve contribution, liquidation price and expiry. The [version reference](README.md#contract-versions) distinguishes the newer source from legacy interfaces.

## Choose a position to clone

Connect the wallet that will supply the collateral and select the intended chain. Match the collateral token address, then compare the available positions. A lower stored liquidation price supports less debt per token but is less likely to exceed the market price. The up-front fee and reserve determine how much of a gross mint reaches your wallet.

Check that the parent can be cloned, not merely that its displayed capacity is positive. An active challenge, cooldown, expiry or closure can prevent cloning. Unlike a new proposal, an eligible clone can deposit collateral and mint in the same transaction, without a new proposal fee or initialisation period.

<figure><img src="../.gitbook/assets/kuva (35).png" alt="Historical list of positions available for cloning"><figcaption><p>Historical availability display, not a current capacity quote.</p></figcaption></figure>

In the pinned newer implementation, the original and its clones share a family limit. The original's collateral can reserve capacity, and other family mints can change what remains available. The displayed limit is not a separate guaranteed allocation to the clone. A clone's expiry cannot exceed the original position's expiry. If the selected parent is itself a clone, follow its `original` reference to find that bound.

## Set collateral, mint amount and expiry

1. **Choose the gross mint amount.** This becomes debt, including the retained reserve and up-front fee. If you need a particular net amount, use the transaction quote to find the gross mint required rather than entering the desired wallet receipt as debt.
2. **Set the collateral deposit.** It must meet the inherited minimum and cover the gross debt at the parent's stored liquidation price. At 1,500 ZCHF per WETH, two WETH cover 3,000 ZCHF of gross debt, subject to family capacity and the other limits. Extra collateral does not automatically lower that price.
3. **Choose the expiry.** Select a date within the original's permitted term. A shorter remaining term reduces the up-front interest fee at the same rate, but brings repayment or expiry settlement closer.
4. **Review the result.** Read the parent and original addresses, effective annual rate, collateral deposit, gross debt, retained reserve, fee and net ZCHF. The rate and capacity can change between viewing the page and execution.

<figure><img src="../.gitbook/assets/kuva (36).png" alt="Historical clone transaction preview"><figcaption><p>Historical clone preview.</p></figcaption></figure>

For the historical example, a gross mint of 3,000 ZCHF with a 10% reserve and a 60 ZCHF up-front fee gives the wallet 2,640 ZCHF. The reserve receives 300 ZCHF. The fee depends on the applicable annual rate and remaining term; the newer source uses the global borrowing rate plus the position's risk premium.

## Submit and manage the clone

Approve the selected minting hub to transfer the collateral if an allowance is needed, then submit the clone transaction. Token approval authorises spending; it does not create the clone or mint ZCHF. Keep the network's native asset available for gas.

After the clone transaction confirms, record the new position address and check its owner, collateral, gross debt, stored price, expiry and received ZCHF. The clone is your position; it does not transfer ownership of the parent. Subsequent minting, repayment and collateral changes follow the [adjustment guide](adjust.md). Monitor its expiry even if you do not plan further changes.
