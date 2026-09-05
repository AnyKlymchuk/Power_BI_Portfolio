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
