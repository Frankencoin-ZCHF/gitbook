---
description: Contract mechanics for FCS, Frankencoin's canonical governance and share token.
---

<a id="frankencoin-share-token-fcs"></a>

# FCS Mechanics

Frankencoin Share Token (FCS) is the canonical governance and share token. It combines participation in the system's equity with time-weighted voting. The [investing and pool shares guide](pool-shares.md) explains the holder journey; this page defines the entry, voting and exit mechanics.

Each FCS wraps one underlying Frankencoin Pool Share (FPS). The Equity contract continues to hold the system's equity capital and to price FPS. FCS and FPS have separate supplies, voting records and contract interfaces.

## Version and terminology

This page describes the final V3 design in ChainSecurity's [14 July 2026 assessment](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf), at commit `c1f229e3b26050367aafcb55da294342b4cae382`. The report and reviewed code call the wrapper **FPS2** and the underlying FPS **FPS1**. This documentation uses **Frankencoin Share Token (FCS)** for the wrapper, retaining `FPS2` in source identifiers. The audited token's `name()` and `symbol()` still return `Frankencoin Pool Shares 2` and `FPS2`.

The contract mechanics below refer to that reviewed version. The [FCS API reference](api-docs/fcs.md) documents the API-reported deployment and fields separately. The continuing Ethereum [FPS contract](https://etherscan.io/address/0x1bA26788dfDe592fec8bcB0Eaff472a42BE341B2) remains FPS, including in price and supply data.

## Entry paths

| Path | What happens | Initial FCS votes |
| --- | --- | --- |
| Invest ZCHF | `deposit` fixes the ZCHF input; `mint` fixes the share output. The wrapper invests in FPS and issues FCS | No immediate votes from the new investment |
| Buy from another holder | A secondary-market trade transfers existing shares | A market purchase does not carry the seller's accumulated votes |
| Wrap existing FPS | `wrap(amount)` transfers FPS into the wrapper and issues the same number of shares | Credits the FPS votes lost by the sender on that transfer |
| Migrate WFPS | Unwrap WFPS into FPS, then wrap FPS into FCS | No carried votes from WFPS; the received FPS starts without accumulated votes |

The one-to-one ratio applies to **FPS wrapping**, not ZCHF investment. ZCHF is the ERC-4626 vault asset; FPS is the token backing each share. See the [migration guide](fcs-migration.md) for the distinction between holder votes and wrapper votes.

## Voting

Votes grow with the holder's balance and average holding duration. Transfers and other balance changes affect that duration. The audited design adds:

* `cap(holder)`: anyone can apply the 365-day holding-duration cap to a particular holder. It reduces that holder's votes and total internal votes together. It is **not automatic expiry** or a continuously applied cap on every account.
* `delegateVoteTo()`: delegation is non-subtractive and transitive. A holder retains their own ability to act, and an address counts only once in a delegation chain.
* `attack()`: a holder sacrifices their votes to destroy an equal number of other holders' votes. This changes voting records, not token balances.

Qualified [governance actions](governance.md#veto-process) require **more than 1% of internal FCS voting power**, including valid delegation. The wrapper must also meet the underlying FPS quorum, described in the audit as at least 2% of FPS voting power. These are different denominators and separate checks.

## Binding

The wrapper is **binding** when it controls **more than two thirds of underlying FPS votes**. This is not two thirds of FPS supply or internal FCS votes. The reviewed `isBinding()` checks `FPS1.relativeVotes(address(this)) * 3 > 2e18`.

Binding can reverse as voting balances change. It enables ZCHF redemption, subject to the wrapper's FPS holding duration, and enables `shoot(target)`. It does not itself prevent unwrapping in V3.

While binding, anyone can call `shoot(target)`. The wrapper spends an equal number of its own FPS votes to destroy the target's accumulated FPS votes through legacy `kamikaze`. The target keeps its FPS tokens, but loses those accumulated votes and must satisfy the legacy redemption-age condition again. Repeated calls can keep disrupting that recovery. This is not token confiscation. See [remaining outside the wrapper](fcs-migration.md#remaining-outside-the-wrapper).

## Exit paths and eligibility

| Operation | Output | Conditions in the reviewed design |
| --- | --- | --- |
| FCS `redeem` or `withdraw` | ZCHF, with the redemption discount | The wrapper must be binding and its own FPS holding duration must satisfy `FPS1.canRedeem(address(this))` |
| FCS `unwrap` | One FPS per share | The caller's FCS holding duration must be at least the average across FCS holders; allowed while binding or unbound |
| Transfer or secondary-market sale | Shares to another address, or the market's quoted asset | Separate from protocol redemption; proceeds depend on the available route and liquidity |

There is no new personal 90-day FCS redemption wait. The relevant 90-day check belongs to the wrapper as an FPS holder. Receiving FPS after an unwrap changes the recipient's FPS holding duration; FCS age is not transferred back as legacy votes. [Direct FPS redemption](fps-reference.md#direct-fps-redemption) then follows the underlying contract's rules.

The final V3 source resolves two inconsistent descriptions in the report: `unwrap` rejects durations **below** the holder average, so equality passes; `Equity.canRedeem` uses **at least** 90 days. See [FPS2.sol](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/c1f229e3b26050367aafcb55da294342b4cae382/contracts/equity/fps2/FPS2.sol#L68-L114) and [Equity.sol](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/c1f229e3b26050367aafcb55da294342b4cae382/contracts/equity/Equity.sol#L114-L119). The earlier p6 statement that unwrapping resumes only after unbinding is superseded by the V3 change on p8.

## Prices and redemption discount

The underlying FPS curve values the outstanding FPS at three times equity at the margin. This is a protocol reference valuation, not a secondary-market price or a fixed transaction quote.

| Value | Meaning |
| --- | --- |
| `ask()` | Underlying `FPS1.price()`, before the FPS fee and transaction-size effects |
| `bid()` | The same marginal price multiplied by the current discount, also before the FPS fee |
| `previewDeposit` / `previewMint` | Entry estimates using the underlying curve |
| `previewRedeem` / `previewWithdraw` | Exit estimates including the redemption discount |
| Market quote | A route-specific price for trading existing tokens |

For current share supply `S`, planned redemption `q` and weighted recent redemptions `R`, the discount **factor** is:

```text
d = ((S - q / 2) / (S + R))^4
ZCHF proceeds = underlying FPS redemption proceeds × d
```

All three inputs use share units. A factor of 1 means no extra discount; a lower factor reduces proceeds. The underlying FPS curve and fee still apply. For example, with `S = 1,000`, `q = 100` and `R = 0`, the factor is `0.81450625`. This is an illustrative calculation, not a quote.

The withheld ZCHF returns to Equity. Weighted recent redemptions decay to zero over seven days **absent further redemptions**. Continuing redemptions reset the decay anchor and can prolong recovery. New investment can offset the tracked redemption volume. A planned redemption still incurs its own size-dependent discount even when recent volume has decayed to zero. [Audit pp6, 25, finding #010.](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf#page=25)

### Withdraw and redeem are different

A single `withdraw`, which specifies ZCHF output, may burn at most **10% of total FCS supply**. This is not 10% of the holder's balance or a daily quota. The share-denominated `redeem` path has no such cap.

For sufficiently large redemptions, burning more shares can return **less ZCHF** because of the discount. Splitting a redemption changes fees, state and timing, so each transaction has its own quote. `redeemExpected` adds a minimum-proceeds condition; an ordinary `redeem` does not. Eligibility and available balance are separate from the preview calculation. [Audit pp11, 26.](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf#page=26)

## Accounting and ERC-4626 views

The final V3 definition is:

```text
totalAssets = ZCHF.equity() × FCS.totalSupply() / FPS1.totalSupply()
```

It measures the equity fraction attributable to the issued wrapper shares, in ZCHF units. It is not the wrapper's full FPS balance valued for liquidation, three times equity or immediately redeemable cash. Extra FPS donated to the wrapper does not increase the numerator's share supply.

`convertToAssets(shares)` uses the underlying marginal FPS price and excludes the exit discount, fees and curve slippage. It is not `previewRedeem`. `maxRedeem(owner)` is denominated in shares; `maxWithdraw(owner)` is denominated in ZCHF. Both return zero when redemptions are disabled.

The audit records remaining ERC-4626 deviations and rounding behaviour: `previewWithdraw` retains the 10%-of-supply cap, `withdraw` can return slightly more ZCHF than requested, and `previewMint(0)` can be non-zero. Integrations must handle these behaviours rather than assume exact standard rounding. [Audit findings #005, #021 and #011](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf#page=20); [reviewed accounting code](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/c1f229e3b26050367aafcb55da294342b4cae382/contracts/equity/fps2/FPS2MintRedeem.sol).

## Related pages

* [Migration from FPS and WFPS](fcs-migration.md)
* [Governance and cross-chain vote snapshots](governance.md)
* [Investing and equity economics](pool-shares.md)
* [Underlying FPS reference](fps-reference.md)
* [Concrete FCS failure modes](risks.md#fcs-mechanisms-and-dependencies)
* [FCS API reference](api-docs/fcs.md)
