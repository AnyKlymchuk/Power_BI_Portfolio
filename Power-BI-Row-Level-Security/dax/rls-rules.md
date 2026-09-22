# RLS DAX rules

## Static RLS

Create a role named `Kyiv Manager` on the `Sales` table:

```DAX
[Region] = "Kyiv"
```

Repeat for Lviv/Odesa if you want to demonstrate multiple static roles.

## Dynamic RLS

Recommended model:

`UserRegionAccess[Region]` (many-to-one) → `Region[Region]` (one) → `Sales[Region]` (many)

Apply this role filter to `UserRegionAccess`:

```DAX
[UserEmail] = USERPRINCIPALNAME()
```

Use a distinct `Region` dimension between the access table and Sales. Enable the security filter path from the access mapping to Region so the authenticated user's allowed regions propagate to Sales.

## Measures for the demo

```DAX
Total Sales = SUM(Sales[SalesAmount])

Transactions = COUNTROWS(Sales)

Average Sale = DIVIDE([Total Sales], [Transactions])
```

## Expected validation

- `manager.kyiv@company.com` → only Kyiv rows.
- `manager.lviv@company.com` → only Lviv rows.
- `manager.odesa@company.com` → only Odesa rows.
- `regional.lead@company.com` → Kyiv + Lviv + Odesa.

In Power BI Desktop use **Modeling → View as → Other user** and enter one of the test emails while the Dynamic RLS role is selected.
