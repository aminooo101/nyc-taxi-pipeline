import functions_framework
from google.cloud import dataproc_v1
import uuid

@functions_framework.cloud_event
def trigger_etl(cloud_event):
    data = cloud_event.data
    bucket = data["bucket"]
    name = data["name"]

    # Validar que el archivo sea un parquet dentro de la carpeta raw/
    if not name.startswith("raw/") or not name.endswith(".parquet"):
        print(f"Ignorado: {name}")
        return

    print(f"🚀 Archivo detectado: gs://{bucket}/{name}")
    
    project_id = "midnight-495805"
    region = "europe-west1"
    batch_id = f"batch-taxi-auto-{uuid.uuid4().hex[:6]}"

    # Configurar el cliente de Dataproc Serverless
    client = dataproc_v1.BatchControllerClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
    )

    # Definir el lote de Spark
    batch_config = dataproc_v1.Batch(
        pyspark_batch=dataproc_v1.PySparkBatch(
            main_python_file_uri=f"gs://{bucket}/scripts/etl_job.py"
        ),
        environment_config=dataproc_v1.EnvironmentConfig(
            execution_config=dataproc_v1.ExecutionConfig(staging_bucket=bucket)
        ),
        runtime_config=dataproc_v1.RuntimeConfig(version="2.2")
    )

    print(f"Enviando lote automático a Dataproc: {batch_id}...")
    operation = client.create_batch(
        parent=f"projects/{project_id}/regions/{region}",
        batch=batch_config,
        batch_id=batch_id,
    )
    print(f"✅ Job enviado con éxito. Operación: {operation.operation.name}")
