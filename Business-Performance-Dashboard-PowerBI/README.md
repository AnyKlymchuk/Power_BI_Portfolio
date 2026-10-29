# Business Performance Dashboard | Power BI

A portfolio case study focused on management reporting, data modeling, DAX, SQL and business-focused data visualization.

## Business problem

Management needs one report to understand:
- How revenue and profit are changing over time
- Which regions and product categories drive performance
- Which customers and segments contribute the most revenue
- Whether order cancellations are increasing
- How current performance compares with the previous year

## Solution

I designed an end-to-end Power BI reporting solution using a star-schema model and reusable DAX measures.

### Data model

**Fact table**
- `Fact_Sales`

**Dimensions**
- `Dim_Date`
- `Dim_Customer`
- `Dim_Product`

Recommended relationships are single-direction `1:*` from dimensions to the fact table.

## Main KPIs

- Total Revenue
- Total Profit
- Profit Margin %
- Orders
- Average Order Value
- Revenue LY
- Revenue YoY %
- Cancelled Orders
- Cancellation Rate %

## Dashboard structure

### KPI cards
Total Revenue | Total Profit | Profit Margin % | Orders | Avg Order Value | Revenue YoY %

### Visuals
- Monthly Revenue Trend
- Revenue & Profit by Region
- Revenue by Product Category
- Top Customers
- Revenue by Customer Segment
- Cancellation Rate

### Slicers
- Date
- Region
- Customer Segment
- Product Category
- Sales Rep

## Tools

- Power BI
- DAX
- Power Query
- SQL / PostgreSQL
- Data Modeling
- Data Visualization
- Business Intelligence

## Data

The project uses a synthetic business dataset with 2,453 sales records so the case can be shared publicly without exposing confidential company information.

## Development workflow

1. Review business questions and KPI definitions
2. Validate source data
3. Build a star-schema model
4. Create reusable DAX measures
5. Design management-focused visuals
6. Add interactive filters
7. Validate report totals against source data
8. Review usability and performance

## Example SQL

See [`sql/portfolio_queries.sql`](sql/portfolio_queries.sql) for monthly performance, regional performance and top-customer queries.

## DAX measures

See [`dax/powerbi_measures.dax`](dax/powerbi_measures.dax).

## What this project demonstrates

This project shows my ability to work beyond visual design: I structure the data model, define business logic, build measures, validate results and create clear reports that support business decisions.

## About me

I am a Power BI / Data Analyst with experience in Power BI, DAX, Power Query, SQL, PostgreSQL, reporting automation and data pipelines.
