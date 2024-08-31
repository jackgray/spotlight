

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 31),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'dagrun_timeout': timedelta(hours=2),
    'pool': 'my_pool',
    'priority_weight': 10,
    'execution_timeout': timedelta(hours=1),
    'queue': 'default',
    'on_failure_callback': failure_callback,
    'on_retry_callback': retry_callback,
    'on_success_callback': success_callback,
}



# Define the DAG
dag = DAG(
    'fetch_swap_equities_from_ice',
    default_args=default_args,
    description='DAG to fetch CSV data from multiple URLs using asyncio',
    schedule_interval=timedelta(days=1),  # Set the desired interval (daily, weekly, etc.)
)



run_task = PythonOperator(
    task_id=f'fetch_ice_swaps_equity_{start_date}-{end_date}',
    python_callable=fetch_data,
    op_kwargs={
        'start_date': 'yesterday',
        'end_date': 'today',
        'schema_dict'=schema_dict,
        'table_name': 'Swaps_ICE_source_af',  # Replace with your actual table name
    },
    dag=dag,
)


from os import getenv
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Get the GitHub repository URL from environment variable
git_repo_url = getenv('GIT_REPO_URL_ICE_SWAPS')

# Define default_args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate a DAG
dag = DAG(
    'fetch_data_from_github',
    default_args=default_args,
    description='Fetch and run script from GitHub',
    schedule_interval=timedelta(days=1),
)

# Task to clone the GitHub repo and run the script
run_script = BashOperator(
    task_id='clone_and_run_script',
    bash_command=(
        f'git clone {git_repo_url} /producers/finance/swaps/sources/ice && '
        'python /producers/finance/swaps/sources/ice/main.py'
        '--start_date {{ ds }} '
        '--end_date {{ next_ds }} '
        '--table_name Swaps_ICE_source_af'
    ),
    dag=dag,
)

run_script

