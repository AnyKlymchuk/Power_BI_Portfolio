let
    Source = Csv.Document(
        File.Contents("F:\\Anna PowerBI Guide\\Agents Performance\\FactSales.csv"),
        [Delimiter=",", Columns=16, Encoding=1252, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Renamed Columns" = Table.RenameColumns(
        #"Promoted Headers",
        {{"channelKey", "ChannelKey"}}
    ),
    #"Changed Type" = Table.TransformColumnTypes(
        #"Renamed Columns",
        {
            {"SalesKey", Int64.Type},
            {"DateKey", type date},
            {"channelkey", Int64.Type},
            {"storeKey", Int64.Type},
            {"ProductKey", Int64.Type},
            {"PromotionKey", Int64.Type},
            {"CurrencyKey", Int64.Type},
            {"UnitCost", type number},
            {"UnitPrice", type number},
            {"SalesQuantity", Int64.Type},
            {"ReturnQuantity", Int64.Type},
            {"ReturnAmount", type number},
            {"DiscountQuantity", Int64.Type},
            {"DiscountAmount", type number},
            {"TotalCost", type number},
            {"SalesAmount", type number}
        }
    ),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each [SalesKey] < 200000),
    #"Removed Columns" = Table.RemoveColumns(
        #"Filtered Rows",
        {"CurrencyKey", "PromotionKey"}
    )
in
    #"Removed Columns"