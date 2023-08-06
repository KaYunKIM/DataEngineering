from airflow import DAG, settings
from airflow.models import DagRun
from airflow.operators.python import PythonOperator
from datetime import datetime, timezone, timedelta


DAG_ID = 'delete_old_dag_runs'

def delete_old_dag_runs(max_age_days=32):
    session = settings.Session()

    # Get days to keep record
    date_threshold = datetime.now(timezone(timedelta(hours=9))) - timedelta(days=max_age_days)
    # Get list of dag runs to delete
    dag_runs_to_delete = session.query(DagRun).filter(DagRun.execution_date <= date_threshold).all()

    # Delete the old dag runs from the database
    for dag_run in dag_runs_to_delete:
        # To check dag_run info from task log
        print(dag_run)
        session.delete(dag_run)

    session.commit()
    session.close()
    return len(dag_runs_to_delete)


with DAG(
    dag_id=DAG_ID,
    default_args=DEFAULT_ARGS,
    schedule_interval='0 7 * * *',
    catchup=False,
) as dag:

    delete_old_dag_runs = PythonOperator(
        task_id='delete_old_dag_runs',
        python_callable=delete_old_dag_runs,
        provide_context=True,
        queue='queue'
    )

    delete_old_dag_runs