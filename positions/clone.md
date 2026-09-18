---
description: Borrowing through an existing position's terms and available family capacity.
---

# Cloning Existing Positions

A clone reuses an accepted position's terms without a new collateral proposal. On the [mint page](https://app.frankencoin.com/mint), select a position for the intended collateral and inspect its available capacity, rate, reserve contribution, liquidation price and expiry. The [version reference](README.md#contract-versions) distinguishes the newer source from legacy interfaces.

<figure><img src="../.gitbook/assets/kuva (35).png" alt="Historical list of positions available for cloning"><figcaption><p>Historical availability display, not a current capacity quote.</p></figcaption></figure>

In the pinned newer implementation, the original and its clones share a family limit. The original's collateral can reserve capacity, and other family mints can change what remains available. The displayed limit is not a separate guaranteed allocation to the clone. A clone's expiry cannot exceed its parent's expiry.

<figure><img src="../.gitbook/assets/kuva (36).png" alt="Historical clone transaction preview"><figcaption><p>Historical clone preview.</p></figcaption></figure>

For the historical example, a gross mint of 3,000 ZCHF with a 10% reserve and a 60 ZCHF up-front fee gives the wallet 2,640 ZCHF. The reserve receives 300 ZCHF. The fee depends on the applicable annual rate and remaining term; the newer source uses the global borrowing rate plus the position's risk premium.

Token approval authorises spending; it is not necessarily the mint transaction. After the clone transaction confirms, the new position address, owner, collateral, gross debt, stored price and received ZCHF identify the result. Subsequent changes follow the [adjustment guide](adjust.md).
