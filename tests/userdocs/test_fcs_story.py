"""FCS narrative regressions, not deployment or UI availability tests.

The baseline contains extracted starting-revision anchors and API code hashes.
Tests guard the document architecture while source-boundary tests guard mechanics.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
BASELINE = json.loads((Path(__file__).parent / 'story-baseline.json').read_text())
spec = importlib.util.spec_from_file_location('story_links', ROOT / 'scripts/check-userdocs.py')
assert spec is not None and spec.loader is not None
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def page(path):
    return (ROOT / path).read_text()


def opening(text):
    text = re.sub(r'\A---\n.*?\n---\n', '', text, flags=re.S)
    text = re.sub(r'^#{1,6} .*$|^<a [^>]+></a>\s*$', '', text, flags=re.M)
    return next(part for part in text.split('\n\n') if part.strip()).strip()


def canonical_first(text):
    intro = opening(text)
    return ('FCS' in intro and 'canonical governance' in intro and
            ('FPS' not in intro or intro.index('FCS') < intro.index('FPS')))


class CanonicalStory(unittest.TestCase):
    def test_core_pages_lead_with_canonical_fcs(self):
        for name in ['pool-shares.md', 'fcs.md', 'governance.md', 'api-docs/fcs.md']:
            with self.subTest(page=name):
                self.assertTrue(canonical_first(page(name)))
                heading = re.search(r'^# (.+)$', page(name), re.M)
                assert heading is not None
                self.assertIn('FCS', heading.group(1))
        overview = page('README.md')
        self.assertIn('## Frankencoin (ZCHF) and Frankencoin Share Token (FCS)', overview)
        token_table = overview.split('| Token | Role |', 1)[1].split('\n\n', 1)[0]
        self.assertIn('Frankencoin Share Token (FCS)', token_table)
        self.assertNotIn('Frankencoin Pool Shares (FPS)', token_table)

    def test_late_or_optional_fcs_is_not_a_canonical_opening(self):
        self.assertFalse(canonical_first('# Shares\n\nFPS leads.\n\nFCS is the canonical governance token.'))
        self.assertFalse(canonical_first('# Shares\n\nFCS adds an optional wrapper over FPS.'))
        self.assertFalse(canonical_first('# Shares\n\nFPS remains primary; FCS is the canonical governance token.'))

    def test_navigation_has_one_primary_share_journey(self):
        nav = page('SUMMARY.md')
        self.assertIn('* [📈 FCS: Investing and Pool Shares](pool-shares.md)', nav)
        self.assertIn('* [⚖️ FCS Governance](governance.md)', nav)
        self.assertIn('  * [FCS Mechanics](fcs.md)', nav)
        self.assertIn('  * [Underlying FPS Reference](fps-reference.md)', nav)
        self.assertNotRegex(nav, r'(?m)^\* \[[^\]]*(?:FPS|Legacy)[^\]]*\]')
        self.assertLess(nav.index('(pool-shares.md)'), nav.index('(fps-reference.md)'))
        self.assertLess(nav.index('(api-docs/fcs.md)'), nav.index('(api-docs/ecosystem.md)'))
        self.assertEqual(1, nav.count('(pool-shares.md)'))

    def test_acquisition_voting_and_exits_precede_background(self):
        text = page('pool-shares.md')
        headings = ['### Acquire FCS', '### Participate in governance',
                    '### Exit an FCS holding', '## Economics', '## Underlying FPS']
        offsets = [text.index(heading) for heading in headings]
        self.assertEqual(sorted(offsets), offsets)
        for phrase in ['Invest ZCHF', 'Buy existing FCS', 'Migrate existing shares',
                       'Redeem into ZCHF', 'Sell existing FCS', 'Unwrap into FPS',
                       'Approval alone does not create shares',
                       'no separate personal 90-day FCS redemption wait']:
            self.assertIn(phrase, text)
        self.assertNotIn('Historical FPS investment interface', text)
        self.assertIn('Historical FPS investment interface', page('fps-reference.md'))

    def test_cross_page_connections_use_fcs_without_relabelling_fps(self):
        expected = {
            'reserve.md': ['FCS holders', 'does not create a separate reserve'],
            'savings.md': ['FCS governance', 'does not acquire FCS or voting power'],
            'positions/README.md': ['FCS holders', 'Borrowers do not need FCS'],
            'positions/open.md': ['FCS governance', '1,000 ZCHF', '1,200 ZCHF and 60 days'],
            'risks.md': ['Qualified FCS holders', 'Equity exposure'],
            'telegram-api-bot.md': ['FCS holders', 'does not submit a transaction'],
            'bridge-to-other-chains.md': ['governance and share token', 'not a spendable FCS balance'],
            'api-docs/README.md': ['canonical governance and share token', 'FPS routes remain'],
        }
        for name, phrases in expected.items():
            for phrase in phrases:
                with self.subTest(page=name, phrase=phrase):
                    self.assertIn(phrase, page(name))
        faq = page('faq.md')
        self.assertLess(faq.index('### What does FCS represent?'),
                        faq.index('### What are Frankencoin Pool Share (FPS) tokens?'))

    def test_legacy_identifiers_and_units_remain_exact(self):
        expected = {
            'fps-reference.md': ['0x1bA26788dfDe592fec8bcB0Eaff472a42BE341B2',
                                 'p = 3 × K / s', '300 ZCHF per FPS',
                                 '7,300 FPS-days', '7,000 FPS-days', '2% quorum'],
            'fcs.md': ['Frankencoin Pool Shares 2', '`FPS2`', '**FPS1**',
                       'FPS1.relativeVotes(address(this)) * 3 > 2e18',
                       'FCS.totalSupply() / FPS1.totalSupply()'],
            'governance.md': ['GovernanceSender.pushVotes', 'MainnetVotes.pushFPS2Votes',
                              'BridgedVotes', 'more than 1%', 'at least 2% of FPS voting power'],
            'api-docs/ecosystem.md': ['/ecosystem/fps/info', 'ZCHF per FPS'],
            'api-docs/prices.md': ['/prices/erc20/fps', 'not an FCS market price'],
            'api-docs/analytics.md': ['fpsTotalSupply', 'fpsPrice', 'earningsPerFPS',
                                     '/analytics/fps/exposure', '/analytics/fps/earnings'],
        }
        for name, phrases in expected.items():
            for phrase in phrases:
                with self.subTest(page=name, phrase=phrase):
                    self.assertIn(phrase, page(name))

    def test_migration_keeps_holder_and_wrapper_votes_separate(self):
        text = page('fcs-migration.md')
        for phrase in ['canonical governance and share token', 'Two voting records',
                       'do not give the wrapper the same accumulated legacy age',
                       'no accumulated votes to carry over from WFPS', 'without immediate votes',
                       'Approval alone does not migrate']:
            self.assertIn(phrase, text)
        self.assertIn('two synchronisations', page('governance.md'))
        self.assertIn('vote snapshots, not tokens', page('governance.md'))

    def test_new_reference_is_in_link_and_format_checker_scope(self):
        report = checker.check(ROOT)
        self.assertEqual(19, report['files'])
        self.assertFalse(report['errors'])
        self.assertFalse(report['pending'])
        self.assertIn('fps-reference.md', [p.name for p in ROOT.glob('*.md')])

    def test_whole_markdown_inventory_is_accounted_for(self):
        observed = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*.md')
                    if '.git' not in p.relative_to(ROOT).parts}
        self.assertEqual(set(BASELINE['anchors']) | {'fps-reference.md'}, observed)

    def test_existing_heading_fragments_survive_restructure(self):
        for name, previous in BASELINE['anchors'].items():
            with self.subTest(page=name):
                self.assertFalse(set(previous) - checker.anchors(page(name)))

    def test_api_code_blocks_are_unchanged_from_tested_base(self):
        for name, expected in BASELINE['api_fence_sha256'].items():
            blocks = re.findall(r'^```[^\n]*\n.*?^```\s*$', page(name), re.M | re.S)
            digest = hashlib.sha256('\n'.join(blocks).encode()).hexdigest()
            self.assertEqual(expected, digest, name)


if __name__ == '__main__':
    unittest.main()
