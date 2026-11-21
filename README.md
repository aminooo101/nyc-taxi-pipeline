# NYC Taxi Pipeline

End-to-end data pipeline that processes NYC Yellow Taxi data using PySpark on Google Cloud.

## Architecture

```
GCS (raw Parquet)
        │
        ▼  [file upload trigger]
Cloud Function (Gen2)
        │
        ▼  [launches batch job]
Dataproc Serverless (PySpark)
        │  - filters invalid trips (distance > 0 and total_amount > 0)
        ▼
BigQuery (yellow_trips_final)
        │
        ▼
SQL Analytics (queries/)
```

## Stack

- **PySpark** — distributed data processing
- **Google Cloud Storage** — data lake (raw + processed)
- **Cloud Function (Gen2)** — event-driven trigger on file upload
- **Dataproc Serverless** — managed Spark without cluster management
- **BigQuery** — analytical queries

## Project structure

```
nyc-taxi-pipeline/
├── etl_job.py              # PySpark ETL job (filter + write)
├── cloud_function/
│   ├── main.py             # GCS trigger → Dataproc launcher
│   └── requirements.txt
├── queries/
│   └── analysis.sql        # Analytical queries on BigQuery
└── README.md
```

## What the Spark job does

The `etl_job.py` script:
- Reads Parquet files from GCS
- Filters out invalid trips (`trip_distance <= 0` or `total_amount <= 0`)
- Writes the cleaned dataset to BigQuery

Aggregation and analytics are done in the SQL queries under `queries/`, not in the Spark job.

## Deploy (high-level)

```bash
gcloud config set project YOUR_PROJECT_ID

# Deploy the Cloud Function trigger
cd cloud_function
gcloud functions deploy trigger_etl \
  --gen2 --runtime=python312 \
  --region=europe-west1 \
  --trigger-location=eu \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=YOUR_BUCKET"

# Upload data to start the pipeline
gsutil cp data/*.parquet gs://YOUR_BUCKET/raw/
```

## Author

Amin Hadian · [github.com/aminooo101](https://github.com/aminooo101)
