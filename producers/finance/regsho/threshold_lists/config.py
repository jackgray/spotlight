primary_schema = {
    "_id": "String",
    "Report_Date": "Date",
    "Security_Symbol": "String"
}

# nasdaq(?)_source_schema = {
#     "ID": "String",
#     "Date": "datetime64[ns]",
#     "Symbol": "str",
#     "Security_Name": "str",
#     "Market_Category": "str",
#     "Market": "str",
#     "Reg_SHO_Threshold_Flag": "str",
#     "Threshold_List_Flag": "str",
#     "FINRA_Rule_4320_Flag": "str",
#     "Rule_3210": "str",
# }

reports_schema = {
    "Report_Date": "Date",
    "Source_Url": "String",
    "Data_Provider": "String"
}