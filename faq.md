---
description: Answers about ZCHF, FCS governance and shares, and the main protocol operations.
---

# ⁉️ Background FAQ

### What is this all about?

Frankencoin lets users mint ZCHF against collateral. Positions record the collateral and repayment obligation. Frankencoin Share Token (FCS) is the canonical governance and share token: holders participate in equity gains and losses and can veto proposals when qualified. The [overview](README.md) maps the components.

<a id="is-the-frankencoin-ecosystem-useful"></a>

### What can I use Frankencoin for?

Its main uses are payments, Swiss franc-denominated holdings and collateralised borrowing. Access and execution depend on the selected wallet, chain and application. You do not need FCS to use ZCHF or deposit it in savings.

### What is the main goal of the Frankencoin?

The system provides a collateral-backed token intended to track the Swiss franc, with on-chain minting and veto-based governance.

### How does Frankencoin differ from other stablecoins?

Collateral challenges and auctions replace an external price oracle. Challengers supply the same collateral asset, which makes its availability part of the mechanism. Auctions take time and depend on active participants; they do not prevent every pricing error. See [Challenges and Auctions](positions/auctions.md).

### What does FCS represent?

FCS combines participation in the system's equity with time-weighted voting. Net income increases shared equity capital; losses reduce it. Each FCS wraps one underlying FPS, but FCS has its own supply and voting records. The [share guide](pool-shares.md) explains ownership, acquisition and exits; the [mechanics reference](fcs.md) defines the contract rules.

<a id="what-role-do-governance-token-holders-play-in-the-frankencoin-ecosystem"></a>

### How do FCS holders take part in governance?

Qualified FCS holders can veto proposals. An action needs more than 1% of internal FCS voting power, including valid delegation, and the FCS contract meeting the underlying FPS quorum. Voting power depends on holding time and delegation, not token balance alone. [FCS governance](governance.md) explains proposals, qualification and cross-chain voting.

### What opportunities does Frankencoin offer for preserving purchasing power and investment?

ZCHF targets the Swiss franc's nominal value. It does not fix purchasing power or guarantee a market price. Savings pays a variable rate on ZCHF; FCS gives equity exposure, whose value can rise or fall. These are different economic positions.

### How can I acquire FCS?

Invest ZCHF through `deposit` or `mint`, buy existing FCS through a market route, or migrate an FPS or WFPS holding. ZCHF investment creates shares at the underlying curve's rate; it is not a one-to-one exchange. Only direct wrapping exchanges one FPS for one FCS. [Acquiring FCS](pool-shares.md#acquire-fcs) explains the routes, and [migration](fcs-migration.md) explains which votes carry over.

### When can I exit FCS?

FCS has no new personal 90-day redemption wait. ZCHF exits need the FCS contract to be binding and eligible to redeem its underlying FPS, then apply a discount. Unwrapping to FPS is available in either binding state when the holder meets the average-duration condition. A market sale is separate from either contract path. See [exit eligibility](fcs.md#exit-paths-and-eligibility).

### Can FCS be bridged to another chain?

The audited system keeps FCS tokens on Ethereum mainnet and sends voting snapshots to other chains. A destination governance action needs both the FCS contract's underlying FPS votes and the individual holder's FCS votes synchronised. This is separate from [bridging ZCHF](bridge-to-other-chains.md).

### Can savings always be withdrawn immediately?

It depends on the version. Legacy SavingsV2 has a ticks-based withdrawal lock. The referral-enabled source has an interest delay without that same withdrawal lock. [Savings](savings.md#contract-versions) separates the versions and explains public interest-collection methods and referral removal.

### Is the Frankencoin a security?

The existing [LEXR memorandum](https://github.com/Frankencoin-ZCHF/www/blob/main/documents/ZCHF_FPS_Memo.pdf) analyses ZCHF and legacy FPS under Swiss law. It is not an FCS classification, and the FPS2 code audit supplies no legal classification.

### Is Frankencoin political?

The design offers an alternative way to create collateral-backed money. Protocol operation is defined by contracts and governance rules, rather than a required political position among users.

### When obtaining Frankencoin against a collateral, is that really _borrowing_?

The contract mints new ZCHF rather than lending an existing deposit. The interface term “borrowing” describes the resulting repayment obligation; “minting” describes the token operation. Both refer here to a collateralised position.

## Underlying FPS and existing holdings

### What are Frankencoin Pool Share (FPS) tokens?

FPS remains the underlying equity token. The Equity curve prices FPS, and its supply and contract address remain FPS data. FCS wraps FPS one to one; WFPS is a separate older wrapper. The [underlying FPS reference](fps-reference.md) documents these identities and legacy rules.

### How can individuals invest in the FPS tokens of the Frankencoin ecosystem?

For the canonical share-token journey, use [FCS](pool-shares.md). Direct FPS investment uses the underlying Equity contract and issues FPS, not FCS. Existing FPS or WFPS holdings can move into FCS through [migration](fcs-migration.md). Historical bank-card, WFPS and Polygon instructions do not identify a current FCS route.

### How long is the locking period for FPS?

FPS is transferable, but direct redemption through Equity requires the holder's average holding duration to be at least 90 days. Transfers, new receipts and vote destruction can affect that duration. This is the underlying FPS rule, not a personal FCS lock. See [direct FPS redemption](fps-reference.md#direct-fps-redemption).

### Are Reserve Pool Shares securities?

The [existing memorandum](https://github.com/Frankencoin-ZCHF/www/blob/main/documents/ZCHF_FPS_Memo.pdf) discusses legacy FPS. FCS has separate mechanics; the documentation does not transfer that conclusion to FCS.
