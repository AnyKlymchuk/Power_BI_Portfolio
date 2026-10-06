let
    Source = FT_DataBase,

    SelectedColumns =
        Table.SelectColumns(
            Source,
            {
                "Направляючий лікар",
                "Відповідальний співробітник лікаря",
                "Код ID контрагента",
                "Контрагент",
                "Відповідальний по контрагенту",
                "Філіал",
                "Проєкт"
            },
            MissingField.UseNull
        ),

    RenamedColumns =
        Table.RenameColumns(
            SelectedColumns,
            {
                {"Направляючий лікар", "Doctor"},
                {"Відповідальний співробітник лікаря", "DoctorResponsible"},
                {"Код ID контрагента", "CounterpartyID"},
                {"Контрагент", "Counterparty"},
                {"Відповідальний по контрагенту", "CounterpartyResponsible"},
                {"Філіал", "Branch"},
                {"Проєкт", "Project"}
            }
        ),

    CleanText =
        Table.TransformColumns(
            RenamedColumns,
            {
                {"Doctor", each if _ = null then null else Text.Trim(Text.From(_)), type text},
                {"DoctorResponsible", each if _ = null then null else Text.Trim(Text.From(_)), type text},
                {"CounterpartyID", each if _ = null then null else Text.Trim(Text.From(_)), type text},
                {"Counterparty", each if _ = null then null else Text.Trim(Text.From(_)), type text},
                {"CounterpartyResponsible", each if _ = null then null else Text.Trim(Text.From(_)), type text},
                {"Branch", each if _ = null then null else Text.Trim(Text.From(_)), type text},
                {"Project", each if _ = null then null else Text.Trim(Text.From(_)), type text}
            }
        ),

    DistinctRows =
        Table.Distinct(CleanText),

    AddedKey =
        Table.AddIndexColumn(
            DistinctRows,
            "ResponsibleMapKey",
            1,
            1,
            Int64.Type
        )
in
    AddedKey
