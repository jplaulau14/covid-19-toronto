import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from io import StringIO
import requests
from pathlib import Path
from datetime import datetime


@task(retries=3, retry_delay_seconds=10, log_prints=True, name="Extract from Opendata Toronto")
def extract() -> pd.DataFrame:
    """
    Extracts the date from Opendata Toronto's COVID-19 dataset
    """
    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

    url = base_url + "/api/3/action/package_show"
    params = {"id": "covid-19-cases-in-toronto"}
    package = requests.get(url, params=params).json()

    # To get resource data:
    for idx, resource in enumerate(package["result"]["resources"]):

        # for datastore_active resources:
        if resource["datastore_active"]:

            # To get all records in CSV format:
            url = base_url + "/datastore/dump/" + resource["id"]
            resource_dump_data = requests.get(url).text
            df = pd.read_csv(StringIO(resource_dump_data))

    return df


@task(retries=3, retry_delay_seconds=10, log_prints=True, name="Convert to Parquet")
def convert_to_parquet(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the dataframe to parquet format
    """
    df.to_parquet("data/covid19-toronto.parquet")
    df = pd.read_parquet("data/covid19-toronto.parquet")
    return df


@task(retries=3, retry_delay_seconds=10, log_prints=True, name="Transform Data")
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the dataframe
    Converts Episode Date and Reported Date to datetime
    """
    df["Episode Date"] = pd.to_datetime(df["Episode Date"])
    df["Reported Date"] = pd.to_datetime(df["Reported Date"])
    return df


@task(retries=3, retry_delay_seconds=10, log_prints=True, name="Load to Local Disk")
def load_local(df: pd.DataFrame) -> Path:
    """
    Loads the dataframe to local disk
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    df.to_parquet(f"data/{current_date}-covid19-toronto.parquet")
    return Path(f"data/{current_date}-covid19-toronto.parquet")


@task(retries=3, retry_delay_seconds=10, log_prints=True)
def load_to_gcs(path: Path):
    """
    Loads the dataframe to GCS
    """
    gcs_block = GcsBucket.load('gcs-block')
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return

@task(retries=3, retry_delay_seconds=10, log_prints=True, name="Extract from GCS")
def extract_from_gcs() -> Path:
    """
    Extracts the date from GCS
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    gcs_path = f"data/{current_date}-covid19-toronto.parquet"
    gcs_block = GcsBucket.load('gcs-block')
    gcs_block.download_object_to_path(
        from_path=gcs_path,
        to_path=gcs_path
    )

    return Path(gcs_path)

@task(retries=3, retry_delay_seconds=10, log_prints=True, name="Rename column headers")
def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the dataframe
    Converts Episode Date and Reported Date to datetime
    """
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df

@task(retries=3, retry_delay_seconds=10, log_prints=True, name="Load to BigQuery")
def load_to_bq(df: pd.DataFrame):
    """
    Loads the dataframe to BigQuery
    """
    gcp_credentials_block = GcpCredentials.load("c19-gcp-creds")
    df.to_gbq(destination_table='covid19_toronto.covid_data', if_exists="replace", project_id="covid-19-toronto",
              credentials=gcp_credentials_block.get_credentials_from_service_account())
    return

@flow(name="ETL Flow")
def main_flow():
    df = extract()
    df = transform(df)
    df = convert_to_parquet(df)
    path = load_local(df)
    load_to_gcs(path)
    path = extract_from_gcs()
    df = pd.read_parquet(path)
    df = rename_columns(df)
    print(df.head())
    load_to_bq(df)

if __name__ == "__main__":
    main_flow()
