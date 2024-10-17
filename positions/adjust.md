---
description: Learn how to adjust a position.
---

# Adjusting a Position

Once you are the proud owner of a position whose cool-down period has passed, you can start to adjust it. You can adjust the outstanding amount, the amount of the deposited collateral, and the liquidation price.&#x20;

To start adjusting your position, head over to the "My Positions" tab. Once there, you can see your existing position(s) at the top of the page. If you don't see your position here, make sure that the wallet that originally created the position is connected. This is crucial: If no wallet or any other wallet is connected, your position will not show up here.&#x20;

<figure><img src="../.gitbook/assets/kuva (37).png" alt=""><figcaption><p>My positions</p></figcaption></figure>

Once you see this, simply click on the "Manage" button. This will take you to the following page:&#x20;

<figure><img src="../.gitbook/assets/kuva (38).png" alt=""><figcaption><p>Adjust your position here</p></figcaption></figure>

When you land on this page, all fields are empty at first. If you have just proposed a new collateral type, note that you haven't actually minted any ZCHF yet!

If the full 2 WETH defined earlier should be used to mint new ZCHF, the parameters would look like this:&#x20;

<figure><img src="../.gitbook/assets/kuva (39).png" alt=""><figcaption><p>Mint new ZCHF</p></figcaption></figure>

The amount is set to 3 000 ZCHF. This was set during the opening of a new position. The liquidation price of 1 500 ZCHF per WETH and two WETH as collateral result in the amount of 3 000 ZCHF.&#x20;

This is confirmed by the "Outcome" section on the right side. While 3 000 new ZCHF will be minted, the number of ZCHF that will be received is actually lower (2 610 ZCHF). This is because of the minting fee, or the interest, which is charged upfront. This was also set during the proposal of WETH as collateral. Similarly, the amount that is added to the reserve was also set during the proposal, in this case 10%. Both of these are charged upfront. You will not get the fee back, but you will likely get the reserve back when you return and burn the minted Frankencoins. The reserve might be used to cover the system's losses in case there are any. This creates an incentive for you to help looking after the system.

When paying back your loan, meaning decreasing the amount, you need to have some Frankencoins in the wallet, but some are also taken out of the reserve. For example, if the reserve ratio is 10%, it suffices to return 900 ZCHF in order to close a 1 000 ZCHF position as the other 100 ZCHF are taken from the reserve.&#x20;

If you would like to add more collateral to achieve a lower liquidation point, you can also do this here. There is no limit for how much collateral you can add.&#x20;

You are also able to increase the liquidation price here. Increasing the liquidation price will allow you to borrow more, but only after the cool-down period has passed again, allowing others to challenge your position at the new price before you can use the higher price to mint Frankencoin.
