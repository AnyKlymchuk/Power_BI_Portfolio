let
    FileBinary = File.Contents("F:\\Anna PowerBI Guide\\Agents Performance\\DimEmployee.csv"),
    FileText = Text.FromBinary(FileBinary, 65001),
    FirstLine = Text.BeforeDelimiter(FileText, "#(lf)"),
    CommaCount = List.Count(Text.PositionOf(FirstLine, ",", Occurrence.All)),
    SemicolonCount = List.Count(Text.PositionOf(FirstLine, ";", Occurrence.All)),
    Delimiter = if SemicolonCount > CommaCount then ";" else ",",
    Source = Csv.Document(FileBinary,[Delimiter=Delimiter,Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Clean Column Names" = Table.TransformColumnNames(#"Promoted Headers", each Text.Trim(Text.Clean(_))),
    ExpectedNames = {"EmployeeKey","ParentEmployeeKey","FirstName","LastName","Title","HireDate","BirthDate","EmailAddress","Phone","EmergencyContactName","EmergencyContactPhone","Gender","PayFrequency","BaseRate","VacationHours","DepartmentName","StartDate","Status","SalaryStatus","IsSalesPerson","IsMarried"},
    RenamePairs = List.RemoveNulls(List.Transform(Table.ColumnNames(#"Clean Column Names"),(CurrentName) => let Match = List.First(List.Select(ExpectedNames, each Text.Lower(_) = Text.Lower(CurrentName)), null) in if Match <> null and Match <> CurrentName then {CurrentName, Match} else null)),
    #"Renamed Columns" = Table.RenameColumns(#"Clean Column Names",RenamePairs,MissingField.Ignore),
    #"Fixed Dates" = Table.TransformColumns(#"Renamed Columns",{{"HireDate", each try Date.FromText(Text.From(_),[Culture="uk-UA"]) otherwise null, type date},{"BirthDate", each try Date.FromText(Text.From(_),[Culture="uk-UA"]) otherwise null, type date},{"StartDate", each try Date.FromText(Text.From(_),[Culture="uk-UA"]) otherwise null, type date}},null,MissingField.Ignore),
    TypeMap = {{"EmployeeKey",Int64.Type},{"ParentEmployeeKey",Int64.Type},{"FirstName",type text},{"LastName",type text},{"Title",type text},{"Gender",type text},{"PayFrequency",Int64.Type},{"BaseRate",type number},{"VacationHours",Int64.Type},{"DepartmentName",type text},{"Status",type text},{"SalaryStatus",type text},{"IsSalesPerson",type text},{"IsMarried",type text}},
    ExistingColumns = Table.ColumnNames(#"Fixed Dates"),
    ExistingTypes = List.Select(TypeMap, each List.Contains(ExistingColumns, _{0})),
    #"Changed Type" = Table.TransformColumnTypes(#"Fixed Dates", ExistingTypes),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"EmailAddress","Phone","EmergencyContactName","EmergencyContactPhone","VacationHours","StartDate","Status","SalaryStatus","IsMarried"},MissingField.Ignore)
in
    #"Removed Columns"