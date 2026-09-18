# Analytics API

Read indexed financial logs and legacy FPS metrics. These routes do not report FCS supply or holder voting power; use [FCS](fcs.md) for its controller.

## Endpoints and limits

| GET path | Response and limit |
| --- | --- |
| `/analytics/profitLossLog` | Recent profit/loss observations, limited to 1000 records |
| `/analytics/transactionLog/json` | `{num, logs, pageInfo}`; default 50 rows; supports `firstItem`, `limit`, `after` |
| `/analytics/transactionLog/csvE18` | Scaled CSV transaction-log page; default 50 rows, not a full export |
| `/analytics/dailyLog/json` | `{num, logs}` of available daily snapshots |
| `/analytics/dailyLog/csvE18` | Scaled CSV daily snapshots |
| `/analytics/fps/exposure` | `{general, exposures}` for legacy FPS |
| `/analytics/fps/earnings` | Scaled earnings/expense categories for legacy FPS |

`firstItem=false` orders transaction logs newest first; `true` requests oldest first. `after` takes the previous `pageInfo.endCursor`. CSV accepts `pageInfo=true`, which appends pagination JSON and thus is not a plain CSV-only document. Daily routes expose no pagination parameters in the reviewed specification; adding `limit=1` did not limit a saved daily response.

## Financial fields

Transaction-log rows include `chainId`, `count`, `timestamp`, `kind`, `amount`, `txHash`, `totalInflow`, `totalOutflow`, `totalEquity`, `totalSavings`, `fpsTotalSupply`, `fpsPrice`, `realizedNetEarnings` and `earningsPerFPS`. Quantities are raw decimal strings with 18 decimals: ZCHF amounts, FPS quantities or ZCHF per FPS as named. `count` is an identifier, not an amount; `timestamp` is Unix seconds. Daily snapshots contain `date` and the available financial totals, not every transaction field.

The reviewed transaction schema does **not** include total ZCHF supply, V1/V2 minting totals or interest rates. Use [ecosystem info](ecosystem.md), [positions](positions.md) and [savings](savings.md) for those current data sources. Do not infer unavailable historical series from current values.

Earnings categories such as `minterProposalFees`, `investFees`, `redeemFees`, `positionProposalFees`, `savingsInterestCosts` and `otherLossClaims` are already scaled ZCHF numbers. For example, the captured `minterProposalFees` value `25000` means 25,000 ZCHF, not 25,000 base units. Exposure values are also scaled: `mint.interestAverage` and ratios are fractions, `positions` fields are counts, and monetary values use their named ZCHF units. Neither family follows a universal raw-string rule.

## Export completeness

A saved two-page transaction-log check advanced from count `4385` to `4384` using the first response's full `endCursor`. The second response returned a distinct cursor. This verifies one pagination step, not full-history traversal. Reject missing, repeated or non-progressing cursors, deduplicate rows and reconcile totals before describing an export as complete.

A page with `hasNextPage=true` needs a valid next cursor. Reaching a page with `hasNextPage=false` only completes that indexer's available traversal, not independent reconciliation with the chain. For complete accounting, use a separately validated indexer or block-range contract logs with receipt and reorg reconciliation.

Daily logs are available observations, not a guarantee of one row for every calendar day. Preserve missing dates as missing data rather than inventing zero values.
