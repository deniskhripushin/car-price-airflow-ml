import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_PATH = "/home/airflow/airflow_hw"

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": dt.timedelta(minutes=1),
}

with DAG(
    dag_id="car_price_prediction",
    default_args=default_args,
    start_date=dt.datetime(2022, 6, 10),
    schedule="0 21 * * 5",   
    catchup=False,
    tags=["hw"],
) as dag:

    pipeline_task = BashOperator(
        task_id="pipeline",
        bash_command=f"cd {PROJECT_PATH} && python modules/pipeline.py",
        env={"PROJECT_PATH": PROJECT_PATH},
    )

    predict_task = BashOperator(
        task_id="predict",
        bash_command=f"cd {PROJECT_PATH} && python modules/predict.py",
        env={"PROJECT_PATH": PROJECT_PATH},
    )

    pipeline_task >> predict_task

