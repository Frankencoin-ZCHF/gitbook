---
description: >-
  The savings module allows users to earn an interest on their Frankencoin
  holdings.
---

# 💰 Savings

### Overview

The savings module ([frontend](https://app.frankencoin.com/savings),  [source code](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/main/contracts/Savings.sol), [deployed contract](https://etherscan.io/address/0x3bf301b0e2003e75a3e86ab82bd1eff6a9dfb2ae)) takes money out of the equity pool and gives it to Frankencoin holders that have stored some of their Frankencoins in the savings module. The transferred amount depends on the currently applicable interest rate.

<figure><img src=".gitbook/assets/image.png" alt=""><figcaption><p>Savers can acquire ZCHF (7), store them in the savings module (8) and earn an interest (9) paid for by the system.</p></figcaption></figure>

### Saving

Anyone can store Frankencoins in the savings module. These Frankencoins are attributable to their owner at all times (i.e. they are fully segregated) and stay in the savings module until their owner withdraws them again. There is no lending or other transfer happening in the background. Also, unlike the minter reserves, the stored Frankencoins cannot be touched to save the system in case of a depeg.

### Delay

Frankencoins can be sent to the Savings module and withdrawn again at any time. However, there is a delay of three days until interest starts to accrue. The purpose of the delay is to discourage users from trying to earn an interest on Frankencoins that are held temporarily for transactional purposes. In case the user already has some Frankencoins in his savings account, the applicable delay is a weighted average between the already stored and the newly added Frankencoins.

### Risks

The main risk for the savers is the depeg risk, i.e. the Frankencoin having an exchange rate below 1.00 Swiss franc when the saved Frankencoins are withdrawn again. An additional small risk is that the interest rate can only be added to the balance as long as the system is solvent. The interest is paid from the equity capital of the system and if there is no equity capital left, no interest can be paid. There is no counterparty risk as the Frankencoins are never transferred outside the savings module. The users can be sure to get the stored Frankencoins back.

### Interest

The applicable interest rate is determined by the [governance ](governance.md)process. The savings rate and the borrow rate are independent values. Proposed interest changes can be enacted after seven days if no veto was cast. For simplicity, the interest is only calculated on the principal amount. There is no interest on the accrued interest.  The interest is automatically collected and added to the account whenever funds are added or withdrawn.
