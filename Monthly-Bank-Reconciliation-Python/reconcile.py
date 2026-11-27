"""Monthly statement/ledger reconciliation. Python 3.10+, standard library only."""
import argparse
import calendar
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = {'row_id', 'account_id', 'currency', 'reference', 'date', 'amount', 'type'}
FIELDS = ['case_id', 'account_id', 'currency', 'status', 'bank_id', 'ledger_id',
          'reference', 'bank_date', 'ledger_date', 'bank_amount', 'ledger_amount',
          'difference', 'age_days', 'suggested_owner', 'action']
POLICY = {
    'exact_match': ('Automation', 'No action; retain evidence'),
    'date_difference': ('Finance', 'Check posting/value date; approve timing classification'),
    'amount_mismatch': ('Finance', 'Investigate amount/sign; obtain correction approval'),
    'fee_difference': ('Finance', 'Check fee agreement and posting'),
    'missing_in_ledger': ('Finance', 'Check missing posting or timing; do not post automatically'),
    'missing_in_bank': ('Operations', 'Check settlement, statement coverage or next period'),
    'duplicate_reference': ('Data team', 'Review repeated reference; never delete automatically'),
    'candidate_match': ('Finance', 'Missing reference: verify candidate manually'),
    'ambiguous_candidate': ('Finance', 'Multiple possible matches; inspect source evidence'),
    'invalid_row': ('Data team', 'Correct source validation issue and rerun'),
}


def money(value):
    """Strict dot-decimal, two-decimal currency contract; no silent rounding."""
    try:
        number = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError('Invalid decimal amount') from exc
    if not number.is_finite() or number != number.quantize(Decimal('.01')):
        raise ValueError('Use finite amounts with at most two decimal places')
    return number


def read_rows(path, source, month):
    valid, invalid = [], []
    seen = set()
    with Path(path).open(newline='', encoding='utf-8-sig') as handle:
        reader = csv.DictReader(handle)
        if not REQUIRED.issubset(reader.fieldnames or []):
            raise ValueError(f'{source}: missing columns {sorted(REQUIRED-set(reader.fieldnames or []))}')
        for line, raw in enumerate(reader, 2):
            row = {k: (v or '').strip() for k, v in raw.items() if k is not None}
            row.update(source=source, source_line=line)
            # A source row ID must be stable and unique, even for rejected rows.
            if not row['row_id'] or row['row_id'] in seen:
                raise ValueError(f'{source} line {line}: missing or repeated row_id')
            seen.add(row['row_id'])
            try:
                if not row['account_id'] or not re.fullmatch(r'[A-Z]{3}', row['currency']):
                    raise ValueError('Account is required; currency must be three uppercase letters')
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',row['date']):
                    raise ValueError('Date must use YYYY-MM-DD')
                row['parsed_date'] = date.fromisoformat(row['date'])
                if row['parsed_date'].strftime('%Y-%m') != month:
                    raise ValueError('Date outside selected month; supply monthly files only')
                row['parsed_amount'] = money(row['amount'])
                if row['type'] not in {'payment', 'receipt', 'fee', 'transfer'}:
                    raise ValueError('Unknown transaction type')
                # Only case and outer whitespace are normalized. Punctuation stays meaningful.
                row['reference'] = row['reference'].upper()
                valid.append(row)
            except (ValueError, InvalidOperation) as exc:
                row['error'] = str(exc)
                invalid.append(row)
    return valid, invalid


def key(row):
    return row['account_id'], row['currency'], row['reference']


