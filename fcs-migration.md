---
description: Entry and exit paths for FPS and WFPS holders in the audited FCS design.
---

# Migrating from FPS and WFPS

FCS wraps FPS one to one. Migration changes which token an address holds and how it exercises governance; it does not replace the underlying Equity contract. The [FCS reference](fcs.md#version-and-terminology) identifies the audited version and terminology used here.

## Identify the starting token

| Starting balance | Route into FCS | Voting effect |
| --- | --- | --- |
| FPS on Ethereum | Approve the selected wrapper for the amount, then call `wrap(amount)` | FCS credits the FPS votes the sender loses on transfer |
| WFPS | Obtain underlying FPS through the WFPS unwrap route, then wrap those FPS into FCS | Unwrapped FPS has no accumulated votes to carry over from WFPS |
| ZCHF | Use ERC-4626 `deposit` or `mint` | The investment buys underlying FPS; the new FCS starts without immediate votes |
| Another asset | Trade for the intended token through a quoted market route | This is a market trade, not a protocol migration |

WFPS on another chain first needs a supported route to the underlying Ethereum FPS. A matching ticker is not a chain or contract identifier. The audited FCS system does not bridge FCS tokens; it sends [voting snapshots](governance.md#cross-chain-governance) to other chains.

## Transaction sequence

1. Identify the chain, starting token, wrapper address and underlying FPS address. The audited `FPS1` and `asset()` views identify the backing FPS and ZCHF asset respectively.
2. Choose the operation by input: `wrap` for FPS, `deposit` for a fixed ZCHF input, or `mint` for a fixed share output. For ZCHF entry, read the corresponding preview rather than dividing by a displayed marginal price.
3. Review the allowance, recipient, amount and quoted output. The reviewed `depositExpected` variant accepts a minimum share output.
4. After confirmation, read the received share balance and holder votes. Separately read the wrapper's underlying FPS votes, binding state and redemption limits.

These are contract operations; application interfaces expose their supported subset. The [API reference](api-docs/fcs.md) distinguishes indexed data from transactions.

## Two voting records

**Holder votes inside FCS** and **the wrapper's votes in FPS** are separate records. Wrapping aged FPS credits the holder's internal FCS votes, but the wrapper receives FPS as an ordinary FPS holder. Those credited internal votes do not give the wrapper the same accumulated legacy age.

The wrapper can therefore fail the underlying FPS quorum even when an FCS holder has more than 1% of internal votes. Legacy `kamikaze` can also reduce the wrapper's FPS votes below that quorum. Binding has a separate threshold: more than two thirds of underlying FPS votes.

Gradual migration by large legacy voters can retain a legacy veto backstop while the wrapper accumulates FPS voting power, as described in ChainSecurity's SC4. [Audit p11.](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf#page=11)

## Returning to FPS or exiting into ZCHF

* **Unwrap:** burn FCS and receive the same amount of FPS. In V3 this works in either binding state if the holder's FCS holding duration is at least the holder average. It does not preserve the returned FPS's former voting age.
* **Redeem or withdraw:** burn FCS for ZCHF. This needs binding plus the wrapper's own 90-day FPS eligibility, and applies the [redemption discount](fcs.md#prices-and-redemption-discount).
* **Sell:** transfer existing shares through a market route. Its liquidity and quote are separate from contract redemption.

Waiting 90 days as an individual FCS holder does not, by itself, enable redemption. `maxRedeem` and `maxWithdraw` reflect the wrapper-level gate; a preview can still return a value while the gate is closed.

## Remaining outside the wrapper

FPS remains transferable and retains its legacy identity. While FCS is binding, anyone can call `shoot(target)` against an external FPS holder. The wrapper sacrifices its own FPS votes to destroy the target's accumulated FPS votes. The tokens remain in the holder's account, but their governance weight and legacy redemption eligibility change.

The report's p5 description gives the resulting 90-day redemption-age consequence; p9 uses broader language about permanent redemption rights. The reviewed code calls legacy `kamikaze`, not a token burn. Destroyed votes do not return, but holding time can accumulate again; repeated shooting can keep resetting it. [Audit pp5 and 9](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf#page=5); [reviewed `shoot` implementation](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/c1f229e3b26050367aafcb55da294342b4cae382/contracts/equity/fps2/FPS2.sol#L89-L97).
