# Power BI Row-Level Security (RLS)

**Status:** In progress

This portfolio project demonstrates how to implement and validate Row-Level Security (RLS) in Power BI so different users can open the same report but only see the rows they are authorized to access.

## Business scenario

A company uses one Power BI report across multiple regions. Regional managers should only see data for their own region, while a senior manager can see all regions.

## What this project will demonstrate

- Static RLS with role-based DAX filters
- Dynamic RLS using a user-to-region mapping table
- `USERPRINCIPALNAME()` for user-based filtering
- Role creation in Power BI Desktop
- Testing with **View as**
- Role assignment and validation in Power BI Service
- Difference between RLS and workspace/report permissions
- Common RLS troubleshooting cases

## Planned model

Example security table:

| UserEmail | Region |
|---|---|
| manager.kyiv@company.com | Kyiv |
| manager.lviv@company.com | Lviv |

Example dynamic RLS rule:

```DAX
[UserEmail] = USERPRINCIPALNAME()
```

## Skills demonstrated

Power BI · DAX · Data Modeling · Row-Level Security · Dynamic RLS · Power BI Service · User Access · Troubleshooting

## Next steps

The implementation will include a sample dataset, model relationships, RLS roles, test users, screenshots, and documented validation results.
