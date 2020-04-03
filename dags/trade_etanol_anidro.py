# --------------------------------------------------------------------------------
# Load The Dependencies
# --------------------------------------------------------------------------------
import json
import airflow
import pandas as pd
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from datetime import date, timedelta, datetime

# --------------------------------------------------------------------------------
# Load The Scripts and Variables
# --------------------------------------------------------------------------------
import format_csv

VAR_CONFIG = Variable.get("trade_etanol_variables", deserialize_json=True)
DAG_NAME = VAR_CONFIG["dag_name"]
DAG_DESCRIB = VAR_CONFIG["dag_describ"]
TEMP_DIR = '/tmp/'
LOCAL_PATH = '/usr/local/airflow/files/'
FILE_NAME = 'trade_etanol_anidro.csv'
LOCAL_PATH_FORMATED = '/usr/local/airflow/files/formated/'
FILE_FORMATED = 'trade_etanol_anidro_formated.csv'


def print_inform():
    file_read = pd.read_csv(LOCAL_PATH_FORMATED + FILE_FORMATED)
    print("Load File Name: trade_etanol_anidro_formated \n" + file_read)
    
# --------------------------------------------------------------------------------
# Init the DAG
# --------------------------------------------------------------------------------
DAG_DEFAULT_ARGS = {
    'owner': 'thiagodf',
    'depends_on_past': False,
    'start_date': datetime(2020, 4, 1),
    'email': ['thiagodf@ciandt.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    DAG_NAME,
    default_args=DAG_DEFAULT_ARGS,
    schedule_interval=timedelta(minutes=10),
    tags=[DAG_NAME],
    description=DAG_DESCRIB,
    catchup=False,
) as dag:

    start_dag = DummyOperator(task_id='start_dag')
            
    # Test => docker-compose -f docker-compose.yml run --rm webserver airflow test trade_etanol_anidro waiting_file_original 2020-04-02
    # verifica se existe o arquivo original
    waiting_file_original = FileSensor(
        task_id="waiting_file_original",
        fs_conn_id="fs_default",
        filepath=LOCAL_PATH + FILE_NAME,
        poke_interval=5)
    
    # Test => docker-compose -f docker-compose.yml run --rm webserver airflow test trade_etanol_anidro execute_file_original 2020-04-02
    # pega o arquivo original e formata ele
    execute_file_original = PythonOperator(
        task_id="execute_file_original",
        python_callable=format_csv.main)
    
    # Test => docker-compose -f docker-compose.yml run --rm webserver airflow test trade_etanol_anidro waiting_file_formated 2020-04-02
    # verifica se existe o arquivo formatado
    waiting_file_formated = FileSensor(
        task_id="waiting_file_formated",
        fs_conn_id="fs_default",
        filepath=TEMP_DIR + FILE_FORMATED,
        poke_interval=5)
    
    # Test => docker-compose -f docker-compose.yml run --rm webserver airflow test trade_etanol_anidro move_file_formated 2020-04-02
    # move o arquivo formatado para a pasta de formatado
    move_file_formated = BashOperator(
        task_id="move_file_formated",
        bash_command="hadoop fs -put -f {0} {1}".format(TEMP_DIR + FILE_FORMATED, LOCAL_PATH_FORMATED + FILE_FORMATED))
    
    # Test => docker-compose -f docker-compose.yml run --rm webserver airflow test trade_etanol_anidro load_file_formated 2020-04-02
    # carrega o arquivo formatado e da um print no log
    load_file_formated = PythonOperator(
        task_id="load_file_formated",
        python_callable=print_inform,
        provide_context=True)
    
    # Test => docker-compose -f docker-compose.yml run --rm webserver airflow test trade_etanol_anidro transfer_into_hive 2020-04-02
    # 
    transfer_into_hive = HiveOperator(
        task_id="transfer_into_hive",
        hql="LOAD DATA IN PATH '/tmp/trade_etanol_anidro_formated.csv' INTO TABLE etanol")
        
    end_dag = DummyOperator(task_id='end_dag')
    
start_dag >> waiting_file_original >> execute_file_original >> waiting_file_formated >> [move_file_formated, load_file_formated] >> transfer_into_hive >> end_dag