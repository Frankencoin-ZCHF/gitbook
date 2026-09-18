"""Instructional regression guards, not deployed-contract or UI execution tests.

Human review establishes explanatory quality. These tests preserve the inputs,
choices, outcomes, examples and source boundaries that make those guides useful.
The source excerpts are extracted from the previously captured pinned Solidity.
"""
from decimal import Decimal
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = json.loads((Path(__file__).parent / 'instructional-evidence.json').read_text())


def page(name):
    return (ROOT / name).read_text()


def section(text, heading):
    return text.split(heading + '\n', 1)[1].split('\n## ', 1)[0]


class Walkthroughs(unittest.TestCase):
    def assert_phrases(self, name, phrases):
        text = page(name)
        for phrase in phrases:
            with self.subTest(page=name, phrase=phrase):
                self.assertIn(phrase, text)

    def test_opening_explains_choices_before_submission(self):
        text = page('positions/open.md')
        headings = ['## Before you start', '## Proposal terms',
                    '## Interest and minting capacity', '## Collateral and liquidation price',
                    '## Reserve and auction duration', '## Submission and confirmation']
        self.assertEqual(sorted(text.index(h) for h in headings),
                         [text.index(h) for h in headings])
        self.assert_phrases('positions/open.md', [
            'cloning it', 'gross amount', 'net ZCHF', '1,000 ZCHF',
            'at least three days', '1,200 ZCHF and 60 days',
            '**Term:**', '**Risk premium:**', '**Family minting limit:**',
            '**minimum collateral**', '**initial collateral**',
            'global borrowing rate plus risk premium',
            'not permanently split', 'not an oracle price',
            'Approval grants an allowance', 'not itself a ZCHF mint',
            '**Follow the initialisation period.**', '**Mint from the accepted position.**'])

    def test_opening_source_boundaries_are_not_universal_ui_claims(self):
        self.assert_phrases('positions/open.md', [
            'In the pinned `MintingHub.openPosition`', '5,000 ZCHF',
            'not a universal minimum for every deployment',
            'when the proposal transaction succeeds', 'duration of each of the two auction phases',
            'historical interface, not current quotes or button names'])
        source = EVIDENCE['sources']['MintingHub.sol']['excerpts']
        self.assertIn('_minCollateral * _liqPrice < 5000 ether * 10 ** 18',
                      source['minimum_liquidation_value'])
        self.assertIn('transferFrom(msg.sender, address(pos), _initialCollateral)',
                      source['collateral_at_creation'])
        self.assertNotIn('hit the "Propose Position"', page('positions/open.md'))

    def test_new_borrowing_illustration_is_consistent(self):
        text = page('positions/open.md')
        rate = (Decimal(20000) + Decimal(10000)) / 1000000
        gross, reserve_fraction = Decimal(10000), Decimal('.10')
        fee, reserve = gross * rate, gross * reserve_fraction
        self.assertEqual((Decimal(300), Decimal(150), Decimal(1000), Decimal(8700)),
                         (fee, fee / 2, reserve, gross - fee - reserve))
        for phrase in ['3% a year', '300 ZCHF fee', '150 ZCHF', 'retains 1,000 ZCHF',
                       'receives 8,700 ZCHF', 'separate 1,000 ZCHF proposal fee',
                       'assumed rates, not current quotes']:
            self.assertIn(phrase, text)
        source = EVIDENCE['sources']['Position.sol']['excerpts']
        self.assertIn('currentRatePPM() + riskPremiumPPM', source['rate'])
        self.assertIn('/ 365 days', source['fee'])

    def test_adjustment_distinguishes_targets_transfers_and_price(self):
        self.assert_phrases('positions/adjust.md', [
            'currently owns', 'target totals', 'additional gross amount',
            '`repay` specifies the wallet amount paid',
            'Clearing debt does not itself withdraw the collateral',
            'Adding collateral alone does not change',
            'add enough collateral, repay enough debt',
            'processes minting before changing the price',
            '## Confirm the adjustment'])
        source = EVIDENCE['sources']['Position.sol']['excerpts']['adjust_order']
        self.assertLess(source.index('_mint('), source.index('_adjustPrice('))
        self.assertIn('newCollateral - colbal', source)

    def test_clone_uses_original_expiry_and_separate_approval(self):
        self.assert_phrases('positions/clone.md', [
            '## Choose a position to clone', '## Set collateral, mint amount and expiry',
            '## Submit and manage the clone', "original position's expiry",
            'If you need a particular net amount',
            'does not create the clone or mint ZCHF', 'new position address'])
        self.assertNotIn("cannot exceed its parent's expiry", page('positions/clone.md'))
        source = EVIDENCE['sources']['Position.sol']['excerpts']['clone_expiry']
        self.assertIn('_expiration > Position(original).expiration()', source)

    def test_challenger_and_bidder_inputs_and_results_are_separate(self):
        text = page('positions/auctions.md')
        challenge = section(text, '## How to Initiate an Auction')
        bid = section(text, '## How to Participate in Ongoing Auctions')
        for phrase in ['same collateral token', '`minimumPrice`',
                       'Approval alone does not start an auction', 'challenge number',
                       '`pendingReturns`', '`returnPostponedCollateral`']:
            self.assertIn(phrase, challenge)
        for phrase in ['ZCHF and native gas', 'takes a collateral size',
                       'not a freely chosen auction price', 'not an offer held',
                       'ZCHF spent, collateral received']:
            self.assertIn(phrase, bid)
        self.assertIn('2% of the accepted bid', text)

    def test_savings_deposit_collect_withdraw_and_remove_referral(self):
        self.assert_phrases('savings.md', [
            '**Select the account and module.**', '**Read the terms.**',
            '**Choose the amount.**', '**Approve and deposit.**',
            '**Confirm the account credit.**', '`adjust(targetAmount)`',
            '### Collecting interest', '### Withdrawing savings',
            'saved balance, not to the spending balance',
            '`withdraw(target, amount)`', 'referrer must be the zero address and the fee zero',
            'interest delay alone does not lock principal'])
        source = EVIDENCE['sources']['AbstractSavings.sol']['excerpts']
        self.assertIn('refresh(msg.sender)', source['drop_referrer'])
        self.assertIn('setReferrer(address(0x0), 0)', source['drop_referrer'])
        self.assertIn('targetAmount - balance.saved', source['target_balance'])

    def test_fcs_journeys_keep_choices_and_two_voting_layers(self):
        self.assert_phrases('pool-shares.md', [
            '**Choose what to fix.**', '**Read the quote and limits.**',
            '**Confirm ownership.**', '**Choose the result you need.**',
            '**Check availability.**', '**Review proceeds for that size.**',
            'more shares can produce less ZCHF', '10% of total FCS supply',
            'no separate personal 90-day FCS redemption wait'])
        self.assert_phrases('governance.md', [
            '### Choose between acting and delegating', 'delegation record',
            'more than 1%', 'underlying FPS quorum', 'two synchronisations'])
        self.assert_phrases('fcs-migration.md', [
            '### If you already hold FPS', '### If you hold WFPS',
            '10 FPS issues 10 FCS', 'It does not spend 10 ZCHF',
            'Two voting records', 'do not give the wrapper the same accumulated legacy age'])

    def test_walkthroughs_preserve_historical_images(self):
        for name, images in EVIDENCE['historical_images'].items():
            with self.subTest(page=name):
                self.assertEqual(images, re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', page(name)))
                self.assertIn('Historical', page(name))


if __name__ == '__main__':
    unittest.main()
