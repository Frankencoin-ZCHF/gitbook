---
description: Answers about ZCHF, FPS, FCS and the main protocol operations.
---

# ⁉️ Background FAQ

### What is this all about?

Frankencoin lets users mint ZCHF against collateral. Positions record the collateral and repayment obligation. The reserve absorbs losses under defined rules; equity holders receive net system income and bear residual losses. The [overview](README.md) maps the components.

### Is the Frankencoin ecosystem useful?

Its main uses are payments, Swiss franc-denominated holdings and collateralised borrowing. Access and execution depend on the selected wallet, chain and application. These uses do not require every user to hold a governance token.

### What is the main goal of the Frankencoin?

The system provides a collateral-backed token intended to track the Swiss franc, with on-chain minting and veto-based governance.

### How does Frankencoin differ from other stablecoins?

Collateral challenges and auctions replace an external price oracle. Challengers supply the same collateral asset, which makes its availability part of the mechanism. Auctions take time and depend on active participants; they do not prevent every pricing error. See [Challenges and Auctions](positions/auctions.md).

### What are Frankencoin Pool Share (FPS) tokens?

FPS is the underlying equity and legacy governance token. Its price follows the Equity curve; its supply and contract address remain FPS data. [FCS](fcs.md), the Frankencoin Share Token, wraps FPS one to one and adds different governance and redemption rules. WFPS is a separate older wrapper. See [legacy FPS](pool-shares.md#reserve-pool-shares) and [migration](fcs-migration.md).

### What role do governance token holders play in the Frankencoin ecosystem?

Holders can veto proposals when they meet the applicable quorum. Legacy FPS uses the underlying 2% rule. Qualified FCS actions need more than 1% of internal FCS votes and the wrapper meeting the underlying FPS quorum. Voting power depends on holding time and delegation, not token balance alone. [Governance](governance.md) explains both layers.

### What opportunities does Frankencoin offer for preserving purchasing power and investment?

ZCHF targets the Swiss franc's nominal value. It does not fix purchasing power or guarantee a market price. Savings pays a variable rate; FPS and FCS give equity exposure, whose value can rise or fall. These are different economic positions.

### How can individuals invest in the FPS tokens of the Frankencoin ecosystem?

First identify the intended asset: FPS, WFPS or FCS. The [equity application](https://app.frankencoin.com/equity) and market venues offer routes that can differ by chain and token. A market trade transfers existing tokens; a protocol investment creates shares against ZCHF; wrapping exchanges the specified underlying token for wrapper shares.

Historical bank-card, WFPS and Polygon instructions are not a current FCS route list. [FCS entry paths](fcs.md#entry-paths) describe direct FPS wrapping and ZCHF investment. [Migration](fcs-migration.md) explains why direct FPS wrapping carries votes but WFPS migration does not.

### How long is the locking period for FPS?

FPS is transferable, but redemption through Equity requires the holder's average holding duration to be at least 90 days. Transfers, new receipts and vote destruction can affect that duration. Secondary-market sales depend on the market rather than the protocol redemption gate.

FCS does not impose a new personal 90-day redemption wait. ZCHF exits need the wrapper to be binding and its own FPS holding-duration condition to pass, then apply a discount. Unwrapping to FPS is a different operation, available in either binding state when the holder meets the average-duration condition. See [exit eligibility](fcs.md#exit-paths-and-eligibility).

### Can FCS be bridged to another chain?

The audited system keeps FCS tokens on Ethereum mainnet and sends voting snapshots to other chains. A destination governance action needs both the wrapper's FPS votes and the individual holder's FCS votes synchronised. This is separate from [bridging ZCHF](bridge-to-other-chains.md).

### Can savings always be withdrawn immediately?

It depends on the version. Legacy SavingsV2 has a ticks-based withdrawal lock. The referral-enabled source has an interest delay without that same withdrawal lock. [Savings](savings.md#contract-versions) separates the versions and explains public interest-collection methods and referral removal.

### Is the Frankencoin a security?

The existing [LEXR memorandum](https://github.com/Frankencoin-ZCHF/www/blob/main/documents/ZCHF_FPS_Memo.pdf) analyses ZCHF and legacy FPS under Swiss law. It is not an FCS classification, and the FPS2 code audit supplies no legal classification.

### Is Frankencoin political?

The design offers an alternative way to create collateral-backed money. Protocol operation is defined by contracts and governance rules, rather than a required political position among users.

### When obtaining Frankencoin against a collateral, is that really _borrowing_?

The contract mints new ZCHF rather than lending an existing deposit. The interface term “borrowing” describes the resulting repayment obligation; “minting” describes the token operation. Both refer here to a collateralised position.

### Are Reserve Pool Shares securities?

The [existing memorandum](https://github.com/Frankencoin-ZCHF/www/blob/main/documents/ZCHF_FPS_Memo.pdf) discusses legacy FPS. FCS has separate wrapper mechanics; the documentation does not transfer that conclusion to FCS.
