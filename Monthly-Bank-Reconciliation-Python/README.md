# Monthly Bank Reconciliation — Python

A portfolio demonstration by Anna Klymchuk. Compare a monthly bank statement with an internal cash ledger from a second system, identify exceptions, and prepare evidence for the month-end reviewer.

**All sample data is synthetic.** This is an independently built demonstration, not a bank deployment or a reproduction of a confidential interview task. No measured client savings or production performance are claimed.

## Run

Python 3.10+; no external packages required. From this project directory:

```bash
python reconcile.py --month 2026-10
python -m unittest discover -s tests -v
```

Open `output/dashboard.html` in a browser. It works offline and includes account/currency selection, status filters, a searchable exception queue, closing balances, a balance bridge, and source controls.

For another month, supply the monthly CSVs and an independent controls file:

```bash
python reconcile.py --bank private_data/bank.csv --ledger private_data/ledger.csv --controls private_data/controls.json --month 2026-11 --out client_output/2026-11
```

The tool writes reports, never changes the inputs or posts accounting adjustments. It overwrites files in the specified output directory on a rerun; use a separate directory for each retained run.

## Algorithm

1. Agree the scope: account mapping, currency, period, sign convention, source completeness and reference semantics. Both sources must represent the same cash account from the company's perspective.
2. Load CSVs, retain source IDs/line numbers, and hash all input files for reproducibility.
3. Require stable unique row IDs, ISO dates, known transaction types, and finite decimal amounts with at most two decimal places. Invalid business rows go to `invalid_rows.csv`; broken schemas and duplicate/missing row IDs stop the run.
4. Group nonblank references by account + currency + normalized reference. Any repeated reference on either side becomes a review exception; do not delete or pick an arbitrary row.
5. Pair unique references one-to-one. Compare signed amounts first, then dates. Same amount/date is an exact match; amount differences, fee differences and date differences remain exceptions.
6. For remaining rows with a blank reference on at least one side, propose candidates with the same account, currency, signed amount and type within three calendar days. Only a mutually unique candidate is paired, and it still requires approval. Ambiguous candidates stay separate. Different nonblank references are never matched automatically.
7. Classify unmatched rows as missing in bank or missing in ledger. This means absent from the supplied monthly extract, not proven missing or erroneous in the underlying system. Inspect adjacent periods for timing items.
8. Verify each source's opening + movement = closing, expected row counts, and rejected rows. Independently reconcile the balance bridge by account/currency. A zero net difference does not prove transaction-level reconciliation.
9. Export all cases, exceptions, rejected rows, account summaries, run metadata and the dashboard. Assign investigation, attach supporting evidence, and obtain reviewer approval outside the demo.

## Data contract

| Column | Meaning |
| --- | --- |
| row_id | Unique nonblank source row ID; bank and ledger IDs may differ |
| account_id | Common mapped cash account identifier in both systems |
| currency | Uppercase three-letter code; demo supports currencies with two decimal places |
| reference | Shared transaction reference; blank is allowed but never auto-approved |
| date | `YYYY-MM-DD` posting date, inside selected month |
| amount | Dot-decimal, signed: inflow positive, outflow negative; no separators |
| type | `receipt`, `payment`, `fee` or `transfer` |

`data/controls.json` contains independently obtained opening/closing balances and expected raw row counts by account/currency. In real work obtain these from source control reports, not from the imported rows: calculated input controls would hide incomplete extracts. Account mapping and debit/credit sign conversion must happen before this program. Empty extracts can be legitimate when the independent expected count is zero.

## Included demonstration

October 2026 has 12 bank rows and 10 ledger rows across EUR and USD accounts. The EUR closing difference is **392.00**; USD is balanced. The scenario includes offsetting/small fee errors, an amount difference, posting delay, a repeated reference, missing items and ambiguous reference-free matches. USD and EUR are never added together.

## Outputs

| File | Purpose |
| --- | --- |
| reconciliation.csv | Every valid row accounted for in a case, with source IDs and signed bank-minus-ledger difference |
| exceptions.csv | Cases requiring review, excluding invalid source rows |
| invalid_rows.csv | Rejected source rows and reasons; always review alongside exceptions |
| summary.csv | One row per account/currency/month with balances and completeness checks |
| run.json | Rules, input hashes, results and controls |
| dashboard.html | Generated interactive offline report |

See [Power BI build guide](docs/POWER_BI.md), [monthly operating procedure](docs/MONTH_END.md), and [Upwork portfolio and service drafts](docs/FREELANCE.md).

## Boundaries and next steps

This prototype handles one-to-one matching and monthly cash balances. It does not implement many-to-one settlements, FX conversion, cross-month automatic matching, bank API connections, reviewer authentication, persistent workflow or automatic journal posting. Date differences are not automatically accepted. Fee classification uses a provided transaction type, not a verified fee contract. Repeated references may be legitimate and need review. The missing-reference candidate search is quadratic; use indexed SQL for large volumes. Accounting materiality and approval controls must be agreed before client use. Current reports have no persisted owner edits or approval history.

Suggested next iteration: approved account/reference mapping, external reconciliation decision log, adjacent-period carry-forward, indexed SQL matching, then Power BI refresh. Financial values use Python `Decimal`; dashboard formatting uses browser numbers for display only.
