let
    Source = Csv.Document(
        File.Contents("F:\\Anna PowerBI Guide\\Agents Performance\\DimStore.csv"),
        [Delimiter = ";", Encoding = 1252, QuoteStyle = QuoteStyle.Csv]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(
        #"Promoted Headers",
        {
            {"StoreKey", Int64.Type},
            {"GeographyKey", Int64.Type},
            {"StoreType", type text},
            {"StoreName", type text},
            {"Status", type text},
            {"EmployeeCount", Int64.Type},
            {"SellingAreaSize", Int64.Type},
            {"EmployeeKey", Int64.Type}
        }
    ),
    #"Removed Columns" = Table.RemoveColumns(
        #"Changed Type",
        {"LastRemodelDate","EntityKey","StorePhone","StoreFax","StoreManager"},
        MissingField.Ignore
    )
in
    #"Removed Columns"