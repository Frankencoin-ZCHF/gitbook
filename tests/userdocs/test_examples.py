"""Regression checks for published arithmetic, units and version boundaries.

These are documentation checks, not execution tests of deployed contracts.
Source-evidence.json contains genuine retrieved excerpts/ABIs. Numerical examples
below are synthetic illustrations explicitly labelled as such in the pages.
"""
from decimal import Decimal as D
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = json.loads((Path(__file__).parent / 'source-evidence.json').read_text())


def page(name):
    return (ROOT / name).read_text()


class NumericalExamples(unittest.TestCase):
    def test_redemption_factor(self):
        text = page('fcs.md')
        match = re.search(r'`S = ([\d,]+)`, `q = ([\d,]+)` and `R = (\d+)`', text)
        assert match is not None
        supply, shares, recent = (D(x.replace(',', '')) for x in match.groups())
        result = ((supply - shares / 2) / (supply + recent)) ** 4
        self.assertEqual(D('0.81450625'), result)
        self.assertIn(f'`{result}`', text)
        self.assertIn('absent further redemptions', text)
        self.assertIn('own size-dependent discount', text)

    def test_legacy_valuation(self):
        self.assertEqual(D(300), D(3) * 1_000_000 / 10_000)
        # The unchanged FPS example now lives in the underlying reference.
        self.assertIn('300 ZCHF per FPS', page('fps-reference.md'))
        self.assertIn('fps-reference.md#proportional-capital-valuation', page('pool-shares.md'))
        # The idealised continuous curve preserves V = p*s = 3*K.
        old_k, old_s, growth = D(1_000_000), D(10_000), D(8)
        new_s = old_s * 2
        new_p = (3 * old_k / old_s) * 4
        self.assertEqual(new_s * new_p, 3 * old_k * growth)

    def test_income_after_savings(self):
        gross = D(30_000_000) * D('0.05')
        expense = D(10_000_000) * D('0.02')
        net = gross - expense
        self.assertEqual((gross, expense, net, net / D('.05')),
                         tuple(map(D, [1_500_000, 200_000, 1_300_000, 26_000_000])))
        for value in ['1,500,000', '200,000', '1,300,000', '26,000,000']:
            self.assertIn(value, page('pool-shares.md'))

    def test_balanced_mint_example(self):
        minted, reserve, fee = D(500), D(100), D(25)
        self.assertEqual(D(375), minted - reserve - fee)
        changes = re.findall(r'\| [^\n]+ \| ([+-][\d,]+) \|', page('reserve.md'))
        values = [int(x.replace(',', '')) for x in changes]
        self.assertEqual([500, 125, 500, 100, 25, -5000, -590, -5000, -1000, 410], values)
        self.assertEqual(sum(values[:2]), sum(values[2:5]))
        self.assertEqual(sum(values[5:7]), sum(values[7:]))

    def test_bid_based_challenge_accounting(self):
        debt, bid, reserve = D(5000), D(4500), D(1000)
        reward = bid * D('.02')
        draw = debt - (bid - reward)
        equity = reserve - draw
        self.assertEqual((reward, draw, equity), (D(90), D(590), D(410)))
        for amount in [90, 590, 410]:
            self.assertIn(f'{amount} ZCHF', page('reserve.md'))

    def test_position_examples(self):
        self.assertEqual(3000, 2 * 1500)
        self.assertEqual(2610, 3000 - 300 - 90)
        self.assertEqual(2640, 3000 - 300 - 60)
        self.assertEqual(1000, 900 + 100)
        self.assertEqual(5000, 2 * 2500)
        self.assertEqual(5000, 20 * 250)
        for value in ['3,000', '2,610', '900', '1,000', '2,000']:
            self.assertIn(value, page('positions/adjust.md'))
        self.assertIn('2,640 ZCHF', page('positions/clone.md'))

    def test_legacy_vote_example(self):
        self.assertGreater(10 * 730, 1000 * 7)
        self.assertIn('7,300 FPS-days', page('fps-reference.md'))
        self.assertIn('7,000 FPS-days', page('fps-reference.md'))
        self.assertIn('fps-reference.md#legacy-votes-and-quorum', page('governance.md'))

    def test_referral_ppm(self):
        gross, ppm, denominator = D(100), D(200000), D(1000000)
        fee = gross * ppm / denominator
        self.assertEqual((fee, gross - fee), (D(20), D(80)))
        self.assertEqual(D('.25'), D(250000) / denominator)
        self.assertIn('80 ZCHF for the user and 20 ZCHF for the referrer', page('savings.md'))

    def test_slippage(self):
        proceeds = D(100000) * D('.98')
        self.assertEqual(D(98000), proceeds)
        self.assertEqual(D('.02'), 1 - proceeds / 100000)
        self.assertIn('98,000 CHF', page('risks.md'))


