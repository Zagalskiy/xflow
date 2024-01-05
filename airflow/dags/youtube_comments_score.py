# Импорт модулей
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
import datetime as dt


# Определение базовых аргументов для DAG
args = {
    "owner": "admin",
    "start_date": dt.datetime(2022, 12, 1),
    "retries": 1,
    "retry_delays": dt.timedelta(minutes=1),
    "depends_on_past": False
    # "schedule": '@hourly'
}

# Создание DAG 
with DAG(
    dag_id='youtube_comments_score',
    default_args=args,
    schedule='30 * * * *',
    max_active_runs=1,
    tags=['youtube', 'score'],
) as dag:
    get_data = BashOperator(task_id='get_data',
                            bash_command="python3 /home/igor/xflow/scripts/get_data.py",
                            dag=dag)
    process_data = BashOperator(task_id='process_data',
                            bash_command="python3 /home/igor/xflow/scripts/process_data.py",
                            dag=dag)
    train_test_split = BashOperator(task_id='train_test_split',
                            bash_command="python3 /home/igor/xflow/scripts/train_test_split.py",
                            dag=dag)  
    train_model = BashOperator(task_id='train_model',
                            bash_command="python3 /home/igor/xflow/scripts/train_model.py",
                            dag=dag)
    test_model = BashOperator(task_id='test_model',
                            bash_command="python3 /home/igor/xflow/scripts/test_model.py",
                            dag=dag)
    get_data >> process_data >> train_test_split >> train_model >> test_model
