

from __future__ import annotations
from itertools import chain
from datetime import datetime

from airflow.decorators import task
from airflow.models.dag import DAG
from sqlalchemy import create_engine
from core.utils.queryset import get_calc_details_from_db

engine = create_engine('postgresql://airflow:airflow@localhost/pipline_db')

with DAG(dag_id="dummy_pratice", schedule=None, start_date=datetime(2022, 3, 4)) as dag:


# push_func = PythonOperator(
#         task_id='push_func',
#         provide_context=True,
#         python_callable=values_function,
#         dag=dag)
#
#     complete = DummyOperator(
#         task_id='All_jobs_completed',
#         dag=dag)
#
#     for i in values_function():
#         push_func >> group(i) >> complete

    def get_calcs(scheduling_group: list):
        # return ['SA' + ("%03d" % i) for i in range(100)]
        get_calc_details_from_db(engine)
        return {"calcs":['SA97','SA98','SA99','SA100','SA101','SA102'],
                "dependency":{'SA100':['SA99','SA97'],'SA101':['SA99'],'SA102':['SA98']},
                "first_order":['SA97','SA98','SA99']}


    # TODO: AS this limits to all the running dags so need to check this

    @task(max_active_tis_per_dag=25)
    def run_query_in_bq(calc_id: str):
        print(f"running calculation: {calc_id}")
        return {calc_id: "success"}


    @task
    def mark_complete(calc_ids: dict, scheduling_group: str):
        # date_list_xcoms = ti.xcom_pull(task_ids="run_query_in_bq")
        print(f"date entered is {calc_ids} - params passed")
        print("All tasks are completed")


    # calcs = get_calcs(scheduling_group=['SAMS_INSTACART'])
    # submitted_jobs = run_query_in_bq.expand(calc_id=calcs)
    #
    # submitted_jobs >> mark_complete(calc_ids=submitted_jobs, scheduling_group="SAMS_INSTACART")
    mck=[]
    data = get_calcs(scheduling_group=['SAMS_INSTACART'])
    mapper={}
    end_nodes_calcs=list(chain(data["dependency"].values()))
    end_node_dags=[]
    for i in data["calcs"]:
        mapper[i]=run_query_in_bq(i)
        if i in end_nodes_calcs:
            end_node_dags.append(mark_complete)
        # if i in data["first_order"]:
        #     get_calcs.set_downstream(mapper[i])
    for i in data["dependency"]:
        parents=data["dependency"][i]
        for j in parents:
            mapper[i].set_upstream(mapper[j])

    # mark_complete.set_downstream(end_node_dags)