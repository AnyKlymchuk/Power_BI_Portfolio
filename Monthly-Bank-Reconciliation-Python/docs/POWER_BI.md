# Power BI dashboard template / build guide

The working dashboard is `output/dashboard.html`. This folder provides a Power BI build specification and measures; no `.pbix` or `.pbit` file is included.

## Import and model

Import `summary.csv` as `Summary` and `reconciliation.csv` as `Reconciliation`. Set dates to Date, financial fields to Fixed Decimal Number, counts/age to Whole Number, and IDs to Text. Import `invalid_rows.csv` separately for a validation detail page. Do not use a transaction-date slicer on the month-level closing balance.

For recurring runs, append a `month` column to each transaction case based on its run.json; retain one approved run per month to avoid duplicate versions. Create a PeriodAccount dimension containing distinct month/account_id/currency combinations and a stable composite key in both facts (use unambiguous JSON serialization or agreed escaping). Set one-to-many, single-direction relationships from the dimension to both facts. Do not relate the facts directly or use a many-to-many account-only relationship. With the one-month demo, account + currency is enough.

Use single-select currency and account slicers and one reporting month. Balances are snapshots: do not sum them over multiple months. Use filters from PeriodAccount so both fact tables are scoped consistently.

## Measures

```dax
Bank Closing =
IF(COUNTROWS(Summary) = 1, SUM(Summary[bank_closing]))

Ledger Closing =
IF(COUNTROWS(Summary) = 1, SUM(Summary[ledger_closing]))

Closing Difference =
IF(COUNTROWS(Summary) = 1, SUM(Summary[closing_difference]))

Exact Bank Match Rate =
IF(COUNTROWS(Summary) = 1,
    DIVIDE(SUM(Summary[exact_bank_rows]), SUM(Summary[bank_rows])))

Open Cases Including Invalid =
IF(COUNTROWS(Summary) = 1, SUM(Summary[exceptions]))

Exception Cases =
CALCULATE(COUNTROWS(Reconciliation),
    Reconciliation[status] <> "exact_match")

Absolute Case Difference =
IF(COUNTROWS(Summary) = 1,
    SUMX(FILTER(Reconciliation, Reconciliation[status] <> "exact_match"),
         ABS(Reconciliation[difference])))
```

`Absolute Case Difference` is a review-volume measure, not net missing cash. Duplicated-reference rows on both sides are separate review cases; their absolute differences can overstate economic exposure. Candidate/date cases can have zero difference and still be open. Use summary exception count to include validation rejects.

## One-page layout

Top: account, currency, reporting month and close status. Cards: bank closing, ledger closing, closing difference, exact bank match rate. Middle: exceptions by reason and balance bridge/source checks. Bottom: searchable/drillable case table with IDs, dates, amounts, difference, age, suggested owner and action. Separate invalid-row detail if needed.

Suggested colors: navy `#102C3A`, teal `#23A795`, amber `#B36B20`, background `#F0F4F7`. Label synthetic data prominently. Export actual screenshots only after building and verifying the Power BI report; the included browser dashboard must not be presented as a completed Power BI implementation.
