from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

gcp_credentials_block = GcpCredentials.load("c19-gcp-creds")

bucket_block = GcsBucket(
    gcp_credentials=gcp_credentials_block,
    bucket='c19-toronto'
)

bucket_block.save('gcs-block', overwrite=True)