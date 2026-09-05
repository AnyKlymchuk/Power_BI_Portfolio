# Implementation checklist

## 1. Create SharePoint List
Create a list named `PowerBI_Comments` with:
- YearMonth — Single line of text
- Comment — Multiple lines of text
- UpdatedBy — Single line of text
- UpdatedAt — Date and time

Add one row per month.

## 2. Build Power BI demo
- Load `sales_dummy.csv`.
- Create a Calendar table or YearMonth field.
- Add a column chart: YearMonth vs Sales.
- Add a YearMonth slicer.
- Connect to the SharePoint list for comments.
- Add the `Selected Comment` measure to a Card/text visual.

## 3. Add Power Apps visual
- Add the Power Apps visual to the report.
- Pass `YearMonth` into the visual.
- Create a new canvas app from the Power Apps visual.
- Add the SharePoint list as a data source.
- Add a multiline text input named `txtComment`.
- Set its default value from the selected month/comment.
- Add a Save button.
- Put the formula from `powerapps/save_comment.fx` on the Save button.
- Save and publish the app.
- Share the app only with intended users.

## 4. Refresh behavior
Important: write-back and Power BI display refresh are separate concerns.

For an Import-mode comments table, a saved SharePoint change is not automatically visible in the imported semantic model until data refresh occurs.

`PowerBIIntegration.Refresh()` has specific limitations and requires the app to be created from the Power Apps visual; Microsoft documents it for DirectQuery-supported sources/connections. Therefore, do not promise instant refresh for a SharePoint Import model without testing the chosen architecture.

For the client demo, clearly show:
1. the edit is saved to SharePoint;
2. the report retrieves the updated comment according to the chosen refresh design.

## 5. Client demo script
- Select September -> September comment appears.
- Select October -> October comment appears.
- Edit October comment in the embedded app.
- Click Save.
- Show the updated SharePoint record.
- Refresh according to the demo architecture and show the updated October annotation.

## Production questions
Before implementation in the client's tenant, confirm:
- Where should comments be stored: SharePoint List, Dataverse, or SQL?
- Which named users may edit?
- Is near-real-time visibility required after Save?
- Is the report Import or DirectQuery?
- Are Power Apps licenses/environment permissions available to report users?
