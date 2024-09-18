from clickhouse_connect import get_client as ch
from config import clickhouse_schema_staging as schema
from spotlight_utils.main import create_table_from_dict, get_schema, ch_typecast
from spotlight_utils.config import ch_settings






# def main(src, dst, ch_settings=ch_settings, schema=schema):
ch_typecast(src_table='rule605_citadel_2021up', dst_table='Rule605_Citadel3', key_col='report_month', ch_settings=ch_settings, schema=schema)
