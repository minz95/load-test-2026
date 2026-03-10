from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="locust_load_test",
    start_date=datetime(2024,1,1),
    schedule_interval=None,
    catchup=False
) as dag:

    run_locust_test = BashOperator(
        task_id="run_locust",
        bash_command="""
        locust -f locust/locust.py \
        --headless \
        -u 50 \
        -r 5 \
        --run-time 60s \
        --host http://api-service
        """
    )
