# Dynamic Power BI Comments

A small Power BI write-back demo showing how business users can view and edit commentary by filter context without republishing the PBIX.

## Business requirement

When a user selects a month in Power BI, the annotation panel shows the comment for that month. A small group of named users can edit the comment and save it without changing or republishing the PBIX file.

## Architecture

Power BI report -> Power Apps visual -> SharePoint List

- **Power BI** displays the chart and the current comment.
- **Power Apps** provides the editable text box and Save button.
- **SharePoint List** stores the comments and audit fields.

## SharePoint list schema

List name: `PowerBI_Comments`

| Column | Type | Purpose |
|---|---|---|
| Title | Single line text | Optional label |
| YearMonth | Single line text | Key such as 2026-10 |
| Comment | Multiple lines text | Business commentary |
| UpdatedBy | Single line text | User email |
| UpdatedAt | Date and time | Last update timestamp |

## Power BI model

Use a Calendar table with `YearMonth` and connect it to the demo fact table. The comments table can be loaded from SharePoint for display.

### DAX measure

```DAX
Selected Comment =
VAR SelectedMonth = SELECTEDVALUE ( 'Calendar'[YearMonth] )
RETURN
    CALCULATE (
        MAX ( Comments[Comment] ),
        Comments[YearMonth] = SelectedMonth
    )
```

Place the measure in a Card or text-style visual next to the chart.

## Power Apps write-back

Pass `YearMonth` and the current comment into the Power Apps visual.

Use this logic on the Save button:

```powerapps
Patch(
    PowerBI_Comments,
    Coalesce(
        LookUp(
            PowerBI_Comments,
            YearMonth = First(PowerBIIntegration.Data).YearMonth
        ),
        Defaults(PowerBI_Comments)
    ),
    {
        YearMonth: First(PowerBIIntegration.Data).YearMonth,
        Comment: txtComment.Text,
        UpdatedBy: User().Email,
        UpdatedAt: Now()
    }
);
Notify("Comment saved", NotificationType.Success)
```

## Demo flow

1. Open the report.
2. Select October 2026.
3. The chart filters to October.
4. The annotation panel shows October's comment.
5. An authorized user edits the comment in the Power Apps visual.
6. The user clicks Save.
7. Power Apps writes the change to SharePoint.
8. Power BI shows the updated comment after the relevant refresh step.

## Files

- `data/sales_dummy.csv` - small demo fact table.
- `data/comments_dummy.csv` - sample comments.
- `dax/selected_comment.dax` - DAX measure.
- `powerapps/save_comment.fx` - Power Apps Patch formula.

## Notes

For a production implementation, access should be restricted in SharePoint/Power Apps to the named editors. Refresh behavior should also be designed explicitly so users understand when a newly saved comment becomes visible in the report.
