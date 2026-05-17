
End-to-end data engineering pipeline that processes NYC Yellow Taxi data using PySpark on Google Cloud.


## Architecture
GCS (raw Parquet)
│
▼  [file upload trigger]
Cloud Function
│
▼  [launches batch job]
Dataproc Serverless (PySpark)
│  - filters invalid trips
│  - aggregates by hour, distance, payment
▼
BigQuery (yellow_trips_final)
│
▼
SQL Analytics (queries/)
## Stack

- **PySpark** — distributed data processing
- **Google Cloud Storage** — data lake (raw + processed)
- **Cloud Function (Gen2)** — event-driven trigger on file upload
- **Dataproc Serverless** — managed Spark without cluster management
- **BigQuery** — analytical queries on 160MB+ datasets

## Project structure
nyc-taxi-pipeline/
├── etl_job.py              # PySpark ETL job
├── cloud_function/
│   ├── main.py             # GCS trigger → Dataproc launcher
│   └── requirements.txt
├── queries/
│   └── analysis.sql        # 3 analytical queries on BigQuery
└── README.md
## Key results

- Processed 3 Parquet files (~160MB) in under 10 seconds on Dataproc Serverless
- BigQuery analytics: revenue by hour, trip distance distribution, payment method breakdown
- Fully automated: uploading a file to GCS triggers the entire pipeline automatically

## Deploy

```bash
# 1. Set your project
gcloud config set project YOUR_PROJECT_ID

# 2. Deploy Cloud Function
cd cloud_function
gcloud functions deploy trigger_etl \
  --gen2 --runtime=python312 \
  --region=europe-west1 \
  --trigger-location=eu \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=YOUR_BUCKET"

# 3. Upload data to trigger the pipeline
gsutil cp data/*.parquet gs://YOUR_BUCKET/raw/
```

## What I learned

- PySpark DataFrame API: filtering, aggregation, Parquet I/O
- GCS as a data lake with structured prefixes (raw/ processed/)
- IAM roles and service account permissions in GCP
- Event-driven architecture with Eventarc + Cloud Functions Gen2
- Dataproc Serverless batch jobs vs traditional cluster management
- BigQuery for analytical SQL on large datasets
