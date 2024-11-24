

from __future__ import annotations
from itertools import chain
from datetime import datetime

from airflow.decorators import task
from airflow.models.dag import DAG

with DAG(dag_id="rerun_test", schedule=None,
         start_date=datetime(2022, 3, 4)) as dag:


    @task
    def start_hello(name:str):
        print(f"Hello user: {name}")
        return ['calc-1','calc-2','calc-3']

    @task
    def run_query(query_id):
        print(f"running query in bigquery: {query_id}")
        if query_id=='calc-3':
            raise Exception("failed to run")

    @task
    def mark_complete():
        print("job is completed")

    start=start_hello('Root')
    run_query.expand(query_id=start) >> mark_complete()

