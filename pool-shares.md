---
description: FCS ownership, acquisition, governance, equity economics and exits.
---

<a id="investing-and-pool-shares"></a>

# 📈 FCS: Investing and Pool Shares

## Reserve Pool Shares

Frankencoin Share Token (FCS) is Frankencoin's canonical governance and share token. Holding FCS gives economic exposure to the system's equity capital and builds time-weighted voting power. Net fees and liquidation results change that capital; losses reduce it.

FCS connects these two roles: holders bear the economic results of the system and can veto proposals through [governance](governance.md). It is a share token, not a Swiss franc stablecoin or a savings deposit paying a set rate.

## Usage

### Acquire FCS

The [equity application](https://app.frankencoin.com/equity) provides investment interfaces. The FCS design has three distinct acquisition routes:

* **Invest ZCHF:** `deposit` specifies the ZCHF input; `mint` specifies the FCS output. The contract buys underlying equity and issues FCS. The exchange rate is not one FCS per ZCHF.
* **Buy existing FCS:** a secondary-market trade transfers shares from another holder. Its quote and availability depend on the venue and liquidity.
* **Migrate existing shares:** FPS holders can wrap their balance one to one into FCS. WFPS holders first unwrap into FPS. The [migration guide](fcs-migration.md) explains the different voting effects.

Use the preview for the intended operation and amount, rather than dividing by a displayed reference price. A preview estimates output; eligibility and transaction limits are separate checks. The [entry reference](fcs.md#entry-paths) defines the contract paths.

For a new ZCHF investment:

1. **Identify the contract.** Connect the wallet holding the ZCHF and check the chain and FCS contract used by the interface. The audited design uses Ethereum mainnet. Keep native currency for gas. These are contract paths; an application may expose only a subset.
2. **Choose what to fix.** Use `deposit` if you have a ZCHF budget and want the resulting shares, or `mint` if you want a specified FCS amount and need to know its ZCHF cost. Direct FPS wrapping is a different operation, covered by [migration](fcs-migration.md).
3. **Read the quote and limits.** Enter the chosen amount, read `previewDeposit` or `previewMint`, and check `maxDeposit` or `maxMint`. Review the expected input, shares, fees and recipient. A reference price multiplied by an amount omits curve and fee effects. If using the reviewed `depositExpected` variant, its minimum-share input can reject an output below your chosen threshold.
4. **Approve and invest.** If an allowance is needed, approve the specified spender for ZCHF, then submit the investment transaction. Approval alone does not create shares.
5. **Confirm ownership.** Check the received FCS balance and ZCHF spent. The new shares start without immediate votes; the governance section below explains what to check before acting.

For a secondary-market purchase, instead review the venue's FCS token address, input asset, expected output and trading costs. Confirm receipt of FCS after settlement. Buying underlying FPS through an older route leaves you with FPS until you wrap it; buying FCS does not transfer the seller's voting age.

### Participate in governance

FCS votes depend on balance and average holding duration, not balance alone. Holders can delegate votes while retaining their own ability to act. Fresh ZCHF investment, WFPS migration and purchases from another holder do not carry immediate voting power; direct wrapping of aged FPS credits the legacy votes lost on transfer.

Qualified actions need more than 1% of internal FCS voting power, including valid delegation, and the FCS contract meeting the underlying FPS quorum. These checks are separate from the binding threshold used for ZCHF exits. See [FCS governance](governance.md) for proposals and vetoes, and [voting mechanics](fcs.md#voting) for accumulation, capping and vote destruction.

### Exit an FCS holding

* **Redeem into ZCHF:** `redeem` fixes the shares burned; `withdraw` fixes the ZCHF output. Both need the FCS contract to be binding and eligible to redeem its underlying FPS, and both apply the redemption discount.
* **Sell existing FCS:** a market sale has its own quote and liquidity. It is not a redemption against the reserve.
* **Unwrap into FPS:** receive one underlying FPS per FCS. The caller's FCS holding duration must be at least the average across FCS holders, whether binding or unbound. This leaves the holder with FPS, not ZCHF.

There is no separate personal 90-day FCS redemption wait. Binding depends on the FCS contract's share of underlying FPS votes, and the 90-day condition applies to that contract as an FPS holder. The [exit reference](fcs.md#exit-paths-and-eligibility) defines these gates and the different limits of `withdraw` and `redeem`.

For a ZCHF exit:

1. **Choose the result you need.** Use `redeem` to burn a specified FCS amount, or `withdraw` to request a specified ZCHF amount. A market sale and an unwrap do not use the same quote or eligibility rules.
2. **Check availability.** Read `maxRedeem` in shares or `maxWithdraw` in ZCHF. A zero limit can reflect the wrapper-level redemption gate. If redemption is disabled, a preview is not permission to execute it, and waiting as an individual holder does not alone open that gate.
3. **Review proceeds for that size.** Read `previewRedeem` or `previewWithdraw`, including the current discount. A single `withdraw` can burn at most 10% of total FCS supply; `redeem` has no such cap. For a large `redeem`, more shares can produce less ZCHF. The reviewed `redeemExpected` variant adds a minimum-proceeds condition; ordinary `redeem` does not.
4. **Submit and confirm.** Check the share amount, recipient and transaction conditions, then submit. After confirmation, verify both the FCS burned and ZCHF received. A changed discount or other intervening activity can change the result from an earlier preview.

To unwrap instead, compare your FCS holding duration with the holder average before choosing the share amount. If eligible, submit `unwrap` and confirm the matching FPS receipt. This delivers FPS, not ZCHF, and does not carry your FCS voting age back into the underlying FPS record.

## Economics

FCS participates in one equity pool, not a second reserve. Each FCS wraps one FPS; the underlying Equity contract holds the capital and prices FPS. ZCHF investment through FCS adds capital to Equity. Income benefits that shared capital, and losses reduce it. FCS does not promise a fixed yield or a separate cash distribution.

### Proportional Capital Valuation

The underlying curve sets a marginal FPS reference valuation of three times equity capital. FCS uses the underlying FPS price for its `ask()` reference and applies a redemption discount to `bid()`. Neither value is a size-specific execution quote or an FCS market price.

The [underlying FPS reference](fps-reference.md#proportional-capital-valuation) gives the formula and numerical example in FPS units. The [FCS pricing reference](fcs.md#prices-and-redemption-discount) explains previews, fees and the size- and activity-dependent discount. An API field reporting FPS supply or price remains an underlying metric, even when displayed beside FCS.

### Equilibrium

A simplified model considers 30,000,000 ZCHF of outstanding mints at 5% annual interest: gross annual borrowing income is 1,500,000 ZCHF. If investors require a 5% return, and if that income continues without expenses or losses, capitalising it gives a valuation of 30,000,000 ZCHF. The underlying FPS curve reaches that reference valuation at 10,000,000 ZCHF of equity. This is a model of the shared equity pool, not a valuation of FCS supply alone.

Savings changes the income available to equity holders:

```text
net equity income = borrowing income + other net income - savings expense - losses
savings expense = interest-bearing savings balance × applicable savings rate
```

For example, an average interest-bearing savings balance of 10,000,000 ZCHF at 2% costs 200,000 ZCHF a year. With the borrowing income above, no other income and no losses, net equity income is 1,300,000 ZCHF. At the same assumed 5% required return, that would support a model valuation of 26,000,000 ZCHF, not 30,000,000 ZCHF. Actual accrual timing, changing rates, referrals and losses affect realised flows. Referral fees divide savings interest between the user and referrer; they are not an extra payment on top of that gross interest.

The one-third equity relationship is a model result under assumptions, not a reserve requirement enforced by the contracts. Borrowing to buy FCS exposes the holder to fees, losses, price changes and redemption conditions; a spread between quoted rates is not a risk-free arbitrage. Comparing the underlying FPS reference valuation with ZCHF supply does not uniquely reveal expected growth.

### Limits to Capital Efficiency

Lower equity means a smaller buffer before losses reach shared minter reserves. More equity provides a larger buffer but changes the returns available per share. Neither the curve nor a proposed equilibrium ensures a particular reserve ratio or market price. [Reserve accounting](reserve.md) explains the flows; [FCS mechanisms and dependencies](risks.md#fcs-mechanisms-and-dependencies) describes how voting state and redemption activity affect holders.

## Underlying FPS

FPS remains the backing token and retains its own supply, address and legacy governance records. It is not a second name for FCS. The [underlying FPS reference](fps-reference.md) contains the Equity curve, direct FPS redemption rules and historical interface examples. The [FCS mechanics reference](fcs.md#version-and-terminology) maps the reader-facing FCS name to the audited `FPS2` identifiers.
