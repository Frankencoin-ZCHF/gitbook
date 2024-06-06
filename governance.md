---
description: >-
  A guide for reserve pool share holders on how they should use their veto
  power.
---

# ⚖️ Governance

The governance system is subject to the following rules:

#### Proposal Submission

**Anyone can make proposals:** The Frankencoin governance system is inclusive, allowing any participant to submit proposals. This ensures diverse ideas and perspectives are considered, promoting a democratic process.

**Proposal Fee:** Making a proposal costs a fee of at least 1000 ZCHF. This fee discourages frivolous proposals and ensures that only serious, well-considered proposals are submitted. Additionally, there might be a higher soft limit by convention, which is socially enforced by vetoing proposals that paid a fee below what is generally considered appropriate. This higher fee is not mandated by smart contracts but is a community norm.

#### Proposal Duration

**Minimum Durations for Proposals:** The duration for which a proposal must remain open depends on its nature:

* **New Minting Modules:** Proposals for new minting modules must remain open for a minimum of 14 days unless vetoed. This period allows sufficient time for thorough discussion and evaluation by the community.
* **New Collateral Types:** Proposals for new types of collateral in the minting hub must remain open for at least 3 days. This shorter duration is still enough to ensure essential scrutiny and feedback.

**Recommendation for Longer Durations:** Proposers are encouraged to allow more time than the minimum required for community members to discuss and evaluate proposals thoroughly. This helps avoid premature vetoes due to rushed assessments and promotes a more comprehensive review process.

#### Veto Power

**Eligibility for Veto Power:** Any participant with more than 2% of the total votes (q = 2% of the total votes V) can exercise veto power. This ensures that significant stakeholders have the ability to block proposals that may be harmful to the system.

**Voting Calculation:** The number of votes a user has is calculated by multiplying their Frankencoin Pool Shares by the duration they have held these shares. This method rewards long-term commitment and prevents short-term manipulative actions. When shares are transferred to a new address, the associated votes are reset to zero, preventing vote trading or sudden shifts in voting power.

#### Delegation of Votes

**Delegation Mechanism:** Users can delegate their votes to other users, who can further delegate these votes. This system allows smaller shareholders to combine their votes, increasing their influence within the governance system. For instance, if Alice has 1% of the votes and delegates them to Bob, and Bob with 1.5% delegates to Charles, both Bob and Charles can exercise veto power. This layered delegation enables minority shareholders to form coalitions and assert their influence.

#### Vote Cancellation

**Vote Cancellation Function:** Users can cancel each other's votes by sacrificing their own votes to reduce another user's votes by an equivalent amount. This function provides a mechanism to balance power within the voting system and prevent any single user from accumulating excessive influence. The specifics of this function are detailed in the governance smart contract but are not yet exposed in the frontend interface.

#### Voting Efficiency

**Efficiency and Outcomes:** This governance system achieves the same outcome as a traditional majority vote but with fewer interventions, making it more efficient. Ideally, there is a broad consensus on what constitutes an acceptable proposal, reducing the need for frequent vetoes.

**Community Engagement:** To foster consensus and facilitate communication, the [Frankencoin forum](https://github.com/Frankencoin-ZCHF/FrankenCoin/discussions) and the [Frankencoin Telegram channel](https://t.me/frankencoinzchf) are used. These platforms are vital for discussion, dissemination of information, and community engagement, helping align stakeholders' interests and opinions.

By following these detailed rules, the Frankencoin governance system ensures a fair, inclusive, and efficient process for making important decisions, encouraging active participation and long-term commitment from its community members.
