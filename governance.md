---
description: >-
  Frankencoin's veto-based governance system pushes the boundaries of being
  scalable and decentralized at the same time.
---

# ⚖️ Governance

## Overview

Unlike other decentralized protocols, Frankencoin does not depend on lengthy voting processes. Instead, it's governance revolves around a light-weith veto process. It is formally defined and analyzed on [pages 43 and following of the Frankencoin thesis](https://www.zora.uzh.ch/id/eprint/259657/1/259657.pdf).

Passing a change takes three steps:

1. Someone makes a proposal, paying a proposal fee
2. Frankencoin Pool Share holders are given time to veto the proposal
3. If no veto was cast, the proposal can be enacted by anyone

## Immutable Modularity

All contracts in the Frankencoin system are immutable. Once deployed, they cannot be changed anymore. However, many contracts have adjustable parameters like the savings rate. Also, the main Frankencoin contract offers the possibility to propose new minting modules. These are smart contracts that can arbitrary mint, move, and burn Frankencoins - making them very powerful and allowing for a wide range of potential extensions. The ability to mint Frankencoins against a collateral is based on such an extension. And so is the savings module and the contracts that allow for sending Frankencoins to other blockchains. The [governance page](https://app.frankencoin.com/governance) lists all minting modules ever proposed.

## Community Consensus&#x20;

The first step before making a proposal is to reach out to the community to sense whether there would be resistance against it. Ideally, there is a broad consensus on what constitutes an acceptable proposal, reducing the need for frequent vetoes. To establish a consensus and increase communication, the [Frankencoin forum](https://github.com/Frankencoin-ZCHF/FrankenCoin/discussions) and the [Frankencoin Telegram channel](https://t.me/frankencoinzchf) can be used. These platforms are vital for discussion, dissemination of information, and community engagement, helping align stakeholders' interests and opinions.

## Proposal Submission

There are different types of proposals that can be submitted in different places. For example, there is a [purpose-built page](https://app.frankencoin.com/mint/create) to propose new types of collateral. Typically, making a proposal is open to anyone. Making a proposal typically costs a fee and comes with a specific veto period. Both can be configured to be higher than the minimum. A longer than minimal proposal period might make sense when the proposal is complex and the community is expected to take additional time to reach a consensus.

## Veto Process

Any participant with more than 2% of the total votes has veto power. A veto can be exercised in a single transaction and has the immediate effect of cancelling the relevant proposal. The system keeps the proposal fee regardless of whether the proposal passes or is denied.

If one address alone does not have a sufficient number of votes, other addresses can help that address by delegating their votes. So if a user has multiple addresses or if multiple users want to cast a veto in collaboration, they can use delegation to bundle their votes, as described in the next section.

## Vote Accumulation

The number of votes of an address is calculated by multiplying their Frankencoin Pool Shares by the duration they have been holding them. This method rewards long-term commitment and prevents short-term manipulative actions. For example someone borroing a lot of FPS in a flash loan has zero votes, because the holding duration is zero. Or someone with 10 FPS that they held onto for two years has more votes than someone with 1000 FPS that they held for a week.

For example, if there is a group of seven FPS holders that delegate their power to each other in a circle, all seven FPS holders gain veto power if they collectively have at least 2% of the votes. Note that the frontend currently ignores delegations when casting a veto. So to actually make use of the delegations, a manual transaction with the help of [etherscan](https://etherscan.io/) or another suitable tool is required for now.

As 2% is quite a low barrier to be able to block all new proposals, there is a mechanism to protect the system against griefing. An altruistic system participant can use the built-in kamikaze function of the FPS contract to sacrifice own votes in order to cancel the same number of votes of one or more target addresses. Doing so reduces the holding duration counter and therefore can also be used to temporarily prevent a target address from redeeming Frankencoin Pool Shares.

## Cross-Chain Governance&#x20;

Frankencoins are present on a multiture of blockchains, including [Arbitrum](https://arbiscan.io/address/0xD4dD9e2F021BB459D5A5f6c24C12fE09c5D45553?__cf_chl_rt_tk=M23HkA3rE6ZYd.t9KezhFDa.1V0Yw76Ouj4TESenpIQ-1753369514-1.0.1.1-QrlEuenjDfRRGpM3hxOrbypU2Bxy6js0n_YKXxXTsu4), [Base](https://basescan.org/address/0xD4dD9e2F021BB459D5A5f6c24C12fE09c5D45553), and [Gnosis](https://gnosisscan.io/address/0xD4dD9e2F021BB459D5A5f6c24C12fE09c5D45553?__cf_chl_rt_tk=gWbmKrrEbWHR8WcoI9fXYBOmIq7R_CMfWfMVKMIPNf8-1753369529-1.0.1.1-Q.0ND5Bbww60RT.UAZWFMcUM3bO2GYIkt7UCcalvxlg). However, [Frankencoin Pool Shares](https://etherscan.io/address/0x1bA26788dfDe592fec8bcB0Eaff472a42BE341B2) and their vote accumulation mechanism is only present on Ethereum mainnet. Nonetheless, there is a very efficient and light-weight way to mirror the proposal process on all the other chains. This is done by having a function a sync function that sends the currently accumulated number of votes for a specific address to the other chain, together with the current total number of votes. This allows a user to prove that they have veto power on mainnet. Once the proof has been made, they can freely use their veto power on the other chain. Veto power is lost again once they lose it on mainnet and some bothers synchronizing their vote count to the other chain. Anyone can synchronize the votes of any address.

## Exceptional Efficiency

Asymptotically, the Frankencoin governance system achieves the same outcome as a traditional majority vote, but much more efficiently. In the ideal case, if every participant is rational, no veto needs to be ever cast, as no one is stupid enough to make a proposal that will be declined. with fewer interventions, making it more efficient. And even if there is a bad proposal every now and then: the effort to cast a veto is much lower than the effort to hold a fully fledged on-chain vote. This makes Frankencoin one of the most efficient decentralized governance system ever conceived.
