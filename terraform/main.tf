provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "data_lake" {
  name     = var.gcs_bucket_name
  location = var.region
}

resource "google_bigquery_dataset" "data_warehouse" {
  dataset_id = var.bigquery_dataset_name
  location   = var.region
}
