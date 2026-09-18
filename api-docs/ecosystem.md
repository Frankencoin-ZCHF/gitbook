# Ecosystem API

Use the Ecosystem API to build a ZCHF overview, discover which collateral tokens appear in lending positions and follow minter proposals. It brings token metadata, chain-specific supply and reserve data into one place.

For Frankencoin's canonical governance and share token, use the [FCS controller](fcs.md). The FPS fields here describe its underlying equity token. See [API conventions](README.md) for units.

## Frankencoin and legacy FPS

| GET path | Response |
| --- | --- |
| `/ecosystem/frankencoin/info` | `erc20`, `chains`, `token`, `fps`, `tvl` objects |
| `/ecosystem/frankencoin/keyvalues` | Metric-ID map of `{id, value, amount}`; interpret `amount` by metric, since it can be a count or a raw quantity |
| `/ecosystem/frankencoin/totalsupply` | ZCHF supply summary, not FCS supply |
| `/ecosystem/coinmarketcap/totalsupply` | Supply route for the market-data integration |
| `/ecosystem/fps/info` | Legacy FPS `erc20`, `chains`, `token`, `earnings`, `reserve` objects |

Frankencoin info has `token.usd` (USD per ZCHF), `token.supply` (scaled ZCHF), chain-specific `supply` values, and `tvl.usd`/`tvl.chf`. The embedded `fps` object remains legacy FPS.

FPS info has `token.price` (ZCHF per FPS), `token.totalSupply` (FPS), `token.marketCap` (ZCHF), `earnings.profit`/`loss` and `reserve.balance`/`equity`/`minter` (ZCHF). These are already scaled JSON numbers. It does not supply `circulatingSupply`, `priceHistory` or `mintingCapacity`. Use the [prices history routes](prices.md) for available historical observations; minting eligibility requires the relevant contract state.

### Build a token overview

1. Request `GET /ecosystem/frankencoin/info` and display ZCHF supply, USD price and TVL with their stated units.
2. Iterate `chains` to show each reported chain's token address and supply. Retain chain ID with each address when linking to an explorer.
3. Request `GET /fcs/info` for FCS supply and reference prices. Use `GET /ecosystem/fps/info` only for the underlying FPS and reserve panel.
4. Add [analytics](analytics.md) for financial history rather than treating the current overview as a historical series.

## Minter proposals

A minter proposal requests authorisation for a contract to mint ZCHF. Use the proposal list to show who proposed a minter, its application period and any recorded denial. The chain-specific route narrows that view to one network; `chainId` is an EIP-155 chain ID, such as `1` for Ethereum.

- `GET /ecosystem/minter/list`
- `GET /ecosystem/minter/list/:chainId`

The response is `{num, list}`. A proposal contains `chainId`, `minter`, `suggestor`, `txHash`, `applicationPeriod`, `applicationFee`, `applyMessage` and `applyDate`, plus nullable denial fields `denyMessage`, `denyDate`, `denyTxHash` and `vetor` (the API's spelling).

`applyDate` and `denyDate` are Unix seconds; `applicationPeriod` is a duration in seconds and `applicationFee` is a raw ZCHF string with 18 decimals. Show `applyMessage` as the proposal description and, where present, `denyMessage` as the denial reason. The list includes denied proposals and has no `active/deprecated/proposed` enum or version field. A null denial field does not establish current authorisation: check the selected chain's contract state before offering a minting action.

## Collateral catalogue

| GET path | Purpose |
| --- | --- |
| `/ecosystem/collateral/list` | `{num, list}` of token metadata |
| `/ecosystem/collateral/mapping` | Address-keyed metadata |
| `/ecosystem/collateral/positions` | Positions grouped by collateral |
| `/ecosystem/collateral/positions/details` | Grouped position details |
| `/ecosystem/collateral/stats` | Collateral statistics |

Metadata includes `chainId`, `address`, `name`, `symbol` and `decimals`. Catalogue membership records use in indexed positions, not approval of a new position or a collateral whitelist. Original positions and clones have their own conditions.

For a collateral explorer, use `/list` to populate a token selector and `/positions` to find related positions. Choose `/positions/details` when the view also needs position balances and owners, or `/stats` for a collateral summary. Match tokens by chain and address, not symbol, and use each token's `decimals` to display its balances.

Position V1/V2 identifies a lending-contract version. It does not identify the FCS governance migration, API version or savings module version. Resolve chain, address and ABI from the [contract repository](https://github.com/Frankencoin-ZCHF/FrankenCoin) and [published SDK](https://www.npmjs.com/package/@frankencoin/zchf), pinned to the deployment used by the application.
