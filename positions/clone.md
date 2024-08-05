---
description: >-
  Immediately mint Frankencoins by cloning an established position that is not
  maxed out.
---

# Cloning Existing Positions

This is the standard way to obtain Frankencoins against a collateral. Unlike creating an entirely new position, which takes a lot of time, borrowing by cloning an established position can be done immediately. To do so, [find an existing position](https://app.frankencoin.com/positions) that is based on your collateral of choice and that is not maxed out yet, i.e. where the borrowed total is below the limit. You can spot such a position by searching for the red "Clone & Mint" button. Note the available amount: This shows how many more ZCHF can be minted by cloning this particular position. The third position shown here has 0.00 ZCHF left and no "Clone & Mint" button, meaning that this position can no longer be cloned. When looking for a position to clone, make sure to pay attention to the liquidation price. In this case, while all three positions are based on WBTC, the liquidation price differs.&#x20;

<figure><img src="../.gitbook/assets/kuva (2) (1) (1).png" alt=""><figcaption><p>Note the "Available Amount"</p></figcaption></figure>

Once you have chosen your collateral type, simply click the "Clone & Mint" button to be taken to the position overview page. Here, you can see a detailed view showing all the relevant parameters.&#x20;

The "Limit" value shows how much this position can mint in total. The "Minted Total" denominates how much of that limit has been used already. In this case, we are left with a difference of 2,791,718.32 ZCHF - the "Available Amount" from the screenshot above.The "Retained Reserve" is calculated based on the "Reserve Requirement" section. The interest that needs to be paid upfront is shown under "Annual Interest". On the right, you can see that this position is not currently being challenged. If you want to proceed with cloning this position, click on "Clone & Mint" on the bottom left.&#x20;

<figure><img src="../.gitbook/assets/kuva (10) (1).png" alt=""><figcaption><p>Position overview</p></figcaption></figure>

After that, you will be redirected to the minting page. First, let's focus on the left side of the screen. While you can discover the page without connecting a wallet, doing so will give you a real-time view of what is possible with your current balance. Once you click on "Connect Wallet" on the bottom left, you will be given a choice of wallets. Choose whichever suits you best.&#x20;

<figure><img src="../.gitbook/assets/kuva (4) (1) (1).png" alt=""><figcaption><p>Connect a wallet of your choice</p></figcaption></figure>

Once you connected a wallet, you can enter how many ZCHF you want to mint. This amount needs to be at or below the limit. The required collateral is adjusted accordingly. The expiration can be set between today and the limit date. The limit date is the date the parent position was minted, plus one year. Note: The amount borrowed can be changed later, but not increased beyond the initial amount. The liquidation price is inherited from the parent position but can be adjusted later. For example, the liquidation price could be doubled and then half of the collateral taken out if the new liquidation price is not challenged.&#x20;

<figure><img src="../.gitbook/assets/kuva (6) (1).png" alt=""><figcaption><p>Choose the amount of ZCHF you want to mint</p></figcaption></figure>

Now, let's focus on the right side of the screen.&#x20;

The "Outcome" section shows you how much of the new ZCHF will be sent to your wallet, and how much will be locked in the borrowers reserve. Unless the Frankencoin system suffers from large losses in the meantime, you will get that reserve back as you repay the outstanding amount. It is possible to repay partially or to repay early but the fee is paid upfront and never returned.

<figure><img src="../.gitbook/assets/kuva (8) (1).png" alt=""><figcaption><p>See a detailed overview of the outcome</p></figcaption></figure>

Once you are ready, you can take the final step and hit "Approve" on the bottom left. When confirming the inputs, a transaction is created that will at the same time deduct the required amount of collateral and mint the indicated amount of Frankencoins into your wallet.&#x20;
