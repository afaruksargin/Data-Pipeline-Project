from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago
import os
import sys

parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_folder)

from dags.baserow_add_data import main

with DAG(
    dag_id = "kafka",
    schedule_interval="@daily",
    start_date=days_ago(1),
    tags=['kafka'],
) as dag:
    
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')  
    
    consumer_task=PythonOperator(
        task_id="consumer_task",
        python_callable=main
    )
        
    start >> consumer_task >> end