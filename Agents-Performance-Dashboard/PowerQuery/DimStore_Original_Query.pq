let
    Source = Csv.Document(File.Contents("F:\\Anna PowerBI Guide\\Agents Performance\\DimStore.csv"),[Delimiter=",", Columns=16, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"StoreKey", Int64.Type}, {"GeographyKey", Int64.Type}, {"StoreManager", Int64.Type}, {"StoreType", type text}, {"StoreName", type text}, {"Status", type text}, {"OpenDate", type date}, {"CloseDate", type date}, {"EntityKey", Int64.Type}, {"StorePhone", type text}, {"StoreFax", type text}, {"CloseReason", type text}, {"EmployeeCount", Int64.Type}, {"SellingAreaSize", Int64.Type}, {"LastRemodelDate", type datetime}, {"EmployeeKey", Int64.Type}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"LastRemodelDate", "EntityKey", "StorePhone", "StoreFax", "StoreManager"})
in
    #"Removed Columns"