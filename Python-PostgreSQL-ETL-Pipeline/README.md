# Python → PostgreSQL ETL Pipeline

A portfolio Data Engineering project demonstrating a reliable ETL workflow with data validation, quarantine, idempotent loading, and run-level monitoring.

> This repository uses synthetic demo data only. No confidential company or healthcare data is included.

## Business problem
Operational source files often contain duplicate IDs, missing required values, invalid dates, inconsistent types, and other data-quality issues. Loading these records directly into reporting tables can produce incorrect dashboards and unreliable KPIs.

This project shows how to validate incoming data before loading it into PostgreSQL, isolate rejected records for investigation, and log every ETL run for monitoring and reconciliation.

## Architecture

```text
CSV / JSON source
      ↓
Python + Pandas ingestion
      ↓
Validation & normalization
      ├── valid rows → PostgreSQL clean table
      └── invalid rows → quarantine table
      ↓
ETL run log
      ↓
Analytics / Power BI
```

## Data-quality rules
The demo pipeline checks for:
- duplicate business IDs;
- missing required fields;
- invalid dates;
- invalid numeric values;
- schema/type inconsistencies.

Rejected rows are not silently deleted. They are stored in a quarantine table together with the rejection reason.

## Reliability features
- Idempotent upsert into the target table
- Data validation before database load
- Quarantine for rejected records
- Run-level logging
- Loaded/rejected row counts
- Error handling with FAILED/SUCCESS status
- PostgreSQL constraints and indexes

## Project structure

```text
Python-PostgreSQL-ETL-Pipeline/
├── README.md
├── requirements.txt
├── data/
│   └── sample_orders.csv
├── src/
│   └── etl_pipeline.py
└── sql/
    └── schema.sql
```

## ETL monitoring
Each execution records:
- run ID;
- start/end timestamps;
- source name;
- rows read;
- rows loaded;
- rows rejected;
- status;
- error message.

This makes the pipeline auditable and provides a foundation for an ETL monitoring dashboard.

## Tech stack
**Python · Pandas · PostgreSQL · SQL · ETL/ELT · Data Quality · Data Validation · Logging**

## Next step
The demo will later be tested against a real-world dataset using the same architecture. Any portfolio results will remain anonymized and will not expose confidential business data.
