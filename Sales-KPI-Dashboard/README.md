# Sales KPI Dashboard in Power BI

A compact Power BI portfolio project focused on sales performance, profitability, target tracking, and business-friendly reporting.

## Business questions

- How much revenue and profit did the business generate?
- Are we above or below monthly revenue and profit targets?
- Which regions, categories, and sales channels perform best?
- How are revenue and profit changing over time?
- What is the average order value and profit margin?

## Data

The project uses synthetic data created only for portfolio/demo purposes.

Files:
- `data/sales.csv` — order-level sales data
- `data/targets.csv` — monthly revenue and profit targets

## Recommended dashboard page

### KPI cards
- Revenue
- Profit
- Profit Margin %
- Orders
- Average Order Value
- Revenue vs Target %

### Visuals
1. Line chart — Revenue by Month
2. Clustered column chart — Revenue vs Revenue Target by Month
3. Bar chart — Revenue by Region
4. Bar chart — Profit by Category
5. Donut chart — Revenue by Channel
6. Matrix — Region × Category with Revenue, Profit and Margin

### Slicers
- Date
- Region
- Category
- Channel

## Data model

Create a Date table and relate:
- `Date[Date]` -> `sales[Date]`
- `Date[MonthStart]` -> `targets[Month]`

Use a one-to-many relationship from Date to sales and Date/MonthStart to targets.

## Portfolio publication without Power BI Service

You do **not** need Power BI Service authorization for this portfolio project.

1. Build the report in Power BI Desktop.
2. Save the file as `Sales_KPI_Dashboard.pbix`.
3. Export or capture 1–3 clean dashboard screenshots.
4. Record a 60–90 second walkthrough video.
5. Add the PBIX, screenshots, and video link to this GitHub project folder.

GitHub becomes the public portfolio page. The report does not have to be publicly hosted in Power BI Service.

## Project status

- [x] Portfolio repository
- [x] Sample dataset
- [x] Dashboard specification
- [x] DAX measures
- [ ] Power BI Desktop report
- [ ] Screenshots
- [ ] Video demo
