---
description: Version-specific savings, interest collection and referral terms.
---

# 💰 Savings

The [savings application](https://app.frankencoin.com/savings) lets users deposit ZCHF and earn a governance-set rate. Interest comes from the system's equity; borrowing and savings rates are separate parameters. Deposited ZCHF remains attributed to the savings account rather than being lent out to borrowers.

## Contract versions

Etherscan's published source and ABI for these Ethereum addresses were checked on 18 September 2026. They confirm the withdrawal-lock distinction and public methods below. Repository references are pinned to `8b4c4ab67bb361b91d58c474b87f4608fc4c0566`; the application may select a different module. The first explorer labels its contract `Savings`, despite the repository's later `SavingsV2.sol` naming.

| Version | Existing address reference | Source behaviour |
| --- | --- | --- |
| Legacy SavingsV2 | [0x3bf301b0e2003e75a3e86ab82bd1eff6a9dfb2ae](https://etherscan.io/address/0x3bf301b0e2003e75a3e86ab82bd1eff6a9dfb2ae#code) | [SavingsV2.sol](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/minting/v2/SavingsV2.sol) applies an interest delay and a `FundsLocked` withdrawal check |
| Referral-enabled Savings | [0x27d9AD987BdE08a0d083ef7e0e4043C857A17B38](https://etherscan.io/address/0x27d9AD987BdE08a0d083ef7e0e4043C857A17B38#code) | [Savings.sol](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/savings/Savings.sol) inherits [AbstractSavings.sol](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/savings/AbstractSavings.sol): an interest delay, no equivalent ticks-based withdrawal lock, and referral support |

### Saving

A savings deposit transfers ZCHF to the selected module and credits the account. An old deposit remains in its original contract. Moving to a different module requires withdrawing under the old module's rules and depositing into the new one; it is not an automatic upgrade. The new deposit uses the new module's delay and referral terms.

### Delay

Both source versions use a three-day delay before a fresh deposit earns interest. Adding funds to an existing account produces a weighted delay rather than restarting the full delay on the entire balance.

In **SavingsV2**, `withdraw` reverts with `FundsLocked` while the account's stored ticks exceed current ticks. The delay therefore also restricts withdrawals. In the **referral-enabled source**, `withdraw` has no equivalent ticks-based lock, so the interest delay does not itself prevent withdrawing principal. The contract version, not the page title, determines which behaviour applies.

### Interest

The rate can change through [governance](governance.md#proposal-submission). Interest accrues on the stored principal. Uncollected interest does not compound; collection adds the user's interest to principal, after which it can earn interest too. Deposits and withdrawals refresh accrued interest as part of their operation.

## Referral Module

A referral fee allocates a share of **earned interest**, not a share of deposited principal, to a referrer. The maximum is 250,000 parts per million (ppm), or 25%. At 200,000 ppm, 100 ZCHF of gross interest becomes 80 ZCHF for the user and 20 ZCHF for the referrer.

### How It Works

The referral-enabled source exposes these signatures:

```text
save(uint192 amount, address referrer, uint24 referralFeePPM)
adjust(uint192 targetAmount, address referrer, uint24 referralFeePPM)
```

Amounts use ZCHF's 18-decimal base units. The fee uses a denominator of 1,000,000; for example, `200_000` means 20%, not 20 basis points. The transaction interface should show the referrer, fee percentage and resulting net interest before the user signs.

### Using the Frankencoin App to Refer Users

A referral link is an application feature, not a contract method. Its query parameters must match the selected application's implementation. The signed transaction's referrer and `referralFeePPM` determine the on-chain setting; an abbreviated address is not a valid transaction argument.

### Claiming Accrued Referral Fees

Collection pays the referrer when the user's interest is refreshed. A separate collection transaction is optional because deposits and withdrawals also refresh interest. The public methods in both pinned source versions are:

```text
refreshMyBalance()
refreshBalance(address owner)
```

The account holder can use `refreshMyBalance()`. A referrer or another caller can use `refreshBalance(userAddress)`. The internal `refresh(address)` function is not an externally callable method. Refreshing another account does not change its owner or redirect the user's principal.

### Wallet Implementation Guide

An integration supplies the amount, referrer and fee to a supported method of the selected contract. It displays the gross rate, referral share and net rate separately. The maximum fee is a protocol limit, not a default fee.

The account holder can remove the referral by calling **`dropReferrer()`** on the referral-enabled contract through an interface exposing its verified ABI. This first collects accrued interest and settles the accrued referral fee, then clears the referrer and sets the fee to zero. Future interest has no referral deduction unless a later transaction sets a referrer again. Removal does not reverse fees already earned.

### Integration Details

[The savings API reference](api-docs/savings.md) describes indexed balances and rates. API reads do not create deposits, collect interest or remove a referrer; those are on-chain transactions.
