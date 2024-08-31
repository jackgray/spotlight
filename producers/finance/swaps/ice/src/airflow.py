
from os import getenv
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

docker_image = os.getenv('DOCKER_IMAGE', 'jackgray/fetch_ice_swaps:latest')
git_repo_url = getenv('GIT_REPO_URL_ICE_SWAPS')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 31),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=15),
    'dagrun_timeout': timedelta(hours=2),
    'pool': 'my_pool',
    'priority_weight': 10,
    'execution_timeout': timedelta(hours=1),
    'queue': 'default',
    'on_failure_callback': failure_callback,
    'on_retry_callback': retry_callback,
    'on_success_callback': success_callback,
}


dag = DAG(
    'fetch_swap_equities_from_ice',
    default_args=default_args,
    description='DAG to fetch CSV data from multiple URLs concurrently using asyncio and stream processing',
    schedule_interval=@daily,  # Set the desired interval (daily, weekly, etc.)
)



def check_image(image_name, **kwargs):
    client = docker.from_env()
    try:
        client.images.get(image_name)
        print(f"Image {image_name} exists.")
    except docker.errors.ImageNotFound:
        raise ValueError(f"Image {image_name} not found. Please build or pull the image.")


def pull_image(image_name, **kwargs):
    client = docker.from_env()
    try:
        client.images.pull(image_name)
        print(f"Pulled image {image_name}.")
    except docker.errors.APIError as e:
        raise RuntimeError(f"Failed to pull image: {e}")


def build_image(image_name, dockerfile, build_context, **kwargs):
    client = docker.from_env()
    try:
        client.images.build(path=build_context, tag=image_name, dockerfile=dockerfile)
        print(f"Built image {image_name}.")
    except docker.errors.APIError as e:
        raise RuntimeError(f"Failed to build image: {e}")



with dag:

    check_image = PythonOperator(
        task_id='check_for_image',
        python_callable=check_image,
        op_kwargs={
            'image_name': docker_image,
            'build_context': '..',
            'dockerfile': 'Dockerfile'
        },
    )

    pull_image = PythonOperator(
        task_id='pull_image',
        python_callable=pull_image,
        op_kwargs={'image_name': docker_image}
    )

    build_image = PythonOperator(
        task_id='build_image',
        python_callable=build_image,
        op_kwargs={
            'image_name': docker_image,
            'dockerfile': 'Dockerfile',
            'build_context': '..'
        }
    )


    pull_latest_commit = BashOperator(
        task_id='pull_latest_commit',
        bash_command=f"""
            git ls-remote {git_repo_url} HEAD | awk '{print $1}' > /tmp/latest_commit.txt
        """,
    )


    # Run from Docker   
    run_docker = DockerOperator(
        task_id=f'fetch_ice_swaps_equity_{start_date}-{end_date}',
        image=docker_image,
        api_version='auto',
        auto_remove=False,
        command='python main.py {args}',
        docker_url='unix://var/run/docker/sock',
        network_mode='bridge',
        force_pull=True,
        dag=dag,
    )


    # Task to clone the GitHub repo and run the script
    run_local = BashOperator(
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


    check_image >> pull_image >> build_image >> run_docker

