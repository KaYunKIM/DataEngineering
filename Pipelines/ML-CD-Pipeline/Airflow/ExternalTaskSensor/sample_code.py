# 함수 생성
def get_client_names(**context):
    client_list = ["test1", "test2"]
    return client_list


def client_sensor(**context):
    clients = context['task_instance'].xcom_pull(task_ids='get_client_names_task')
    tasks = []
    for client in clients:
        client_task = ExternalTaskSensor(
            task_id="keyword_{}_sensor".format(client),
            external_dag_id="keyword_{}_v2.0".format(client),
            external_task_id=None,  # wait until DAG is completed
            execution_date_fn=lambda x: x,
            mode="reschedule",
            timeout=7200,  # fail after 2Hrs
            queue="keyword_train",
            dag=dag,
        )
        tasks.append(client_task)
    return tasks