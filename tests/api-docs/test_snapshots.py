"""Point-in-time evidence tests, separate from synthetic example behaviour tests."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / 'tests/api-docs/fixtures'


def body(number):
    return json.loads((FIXTURES / f'{number:02d}.body').read_text())


def examples(page):
    text = (ROOT / 'api-docs' / page).read_text()
    return [json.loads(block) for block in re.findall(r'```json\n(.*?)\n```', text, re.S)]


class CapturedEvidence(unittest.TestCase):
    def test_every_captured_fixture_matches_its_provenance(self):
        manifest = json.loads((FIXTURES / 'manifest.json').read_text())
        self.assertEqual(len(manifest), 32)
        self.assertEqual(len({x['file'] for x in manifest}), len(manifest))
        for entry in manifest:
            self.assertEqual(entry['kind'], 'captured-public-response')
            self.assertEqual(hashlib.sha256((FIXTURES / entry['file']).read_bytes()).hexdigest(), entry['sha256'])
            self.assertTrue(entry['url'].startswith('https://api.frankencoin.com/'))

    def test_printed_json_is_captured_data_not_pseudo_json(self):
        self.assertEqual(examples('fcs.md'), [body(33), body(34)])
        self.assertEqual(examples('savings.md'), [body(6)])

    def test_fcs_and_legacy_fps_identity_and_units_are_distinct(self):
        fps, fcs, discount = body(3), body(33), body(34)
        self.assertEqual(fps['erc20']['symbol'], 'FPS')
        self.assertEqual(fcs['erc20']['symbol'], 'FCS')
        self.assertNotEqual(fps['chains']['1']['address'], fcs['chain']['address'])
        self.assertNotEqual(fps['token']['totalSupply'], fcs['token']['totalSupply'])
        self.assertIsInstance(fcs['token']['isBinding'], bool)
        self.assertIsInstance(fcs['token']['totalAssets'], float)
        self.assertEqual(discount['discount'], 1)
        self.assertIsInstance(discount['weightedRecentRedemptions'], str)
        self.assertEqual(discount['recoveryPeriodSeconds'], 7 * 24 * 3600)

    def test_history_error_and_exact_reference_evidence(self):
        self.assertIn('NaN', body(18)['error']['message'])
        self.assertEqual(len(body(29)), 7)
        self.assertEqual(body(37), [])
        self.assertEqual(body(49), [])
        self.assertEqual(body(50)[0]['reference'], '12 months loan')
        self.assertEqual(len(body(50)), 1)
        self.assertEqual(body(29)[0]['targetChain'], '0')
        self.assertTrue(any(int(row['targetChain']) > 2**53 - 1 for row in body(29)))

    def test_transfer_counter_and_null_rows_do_not_form_a_cursor(self):
        self.assertEqual(body(16), 1000)
        self.assertEqual(body(28)['count'], '1001')
        self.assertEqual(body(51), 0)
        listing = body(27)
        self.assertEqual(listing['num'], len(listing['list']))
        self.assertIn(None, listing['list'])

    def test_savings_roots_modules_and_ppm_types(self):
        info, balances = body(5), body(6)
        self.assertEqual(set(info), {'status', 'totalBalance', 'ratioOfSupply', 'totalInterest'})
        self.assertEqual(sorted(row['rate'] for row in info['status']['1'].values()), [10000, 35000])
        for chain, modules in balances.items():
            for module, row in modules.items():
                self.assertEqual(row['chainId'], int(chain))
                self.assertEqual(row['module'], module)
                for field in ['balance', 'save', 'withdraw', 'interest']:
                    self.assertRegex(row[field], r'^\d+$')
        self.assertIn('rate', body(8))
        self.assertNotIn('address', balances)

    def test_prices_and_collateral_have_field_specific_units(self):
        mapping = body(9)
        self.assertTrue(all(key == key.lower() for key in mapping))
        self.assertTrue(any(row['source'] is None and row['timestamp'] == 0 for row in mapping.values()))
        self.assertTrue(any(row['timestamp'] > 10**12 for row in mapping.values()))
        self.assertTrue(any(row['price']['usd'] != row['price']['chf'] for row in mapping.values()))
        self.assertTrue({0, 6, 8, 18}.issubset({row['decimals'] for row in body(25)['list']}))

    def test_historical_minter_proposals_are_not_active_minter_list(self):
        proposals = body(24)['list']
        self.assertTrue(any(row['denyDate'] is not None for row in proposals))
        self.assertTrue(all('status' not in row and 'version' not in row for row in proposals))
        for absent in ['circulatingSupply', 'priceHistory', 'mintingCapacity']:
            self.assertNotIn(absent, body(3)['token'])

    def test_challenge_success_does_not_prove_collateral_acquisition(self):
        self.assertTrue(any(row['status'] == 'Success' and row['acquiredCollateral'] == '0' for row in body(14)['list']))
        bids = body(15)
        self.assertEqual(set(bids['bidIds']), set(bids['map']))
        self.assertTrue(all('-bid-' in key for key in bids['map']))
        self.assertEqual(body(52), {'num': 0, 'ids': [], 'map': {}})

    def test_analytics_units_and_cursor_limitations(self):
        self.assertEqual(body(21)['minterProposalFees'], 25000)
        self.assertIsInstance(body(20)['general']['fpsPrice'], float)
        first, second = body(22), body(36)
        self.assertEqual(first['logs'][0]['count'], '4385')
        self.assertEqual(second['logs'][0]['count'], '4384')
        self.assertNotEqual(first['pageInfo']['endCursor'], second['pageInfo']['endCursor'])
        self.assertNotIn('...', first['pageInfo']['endCursor'])
        self.assertEqual(len(first['pageInfo']['endCursor']), 204)
        self.assertTrue(first['pageInfo']['hasNextPage'])
        self.assertIsInstance(first['logs'][0]['amount'], str)
        for absent in ['totalSupply', 'interestRate', 'mintingTotalV1', 'mintingTotalV2']:
            self.assertNotIn(absent, first['logs'][0])

    def test_daily_rows_ignore_limit_and_use_seconds_with_missing_dates(self):
        daily = body(23)
        self.assertEqual(daily['num'], len(daily['logs']))
        self.assertEqual(daily['num'], 818)
        self.assertNotIn('pageInfo', daily)
        timestamps = [int(row['timestamp']) for row in daily['logs']]
        self.assertEqual(timestamps, sorted(timestamps))
        self.assertTrue(any(b - a > 86400 for a, b in zip(timestamps, timestamps[1:])))
        for row, timestamp in zip(daily['logs'], timestamps):
            self.assertEqual(datetime.fromtimestamp(timestamp, timezone.utc).date().isoformat(), row['date'])
        source = json.loads((ROOT / 'tests/api-docs/reader-source-evidence.json').read_text())
        self.assertEqual(source['commit'], '9013d8fadf2bcc251d236c78328958ebcfbe1c26')
        quotes = [quote for entry in source['sources'] for quote in entry['quotes']]
        self.assertIn('analyticDailyLogs(orderBy: "timestamp", orderDirection: "asc", limit: 1000)', quotes)


if __name__ == '__main__':
    unittest.main()
