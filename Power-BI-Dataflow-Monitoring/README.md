# Power BI Dataflow Monitoring & Validation Dashboard

A portfolio project for monitoring, validating, and comparing legacy and new Power BI dataflows.

## Project Goal

The goal of this project is to build a reusable monitoring layer that helps verify whether migrated or redesigned dataflows:

- return the same business results as legacy dataflows;
- contain complete and valid data;
- refresh successfully and consistently;
- improve refresh performance;
- make discrepancies easy to identify and investigate.

## Dashboard Pages

### 1. Data Reconciliation

Compares OLD and NEW dataflows using the same reporting period and business filters.

Main controls:

- Row count
- Orders
- Units
- Sales
- Price amount
- Unique products / analyses
- Unique branches
- Unique counterparties
- Absolute variance
- Variance %
- Validation status

Example:

| Metric | OLD | NEW | Difference | Difference % | Status |
|---|---:|---:|---:|---:|---|
| Sales | 15,200,000 | 15,200,000 | 0 | 0.00% | OK |
| Units | 182,000 | 181,900 | -100 | -0.05% | Check |

The purpose of this page is to answer one question: **Do the new dataflows return the same business results as the legacy dataflows, and if not, where does the difference come from?**

### 2. Data Quality

Controls the quality and completeness of the loaded data.

Planned checks:

- NULL values in key fields
- Missing order or product keys
- Duplicates
- Invalid dates
- Completion date earlier than creation date
- Missing dimension mappings
- Minimum and maximum loaded date
- Unexpected new values
- Negative or invalid amounts

### 3. Refresh Performance

Compares refresh performance of legacy and new dataflows.

Planned KPIs:

- Refresh Duration
- Rows Processed
- Rows per Second
- MB per Second
- Processor Time
- Wait Time
- Success Rate
- Average Refresh Duration
- P95 Refresh Duration
- Refresh Failures

### 4. Monitoring Overview

Executive monitoring page combining the most important validation indicators.

Example indicators:

- Dataflows checked
- Reconciliation passed / failed
- Data quality score
- Refresh success rate
- Performance improvement
- Last successful refresh
- Last loaded data date

## Suggested Architecture

```text
Legacy Dataflow ---------\
                         > Validation Layer -> Power BI Monitoring Dashboard
New Dataflow ------------/

Validation Layer
  -> Data Reconciliation
  -> Data Quality
  -> Refresh Performance
  -> Monitoring Overview
```

## Repository Structure

```text
Power-BI-Dataflow-Monitoring/
├── README.md
├── dashboard/
│   └── README.md
├── screenshots/
│   └── README.md
├── sample-data/
│   └── README.md
└── documentation/
    └── metrics.md
```

## Portfolio Safety

This repository must not contain confidential production data. The public portfolio version should use anonymized or synthetic data only. Company names, patient/customer names, internal identifiers, production URLs, credentials, and sensitive business information must not be published.

## Technologies

- Microsoft Power BI
- Power Query
- DAX
- Power BI Dataflows
- Data validation / reconciliation
- Data quality monitoring
- Refresh performance monitoring

## Status

**In progress.**

Current phase: design and implementation of the **Data Reconciliation** page.

## Next Steps

1. Build the OLD vs NEW reconciliation dataset.
2. Create reconciliation measures and status rules.
3. Design the first Power BI page.
4. Add data quality checks.
5. Add refresh-performance history.
6. Replace production data with synthetic demo data for the public portfolio version.
7. Add dashboard screenshots and the final PBIX file.
