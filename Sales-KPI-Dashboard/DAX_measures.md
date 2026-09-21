# DAX Measures

Create these measures after loading `sales.csv` and `targets.csv`.

```DAX
Revenue =
SUM ( sales[Revenue] )

Profit =
SUM ( sales[Profit] )

Cost =
SUM ( sales[Cost] )

Orders =
DISTINCTCOUNT ( sales[OrderID] )

Units =
SUM ( sales[Units] )

Profit Margin % =
DIVIDE ( [Profit], [Revenue], 0 )

Average Order Value =
DIVIDE ( [Revenue], [Orders], 0 )

Revenue Target =
SUM ( targets[RevenueTarget] )

Profit Target =
SUM ( targets[ProfitTarget] )

Revenue Variance =
[Revenue] - [Revenue Target]

Revenue Variance % =
DIVIDE ( [Revenue] - [Revenue Target], [Revenue Target], 0 )

Profit Variance =
[Profit] - [Profit Target]

Profit Variance % =
DIVIDE ( [Profit] - [Profit Target], [Profit Target], 0 )
```

## Date table

```DAX
Date =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2025, 1, 1 ), DATE ( 2026, 8, 31 ) ),
    "Year", YEAR ( [Date] ),
    "Month No", MONTH ( [Date] ),
    "Month", FORMAT ( [Date], "MMM" ),
    "Year Month", FORMAT ( [Date], "YYYY-MM" ),
    "MonthStart", DATE ( YEAR ( [Date] ), MONTH ( [Date] ), 1 )
)
```

Sort `Date[Month]` by `Date[Month No]`.
