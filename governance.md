---
description: FCS veto-based governance, voting power and cross-chain voting snapshots.
---

<a id="governance"></a>

# ⚖️ FCS Governance

## Overview

[Frankencoin Share Token (FCS)](pool-shares.md) is Frankencoin's canonical governance token. Holders build time-weighted voting power and can delegate it to other participants. Frankencoin uses a veto process rather than a ballot on every proposal. For proposals with a waiting period:

1. A participant submits a proposal and pays any applicable fee.
2. Qualified holders can veto it during the relevant period.
3. If no veto succeeds, the change can be enacted under the module's rules.

The [Frankencoin thesis](https://www.zora.uzh.ch/id/eprint/259657/1/259657.pdf) describes the general model. FCS is the holder-facing governance interface. Its contract exercises underlying FPS votes, so qualification depends on both the holder's FCS voting power and the contract's underlying quorum.

## Taking part with FCS

1. **Build or delegate votes.** Acquire FCS through the [share guide](pool-shares.md#usage), then read your voting power. New tokens do not necessarily bring immediate votes. Use `delegateVoteTo()` to delegate to another participant; you retain your own ability to act.
2. **Choose a proposal to examine.** The [governance application](https://app.frankencoin.com/governance) lists proposals and their state. Read the proposed module or parameter, chain, proposer and deadline. The [notification bot](telegram-api-bot.md) can report indexed events, but does not cast vetoes.
3. **Check qualification for the action.** Read your internal FCS voting power, any valid delegation and the FCS contract's underlying quorum. On another chain, first complete the [two vote synchronisations](#cross-chain-governance). Token balance alone is not an eligibility check.
4. **Submit and confirm.** Use the relevant module's proposal or veto operation while its timing conditions permit. After the transaction confirms, read the proposal's on-chain state. A discussion message, API response or wallet approval is not a proposal or veto transaction.

The module table below identifies the available actions. You do not need FCS votes to submit a new minter application, but qualified actions such as position vetoes and rate proposals require them.

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

## Vote Accumulation

FCS votes grow with balance and average holding duration. An incoming balance does not carry the sender's holding time. Anyone can apply `cap()` to limit a particular holder's recorded duration to 365 days; this is not an automatic global cap. Direct FPS wrapping credits the holder's lost legacy votes, while ZCHF entry and WFPS migration provide no immediate carried votes.

`delegateVoteTo()` is transitive and non-subtractive. `attack()` lets a holder sacrifice votes to destroy an equal number of another holder's votes without changing token balances. The [FCS voting reference](fcs.md#voting) defines these mechanisms.

## Cross-Chain Governance

FCS holders can exercise governance on other chains without moving their shares off mainnet. The audited system needs **two synchronisations** before a holder can act on a target chain:

1. Send the wrapper's underlying FPS votes through `GovernanceSender.pushVotes`.
2. Send the individual holders' FCS votes through `MainnetVotes.pushFPS2Votes` to `BridgedVotes` on the target chain.

Select the target chain and holders to update, obtain the CCIP fee and submit each required synchronisation. Anyone can trigger these calls and pay the fee in the native asset or LINK. Track both messages to delivery and read the destination voting state before submitting a governance action. FCS tokens remain on mainnet in this design: **vote snapshots, not tokens, cross the bridge**.

Snapshots are not live mainnet balances. A selective sync can update total votes without updating every holder. A mainnet sync also overwrites local sidechain delegation for each included address. Old failed messages can later execute and overwrite a newer corrective sync; restoring state may require processing outstanding messages before sending fresh snapshots. CCIP delivery, message ordering and complete updates therefore affect destination qualification. [Audit pp7–10 and finding #006, pp22–23](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf#page=22).

<a id="exceptional-efficiency"></a>

## Proposal monitoring

The veto design avoids a full ballot for uncontested proposals. Its operation still depends on holders examining proposals and acting within the applicable period. The audit's trust model assumes no malicious majority of internal FCS votes after binding. See [governance failure modes](risks.md#fcs-mechanisms-and-dependencies).

### Legacy FPS qualification

FPS still maintains the underlying votes and its own quorum; FCS does not globally replace that contract's rules. Direct FPS voting and the legacy holding-time example are documented in the [underlying FPS reference](fps-reference.md#legacy-votes-and-quorum). Existing holders can follow the [migration guide](fcs-migration.md) to take part through FCS.
