---
description: Collateral challenges, the two auction phases and settlement.
---

# Challenges and Auctions

## Auction Design

A challenge tests a position's stored liquidation price against the market. It is economically justified when **market value is below the liquidation price**. The challenger supplies the same collateral asset as the position. The [pinned minting sources](README.md#contract-versions) define the implementation described here.

The auction has two phases:

1. **Fixed-price phase:** bidders buy the challenger's collateral at the position's liquidation price. Taking the challenged amount in this phase averts liquidation of that amount of the position's collateral.
2. **Declining-price phase:** if collateral remains challenged, the auction price falls towards zero. Bidders buy the position's collateral, and the challenger recovers the corresponding posted collateral under the settlement rules.

This separation makes defending an excessive liquidation price costly. If collateral worth 950 ZCHF is challenged at a liquidation value of 1,000 ZCHF, the owner cannot merely buy back their own collateral at 1,000 ZCHF: a first-phase defence buys the challenger's collateral. Repeated challenges therefore depend on challengers having access to that asset. A collateral asset wholly controlled by the position owner cannot support that mechanism.

After a successful challenge, the debt, sale proceeds, challenger reward and assigned reserve determine settlement. In the pinned implementation the challenger reward is 2% of the accepted bid, not an unconditional 2% return on posted collateral. The [reserve example](../reserve.md#challenge-settlement) shows the accounting for an unimpaired reserve. Partial liquidations and excess proceeds have their own allocation rules.

Adding collateral and lowering the stored liquidation price are separate operations. The [adjustment guide](adjust.md#lowering-the-liquidation-price) explains their debt and collateral constraints.

## How to Initiate an Auction

The [monitoring page](https://app.frankencoin.com/monitoring) lists positions. Start with the position address, chain, collateral token and stored liquidation price. Compare that price with the amount a market buyer would pay for the collateral; the protocol does not obtain an oracle price for you.

1. **Select the amount to challenge.** You need that amount of the same collateral token in your own wallet, as well as native gas. The challenged size is an amount of collateral, not a ZCHF bid. Check the position's minimum challenge size and existing challenges.
2. **Review the price and timing.** Read the current stored price and phase duration. The pinned `challenge` operation also takes `minimumPrice`: it reverts if the position's price has fallen below that value before execution. This protects the price condition you chose; it is not an oracle input.
3. **Approve and submit.** If needed, approve the hub to transfer your collateral, then submit the challenge transaction. Approval alone does not start an auction. Your posted collateral can be bought in the first phase, so a challenge is not a risk-free report or a guaranteed reward.
4. **Confirm and follow settlement.** Record the challenge number from the confirmed transaction and read its start time, size and phase. Follow bids to see how much was averted or settled. A first-phase purchase sells your posted collateral; later-phase settlement normally returns the corresponding posted collateral and pays the bid-based reward.

<figure><img src="../.gitbook/assets/kuva (41).png" alt="Historical challenge entry point"><figcaption><p>Historical monitoring interface.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/kuva (42).png" alt="Historical challenge setup"><figcaption><p>Historical challenge setup, not a current quote.</p></figcaption></figure>

Some collateral returns can be postponed. In that case, read the hub's `pendingReturns` for your token and address, then use `returnPostponedCollateral` to collect it to the intended recipient. An indexed success label alone does not tell you whether collateral was returned or proceeds received; check the transaction and balances.

## How to Participate in Ongoing Auctions

The [auctions page](https://app.frankencoin.com/challenges) shows indexed challenges. The phase, remaining amount and transaction quote determine what collateral a bid buys and at what price. A confirmed bid can change the remaining amount before another transaction executes.

1. **Identify the challenge.** Match its chain, hub, position and challenge number. Read its remaining size and current phase. In the first phase you buy the challenger's collateral at the fixed liquidation price; in the second you buy the position's collateral at the declining price.
2. **Choose how much collateral to buy.** Obtain the corresponding ZCHF cost from the current quote and compare it with your intended purchase. The pinned `bid` method takes a collateral size, not a freely chosen auction price, and reduces that size if less remains available.
3. **Fund and submit the bid.** You need ZCHF and native gas. Approve the relevant spender if required, review the transaction's phase and expected amounts, then submit. A bid executes the purchase; it is not an offer held until all bids are collected at an auction deadline.
4. **Check what arrived.** After confirmation, check the ZCHF spent, collateral received and remaining challenge size. Partial bids can leave more collateral under challenge. If the phase changed or another bid executed first, the old page quote may no longer describe the result.

<figure><img src="../.gitbook/assets/kuva (43).png" alt="Historical empty auction list"><figcaption><p>Historical empty state, not a statement about current auctions.</p></figcaption></figure>
