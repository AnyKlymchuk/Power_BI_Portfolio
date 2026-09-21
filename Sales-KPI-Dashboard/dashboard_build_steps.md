# Dashboard Build Steps

## 1. Load data
In Power BI Desktop:
- Home -> Get data -> Text/CSV
- Load `sales.csv`
- Load `targets.csv`

Set:
- sales[Date] = Date
- targets[Month] = Date
- Revenue / Cost / Profit / targets = Decimal Number
- Units / OrderID = Whole Number

## 2. Create Date table
Use the DAX from `DAX_measures.md`.

## 3. Relationships
- Date[Date] 1:* sales[Date]
- Date[MonthStart] 1:* targets[Month]

## 4. Build one-page dashboard

Top row:
- Revenue
- Profit
- Profit Margin %
- Orders
- Average Order Value
- Revenue Variance %

Middle:
- Revenue by Month
- Revenue vs Target by Month

Bottom:
- Revenue by Region
- Profit by Category
- Revenue by Channel

Left or top:
- Date, Region, Category, Channel slicers

## 5. Formatting
Use a clean white background, one dark accent color, and one highlight color for target/variance.
Keep labels short and avoid unnecessary borders.

## 6. Portfolio export
Take a clean screenshot at 16:9 and save it as:
`images/sales-kpi-dashboard.png`

Then add the PBIX file:
`Sales_KPI_Dashboard.pbix`
