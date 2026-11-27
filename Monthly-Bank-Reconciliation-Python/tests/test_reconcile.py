import csv
import json
import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from reconcile import money, read_rows, reconcile, run


def row(identifier,reference='REF',amount='100.00',day=2,account='A',currency='EUR',kind='receipt'):
    return dict(row_id=identifier,reference=reference,parsed_amount=Decimal(amount),
                parsed_date=date(2026,10,day),date=f'2026-10-{day:02d}',
                account_id=account,currency=currency,type=kind)


class MatchingTests(unittest.TestCase):
    def go(self,b,l): return reconcile(b,l,date(2026,10,31))
    def test_exact(self):
        self.assertEqual(self.go([row('B')],[row('L')])[0]['status'],'exact_match')
    def test_amount_precision(self):
        self.assertEqual(money('0.10')+money('0.20'),money('0.30'))
        for value in ['NaN','Infinity','1.001','1,000.00']:
            with self.subTest(value=value), self.assertRaises(ValueError): money(value)
    def test_date_requires_review(self):
        self.assertEqual(self.go([row('B')],[row('L',day=3)])[0]['status'],'date_difference')
    def test_amount_and_fee(self):
        self.assertEqual(self.go([row('B')],[row('L',amount='90')])[0]['difference'],'10.00')
        self.assertEqual(self.go([row('B',kind='fee')],[row('L',amount='90',kind='fee')])[0]['status'],'fee_difference')
    def test_duplicate_on_either_side_consumes_no_arbitrary_pair(self):
        for b,l in [([row('B1'),row('B2')],[row('L')]),([row('B')],[row('L1'),row('L2')])]:
            cases=self.go(b,l)
            self.assertEqual(len(cases),3)
            self.assertTrue(all(r['status']=='duplicate_reference' for r in cases))
    def test_account_and_currency_isolation(self):
        for ledger in [row('L',account='OTHER'),row('L',currency='USD')]:
            self.assertEqual({r['status'] for r in self.go([row('B')],[ledger])},
                             {'missing_in_bank','missing_in_ledger'})
    def test_missing_reference_unique_is_only_candidate(self):
        self.assertEqual(self.go([row('B',reference='')],[row('L',day=4)])[0]['status'],'candidate_match')
    def test_ambiguity_keeps_all_rows_separate(self):
        cases=self.go([row('B1',reference=''),row('B2',reference='')],[row('L',reference='')])
        self.assertEqual(len(cases),3)
        self.assertTrue(all(r['status']=='ambiguous_candidate' for r in cases))
    def test_candidate_window_and_different_nonblank_references(self):
        self.assertEqual(len(self.go([row('B',reference='')],[row('L',day=9)])),2)
        self.assertEqual(len(self.go([row('B')],[row('L',reference='OTHER')])),2)
    def test_offsets_do_not_hide_errors(self):
        cases=self.go([row('B1','X','100'),row('B2','Y','80')],
                      [row('L1','X','90'),row('L2','Y','90')])
        self.assertEqual(sum(Decimal(r['difference']) for r in cases),0)
        self.assertTrue(all(r['status']=='amount_mismatch' for r in cases))


class FileAndControlTests(unittest.TestCase):
    def test_validation_and_fail_fast_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'test.csv'
            header='row_id,account_id,currency,reference,date,amount,type\n'
            p.write_text(header+'B,A,EUR,REF,2026-11-01,20,receipt\n')
            good,bad=read_rows(p,'bank','2026-10')
            self.assertFalse(good)
            self.assertIn('outside',bad[0]['error'])
            p.write_text(header+'B,A,EUR,REF,2026-10-01,20,receipt\nB,A,EUR,R2,2026-10-01,20,receipt\n')
            with self.assertRaises(ValueError): read_rows(p,'bank','2026-10')
    def test_demo_controls_bridge_and_reproducibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            args=[ROOT/'data/bank.csv',ROOT/'data/ledger.csv',ROOT/'data/controls.json','2026-10',tmp]
            a=run(*args)
            self.assertEqual(a,run(*args))
            eur,usd=a['accounts']
            self.assertEqual(eur['closing_difference'],'392.00')
            self.assertEqual(eur['completeness'],'PASS')
            self.assertEqual(eur['bridge_residual'],'0.00')
            self.assertEqual(eur['close_status'],'REVIEW REQUIRED')
            self.assertEqual(usd['close_status'],'READY FOR REVIEW')
            self.assertEqual(len([r for r in a['cases'] if r['bank_id']]),12)
            self.assertEqual(len([r for r in a['cases'] if r['ledger_id']]),10)
            self.assertNotIn('__DATA__',(Path(tmp)/'dashboard.html').read_text())
    def test_independent_count_and_balance_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            c=json.loads((ROOT/'data/controls.json').read_text())
            c['accounts'][0]['expected_bank_rows']=999
            c['accounts'][1]['bank_closing']='2300'
            p=Path(tmp)/'controls.json';p.write_text(json.dumps(c))
            result=run(ROOT/'data/bank.csv',ROOT/'data/ledger.csv',p,'2026-10',Path(tmp)/'out')
            self.assertTrue(all(a['completeness']=='FAIL' for a in result['accounts']))
            self.assertEqual(result['accounts'][1]['bank_control_residual'],'100.00')
    def test_invalid_amount_reported_and_blocks_completeness(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bank.csv'
            p.write_text((ROOT/'data/bank.csv').read_text().replace('1000.00','NaN'))
            result=run(p,ROOT/'data/ledger.csv',ROOT/'data/controls.json','2026-10',Path(tmp)/'out')
            self.assertEqual(result['accounts'][0]['completeness'],'FAIL')
            self.assertEqual(result['invalid_rows'][0]['row_id'],'B001')
    def test_period_mismatch_stops_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            c=json.loads((ROOT/'data/controls.json').read_text());c['month']='2026-11'
            p=Path(tmp)/'controls.json';p.write_text(json.dumps(c))
            with self.assertRaises(ValueError):
                run(ROOT/'data/bank.csv',ROOT/'data/ledger.csv',p,'2026-10',tmp)


if __name__=='__main__': unittest.main()
