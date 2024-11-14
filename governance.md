---
description: >-
  Frankencoin's veto-based governance system pushes the boundaries of being
  scalable and decentralized at the same time.
---

# ⚖️ Governance

## Veto Power

Unlike other decentralized protocols, Frankencoin does not depend on lengthy voting processes. Instead, it's governance revolves around veto power. Anyone who has (alone or in coordination with others) at least 2% of the FPS tokens can obtain veto power over time.

More precisely, the voting power of an address is calculated by multiplying the FPS it holds with the average time these FPS have been held. It is possible to delegate voting power to others, and delegate delegated voting power further. Unlike in other systems, delegation does not remove your own voting power, so it is more like an "authorization to act on one's behalf" than a true delegation.

For example, if there is a group of seven FPS holders that delegate their power to each other in a circle, all seven FPS holders gain veto power if they collectively have at least 2% of the votes. (Note: the frontend currently ignores delegations when exercising veto rights. So to actually make use of the delegations, you have to do it directly on etherscan or so until this is implemented.)

## Proposal Submission

**Anyone can make proposals:** The Frankencoin governance system is inclusive, allowing any participant to submit proposals. This ensures diverse ideas and perspectives are considered, promoting a democratic process.

**Proposal Fee:** Making a proposal costs a fee of at least 1 000 ZCHF. This fee discourages frivolous proposals and ensures that only serious, well-considered proposals are submitted. Additionally, there might be a higher soft limit by convention, which is socially enforced by vetoing proposals that paid a fee below what is generally considered appropriate. This higher fee is not mandated by smart contracts but is a community norm.

## Proposal Duration

**Minimum durations for proposals:** The duration for which a proposal must remain open depends on its nature:

* **New minting modules:** Proposals for new minting modules must remain open for a minimum of 14 days unless vetoed. This period allows sufficient time for thorough discussion and evaluation by the community.
* **New collateral types:** Proposals for new types of collateral in the minting hub must remain open for at least 3 days. This shorter duration is still enough to ensure essential scrutiny and feedback.

**Recommendation for longer durations:** Proposers are encouraged to allow more time than the minimum required for community members to discuss and evaluate proposals thoroughly. This helps avoid premature vetoes due to rushed assessments and promotes a more comprehensive review process.

## Veto Power

**Eligibility for veto power:** Any participant with more than 2% of the total votes (q = 2% of the total votes V) can exercise veto power. This ensures that significant stakeholders have the ability to block proposals that may be harmful to the system.

**Voting calculation:** The number of votes a user has is calculated by multiplying their Frankencoin Pool Shares by the duration they have been holding these shares. This method rewards long-term commitment and prevents short-term manipulative actions. When shares are transferred to a new address, the votes are reset to zero, preventing vote trading or sudden shifts in voting power.

## Delegation of Votes

**Delegation mechanism:** Users can delegate their votes to other users, who can further delegate these votes. This system allows smaller shareholders to combine their votes, increasing their influence within the governance system. For instance, if Alice has 1% of the votes and delegates them to Bob, and Bob with 1.5% delegates to Charles, both Bob and Charles can exercise veto power. This layered delegation enables minority shareholders to form coalitions and assert their influence.

## Vote Cancellation

**Vote cancellation function:** Users can cancel each other's votes by sacrificing their own votes to reduce another user's votes by an equivalent amount. This function provides a mechanism to balance power within the voting system and prevent any single user from accumulating excessive influence. The specifics of this function are detailed in the governance smart contract but are not yet exposed in the frontend interface.

## Voting Efficiency

**Efficiency and outcomes:** This governance system achieves the same outcome as a traditional majority vote but with fewer interventions, making it more efficient. Ideally, there is a broad consensus on what constitutes an acceptable proposal, reducing the need for frequent vetoes.

**Community engagement:** To establish a consensus and increase communication, the [Frankencoin forum](https://github.com/Frankencoin-ZCHF/FrankenCoin/discussions) and the [Frankencoin Telegram channel](https://t.me/frankencoinzchf) are used. These platforms are vital for discussion, dissemination of information, and community engagement, helping align stakeholders' interests and opinions. Frankencoin is also[ on X](https://x.com/frankencoinzchf) (formerly known as Twitter).&#x20;
