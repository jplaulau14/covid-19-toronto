output "gcs_bucket_url" {
  value       = google_storage_bucket.data_lake.url
  description = "The URL of the GCS bucket."
}

output "bigquery_dataset_id" {
  value       = google_bigquery_dataset.data_warehouse.dataset_id
  description = "The ID of the BigQuery dataset."
}
