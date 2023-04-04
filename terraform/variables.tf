variable "project_id" {
  type        = string
  description = "The ID of the GCP project."
}

variable "region" {
  type        = string
  description = "The GCP region."
}

variable "gcs_bucket_name" {
  type        = string
  description = "The name of the GCS bucket."
}

variable "bigquery_dataset_name" {
  type        = string
  description = "The name of the BigQuery dataset."
}
