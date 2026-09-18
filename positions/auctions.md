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

The [monitoring page](https://app.frankencoin.com/monitoring) lists positions. A challenge needs the selected collateral amount, any required allowance and the challenge transaction. The challenger supplies collateral that can be bought in the first phase; a submitted challenge does not guarantee a reward.

<figure><img src="../.gitbook/assets/kuva (41).png" alt="Historical challenge entry point"><figcaption><p>Historical monitoring interface.</p></figcaption></figure>

<figure><img src="../.gitbook/assets/kuva (42).png" alt="Historical challenge setup"><figcaption><p>Historical challenge setup, not a current quote.</p></figcaption></figure>

## How to Participate in Ongoing Auctions

The [auctions page](https://app.frankencoin.com/challenges) shows indexed challenges. The phase, remaining amount and transaction quote determine what collateral a bid buys and at what price. A confirmed bid can change the remaining amount before another transaction executes.

<figure><img src="../.gitbook/assets/kuva (43).png" alt="Historical empty auction list"><figcaption><p>Historical empty state, not a statement about current auctions.</p></figcaption></figure>
