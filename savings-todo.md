---
description: >-
  The savings module allows users to park their Frankencoin and earn an
  interest. This feature is under development and not yet available.
---

# 💰 Savings (TODO)

TODO: show UI of the savings module

## Economic and Technical Background

When saving, your Frankencoins are stored under a segregated account in the [savings contract](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/savings/contracts/Savings.sol). They are locked up until you withdraw them again. The average interest rate the users of the savings module get is limited by the interest rate that the system gets from those who used the collateralized minting mechanism to create Frankencoins. However, as the savings contract does not know the full list of available positions to calculate the average, it is dependent on user hints when depositing and withdrawing, allowing those users that come first to earn above average interest rates (by only telling the savings contract about reference positions with higher interest rates). The frontend automatically optimizes this for you. This information is only provided to explain why users that come earlier might get better interest rates than users that come later. The interest itself is paid out of the equity capital of the system and therefore slightly diminishes the price of the FPS token whenever accrued interests are paid out. However, the interest paid out cannot exceed the interest earned by the system.
