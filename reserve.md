---
description: Reserve and equity accounting, with explicit example assumptions.
---

# 🏦 Reserve

The reserve consists of ZCHF held for minter reserves and equity. [FCS holders](pool-shares.md) participate in the equity through the token's underlying FPS backing. Protocol income increases that shared capital, while savings expense and losses reduce it. FCS does not create a separate reserve.

External stablecoins in conversion bridges are separate assets. Collateral remains in individual positions; the stylised balance sheet below records the associated repayment obligations rather than adding the collateral a second time.

## Balance Sheet Diagram

The accounting model is:

```text
Assets                         Liabilities and equity
x: external bridge assets      z: total ZCHF supply
m: minter repayment claims      b: minter-reserve allocation
r: ZCHF reserve                e: equity

x + m + r = z + b + e
```

This gross presentation includes reserve-held ZCHF within total supply. It is an explanatory protocol balance sheet, not a company balance sheet or a valuation of every collateral token.

## Assets

* **Bridge assets (`x`):** external stablecoins held by stablecoin-conversion bridges. XCHF was used by the bootstrap bridge; that is a historical example, not a list of active bridges.
* **Minter repayment claims (`m`):** outstanding gross ZCHF debt recorded by positions.
* **Reserve (`r`):** ZCHF held for the system's minter-reserve allocation and equity.

## Liabilities and Equity

* **Total ZCHF supply (`z`):** issued ZCHF, including reserve holdings in this model.
* **Minter reserve (`b`):** the reserve allocation associated with minted debt. It can absorb losses and is not unconditionally recoverable by each minter.
* **Equity (`e`):** the residual reserve capital in which FCS holders participate. The underlying Equity contract accounts for this capital and issues the FPS backing each FCS.

## Example Scenarios

All amounts below are ZCHF-denominated illustrations, not observations of deployed positions.

### Historical stablecoin conversion

A 100 ZCHF redemption through the historical one-to-one XCHF bridge reduces bridge assets `x` and ZCHF supply `z` by 100. The example assumes available bridge assets and an eligible redemption; it says nothing about current route availability.

### Minting

Assume a gross mint of 500 ZCHF, a 20% reserve contribution and a 5% up-front fee. The wallet receives 375 ZCHF; the reserve retains 100 ZCHF for the minter and 25 ZCHF as equity income.

| Account | Change in ZCHF |
| --- | ---: |
| Minter repayment claims `m` | +500 |
| Reserve `r` | +125 |
| Total supply `z` | +500 |
| Minter reserve `b` | +100 |
| Equity `e` | +25 |

Both sides increase by 625 ZCHF under the gross presentation.

### Challenge settlement

Assume a fully liquidated debt of 5,000 ZCHF, an unimpaired 20% assigned reserve of 1,000 ZCHF, and a winning bid of 4,500 ZCHF. Use a challenger reward of **2% of the bid**, as in the [pinned MintingHub source](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/minting/MintingHub.sol). This example describes that source's accounting, not an unidentified historical deployment.

The challenger receives 90 ZCHF. The remaining 4,410 ZCHF of bid proceeds leaves a 590 ZCHF shortfall against the 5,000 ZCHF burn. The full 1,000 ZCHF minter-reserve liability is released; after covering the shortfall, equity gains 410 ZCHF.

| Account | Change in ZCHF |
| --- | ---: |
| Minter repayment claims `m` | -5,000 |
| Reserve `r` | -590 |
| Total supply `z` | -5,000 |
| Minter reserve `b` | -1,000 |
| Equity `e` | +410 |

Both sides fall by 5,590 ZCHF. The equity gain is not the same as the minter-reserve release. Different reward bases, partial liquidations or impaired reserves change the calculation. Expiry sales follow a [separate settlement path](risks.md#missing-maturity-dates).

## Protection Mechanisms During Liquidation

Losses first use the affected position's minter reserve, then equity, then shared minter reserves. The last step can increase what other borrowers must return to settle their debt. This order describes loss allocation, not a guarantee that losses will fit within the available reserve.

## Equilibrium of Equity

The simplified model without savings expense, losses or different required returns gives:

```text
3e = z - x
```

Here `e` is equity, `z` is total ZCHF supply and `x` is bridge-backed issuance, measured in ZCHF under the model's one-to-one bridge assumption. It is not an enforced reserve requirement. The [economic model](pool-shares.md#equilibrium) explains how savings expense changes net equity income. FCS redemption prices and market quotes are separate from this relationship.
