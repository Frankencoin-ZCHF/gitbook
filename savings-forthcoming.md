---
description: >-
  The savings module allows users to earn an interest on their Frankencoin
  holdings.
---

# 💰 Savings

The Savings Module ([frontend](https://app.frankencoin.com/savings)) allows users to earn interest on their Frankencoin (ZCHF) holdings by storing them in the protocol. There are currently two types of savings modules available: SavingsV2 and SavingsReferral.

### Overview

The savings module takes money out of the equity pool and gives it to Frankencoin holders that have stored some of their Frankencoins in the savings module. The transferred amount depends on the currently applicable interest rate.

<figure><img src=".gitbook/assets/image (2).png" alt=""><figcaption><p>Savers can acquire ZCHF (7), store them in the savings module (8) and earn an interest (9) paid for by the system.</p></figcaption></figure>

### Saving

Anyone can store Frankencoins in the savings module. These Frankencoins are attributable to their owner at all times (i.e. they are fully segregated) and stay in the savings module until their owner withdraws them again. There is no lending or other transfer happening in the background. Also, unlike the minter reserves, the stored Frankencoins cannot be touched to save the system in case of a depeg.

### Delay

Frankencoins can be sent to the Savings module and withdrawn again at any time. However, there is a delay of three days until interest starts to accrue. The purpose of the delay is to discourage users from trying to earn an interest on Frankencoins that are held temporarily for transactional purposes. In case the user already has some Frankencoins in his savings account, the applicable delay is a weighted average between the already stored and the newly added Frankencoins.

### Risks

The main risk for the savers is the depeg risk, i.e. the Frankencoin having an exchange rate below 1.00 Swiss franc when the saved Frankencoins are withdrawn again. An additional small risk is that the interest rate can only be added to the balance as long as the system is solvent. The interest is paid from the equity capital of the system and if there is no equity capital left, no interest can be paid. There is no counterparty risk as the Frankencoins are never transferred outside the savings module. The users can be sure to get the stored Frankencoins back.

### Interest

The applicable interest rate is determined by the [governance process](governance.md). The savings rate and the borrow rate are independent values. Proposed interest changes can be enacted after seven days if no veto was cast. For simplicity, the interest is only calculated on the principal amount. There is no interest on the accrued interest. The interest is automatically collected and added to the account whenever funds are added or withdrawn.

## Savings Module Variants

### Savings V2

([source code](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/main/contracts/minting/v2/SavingsV2.sol), [deployed contract](https://etherscan.io/address/0x3bf301b0e2003e75a3e86ab82bd1eff6a9dfb2ae))

The SavingsV2 Module is integrated with MintingHubV2, using a governance-controlled lead rate to determine the borrow rate across the system, including PositionV2.

Interest on deposited funds in the SavingsV2 Module begins to accrue after a 3-day locktime, discouraging short-term or transactional deposits.

### Savings Referral

([source code](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/main/contracts/savings/Savings.sol), [deployed contract](https://etherscan.io/address/0x27d9AD987BdE08a0d083ef7e0e4043C857A17B38))

The SavingsReferral Module operates independently from the minting hubs and introduces a referral-based incentive system designed to encourage network growth.

Users can deposit Frankencoins and withdraw at any time without a lock period, making it more flexible than the SavingsV2 Module. However, interest still begins accruing only after a 3-day delay, consistent with the system’s overall design to discourage short-term deposits.

A key feature of this module is the ability to assign a referrer address, allowing interest earnings to be shared between the saver and their referrer. The system supports a maximum referral split of 25%, meaning up to a quarter of the earned interest can be allocated to the referrer.

**Please note:** Frontend support for the SavingsV2 Module is planned to be phased out and replaced by support for the SavingsReferral Module. Users may eventually need to interact with SavingsV2 through alternative interfaces or directly via smart contracts.
