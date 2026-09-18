# Wallet integration

This guide connects a wallet's ZCHF balance and savings view to contract actions. Use the API for indexed account activity and cross-module summaries, contract reads for current balances and pending interest, and wallet transactions for deposits, withdrawals and interest collection.

The [savings API](savings.md) defines HTTP schemas, units and limits; the [common helpers](README.md#executable-examples) preserve integer quantities.

## Chain, token and module selection

Configure each integration with an EIP-155 chain ID, ZCHF token address, savings module address and the ABI for that deployment. Addresses can coincide across chains without identifying the same contract state. The API's `status[chainId][moduleAddress]` lookup is explicit: mainnet has more than one reported module.

ZCHF uses 18 decimals and ERC-20 transfers, balances and allowances. Amounts passed to contracts are integer base units. Check the token address and spender for the selected chain rather than taking them from an arbitrary API record. Use the [contract repository](https://github.com/Frankencoin-ZCHF/FrankenCoin) and a pinned version of the [published SDK](https://www.npmjs.com/package/@frankencoin/zchf) to resolve deployment interfaces.

Read `balanceOf(account)` for the wallet's liquid ZCHF balance and `allowance(owner, spender)` before an operation that pulls tokens. Keep liquid ZCHF separate from funds credited to a savings account. Ordinary token transfers use the ERC-20 `transfer` or `transferFrom` interface; the [reference-transfer API](transfers.md) covers only transfers carrying reference messages.

## Savings contract interface

The methods below describe the referral-capable `AbstractSavings` interface at the [linked source revision](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/savings/AbstractSavings.sol). Older `SavingsV2` contracts do not have the same account/referral interface. Resolve the ABI and conditions for the selected module rather than assuming every indexed module implements these methods.

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

### Deposit ZCHF

1. Select the wallet account, chain and savings module. Read its rate, entry-delay rules and any referral terms for display before confirmation.
2. Convert the entered ZCHF amount to 18-decimal integer base units. Read the wallet balance and allowance for that module.
3. If an allowance is needed, submit `approve(spender, amount)` to the ZCHF token with the selected module as spender. Wait for its successful receipt before the deposit.
4. Submit the supported `save(amount)` call, or `save(owner, amount)` to credit another account. Where referral overloads are supported, show the referrer and fee before requesting the signature.
5. After the deposit receipt succeeds, re-read the savings account. Indexed activity may appear later; approval alone does not deposit funds.

### Collect interest or withdraw

Use `refreshMyBalance()` or `refreshBalance(owner)` to collect interest into the saved balance, with any referral fee paid under the account's terms. This is a transaction, not a balance refresh performed by the API. After its receipt, re-read credited balance and pending interest to avoid displaying the same interest twice.

For a withdrawal, read the account and module conditions, then submit the supported `withdraw(target, amount)` with a validated recipient and base-unit amount. Use the receipt and resulting balances to report the amount transferred; the requested amount is not proof of the amount received. `adjust(targetAmount)` instead sets a target savings balance, depositing or withdrawing as needed, and may require allowance for a deposit.

## Displaying savings

Keep these values separate:

- **Saved balance**: the contract's current credited principal, including previously collected net interest.
- **Gross pending interest**: `accruedInterest(account)` before any referral deduction.
- **Net pending interest**: gross minus the applicable integer-rounded referral fee.
- **Cumulative collected interest**: indexed historical `interest`, not additional pending funds.

Read account terms and accrued interest at a consistent block. `saved + grossPending` is not the user's net balance when a referral fee applies. In this referral-capable contract the fee is at most 250,000 PPM (25% of gross interest), with no deduction for a zero referrer. Account referral terms and the selected version determine the actual deduction.

The entry delay, weighted tick adjustment and withdrawal conditions depend on the module version. Do not infer a universal lock period from the HTTP balance or a rate field. See [savings mechanics](../savings.md) and [source](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/savings/AbstractSavings.sol).

## Indexed activity and other integrations

`/savings/core/activity/:account` returns at most 1000 recent records. Several events can share a transaction hash, so the hash alone is not a unique event key. A complete history requires an independent event traversal and reconciliation; a capped response cannot establish it.

For reference-bearing payments, use the [candidate-only transfer example](transfers.md#candidate-lookup-example). For the canonical share token FCS, distinguish [reference prices, previews and transaction limits](fcs.md#contract-reads-and-transactions). Use FCS-specific supply and contract references; the underlying FPS fields are not substitutes.

The [API package](https://www.npmjs.com/package/@frankencoin/api) can provide types for a pinned release. TypeScript types do not validate runtime JSON; retain HTTP, schema and unit checks.
