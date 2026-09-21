let
    FileBinary = File.Contents("F:\\Anna PowerBI Guide\\Agents Performance\\FactSales.csv"),
    FileText = Text.FromBinary(FileBinary, 1252),
    FirstLine = Text.BeforeDelimiter(FileText, "#(lf)"),
    CommaCount = List.Count(Text.PositionOf(FirstLine, ",", Occurrence.All)),
    SemicolonCount = List.Count(Text.PositionOf(FirstLine, ";", Occurrence.All)),
    Delimiter = if SemicolonCount > CommaCount then ";" else ",",
    Source = Csv.Document(FileBinary,[Delimiter=Delimiter,Encoding=1252,QuoteStyle=QuoteStyle.Csv]),
    #"Promoted Headers" = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    #"Clean Column Names" = Table.TransformColumnNames(#"Promoted Headers", each Text.Trim(Text.Clean(_))),
    ExpectedNames = {"SalesKey","DateKey","ChannelKey","StoreKey","ProductKey","PromotionKey","CurrencyKey","UnitCost","UnitPrice","SalesQuantity","ReturnQuantity","ReturnAmount","DiscountQuantity","DiscountAmount","TotalCost","SalesAmount"},
    RenamePairs = List.RemoveNulls(List.Transform(Table.ColumnNames(#"Clean Column Names"),(CurrentName) => let Match = List.First(List.Select(ExpectedNames, each Text.Lower(_) = Text.Lower(CurrentName)), null) in if Match <> null and Match <> CurrentName then {CurrentName, Match} else null)),
    #"Renamed Columns" = Table.RenameColumns(#"Clean Column Names", RenamePairs, MissingField.Ignore),
    #"Fixed DateKey" = Table.TransformColumns(#"Renamed Columns",{{"DateKey", each Date.FromText(Text.Trim(Text.From(_)),[Format="dd.MM.yyyy",Culture="uk-UA"]), type date}}),
    TypeMap = {{"SalesKey",Int64.Type},{"ChannelKey",Int64.Type},{"StoreKey",Int64.Type},{"ProductKey",Int64.Type},{"PromotionKey",Int64.Type},{"CurrencyKey",Int64.Type},{"UnitCost",type number},{"UnitPrice",type number},{"SalesQuantity",Int64.Type},{"ReturnQuantity",Int64.Type},{"ReturnAmount",type number},{"DiscountQuantity",Int64.Type},{"DiscountAmount",type number},{"TotalCost",type number},{"SalesAmount",type number}},
    ExistingColumns = Table.ColumnNames(#"Fixed DateKey"),
    ExistingTypes = List.Select(TypeMap, each List.Contains(ExistingColumns, _{0})),
    #"Changed Type" = Table.TransformColumnTypes(#"Fixed DateKey", ExistingTypes),
    #"Filtered Rows" = if List.Contains(Table.ColumnNames(#"Changed Type"),"SalesKey") then Table.SelectRows(#"Changed Type", each [SalesKey] < 200000) else #"Changed Type",
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"CurrencyKey","PromotionKey"},MissingField.Ignore)
in
    #"Removed Columns"