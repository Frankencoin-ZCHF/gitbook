---
description: Bot subscriptions, confirmation and the scope of position alerts.
---

# 🤖 Notification Bot

The [Frankencoin API Telegram Bot](https://t.me/FrankencoinApiBot), **@FrankencoinApiBot**, reports proposals, position activity and other indexed events. FCS holders can use governance alerts to follow proposals; borrowers can follow their positions. Receiving an alert does not submit a transaction or establish voting eligibility. The [FCS governance guide](governance.md#taking-part-with-fcs) explains how to act on a proposal.

## How to find it?

Open the linked bot in Telegram and send `/help`. The commands below are implemented in [telegram.service.ts at commit 4fdbd1007a2c75bddff2aaadf2d370e5dc296dd4](https://github.com/Frankencoin-ZCHF/frankencoin-api/blob/4fdbd1007a2c75bddff2aaadf2d370e5dc296dd4/src/integrations/telegram/telegram.service.ts). They were checked against public source on 18 September 2026, not by sending messages to the live bot.

## Subscription Handels

The heading above is retained for existing links. Subscription commands are:

| Command | Effect |
| --- | --- |
| `/help` | Show available commands |
| `/status` | Show active governance, all-position and owner subscriptions |
| `/start GOV` | Subscribe to governance alerts |
| `/stop GOV` | Remove governance alerts |
| `/start ALL` | Subscribe to all-position alerts |
| `/stop ALL` | Remove all-position alerts |
| `/start <owner address>` | Subscribe to positions belonging to a complete `0x` plus 40-hex-digit owner address |
| `/stop <owner address>` | Remove that owner subscription |

Angle-bracket text is a placeholder, not a literal command argument. The first message registers the chat in the inspected implementation and enables governance and all-position alerts by default. `/status` shows the resulting state; unwanted categories can then be removed explicitly. The older `/MintingUpdates` toggle shown in historical material is not the command model above.

After subscribing, the bot returns a confirmation. Send `/status` and check the category or full owner address. To test the subscription controls without creating a protocol event, remove and re-add the category, checking `/status` after each change. This checks the subscription response, not future event delivery.

## Basic Messages

### Welcome and Environment Information

Help and status identify the chat and subscriptions. Event messages link to relevant transactions, addresses or application views.

### Minter Proposals

Governance alerts include minter proposals and vetoes, interest-rate changes and CCIP proposals or rate-limit changes.

### Minter Proposals Vetoed

<figure><img src=".gitbook/assets/Screenshot 2024-09-26 at 12.13.41 PM.png" alt="Historical minter-veto notification"><figcaption><p>Historical message format.</p></figcaption></figure>

### Position Proposals

<figure><img src=".gitbook/assets/Screenshot 2024-09-26 at 12.10.32 PM.png" alt="Historical position-proposal notification"><figcaption><p>Historical message format.</p></figcaption></figure>

### Challenges Started

<figure><img src=".gitbook/assets/Screenshot 2024-09-26 at 12.16.07 PM.png" alt="Historical challenge notification"><figcaption><p>Historical message format.</p></figcaption></figure>

### Minting Updates

<figure><img src=".gitbook/assets/Screenshot 2024-09-26 at 12.15.21 PM.png" alt="Historical minting update"><figcaption><p>Historical message format.</p></figcaption></figure>

### Expiry and price alerts

The inspected source includes expiry notifications at the seven-day and one-day thresholds, and after expiry. Price alerts compare the service's collateral price feed with the position's liquidation price, using warning bands and cooldowns. Owner subscriptions follow the position's owner address; they are not subscriptions to a position address.

Notifications depend on service uptime, indexing, price coverage and Telegram delivery. They do not execute repayment or liquidation-price changes, and a missing alert does not change the contract's expiry or stored price.

### Historical subscription screenshots

These local assets preserve the older interface; the textual commands above describe the pinned implementation.

<figure><img src=".gitbook/assets/Screenshot 2024-09-26 at 12.25.01 PM.png" alt="Historical subscription settings"><figcaption><p>Historical subscription interface.</p></figcaption></figure>

<figure><img src=".gitbook/assets/Screenshot 2024-09-26 at 12.25.11 PM.png" alt="Historical subscription confirmation"><figcaption><p>Historical subscription interface.</p></figcaption></figure>
