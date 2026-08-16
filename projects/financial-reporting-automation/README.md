# Automated Financial Reporting System

**Power BI | SQL | Power Query | DAX | Financial Reporting | Data Quality**

## Project Overview

This portfolio project demonstrates an end-to-end financial reporting solution: from a business problem and raw transactional data to an automated Power BI reporting system.

The solution is designed to replace manual Excel-based reporting with a structured analytical model for **P&L, Cash Flow, Budget vs Actual and management KPIs**.

### End-to-End Workflow

**Business Problem → Raw Data → SQL / Power Query → Data Cleaning → Data Model → DAX → P&L / Cash Flow / KPI → Power BI → Automated Refresh → Error Detection & Troubleshooting**

## Business Problem

A company stores financial and operational data across multiple sources. Management reporting is prepared manually, which creates several problems:

- reporting takes too much time;
- financial figures may not reconcile;
- duplicated or missing transactions can affect KPIs;
- budget and actual data are difficult to compare;
- reporting logic is distributed across spreadsheets;
- management does not have a single reliable view of business performance.

## Project Goal

Build an automated financial reporting system that:

- integrates multiple data sources;
- cleans and validates raw data;
- creates a scalable star-schema data model;
- automates financial calculations;
- provides P&L and Cash Flow reporting;
- compares Actual vs Budget;
- monitors key business KPIs;
- identifies data-quality and reporting issues;
- supports scheduled refresh in Power BI.

## Data Sources

The project uses a realistic synthetic business dataset containing:

| Dataset | Purpose |
|---|---|
| Customers | Customer master data and segmentation |
| Products | Product catalogue and cost information |
| Orders | Sales order headers |
| Order Lines | Products, quantities, prices and discounts |
| Payments | Customer payments and cash inflows |
| Expenses | Operating expenses by category and department |
| Accounts | Financial account mapping |
| Budget | Monthly budget by department and account |

The raw dataset will intentionally contain common real-world data-quality problems such as duplicates, NULL values, inconsistent categories, incorrect data types, unmatched transactions and reconciliation differences.

## Data Transformation

### SQL

SQL is used for staging, joins, validation and preparation of analytical datasets.

Planned transformations include:

- duplicate detection;
- NULL handling;
- transaction validation;
- customer and product joins;
- account mapping;
- aggregation and reconciliation checks.

### Power Query

Power Query is used for ETL transformations before loading data into the semantic model:

- data type correction;
- column standardization;
- category normalization;
- error handling;
- reference table mapping;
- calculated transformation columns;
- data-quality checks.

## Data Model

The Power BI model follows a star-schema approach.

```text
                 Dim_Date
                    |
                    |
Dim_Customer -- Fact_Sales -- Dim_Product
                    |
                    |
               Dim_Account
                    |
              Fact_Budget

Dim_Date ------ Fact_Expenses
     |
     +--------- Fact_CashFlow
```

### Fact Tables

- Fact_Sales
- Fact_Expenses
- Fact_Budget
- Fact_CashFlow

### Dimension Tables

- Dim_Date
- Dim_Customer
- Dim_Product
- Dim_Account
- Dim_Department

## DAX Measures

The semantic model will include financial and management measures such as:

### Profit & Loss

- Revenue
- COGS
- Gross Profit
- Gross Margin %
- Operating Expenses
- EBITDA
- EBITDA Margin %
- Net Profit

### Budget Analysis

- Actual
- Budget
- Variance
- Variance %

### Cash Flow

- Cash In
- Cash Out
- Net Cash Flow
- Opening Cash
- Closing Cash

### Business KPIs

- Orders
- Customers
- Average Order Value
- Revenue YTD
- Revenue YoY
- Rolling 12M Revenue

## Power BI Report

The final report will contain five core pages.

### 1. Executive Overview

Management overview of Revenue, EBITDA, Net Profit, Cash, Budget Variance and major trends.

### 2. P&L Statement

Interactive Profit & Loss statement with monthly and yearly analysis.

### 3. Cash Flow

Cash inflows, cash outflows, net cash movement and closing cash position.

### 4. Budget vs Actual

Comparison of actual financial performance against budget by month, department and account.

### 5. Data Quality Monitor

A dedicated monitoring page for:

- duplicate transactions;
- missing mappings;
- unmatched payments and orders;
- invalid values;
- reconciliation differences;
- refresh status.

## Automation

The final solution is designed for automated Power BI refresh rather than manual report preparation.

The reporting pipeline will demonstrate how new source data can flow through transformation, validation, the semantic model and financial reports with minimal manual intervention.

## Troubleshooting & Data Quality

A major part of this project is not only dashboard development but investigation of reporting problems.

Example scenarios will include:

1. Revenue does not match source-system totals.
2. Duplicate transactions inflate sales.
3. Payments exist without matching orders.
4. Account mappings are missing.
5. Incorrect data types break refresh.
6. Budget categories do not match actual categories.
7. Business logic produces inconsistent KPI results.

Each scenario will document the issue, root cause, fix and validation method.

## Repository Structure

```text
financial-reporting-automation/
|
|-- README.md
|-- data/
|   |-- raw/
|   `-- processed/
|-- sql/
|-- power-query/
|-- dax/
|-- documentation/
|-- screenshots/
`-- power-bi/
```

## Tools & Technologies

- Power BI
- DAX
- Power Query / M
- SQL
- Data Modeling
- Financial Reporting
- Data Validation
- Data Quality Analysis
- ETL
- Automated Refresh

## Skills Demonstrated

This project demonstrates the ability to translate a business reporting problem into a complete BI solution, including requirements analysis, data preparation, financial modeling, dashboard development, automation and troubleshooting.

## Project Status

**In development.**

### Next Steps

- [ ] Create synthetic raw datasets
- [ ] Add intentional data-quality issues
- [ ] Build SQL staging layer
- [ ] Create Power Query transformations
- [ ] Build star-schema model
- [ ] Create DAX measures
- [ ] Build Executive Overview
- [ ] Build P&L Statement
- [ ] Build Cash Flow report
- [ ] Build Budget vs Actual analysis
- [ ] Build Data Quality Monitor
- [ ] Configure refresh workflow
- [ ] Add screenshots and model diagram
- [ ] Document troubleshooting cases

---

**Author:** Anna Klymchuk  
**Role:** Power BI Developer / Data Analyst