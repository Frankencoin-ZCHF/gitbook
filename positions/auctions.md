---
description: >-
  Challenges and the resulting auctions are a mechanism to ensure positions are
  backed by sound collateral.
---

# Challenges and Auctions

## Auction Design

Challenging a position triggers an auction of the collateral. The auction serves two purposes, the determination of the market price and the liquidation of the collateral at that market price. The auction frees the system from the need for an external oracle. The difficulty lies in designing the auction such that it cannot be profitably manipulated.

Traditional auctions are prone to price manipulation by the owner of the auctioned assets. For example, if Alice minted 1 000 ZCHF against a collateral whose value has dropped to 950 ZCHF, she might be tempted to bid 1 001 ZCHF for that collateral in an auction, thereby planting the false believe that the position is still well-collateralized. Frankencoin prevents this by cleverly switching the collateral the bidders are bidding for at the critical price point. For bids below 1 000 ZCHF, the bidders will get Alice's collateral. When bidding above 1 000 ZCHF, the bidders will get the collateral asset from the challenger. Thanks to this approach, price manipulation becomes very expensive for Alice as the 1 001 ZCHF bid would not go to her own pockets, but the pockets of the challenger. In order to prevent her position from being liquidated, she would have to pay 1 001 ZCHF for an asset worth 950 ZCHF as often as the challenger chooses to repeat the challenge.

This example reveals one of the underlying assumptions of the system and a requirement for an asset to be acceptable as a collateral. While it is not necessary that there is a liquid market, it is important that the potential challengers own enough of the collateral asset (or can acquire it somewhere) to repeatedly challenge Alice. Once Alice ends up owning 100% of the collateral asset in circulation, she cannot be challenged anymore and can start minting arbitrary amounts of Frankencoins. That is also why the Frankencoin auction system does not work with non-fungible tokens. It is important that no position is ever accepted that is based on collateral with too limited availability.

One good property about the auction design is that as long as someone is willing to bid the market price for a collateral asset, the maintenance of the position does not require any attention of the owner. Only when the market price is about to fall below the liquidation price, the owner should start thinking about repaying it or making it more sound again by providing more collateral and adjusting the liquidation price downwards.

I the highest bid is below the liquidation price, the challenge is considered successful. After a successful challenge, the minter reserve associated with the position is dissolved and added to the proceeds from the auction. The total proceeds are then used to repay the position and to reward the challenger. If there are not enough funds to do that, equity holders have to jump in and suffer a loss. If there is something left, the remaining amount is sent to the equity holders as a profit. For example, if the minter reserve was 20% and the highest bid for Alice's collateral was 950 ZCHF, the equity holders make a profit of 150 ZCHF, minus the challenger reward. However, if the highest bid was below 800 ZCHF, they will make a loss.

## How to Initiate an Auction

On the [Monitoring page](https://app.frankencoin.com/monitoring) you can find a list of all open positions. If you believe that the conditions are right to challenge a position, you can simply click on the "Challenge" button here.&#x20;

<figure><img src="../.gitbook/assets/kuva (41).png" alt=""><figcaption><p>Click on "Challange" to initiate a new challenge</p></figcaption></figure>

After that, you can initiate a new challenge.&#x20;

<figure><img src="../.gitbook/assets/kuva (42).png" alt=""><figcaption><p>Initiate a new challenge</p></figcaption></figure>

Here, you can choose the amount of collateral you want to challenge. For that, you need to have the corresponding amount of the collateral asset in your wallet. The "Potential Reward" corresponds to 2%. The challenge itself is divided into two phases. In the first phase, the price remains fixed. In the second phase (in case there is still some collateral left), the price starts to decline towards zero. At this stage, the bidders are buying the original minter's collateral.&#x20;

## How to Participate in Ongoing Auctions

Under the [Auctions page](https://app.frankencoin.com/challenges), you can find all ongoing challenges. As of writing this page, there are no ongoing challenges.

<figure><img src="../.gitbook/assets/kuva (43).png" alt=""><figcaption><p>No active challenges</p></figcaption></figure>

If there were any ongoing challenge, they would show up under this tab. Here, you will have the chance to participate.&#x20;
