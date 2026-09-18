# Wallet integration

Use API GET requests for indexed display data and contract reads for current account state. Transactions change that state. The [savings API](savings.md) is the shared reference for HTTP schemas, units and limits; the [common helpers](README.md#executable-examples) preserve integer quantities.

## Chain, token and module selection

Configure each integration with an EIP-155 chain ID, ZCHF token address, savings module address and the ABI for that deployment. Addresses can coincide across chains without identifying the same contract state. The API's `status[chainId][moduleAddress]` lookup is explicit: mainnet has more than one reported module.

ZCHF uses 18 decimals and ERC-20 transfers, balances and allowances. Amounts passed to contracts are integer base units. Check the token address and spender for the selected chain rather than taking them from an arbitrary API record. Use the [contract repository](https://github.com/Frankencoin-ZCHF/FrankenCoin) and a pinned version of the [published SDK](https://www.npmjs.com/package/@frankencoin/zchf) to resolve deployment interfaces.

## Savings contract interface

The methods below describe the inspected referral-capable `AbstractSavings` interface. Older `SavingsV2` contracts do not have the same account/referral interface. Resolve the ABI and conditions for the selected module rather than assuming every indexed module implements these methods.

| Method or getter | Classification | Purpose |
| --- | --- | --- |
| `savings(account)` | Read-only | Saved balance, ticks and, where supported, referrer and referral fee |
| `accruedInterest(account)` | Read-only | Gross pending interest at current state |
| `accruedInterest(account, timestamp)` | Read-only | Gross interest at the supplied timestamp under contract tick rules |
| `currentRatePPM`, `currentTicks`, `INTEREST_DELAY` | Read-only | Rate, tick counter and entry-delay parameter |
| `refreshBalance(owner)`, `refreshMyBalance()` | **Transaction** | Collect interest, pay any referral fee and update saved balance/ticks |
| `save(amount)`, `save(owner, amount)` | **Transaction** | Deposit ZCHF under the module's conditions |
| `withdraw(target, amount)` | **Transaction** | Withdraw under the module's conditions |
| `adjust(targetAmount)` | **Transaction** | Adjust savings balance |
| Referral overloads and `dropReferrer()` | **Transaction**, ABI-dependent | Set or remove referral terms |

An `eth_call` simulation of a mutating method does not persist its result. It does not turn `refreshBalance` into a view method. Deposits that pull ZCHF require the appropriate allowance to the selected savings module.

## Displaying savings

Keep these values separate:

- **Saved balance**: the contract's current credited principal, including previously collected net interest.
- **Gross pending interest**: `accruedInterest(account)` before any referral deduction.
- **Net pending interest**: gross minus the applicable integer-rounded referral fee.
- **Cumulative collected interest**: indexed historical `interest`, not additional pending funds.

Read account terms and accrued interest at a consistent block. `saved + grossPending` is not the user's net balance when a referral fee applies. In the inspected referral-capable contract the fee is at most 250,000 PPM (25% of gross interest), with no deduction for a zero referrer. Account referral terms and the selected version determine the actual deduction.

The entry delay, weighted tick adjustment and withdrawal conditions depend on the module version. Do not infer a universal lock period from the HTTP balance or a rate field. See [savings mechanics](../savings.md) and [source](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/savings/AbstractSavings.sol).

## Indexed activity and other integrations

`/savings/core/activity/:account` returns at most 1000 recent records. Several events can share a transaction hash, so the hash alone is not a unique event key. A complete history requires an independent event traversal and reconciliation; a capped response cannot establish it.

For reference-bearing payments, use the [candidate-only transfer example](transfers.md#candidate-lookup-example). For FCS, distinguish [reference prices, previews and transaction limits](fcs.md#contract-reads-and-transactions). Neither endpoint family supplies a transaction approval or settlement decision.

The [API package](https://www.npmjs.com/package/@frankencoin/api) can provide types for a pinned release. TypeScript types do not validate runtime JSON; retain HTTP, schema and unit checks.
