---
description: Frankencoin (ZCHF), Frankencoin Share Token (FCS) and the structure of the system.
---

# 🧀 Overview

## Structure and Purpose

Frankencoin is a collateral-backed Swiss franc stablecoin system. This documentation explains minting, savings, equity and governance. The [application](https://app.frankencoin.com) provides transaction interfaces; the [research publication](https://app.frankencoin.com/thesis-frankencoin.pdf) examines the economic model. Documentation feedback belongs in the [Frankencoin Telegram group](https://t.me/frankencoinzchf); the source is the [GitBook repository](https://github.com/Frankencoin-ZCHF/gitbook).

<a id="frankencoin-zchf-and-frankencoin-pool-shares-fps"></a>

## Frankencoin (ZCHF) and Frankencoin Share Token (FCS)

| Token | Role |
| --- | --- |
| [Frankencoin (ZCHF)](https://etherscan.io/address/0xB58E61C3098d85632Df34EecfB899A1Ed80921cB) | Stablecoin intended to track the Swiss franc |
| [Frankencoin Share Token (FCS)](pool-shares.md) | Canonical governance and share token, representing participation in the system's equity |

FCS holders participate in [governance](governance.md) and share the economic gains and losses of the reserve's equity capital. Start with [investing and pool shares](pool-shares.md) for acquisition, voting and exits, then use the [FCS mechanics reference](fcs.md) for contract rules. Existing FPS and WFPS holders can use the [migration guide](fcs-migration.md).

FPS continues as the underlying equity token: each FCS wraps one FPS. The Equity contract holds capital and prices that underlying token. Its [Ethereum address](https://etherscan.io/address/0x1bA26788dfDe592fec8bcB0Eaff472a42BE341B2), supply and prices remain FPS identities, not FCS data. The mechanics reference identifies the audited `FPS2` version behind the FCS design.

ZCHF has no fixed redemption promise for Swiss francs. Collateral, reserves, borrowing costs and market activity support its exchange rate. Auctions test the value of collateral without an external price oracle. They can take days, so their response differs from oracle-triggered liquidations. [Positions](positions/README.md) describe the mechanism; [Risks](risks.md) describes its failure modes.

Net fees and liquidation results change equity capital; losses reduce it. FCS governance uses vetoes, with time-weighted votes rather than token balances alone. A qualified action needs more than 1% of internal FCS voting power and the FCS contract meeting the underlying FPS quorum.

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
| FCS and governance modules | Provide the share-token interface, time-weighted voting and ZCHF entry and exit paths |
| Underlying Equity / FPS | Hold equity capital, price the FPS backing and maintain the underlying votes used by FCS |
| Savings | Pay interest from the system to deposited ZCHF |
| Stablecoin-conversion bridges | Exchange ZCHF against a specified external stablecoin under a limit and expiry |
| Cross-chain bridges | Transfer ZCHF between supported chains; distinct modules send voting snapshots |

The [governance application](https://app.frankencoin.com/governance) lists proposed modules and their state. The early architecture used an XCHF bootstrap bridge; that historical example is not a statement about today's module count or bridge availability.
