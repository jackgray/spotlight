from spotlight_utils import main

dates = main.generate_date_strings(start_date='20190101', end_date='today')
print(dates)

from step1_sourcing import download_batch
# from step2_staging import drop_tables
# from config import dtcc_source_schema, dtcc_source_schema2, ice_source_schema, ch_settings
# DANGER - this function probably shouldn't exist. Used for dev purposes
# drop_tables(['Swaps_DTCC_sourcee','Swaps_ICE_sourcee','Swaps_ICE_sourcee2','Swaps_DTCC_sourcee2'], ch_settings)

# download_batch(start_date='20240321', end_date='today', ice_schema=ice_source_schema, dtcc_schema=dtcc_source_schema, dtcc_schema2=dtcc_source_schema2, ch_settings=ch_settings)
