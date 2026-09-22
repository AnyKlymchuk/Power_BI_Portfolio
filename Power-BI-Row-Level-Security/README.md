# Power BI Row-Level Security (RLS)

**Status:** Implementation kit ready — Power BI Desktop validation/screenshots pending

A practical Power BI security case demonstrating **static and dynamic Row-Level Security (RLS)**. Different users can open the same report while seeing only the regions they are authorized to access.

## Business scenario

A company has one sales report for Kyiv, Lviv and Odesa. Each regional manager must only see their own region. A regional lead can see all three regions. The solution must avoid maintaining a separate report for every manager.

## Repository contents

- `data/sales.csv` — sample fact data
- `data/region.csv` — region dimension
- `data/user_region_access.csv` — user-to-region security mapping
- `dax/rls-rules.md` — static/dynamic RLS rules, measures and validation cases

## Data model

Build these relationships in Power BI Desktop:

```text
UserRegionAccess (*) ── Region (1) ── Sales (*)
       security             filter
         path                path
```

Use `Region` as the shared dimension. The access table can contain multiple rows per user, which means one user can be authorized for several regions.

## 1. Static RLS

Create a role in **Modeling → Manage roles** called `Kyiv Manager` and filter the `Sales` table:

```DAX
[Region] = "Kyiv"
```

Test it with **Modeling → View as**. Only Kyiv sales should remain visible.

## 2. Dynamic RLS

Create a role called `Dynamic RLS` and apply the filter to `UserRegionAccess`:

```DAX
[UserEmail] = USERPRINCIPALNAME()
```

The authenticated email filters the access table, then the allowed region(s), and finally the Sales rows.

### Test identities

| User | Expected access |
|---|---|
| manager.kyiv@company.com | Kyiv |
| manager.lviv@company.com | Lviv |
| manager.odesa@company.com | Odesa |
| regional.lead@company.com | Kyiv, Lviv, Odesa |

## 3. Demo measures

```DAX
Total Sales = SUM(Sales[SalesAmount])

Transactions = COUNTROWS(Sales)

Average Sale = DIVIDE([Total Sales], [Transactions])
```

Recommended report page: KPI cards for Total Sales / Transactions / Average Sale, a monthly sales chart, a region slicer, and a detail table. This makes the security effect immediately visible when switching test users.

## 4. Validation checklist

1. Load all three CSV files.
2. Create the relationships shown above.
3. Create the three demo measures.
4. Create `Kyiv Manager` static role.
5. Create `Dynamic RLS` role with `USERPRINCIPALNAME()`.
6. Test Static RLS with **View as** and confirm only Kyiv rows remain.
7. Test Dynamic RLS with **View as → Other user** for each test email.
8. Confirm the regional lead sees all three regions.
9. Publish to Power BI Service when a suitable account/license is available and assign real users/groups to the role.

## Screenshots to capture in Power BI Desktop

Save screenshots in a `screenshots/` folder with these names:

- `01-data-model.png` — relationships between UserRegionAccess, Region and Sales
- `02-static-role.png` — static Kyiv role filter
- `03-dynamic-role.png` — `USERPRINCIPALNAME()` rule
- `04-view-as-kyiv.png` — report filtered as Kyiv manager
- `05-view-as-lviv.png` — report filtered as Lviv manager
- `06-view-as-regional-lead.png` — report showing all authorized regions

## RLS vs Power BI permissions

RLS controls **which rows a report consumer can see**. Workspace roles, app permissions, Build permission and sharing control **which Power BI artifacts a user can access or what they can do with them**. They solve different security problems and are often used together.

## Troubleshooting notes

- If every user sees all rows, verify the role is applied to the correct security table and that the security filter can propagate to the fact table.
- If a user sees no rows, check that the email returned by `USERPRINCIPALNAME()` exactly matches `UserRegionAccess[UserEmail]`.
- Keep the user-to-region mapping separate from the fact table so access changes can be maintained without rewriting business data.
- Test a multi-region user to verify the model supports many access rows for one identity.

## Skills demonstrated

Power BI · DAX · Data Modeling · Static RLS · Dynamic RLS · `USERPRINCIPALNAME()` · User Access · Security Modeling · Power BI Service · Troubleshooting

## Portfolio note

The data, security model, DAX rules and validation plan are complete in this repository. Final screenshots must be captured from Power BI Desktop after opening/building the model locally; they are intentionally not fabricated.
