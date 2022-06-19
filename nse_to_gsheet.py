from email.policy import default
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'start_date' : datetime(2022,6,18),
    'retries' : 0
}

dag = DAG(dag_id="nse_gsheet",
default_args=default_args, # Dag id
schedule_interval='@daily',  # Cron expression, here it is a preset of Airflow, @daily means once every day.
catchup=False  # Catchup
)

t1 = BashOperator(
    task_id='nse_gsheet',
    bash_command='python /home/airflow/airflow/dags/nse_gsheet/stock_data.py',
    dag=dag)

start = DummyOperator(task_id = 'start',dag=dag)
end = DummyOperator(task_id = 'end',dag=dag)

start>>t1>>end
