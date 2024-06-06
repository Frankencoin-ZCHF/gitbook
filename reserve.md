---
description: The three types of reserves that help with stabilizing the system.
---

# 🏦 Reserve

There are three types of reserves in the Frankencoin system. The first one consists of other Swiss franc stablecoins that reside in a bridge, the second one consists of funds provided by the borrowers when they mint new Frankencoins, and the third one is provided by the holders of reserve pool shares. The collateral used to mint Frankencoin is not considered reserve as it conceptually stays outside the "balance sheet" of the Frankencoin system.

**Balance Sheet Diagram:**

<div data-full-width="true">

<figure><img src=".gitbook/assets/image (6).png" alt="" width="375"><figcaption><p>The Frankencoin "balance sheet"</p></figcaption></figure>

</div>

If the Frankencoin system was a company, its balance sheet would roughly look as shown above:

**Assets:**

* **Stablecoins Locked in Bridges:** These are stablecoins like XCHF that are locked within bridge contracts, facilitating the exchange between Frankencoin (ZCHF) and other stablecoins.
* **Minter Repayment Obligations:** This represents the amount borrowers need to repay after minting Frankencoin. It reflects the debt owed by users who have collateralized their assets to mint ZCHF.
* **Reserve:** This includes the funds in the reserve pool contributed by minters and reserve pool share holders. These funds grow over time, providing a buffer.

**Liabilities and Equity:**

* **Total Frankencoin (ZCHF) Supply:** This is the total amount of Frankencoins in circulation, representing the system's obligations to the holders of ZCHF.
* **Minters Reserve:** The specific reserve funds allocated to cover potential losses from minter defaults, ensuring the stability of the system.
* **Equity:** Owned by reserve pool share holders, this represents the net value of the system after accounting for assets and liabilities. Holders of reserve pool shares play a crucial role in the system's governance and stability, benefiting from a share of the system's profits and having a say in governance decisions .

#### Example Scenarios to Understand the Balance Sheet:

1. **User Swaps ZCHF for XCHF:**
   * If a user sends 100 ZCHF to the stablecoin bridge to swap them into XCHF, the balance sheet items for stablecoins locked in bridges (x) and the total ZCHF supply (z) both decrease by 100 units. Other balance sheet items remain unaffected.
2. **User Mints New Frankencoins:**
   * Suppose a user mints 500 ZCHF against collateral with a reserve ratio of 20% and a fee of 5%. On the asset side:
     * **Minter Repayment Obligations (m):** Increases by 500 ZCHF.
     * **Reserve (r):** Increases by 125 ZCHF (100 ZCHF into minters reserve and 25 ZCHF as fees).
   * On the liabilities side:
     * **Total ZCHF Supply (z):** Increases by 500 ZCHF.
     * **Minters Reserve (b):** Increases by 100 ZCHF.
     * **Equity (e):** Increases by 25 ZCHF (the fee retained by the system).
   * The minting process thus expands the balance sheet by 625 ZCHF, which reflects both the debt and the new reserves.
3. **Successful Challenge of a Minter's Position:**
   * For a position that minted 5000 ZCHF and is successfully challenged with a highest bid of 4500 ZCHF:
     * **Reserve (r):** Decreases by 600 ZCHF to cover the shortfall.
     * **Total ZCHF Supply (z):** Decreases by 5000 ZCHF as the loan is repaid.
     * **Minter Repayment Obligations (m):** Decreases by 5000 ZCHF.
     * **Minters Reserve (b):** Adjusts to reflect 400 ZCHF reassigned to equity as liquidation profit.
     * **Equity (e):** Increases by 400 ZCHF.

#### Protection Mechanisms During Liquidation:

When a position is liquidated, the system employs three layers of protection to prevent losses:

1. **Borrower's Reserve:** Directly associated with the liquidated position, used first to cover any losses.
2. **Equity:** If the borrower's reserve is insufficient, losses are absorbed by reducing the equity, impacting the value of reserve pool shares.
3. **General Borrower's Reserve:** As a last resort, this reserve is tapped into, potentially requiring other users to repay more than initially anticipated, creating an incentive for all participants to maintain system integrity.

#### Equilibrium of Equity:

The system is designed to ensure that in efficient markets, the equity will approximate one third of the Frankencoins not created through a bridge, mathematically represented as 3e=z−x3e = z - x3e=z−x. This equilibrium ensures a robust financial foundation, detailed further in the research paper.
