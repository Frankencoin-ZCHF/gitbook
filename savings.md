---
description: >-
  The savings module allows users to earn an interest on their Frankencoin
  holdings.
---

# 💰 Savings

([source code](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/main/contracts/minting/v2/SavingsV2.sol), [deployed contract](https://etherscan.io/address/0x3bf301b0e2003e75a3e86ab82bd1eff6a9dfb2ae))

The Savings Module ([frontend](https://app.frankencoin.com/savings)) allows users to earn interest on their Frankencoin (ZCHF) holdings by storing them in the protocol.

### Overview

The savings module takes money out of the equity pool and gives it to Frankencoin holders that have stored some of their Frankencoins in the savings module. The transferred amount depends on the currently applicable interest rate.

<figure><img src=".gitbook/assets/image (2).png" alt=""><figcaption><p>Savers can acquire ZCHF (7), store them in the savings module (8) and earn an interest (9) paid for by the system.</p></figcaption></figure>

### Saving

Anyone can store Frankencoins in the savings module. These Frankencoins are attributable to their owner at all times (i.e. they are fully segregated) and stay in the savings module until their owner withdraws them again. There is no lending or other transfer happening in the background. Also, unlike the minter reserves, the stored Frankencoins cannot be touched to save the system in case of a depeg.

### Delay

Frankencoins can be sent to the Savings module and withdrawn again at any time. However, there is a delay of three days until interest starts to accrue. The purpose of the delay is to discourage users from trying to earn an interest on Frankencoins that are held temporarily for transactional purposes. In case the user already has some Frankencoins in his savings account, the applicable delay is a weighted average between the already stored and the newly added Frankencoins.

### Interest

The applicable interest rate is determined by the [governance process](governance.md). The savings rate and the borrow rate are independent values. Proposed interest changes can be enacted after seven days if no veto was cast. For simplicity, the interest is only calculated on the principal amount. There is no interest on the accrued interest. The interest is automatically collected and added to the account whenever funds are added or withdrawn.

## Referral Module

([source code](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/main/contracts/savings/Savings.sol), [deployed contract](https://etherscan.io/address/0x27d9AD987BdE08a0d083ef7e0e4043C857A17B38))

The **SavingsReferral Module** introduces a referral-based incentive layer on top of Frankencoin's decentralized savings infrastructure. It is designed to help wallets, dApps, and integrators build sustainable revenue models while offering a native Swiss Franc-denominated yield product to their users. Using the SavingsReferral module, builders can get up to 25% of the savings earned by "their" users.

### How It Works

1. A frontend/wallet integrates the savings UI
2. When calling `save()` or `adjust()` methods, a **referrer address** and **referral fee (ppm)** are passed
3. Interest accrues on user deposits after a 3-day delay
4. When interest is claimed, the smart contract:
   * Pays the user
   * Automatically redirects up to 25% of earned interest to the referrer

### Using the Frankencoin App to Refer Users

You can also use the Frankencoin App to share referral links as follows:

```
<https://app.frankencoin.com/savings?referrer=0x123...4&fee=500>
```

This will automatically set the referrer and fee when the user lands on the page and initiates a savings deposit.

### Claiming Accrued Referral Fees

Referral fees are automatically distributed to the referrer whenever a user’s interest is collected. Referrers do not need to actively claim fees — they are transferred on-chain in real-time as interest is paid out to users.

However, **interest collection must be triggered** manually by calling `refresh()` or `refreshBalance()` on the user’s account. This can be done by:

* The user
* The referrer (to collect their share)
* A third party (e.g., a keeper bot)

This means that a referrer can actively call `refresh()` on behalf of their referred users to ensure interest (and thus their fee) is paid out regularly.



### Wallet Implementation Guide

To ensure users of your wallet automatically assign your address as the referrer:

* Add a custom savings integration UI that interfaces with the Frankencoin contract
* In the backend or UI logic, always pass your designated referrer address and chosen referral fee (e.g., 200\_000 ppm) to the `save()` or `adjust()` calls
* Example:

```solidity
savings.save(1_000e18, 0xYourFrontendAddress, 200_000); // 20% referral fee
```

* Optional: Give users the ability to drop/change their referrer, or hide this setting depending on UX goals

### Integration Details

* Call `save(amount, referrer, referralFeePPM)` or `adjust(targetAmount, referrer, referralFeePPM)`
* Max referral fee is **250,000 ppm** (25%)



