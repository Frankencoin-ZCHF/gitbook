---
description: How to adjust a position
---

# Adjusting a Position

Once you are the proud owner of a position whose cool-down period has passed, you can start to adjust it. You can adjust the outstanding amount, the amount of the deposited collateral, and the liquidation price.&#x20;

To start adjusting your position, head over to the "Positions" tab. Once there, you can see your existing position(s) at the top of the page. If you don't see your position here, make sure that the wallet that originally created the position is connected. This is crucial: If none or any other wallet is connected, your position will not show up here.&#x20;

<figure><img src="../.gitbook/assets/kuva (19).png" alt=""><figcaption><p>My Positions</p></figcaption></figure>

Once you see this, simply click on the "Adjust" button. This will take you to the following page:&#x20;

<figure><img src="../.gitbook/assets/kuva (20).png" alt=""><figcaption><p>Adjust Position without Parameters</p></figcaption></figure>

When you're directed here, all fields are empty at first. If you have just proposed a new collateral type, note that you haven't actually minted any ZCHF yet.

In the above example, you can see that the "Collateral" part indicates that 2 WETH will be sent back to the wallet, as long as the input is 0.  However, it is important to observe the dust limit. For example, if the minimum collateral is 2 WETH (as it is in this example), the collateral cannot be reduced to 1.9 WETH. This means that this particular transaction would fail. However, if there is any excess collateral above the minimum requirement, it can be withdrawn here.&#x20;

On the other hand, if the full 2 WETH should be used to mint new ZCHF, the parameters would look like this:&#x20;

<figure><img src="../.gitbook/assets/kuva (21).png" alt=""><figcaption><p>Adjust Position with Parameters</p></figcaption></figure>

Now, the amount is set to the 5,000 ZCHF. This was set during the opening of a new position. The liquidation price of 2,500 ZCHF per WETH and two WETH as collateral, result in the amount of 5,000 ZCHF.&#x20;

This is confirmed by the "Outcome" section on the right side. While 5,000 ZCHF are minted, the number of ZCHF that will be received is actually lower (4,352.05 ZCHF). This is because of the minting fee, or the interest, that is charged. This was also set during the proposal of WETH as collateral. Similarly, the amount that is added to the reserve was also set during the proposal, in this case 10%. Both of these are charged upfront. You will never get the fee back, but you will likely get the reserve back when you return and burn the minted Frankencoins. The reserve might be used to cover the system's losses after all equity has been wiped out. This creates an incentive for you to help looking after the system.

If you want to decrease or increase the liquidation price, you can adjust it here as well.&#x20;

<figure><img src="../.gitbook/assets/kuva (26).png" alt=""><figcaption><p>Adjust liquidation price</p></figcaption></figure>

In this example, the liquidation price is decreased to 2,000 ZCHF. With 2 WETH as collateral, the new maximum amount that can now be minted is 4,000 ZCHF.

When paying back your loan, meaning decreasing the amount, you need to have some Frankencoins in the wallet, but some are also taken out of the reserve. For example, if the reserve ratio is 10%, it suffices to return 900 ZCHF in order to close a 1000 ZCHF position as the other 100 ZCHF are taken from the reserve.&#x20;

If you would like to add more collateral to achieve a lower liquidation point, you can also do this here. There is no limit for how much collateral you can add.&#x20;

You are also able to increase the liquidation price here. Increasing the liquidation price will allow you to borrow more, but only after the cool-down period has passed again, allowing others to challenge your position at the new price before you can use the higher price to mint Frankencoin.