def reconcile(bank, ledger, as_of, window_days=3):
    """One-to-one reference matching; unreferenced candidates require human review."""
    output, used_b, used_l = [], set(), set()
    def emit(status, b=None, l=None):
        row = b or l
        ba = b['parsed_amount'] if b else Decimal('0')
        la = l['parsed_amount'] if l else Decimal('0')
        owner, action = POLICY[status]
        output.append(dict(zip(FIELDS, [f'CASE-{len(output)+1:04d}', row['account_id'],
            row['currency'], status, b['row_id'] if b else '', l['row_id'] if l else '',
            row['reference'], b['date'] if b else '', l['date'] if l else '',
            str(ba), str(la), str(ba-la),
            (as_of-min(x['parsed_date'] for x in (b,l) if x)).days, owner, action])))
        if b: used_b.add(b['row_id'])
        if l: used_l.add(l['row_id'])
    bg, lg = defaultdict(list), defaultdict(list)
    for r in bank:
        if r['reference']: bg[key(r)].append(r)
    for r in ledger:
        if r['reference']: lg[key(r)].append(r)
    for k in sorted(set(bg) | set(lg)):
        bs, ls = bg[k], lg[k]
        if len(bs)>1 or len(ls)>1:
            for b in bs: emit('duplicate_reference', b=b)
            for l in ls: emit('duplicate_reference', l=l)
        elif bs and ls:
            b,l=bs[0],ls[0]
            if b['parsed_amount'] != l['parsed_amount']:
                status='fee_difference' if b['type']==l['type']=='fee' else 'amount_mismatch'
            elif b['parsed_date'] != l['parsed_date']:
                status='date_difference'
            else: status='exact_match'
            emit(status,b,l)
    remaining_b=[r for r in bank if r['row_id'] not in used_b]
    remaining_l=[r for r in ledger if r['row_id'] not in used_l]
    edges, reverse=defaultdict(list),defaultdict(list)
    for b in remaining_b:
        for l in remaining_l:
            if (not b['reference'] or not l['reference']) and (
                b['account_id'],b['currency'],b['parsed_amount'],b['type']) == (
                l['account_id'],l['currency'],l['parsed_amount'],l['type']) and abs(
                (b['parsed_date']-l['parsed_date']).days)<=window_days:
                edges[b['row_id']].append(l)
                reverse[l['row_id']].append(b)
    for b in remaining_b:
        candidates=edges[b['row_id']]
        if len(candidates)==1 and len(reverse[candidates[0]['row_id']])==1:
            emit('candidate_match',b,candidates[0])
        elif candidates: emit('ambiguous_candidate',b=b)
        else: emit('missing_in_ledger',b=b)
    for l in remaining_l:
        if l['row_id'] not in used_l:
            emit('ambiguous_candidate' if reverse[l['row_id']] else 'missing_in_bank',l=l)
    assert len(used_b)==len(bank) and len(used_l)==len(ledger), 'Unaccounted source rows'
    assert sum((Decimal(r['difference']) for r in output),Decimal(0)) == (
        sum((r['parsed_amount'] for r in bank),Decimal(0))-
        sum((r['parsed_amount'] for r in ledger),Decimal(0)))
    return output


