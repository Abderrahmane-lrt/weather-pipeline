import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG

try:
    from airflow.providers.standard.operators.python import PythonOperator
except ImportError:
    from airflow.operators.python import PythonOperator

AIRFLOW_HOME = Path(__file__).resolve().parents[1]
for path in (AIRFLOW_HOME, AIRFLOW_HOME / "scripts"):
    path_str = str(path)
    if path.exists() and path_str not in sys.path:
        sys.path.insert(0, path_str)

from scripts.script_01_extract import run_extraction
from scripts.script_02_transform import run_transform
from scripts.script_03_load import run_load


with DAG(
    dag_id="weather_pipeline",
    description="Extract, transform and load weather risk data for Morocco",
    start_date=datetime(2026, 9, 17),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["weather", "morocco"],
) as dag:

    extract_task = PythonOperator(
        task_id="execute_extract",
        python_callable=run_extraction,
    )

    transform_task = PythonOperator(
        task_id="execute_transform",
        python_callable=run_transform,
    )

    load_weather_task = PythonOperator(
        task_id="execute_load_weather",
        python_callable=run_load,
    )

    extract_task >> transform_task >> load_weather_task
