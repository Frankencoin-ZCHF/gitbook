---
description: Cross-chain ZCHF transfers and the distinction from voting synchronisation.
icon: bridge
---

# Bridge to other Chains

A cross-chain route transfers ZCHF between supported networks. A stablecoin-conversion route exchanges ZCHF for another stablecoin; it is not the same operation. The [Frankencoin website](https://frankencoin.com) lists network and service references, and the [application](https://app.frankencoin.com) provides the available transfer interfaces.

## Network and token identity

Ethereum mainnet has chain ID **1**. Its ZCHF token is [0xB58E61C3098d85632Df34EecfB899A1Ed80921cB](https://etherscan.io/address/0xB58E61C3098d85632Df34EecfB899A1Ed80921cB). Destination instances have their own chain IDs and token addresses. The maintained [token information API](api-docs/ecosystem.md) supplies network-specific references; a matching token symbol alone does not identify a destination token or an available route.

The following destination references were returned by the public token information API on **18 September 2026**. They identify indexed ZCHF instances, not a guarantee of an active route between every pair.

| Chain | Chain ID | Indexed ZCHF address |
| --- | ---: | --- |
| Optimism | 10 | `0xd4dd9e2f021bb459d5a5f6c24c12fe09c5d45553` |
| Gnosis | 100 | `0xd4dd9e2f021bb459d5a5f6c24c12fe09c5d45553` |
| Polygon | 137 | `0xd4dd9e2f021bb459d5a5f6c24c12fe09c5d45553` |
| Sonic | 146 | `0xd4dd9e2f021bb459d5a5f6c24c12fe09c5d45553` |
| Base | 8453 | `0xd4dd9e2f021bb459d5a5f6c24c12fe09c5d45553` |
| Arbitrum One | 42161 | `0xd4dd9e2f021bb459d5a5f6c24c12fe09c5d45553` |
| Avalanche C-Chain | 43114 | `0xd4dd9e2f021bb459d5a5f6c24c12fe09c5d45553` |

Route availability also depends on bridge configuration, limits and current state, not just the existence of tokens on both chains.

## Transfer sequence

1. Select the source and destination networks in the transfer interface. Match the wallet's source chain, the source token address and the destination token reference.
2. Set the recipient on the destination chain and the ZCHF amount. Contract-wallet addresses can differ between chains.
3. Read the route quote: source transaction gas, bridge or message fee, destination amount and any execution limits. Destination gas may be needed for later use of the received tokens; receiving ZCHF does not itself supply that gas.
4. If required, approve the route's spender, then submit the transfer. Approval alone does not send the tokens across chains.
5. Record the source transaction and message identifier. A confirmed source transaction is not destination completion.
6. Track delivery in the route's status view or, for CCIP routes, [CCIP Explorer](https://ccip.chain.link/). Destination completion means the destination transaction succeeded and the expected token balance arrived.

Rate limits, message execution errors and chain conditions can delay delivery. An unresolved source transfer should be traced by its identifier rather than assumed absent and sent again. The [bridge dependencies](risks.md#ccip-and-blockchain-hacks) describe how a compromised chain or message path affects the system.

## FCS votes are not bridged tokens

[FCS](pool-shares.md) is the governance and share token; the audited design keeps those shares on mainnet. To take part in governance on another chain, synchronise the FCS contract's underlying FPS votes and the individual holders' FCS votes. [Cross-chain governance](governance.md#cross-chain-governance) guides both steps. A voting snapshot is not a spendable FCS balance on the destination chain, and the ZCHF transfer sequence above does not migrate FCS.
