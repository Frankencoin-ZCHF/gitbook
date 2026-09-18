---
description: Proposing a collateralised position and selecting its borrowing terms.
---

# Opening New Positions

If the available positions do not offer your collateral or borrowing terms, you can propose a new position. You choose its collateral, capacity, price and other terms, deposit the initial collateral and pay a proposal fee. Qualified holders then have time to examine and veto it. If an accepted position already suits your needs, [cloning it](clone.md) avoids a new proposal and its waiting period.

Start at the [creation page](https://app.frankencoin.com/mint/create). The walkthrough below follows the decisions needed to create a position, rather than a particular screen layout. Contract rules refer to the [pinned minting sources](README.md#contract-versions); screenshots show a historical interface, not current quotes or button names.

<figure><img src="../.gitbook/assets/kuva (46).png" alt="Historical new-position button"><figcaption><p>Historical entry point for proposing a position.</p></figcaption></figure>

## Before you start

Connect the wallet that will own the position on the intended chain. You need the initial collateral, ZCHF for the proposal fee and the network's native asset for transaction gas. Identify the collateral by its token address, not just its symbol. The chain and selected minting hub determine which version's rules apply.

Plan both the gross amount you want to mint and the net ZCHF you need in your wallet. The proposal fee is separate from the fee and reserve deducted when you later mint. Opening the position transfers collateral but does not yet supply spending money.

## Proposal terms

In the pinned source, opening a position costs **1,000 ZCHF**. The fee goes to equity and is not returned after a veto. Choose an initialisation period of **at least three days**. During that period, a qualified holder can veto the proposal; a denied position cannot mint. The [FCS governance](../governance.md#veto-process) guide explains the holder and underlying-contract qualification checks.

Position creation is separate from the FCS minter-application rule of **1,200 ZCHF and 60 days**. You are proposing a collateral position, not applying to add a minting module.

<figure><img src="../.gitbook/assets/kuva (30).png" alt="Historical position proposal terms"><figcaption><p>Historical proposal form: fee and initialisation period.</p></figcaption></figure>

## Interest and minting capacity

Choose the term, risk premium and family minting limit together:

* **Term:** decide how long you need the position. In the pinned source, the duration runs from the end of initialisation to expiry. Later mints pay for the remaining term, not a new full term. At expiry, further minting stops and collateral can enter the [forced-sale process](../risks.md#missing-maturity-dates).
* **Risk premium:** choose the position-specific addition to the global borrowing rate. The newer `contracts/minting/Position.sol` calculates the annual rate as **global borrowing rate plus risk premium**. The proposer does not set the global rate. Contract inputs use parts per million (ppm): 10,000 ppm is 1%.
* **Family minting limit:** choose the maximum gross ZCHF debt for the original position and its clones together. This bounds the system's exposure through this position family; it is not the amount you must borrow at opening.

Minting deducts the interest fee up front, using the applicable annual rate at that mint and a 365-day year. The source caps the fee fraction at 100%. For an illustration, a global rate of 2% plus a 1% risk premium gives 3% a year. Minting 10,000 ZCHF with 365 days remaining incurs a 300 ZCHF fee; half that term incurs 150 ZCHF, before integer rounding. These are assumed rates, not current quotes. Repaying early does not return the fee.

Older interfaces described a user-set annual interest rate. For the pinned newer source, read both rate components and the resulting up-front fee rather than treating that older field as the complete formula.

The original position and its clones share a family minting limit. The original's collateral reserves some capacity for its own minting; family mints and repayments change what remains for clones. Capacity is not permanently split into independent clone allocations. A displayed available amount can change before execution.

<figure><img src="../.gitbook/assets/kuva (31).png" alt="Historical position financial terms"><figcaption><p>Historical financial terms; field names differ between versions.</p></figcaption></figure>

## Collateral and liquidation price

### Choose the asset and amounts

Enter the collateral token address for the selected chain. Examine how other participants can obtain and value that asset: challengers must supply the same token to use the [auction mechanism](auctions.md). The [collateral discussion](https://github.com/Frankencoin-ZCHF/FrankenCoin/discussions/11) explains selection considerations.

Set the **minimum collateral** in units of that token, then choose an **initial collateral** amount at least as large. The minimum prevents small residual positions. In the pinned implementation, withdrawing below it closes the position and requires clearing its debt. The initial amount is what the hub transfers from your wallet into the position when the proposal transaction succeeds, not when you later mint.

<figure><img src="../.gitbook/assets/kuva (33).png" alt="Historical collateral fields"><figcaption><p>Historical collateral selection: token, minimum amount and initial deposit.</p></figcaption></figure>

### Set the liquidation price

The liquidation price is the stored ZCHF value per collateral token used for minting and challenges. It is not an oracle price or an automatically calculated debt-to-collateral ratio. A higher price supports more gross debt for the same collateral, but makes a challenge more likely to be justified when the market price falls below it. Minting less does not itself lower this stored price.

In the pinned `MintingHub.openPosition`, minimum collateral multiplied by liquidation price must represent at least **5,000 ZCHF**. This is a rule of that version, not a universal minimum for every deployment. For example, two WETH at 2,500 ZCHF per WETH have a liquidation value of 5,000 ZCHF; 20 WETH at 250 ZCHF have the same value. Neither example is a market quote or a recommendation for WETH's price.

Check the amounts together: initial collateral must meet the minimum, its value at the stored price must cover the debt you intend to mint, and the family limit must permit that debt. The source also requires the minimum collateral's liquidation value not to exceed the family limit. A contract-valid proposal can still be vetoed during initialisation.

## Reserve and auction duration

Choose the **reserve contribution**, the fraction of each gross mint retained in the reserve rather than paid to your wallet. It can absorb losses under the [reserve rules](../reserve.md). With an unimpaired reserve, that allocation helps repay the debt later; it is not a refundable interest fee or an unconditional claim to cash.

For example, a 10% reserve on a gross mint of 10,000 ZCHF retains 1,000 ZCHF. With the illustrative 300 ZCHF interest fee above, your wallet receives 8,700 ZCHF. The separate 1,000 ZCHF proposal fee is not part of this mint calculation.

Choose the **challenge period** with the collateral's trading conditions in mind. Bidders need time to obtain funds and assess the asset; a longer sale also leaves more time for its price to move. In the pinned implementation, `challengePeriod` sets the duration of each of the two auction phases: first fixed-price, then declining-price. Check how the selected interface expresses that duration rather than assuming a field labelled “Auction Duration” means the combined time.

Collateral volatility and the time needed to sell it inform the reserve choice. A larger reserve leaves less net ZCHF from a mint but provides more funds for settlement. It does not guarantee that a sale covers all debt and rewards. The [auction guide](auctions.md) explains what each phase sells.

<figure><img src="../.gitbook/assets/kuva (34).png" alt="Historical liquidation parameters"><figcaption><p>Historical liquidation-price, reserve and auction-duration fields.</p></figcaption></figure>

## Submission and confirmation

1. **Review the proposal.** Check the chain, hub, collateral address, minimum and initial collateral, initialisation period, expiry, rate components, reserve contribution, stored liquidation price and family limit. Compare your intended gross mint with its net wallet receipt.
2. **Authorise the collateral transfer.** If needed, approve the selected hub to transfer the initial collateral. Keep enough ZCHF available for the proposal fee. Approval grants an allowance; it does not open the position.
3. **Submit the proposal transaction.** After confirmation, record the new position address and check its owner, deposited collateral, terms and start time. The fee has been paid and the collateral deposited; opening a proposal is not itself a ZCHF mint.
4. **Follow the initialisation period.** Read the proposal state and whether it was vetoed. Passing the waiting period alone does not override an active challenge, closure or another minting restriction.
5. **Mint from the accepted position.** Once it is eligible, open its management view and choose the amount to mint. Review the reserve, up-front fee and net receipt, then submit and confirm the mint. The [adjustment guide](adjust.md) covers this first mint and later changes.

If the proposal is vetoed, it cannot mint and the fee is not returned. Remaining collateral can be withdrawn under the position's withdrawal rules, including any challenge or cooldown restriction.
