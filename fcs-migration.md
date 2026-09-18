---
description: Entry and exit paths for FPS and WFPS holders in the audited FCS design.
---

# Migrating from FPS and WFPS

Use this guide to move an existing FPS or WFPS holding into Frankencoin Share Token (FCS), the canonical governance and share token. FCS wraps FPS one to one. Migration changes the token you hold and how you exercise governance; it does not replace the underlying Equity contract. For a new investment with ZCHF, start with [acquiring FCS](pool-shares.md#acquire-fcs). The [FCS reference](fcs.md#version-and-terminology) identifies the audited version and terminology used here.

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
3. If starting with WFPS, complete its unwrap route first and confirm receipt of FPS on Ethereum. Then approve the FCS contract for the intended FPS amount. For ZCHF entry, approve the required ZCHF amount instead. Approval alone does not migrate the holding.
4. Review the recipient, input, output and fees, then submit the chosen wrap or investment transaction. The reviewed `depositExpected` variant accepts a minimum share output.
5. After confirmation, read the received FCS balance and holder votes. Separately read the FCS contract's underlying FPS votes, binding state and redemption limits. A successful migration need not make a governance action or ZCHF exit immediately available.

These are contract operations; application interfaces expose their supported subset. The [API reference](api-docs/fcs.md) distinguishes indexed data from transactions.

### If you already hold FPS

Choose how much FPS to move rather than treating migration as an all-or-nothing account change. For example, wrapping 10 FPS issues 10 FCS and reduces your FPS balance by 10. It does not spend 10 ZCHF. For aged FPS, read the internal FCS votes credited by the transfer as well as the token balance. A partial wrap moves only the selected shares and the legacy votes lost on that transfer.

### If you hold WFPS

Complete the supported WFPS unwrap and any required route to Ethereum first. Confirm the underlying FPS token and amount actually received before approving the FCS wrapper. Wrap that received FPS balance, then confirm the FCS receipt. WFPS holding time is not carried into FCS: the intermediate FPS arrives without accumulated votes. The two token conversions are not a promise of immediate voting eligibility or ZCHF redemption.

## Two voting records

**Holder votes inside FCS** and **the wrapper's votes in FPS** are separate records. Wrapping aged FPS credits the holder's internal FCS votes, but the wrapper receives FPS as an ordinary FPS holder. Those credited internal votes do not give the wrapper the same accumulated legacy age.

The wrapper can therefore fail the underlying FPS quorum even when an FCS holder has more than 1% of internal votes. Legacy `kamikaze` can also reduce the wrapper's FPS votes below that quorum. Binding has a separate threshold: more than two thirds of underlying FPS votes.

Gradual migration by large legacy voters can retain a legacy veto backstop while the wrapper accumulates FPS voting power, as described in ChainSecurity's SC4. [Audit p11.](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf#page=11)

## Returning to FPS or exiting into ZCHF

* **Unwrap:** burn FCS and receive the same amount of FPS. In V3 this works in either binding state if the holder's FCS holding duration is at least the holder average. It does not preserve the returned FPS's former voting age.
* **Redeem or withdraw:** burn FCS for ZCHF. This needs binding plus the wrapper's own 90-day FPS eligibility, and applies the [redemption discount](fcs.md#prices-and-redemption-discount).
* **Sell:** transfer existing shares through a market route. Its liquidity and quote are separate from contract redemption.

Waiting 90 days as an individual FCS holder does not, by itself, enable redemption. `maxRedeem` and `maxWithdraw` reflect the wrapper-level gate; a preview can still return a value while the gate is closed.

For an unwrap, read your current FCS holding duration and the holder average, choose the shares to unwrap, then confirm the same number of FPS arrived after the transaction. For ZCHF proceeds, follow the [share guide's exit walkthrough](pool-shares.md#exit-an-fcs-holding) instead. That route needs a size-specific quote and the wrapper-level gate, not the unwrap duration check.

## Remaining outside the wrapper

FPS remains transferable and retains its legacy identity. While FCS is binding, anyone can call `shoot(target)` against an external FPS holder. The wrapper sacrifices its own FPS votes to destroy the target's accumulated FPS votes. The tokens remain in the holder's account, but their governance weight and legacy redemption eligibility change.

The report's p5 description gives the resulting 90-day redemption-age consequence; p9 uses broader language about permanent redemption rights. The reviewed code calls legacy `kamikaze`, not a token burn. Destroyed votes do not return, but holding time can accumulate again; repeated shooting can keep resetting it. [Audit pp5 and 9](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf#page=5); [reviewed `shoot` implementation](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/c1f229e3b26050367aafcb55da294342b4cae382/contracts/equity/fps2/FPS2.sol#L89-L97).
