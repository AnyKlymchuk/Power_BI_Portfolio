let
    Source = Csv.Document(File.Contents("F:\\Anna PowerBI Guide\\Agents Performance\\DimEmployee.csv"),[Delimiter=",", Columns=21, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"EmployeeKey", Int64.Type}, {"ParentEmployeeKey", Int64.Type}, {"FirstName", type text}, {"LastName", type text}, {"Title", type text}, {"HireDate", type date}, {"BirthDate", type date}, {"EmailAddress", type text}, {"Phone", type text}, {"EmergencyContactName", type text}, {"EmergencyContactPhone", type text}, {"Gender", type text}, {"PayFrequency", Int64.Type}, {"BaseRate", type number}, {"VacationHours", Int64.Type}, {"DepartmentName", type text}, {"StartDate", type date}, {"Status", type text}, {"SalaryStatus", type text}, {"IsSalesPerson", type text}, {"IsMarried", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"EmailAddress", "Phone", "EmergencyContactName", "EmergencyContactPhone", "VacationHours", "StartDate", "Status", "SalaryStatus", "IsMarried"})
in
    #"Removed Columns"