def write_csv(path, rows, fields):
    with Path(path).open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=fields,extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def run(bank_path, ledger_path, controls_path, month, out, window_days=3):
    if not re.fullmatch(r'\d{4}-\d{2}',month): raise ValueError('Month must be YYYY-MM')
    y,m=map(int,month.split('-'))
    as_of=date(y,m,calendar.monthrange(y,m)[1])
    if window_days<0: raise ValueError('Date window must be nonnegative')
    bank,bad_b=read_rows(bank_path,'bank',month)
    ledger,bad_l=read_rows(ledger_path,'ledger',month)
    cases=reconcile(bank,ledger,as_of,window_days)
    controls=json.loads(Path(controls_path).read_text())
    if controls['month']!=month: raise ValueError('Control period differs from run period')
    group_controls={}
    for c in controls['accounts']:
        k=(c['account_id'],c['currency'])
        if k in group_controls: raise ValueError('Repeated account/currency in controls')
        group_controls[k]=c
    all_rows=bank+ledger+bad_b+bad_l
    unknown={(r['account_id'],r['currency']) for r in all_rows}-set(group_controls)
    if unknown: raise ValueError(f'Accounts/currencies missing in controls: {sorted(unknown)}')
    summaries=[]
    for (account,currency),c in sorted(group_controls.items()):
        def scoped(rows): return [r for r in rows if (r['account_id'],r['currency'])==(account,currency)]
        bs,ls,br,lr=scoped(bank),scoped(ledger),scoped(bad_b),scoped(bad_l)
        cc=[r for r in cases if (r['account_id'],r['currency'])==(account,currency)]
        bm=sum((r['parsed_amount'] for r in bs),Decimal(0))
        lm=sum((r['parsed_amount'] for r in ls),Decimal(0))
        bo,bc,lo,lc=[money(c[f]) for f in ['bank_opening','bank_closing','ledger_opening','ledger_closing']]
        bank_residual=bc-bo-bm
        ledger_residual=lc-lo-lm
        counts_ok=(len(bs)+len(br)==c['expected_bank_rows'] and len(ls)+len(lr)==c['expected_ledger_rows'])
        complete=counts_ok and not br and not lr and bank_residual==0 and ledger_residual==0
        exceptions=sum(r['status']!='exact_match' for r in cc)+len(br)+len(lr)
        summaries.append(dict(account_id=account,currency=currency,month=month,
            bank_rows=len(bs)+len(br),ledger_rows=len(ls)+len(lr),
            expected_bank_rows=c['expected_bank_rows'],expected_ledger_rows=c['expected_ledger_rows'],
            invalid_rows=len(br)+len(lr),bank_opening=str(bo),bank_closing=str(bc),
            ledger_opening=str(lo),ledger_closing=str(lc),bank_movement=str(bm),ledger_movement=str(lm),
            closing_difference=str(bc-lc),opening_difference=str(bo-lo),
            transaction_difference=str(bm-lm),bank_control_residual=str(bank_residual),
            ledger_control_residual=str(ledger_residual),
            bridge_residual=str((bc-lc)-(bo-lo)-(bm-lm)),
            completeness='PASS' if complete else 'FAIL',
            exact_bank_rows=sum(r['status']=='exact_match' and bool(r['bank_id']) for r in cc),
            exceptions=exceptions,close_status='READY FOR REVIEW' if complete and exceptions==0 and bc==lc else 'REVIEW REQUIRED'))
    invalid=[]
    for r in bad_b+bad_l:
        invalid.append({k:v for k,v in r.items() if not k.startswith('parsed_')})
    result={'month':month,'as_of':as_of.isoformat(),'rule_version':'1.0',
            'date_window_days':window_days,'accounts':summaries,'cases':cases,'invalid_rows':invalid,
            'inputs':{str(Path(p).name):hashlib.sha256(Path(p).read_bytes()).hexdigest()
                      for p in [bank_path,ledger_path,controls_path]}}
    out=Path(out)
    out.mkdir(parents=True,exist_ok=True)
    write_csv(out/'reconciliation.csv',cases,FIELDS)
    write_csv(out/'exceptions.csv',[r for r in cases if r['status']!='exact_match'],FIELDS)
    write_csv(out/'summary.csv',summaries,list(summaries[0]) if summaries else ['account_id'])
    write_csv(out/'invalid_rows.csv',invalid,['source','source_line',*sorted(REQUIRED),'error'])
    (out/'run.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    template=Path(__file__).with_name('dashboard_template.html').read_text(encoding='utf-8')
    payload=json.dumps(result).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    (out/'dashboard.html').write_text(template.replace('__DATA__',payload),encoding='utf-8')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bank',default='data/bank.csv')
    parser.add_argument('--ledger',default='data/ledger.csv')
    parser.add_argument('--controls',default='data/controls.json')
    parser.add_argument('--month',default='2026-10')
    parser.add_argument('--out',default='output')
    parser.add_argument('--date-window-days',type=int,default=3)
    args=parser.parse_args()
    result=run(args.bank,args.ledger,args.controls,args.month,args.out,args.date_window_days)
    for account in result['accounts']:
        print(f"{account['account_id']} {account['currency']}: {account['close_status']}; "
              f"closing difference {account['closing_difference']}; exceptions {account['exceptions']}")