class SourceAndCopyBoundaries(unittest.TestCase):
    def test_fcs_version_and_exact_source_comparators(self):
        quotes = {x['id']: x['quote'] for x in EVIDENCE['source_checks']}
        self.assertIn(' < averageHoldingDuration()', quotes['unwrap_comparison'])
        self.assertIn('>= MIN_HOLDING_DURATION', quotes['legacy_age'])
        self.assertIn('isBinding() && FPS1.canRedeem', quotes['redemption_gate'])
        self.assertIn('totalSupply() / FPS1.totalSupply()', quotes['total_assets'])
        text = page('fcs.md')
        self.assertIn(EVIDENCE['fcs_commit'], text)
        self.assertIn('equality passes', text)
        self.assertIn('FCS.totalSupply() / FPS1.totalSupply()', text)
        self.assertIn('no such cap', text)
        self.assertIn('more than 1%', text)
        self.assertIn('not two thirds of FPS supply or internal FCS votes', text)

    def test_public_savings_methods_exist_in_observed_abis(self):
        for name, abi in EVIDENCE['savings_abis'].items():
            methods = {x['name'] for x in abi if x['type'] == 'function'}
            self.assertTrue({'refreshBalance', 'refreshMyBalance'} <= methods)
            self.assertNotIn('refresh', methods)
            self.assertEqual('referral' in name, 'dropReferrer' in methods)
        self.assertIn('internal `refresh(address)`', page('savings.md'))
        self.assertIn('Future interest has no referral deduction', page('savings.md'))

    def test_indexed_network_table_matches_stored_response(self):
        rows = re.findall(r'\| [^|]+ \| (\d+) \| `(0x[0-9a-f]{40})` \|', page('bridge-to-other-chains.md'))
        self.assertEqual(7, len(rows))
        for chain, address in rows:
            self.assertEqual(address, EVIDENCE['zchf_instances_observed'][chain]['address'])

    def test_legacy_identities_and_ui_snapshots(self):
        overview = page('README.md')
        for address in ['0xB58E61C3098d85632Df34EecfB899A1Ed80921cB', '0x1bA26788dfDe592fec8bcB0Eaff472a42BE341B2']:
            self.assertIn(address, overview)
        self.assertNotIn('raw/telegram-bot/', page('telegram-api-bot.md'))
        self.assertIn('not by sending messages to the live bot', page('telegram-api-bot.md'))
        self.assertIn('market value of the collateral is below', page('positions/README.md'))
        self.assertIn('Adding collateral alone does not change', page('positions/adjust.md'))

    def test_user_page_style_invariants(self):
        files = list(ROOT.glob('*.md')) + list((ROOT / 'positions').glob('*.md'))
        self.assertEqual(19, len(files))
        self.assertIn(ROOT / 'fps-reference.md', files)
        for file in files:
            text = file.read_text()
            self.assertNotIn('\u2014', text, file.name)
            self.assertNotIn('Frankencoin Capital Shares', text, file.name)
            self.assertNotIn('TODO', text, file.name)


if __name__ == '__main__':
    unittest.main()
