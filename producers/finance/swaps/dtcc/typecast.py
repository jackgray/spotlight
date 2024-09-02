from clickhouse_connect import get_client as ch
from config import ch_settings, dtcc_staging_schema as schema
from spotlight_utils.main import create_table_from_dict, get_schema, ch_typecast






# def main(src, dst, ch_settings=ch_settings, schema=schema):
ch_typecast(src_table='Swaps_DTCC_source3', dst_table='Swaps_DTCC_staging70', key_col='_Record_Id', ch_settings=ch_settings, schema=schema)
