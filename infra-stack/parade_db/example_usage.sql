-- Create the Parquet foreign data wrapper
CREATE FOREIGN DATA WRAPPER parquet_wrapper
HANDLER parquet_fdw_handler
VALIDATOR parquet_fdw_validator;

-- Create the foreign server for MinIO
CREATE SERVER parquet_server
FOREIGN DATA WRAPPER parquet_wrapper;

-- Create the foreign table with the S3/MinIO file
CREATE FOREIGN TABLE parquet_table ()
SERVER parquet_server
OPTIONS (files 's3://${MINIO_BUCKET_NAME}/path/to/your/file.parquet');

-- Provide credentials for accessing the MinIO bucket
CREATE USER MAPPING FOR public
SERVER parquet_server
OPTIONS (
  type 'S3',
  key_id '${MINIO_ACCESS_KEY}',
  secret '${MINIO_SECRET_KEY}',
  region 'us-east-1', -- Modify this if your MinIO setup is in a different region
  endpoint '${MINIO_ENDPOINT}', 
  use_ssl 'false' -- Change to 'true' if your MinIO endpoint is HTTPS
);

