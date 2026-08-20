# Monitoring Metrics

## Data Reconciliation

| Metric | Purpose |
|---|---|
| Row Count | Compare physical dataset volume between OLD and NEW |
| Orders | Validate order-level business totals |
| Units | Validate completed/service units |
| Sales | Validate revenue/turnover |
| Unique Products / Analyses | Detect missing or additional product codes |
| Unique Branches | Validate organizational coverage |
| Unique Counterparties | Validate customer/counterparty coverage |
| Difference | NEW - OLD |
| Difference % | Relative variance between NEW and OLD |
| Status | OK / Check based on defined tolerance |

## Data Quality

- NULL values in required fields
- Duplicate keys or rows
- Missing dimension mappings
- Invalid date chronology
- Minimum loaded date
- Maximum loaded date
- Negative or unexpected amounts
- Unexpected categorical values

## Refresh Performance

- Refresh Duration
- Rows Processed
- Rows per Second
- MB per Second
- Processor Time
- Wait Time
- Success Rate
- Average Refresh Duration
- P95 Refresh Duration
- Failed Refresh Count

## Validation Principle

OLD and NEW must be compared for the same reporting period, filters, grain, and business calculation rules. A difference should only be marked as an error when the expected methodology requires equality or the variance exceeds an explicitly defined tolerance.
