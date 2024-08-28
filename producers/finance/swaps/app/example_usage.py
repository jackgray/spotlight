from step1_sourcing import download_batch
from step2_staging import drop_tables
from config import dtcc_source_schema, dtcc_source_schema2, ice_source_schema, ch_settings

# DANGER - this function probably shouldn't exist. Used for dev purposes
# drop_tables(['Swaps_DTCC_source','Swaps_ICE_source','Swaps_ICE_source2','Swaps_DTCC_source2'], ch_settings)

download_batch(start_date='20240227', end_date='today', ice_schema=ice_source_schema, dtcc_schema=dtcc_source_schema, dtcc_schema2=dtcc_source_schema2, ch_settings=ch_settings)
