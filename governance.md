---
description: Veto-based governance, token-specific qualification and cross-chain voting snapshots.
---

# ⚖️ Governance

## Overview

Frankencoin uses a veto process rather than a ballot on every proposal. For proposals with a waiting period:

1. A participant submits a proposal and pays any applicable fee.
2. Qualified holders can veto it during the relevant period.
3. If no veto succeeds, the change can be enacted under the module's rules.

The [Frankencoin thesis](https://www.zora.uzh.ch/id/eprint/259657/1/259657.pdf) describes the general model. [FCS](fcs.md) adds a governance layer over legacy FPS. The rules below distinguish these layers.

## Immutable Modularity

The core contracts use separate modules for collateralised minting, savings, stablecoin conversion and cross-chain transfers. Parameters can change under their governance rules; an approved new module does not rewrite an old contract. Minting modules can mint, move and burn ZCHF. The [application's governance page](https://app.frankencoin.com/governance) lists proposals and module state; there is no fixed count of active modules in this guide.

## Community Consensus

Proposals can be discussed in the [Frankencoin forum](https://github.com/Frankencoin-ZCHF/FrankenCoin/discussions) and [Telegram group](https://t.me/frankencoinzchf). Discussion does not replace the on-chain proposal or veto.

## Proposal Submission

[New collateral positions](positions/open.md) have their own proposal process. The following table describes the audited FCS governance modules, not every legacy deployment. Source: [audit pp7 and 10](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf#page=7).

| Module or action | Who can act | Timing and fee |
| --- | --- | --- |
| `MinterGovernance.suggestMinter` | Anyone may submit a minter application | Minimum 60-day application period and 1,200 ZCHF fee; up to 200 ZCHF replenishes the reward pool |
| `denyMinter` / `denyPosition` | Qualified FCS holders | Veto during the relevant proposal period |
| `denyUnannouncedMinter` | Anyone | Enforcement against a minter proposal bypassing the FCS announcement process; caller receives 10% of the reward pool |
| `InterestGovernance` | Qualified FCS holders on mainnet | Borrowing and savings rate proposals use parts per million and a seven-day grace period |
| `CCIPGovernance` | Qualified FCS holders | Configuration proposals follow CCIPAdmin rules; chain removal has a seven-day wait, but rate-limit changes apply immediately |

The 60 days and 1,200 ZCHF apply to **new minter applications**, not position creation or interest-rate changes. Sidechains receive rate updates from mainnet; they have no local interest-rate proposal path in this design.

`denyUnannouncedMinter` does not detect every bypass. A direct legacy FPS veto can leave a stale announcement, as described in audit finding #028. Rate-limit increases remain immediate in the audited version; finding #025 discusses a future delay, not an implemented one. These mechanisms still depend on participants monitoring proposals.

## Veto Process

### FCS qualification

Two checks apply to qualified FCS governance actions:

* The caller, including valid delegation, needs **more than 1% of internal FCS voting power**. Exactly 1% is not enough.
* The wrapper must satisfy the **underlying FPS quorum**, described in the audit as at least 2% of FPS voting power. This is a separate contract check, not 2% of FCS supply.

The underlying quorum and the [binding threshold](fcs.md#binding) are different. FCS governance can become usable before the wrapper is binding. A high internal voting share alone does not prove that the wrapper can exercise an underlying veto.

### Legacy FPS qualification

Legacy FPS uses the underlying 2% quorum and its delegation mechanism. Existing FPS governance has not been globally changed to a 1% rule. The applicable contract's quorum check determines eligibility, including fixed-point rounding at the boundary.

## Vote Accumulation

Legacy FPS votes grow with balance and average holding duration. For example, 10 FPS held for 730 days gives 7,300 FPS-days, compared with 7,000 FPS-days for 1,000 FPS held for seven days, before balance changes. A freshly borrowed balance carries no accumulated holding time. Legacy `kamikaze` sacrifices the caller's votes to destroy the same number of votes at other addresses, affecting their redemption age too.

FCS retains time-weighted votes but adds permissionless, explicit per-holder `cap()` at 365 days. It is not an automatic global cap. Direct FPS wrapping credits the holder's lost legacy votes; ZCHF entry and WFPS migration provide no immediate carried votes. `delegateVoteTo()` is transitive and non-subtractive; `attack()` is the FCS counterpart of legacy `kamikaze`. See [FCS voting](fcs.md#voting).

## Cross-Chain Governance

Legacy cross-chain governance sends an address's underlying votes and total votes from mainnet. The audited FCS system needs **two synchronisations** before a holder can act on a target chain:

1. Send the wrapper's underlying FPS votes through `GovernanceSender.pushVotes`.
2. Send the individual holders' FCS votes through `MainnetVotes.pushFPS2Votes` to `BridgedVotes` on the target chain.

Anyone can trigger these synchronisations and pay the CCIP fee, in the native asset or LINK. The destination needs both messages delivered and the relevant stored voting state. FCS tokens remain on mainnet in this design: **vote snapshots, not tokens, cross the bridge**.

Snapshots are not live mainnet balances. A selective sync can update total votes without updating every holder. A mainnet sync also overwrites local sidechain delegation for each included address. Old failed messages can later execute and overwrite a newer corrective sync; restoring state may require processing outstanding messages before sending fresh snapshots. CCIP delivery, message ordering and complete updates therefore affect destination qualification. [Audit pp7–10 and finding #006](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf#page=20).

## Exceptional Efficiency

The veto design avoids a full ballot for uncontested proposals. Its operation still depends on holders examining proposals and acting within the applicable period. The audit's trust model assumes no malicious majority of internal FCS votes after binding. See [governance failure modes](risks.md#fcs-mechanisms-and-dependencies).
