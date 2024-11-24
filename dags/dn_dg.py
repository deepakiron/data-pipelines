from __future__ import annotations

from datetime import datetime

from airflow.decorators import task
from airflow.models.dag import DAG

with DAG(dag_id="example_dynamic_task_mapping_7", schedule=None, start_date=datetime(2022, 3, 4)) as dag:

    # @task
    # def add_one(x: int):
    #     return x + 1
    #
    # @task
    # def sum_it(values):
    #     total = sum(values)
    #     print(f"Total was {total}")
    #
    # added_values = add_one.expand(x=[1, 2, 3])
    # sum_it(added_values)
    @task
    def get_calcs(scheduling_group: list):
        return ['SA'+("%03d"%i) for i in range(100)]

    # TODO: AS this limits to all the running dags so need to check this
    @task(max_active_tis_per_dag=25)
    def run_query_in_bq(calc_id: str):
        print(f"running calculation: {calc_id}")
        return {calc_id:"success"}


    @task
    def mark_complete(calc_ids:dict,scheduling_group: str):
        # date_list_xcoms = ti.xcom_pull(task_ids="run_query_in_bq")
        print(f"date entered is {calc_ids} - params passed")
        print("All tasks are completed")
    calcs=get_calcs(scheduling_group=['SAMS_INSTACART'])
    submitted_jobs=run_query_in_bq.expand(calc_id=calcs)

    submitted_jobs >> mark_complete(calc_ids=submitted_jobs,scheduling_group="SAMS_INSTACART")
