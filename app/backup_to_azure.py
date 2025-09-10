import os
import pandas as pd
import psycopg
from azure.storage.blob import BlobServiceClient
from oltp_client import DSN

# Read credentials from environment variables (no hardcoding)
account_name = os.getenv("AZURE_STORAGE_ACCOUNT")
account_key = os.getenv("AZURE_STORAGE_KEY")

conn_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service_client.get_container_client("oltp-pipeline-demo")

def upload_table_to_blob(table_name):
    with psycopg.connect(DSN) as conn:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    local_file = f"/tmp/{table_name}.csv"
    df.to_csv(local_file, index=False)

    blob_client = container_client.get_blob_client(f"raw/{table_name}.csv")
    with open(local_file, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f" Uploaded {table_name}.csv to Azure Blob Storage")

if __name__ == "__main__":
    tables = ["customers", "accounts", "transactions"]
    for table in tables:
        upload_table_to_blob(table)
