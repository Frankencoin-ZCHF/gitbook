---
description: Frankencoin, equity tokens and the structure of the system.
---

# 🧀 Overview

## Structure and Purpose

Frankencoin is a collateral-backed Swiss franc stablecoin system. This documentation explains minting, savings, equity and governance. The [application](https://app.frankencoin.com) provides transaction interfaces; the [research publication](https://app.frankencoin.com/thesis-frankencoin.pdf) examines the economic model. Documentation feedback belongs in the [Frankencoin Telegram group](https://t.me/frankencoinzchf); the source is the [GitBook repository](https://github.com/Frankencoin-ZCHF/gitbook).

## Frankencoin (ZCHF) and Frankencoin Pool Shares (FPS)

| Token | Role |
| --- | --- |
| [Frankencoin (ZCHF)](https://etherscan.io/address/0xB58E61C3098d85632Df34EecfB899A1Ed80921cB) | Stablecoin intended to track the Swiss franc |
| [Frankencoin Pool Shares (FPS)](https://etherscan.io/address/0x1bA26788dfDe592fec8bcB0Eaff472a42BE341B2) | Underlying equity and legacy governance token |
| [Frankencoin Share Token (FCS)](fcs.md) | One-to-one FPS wrapper with revised governance and redemption mechanics |

The linked ZCHF and FPS addresses are Ethereum instances. The FCS reference describes the audited `FPS2` design; it does not relabel FPS addresses, prices or supply as FCS. Existing FPS and WFPS holders can use the [migration guide](fcs-migration.md) to compare their entry and exit paths.

ZCHF has no fixed redemption promise for Swiss francs. Collateral, reserves, borrowing costs and market activity support its exchange rate. Auctions test the value of collateral without an external price oracle. They can take days, so their response differs from oracle-triggered liquidations. [Positions](positions/README.md) describe the mechanism; [Risks](risks.md) describes its failure modes.

Equity holders receive the economic benefit of net fees and liquidation results, and bear residual losses. [Governance](governance.md) uses vetoes. Legacy FPS has its underlying 2% quorum; qualified FCS actions require more than 1% of internal FCS votes and the wrapper meeting the underlying FPS quorum.

## Use Cases

### Payments

ZCHF can be transferred between addresses or used through payment services. The [Frankencoin website](https://frankencoin.com) lists services. On another chain, the token address, network and transfer route identify the asset; see [cross-chain transfers](bridge-to-other-chains.md).

### Store of Wealth

ZCHF provides Swiss franc-denominated exposure on-chain. Its market price can diverge from one Swiss franc. [Savings](savings.md) pays a governance-set rate to deposited ZCHF, with terms that depend on the savings contract version.

### Borrowing / Seignorage

Users can mint ZCHF against collateral in a position. The position records collateral and an amount to repay. A mint deducts the applicable up-front fee and retains a minter reserve, so the wallet receives less than the gross minted amount. The [opening](positions/open.md), [cloning](positions/clone.md) and [adjustment](positions/adjust.md) guides explain the terms.

## Technical Architecture

| Component | Function |
| --- | --- |
| ZCHF token and approved minting modules | Create, move and burn ZCHF under each module's rules |
| MintingHub and positions | Manage collateral-backed minting, challenges and settlement |
| Equity / FPS | Hold equity capital, price FPS and maintain underlying governance votes |
| FCS wrapper and governance modules | Wrap FPS and apply the versioned FCS voting, binding and redemption rules |
| Savings | Pay interest from the system to deposited ZCHF |
| Stablecoin-conversion bridges | Exchange ZCHF against a specified external stablecoin under a limit and expiry |
| Cross-chain bridges | Transfer ZCHF between supported chains; distinct modules send voting snapshots |

The [governance application](https://app.frankencoin.com/governance) lists proposed modules and their state. The early architecture used an XCHF bootstrap bridge; that historical example is not a statement about today's module count or bridge availability.
