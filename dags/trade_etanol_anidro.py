# --------------------------------------------------------------------------------
# Load The Dependencies
# --------------------------------------------------------------------------------
import json
import csv
import airflow
import pandas as pd
from airflow import DAG
from airflow.models import Variable
from sqlalchemy import create_engine
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# --------------------------------------------------------------------------------
# Load The Variables
# --------------------------------------------------------------------------------
var_config = Variable.get("trade_etanol_variables", deserialize_json=True)
dag_name = var_config["dag_name"]
dag_describ = var_config["dag_describ"]
local_path = var_config["local_path"]
local_tmp = var_config["local_tmp"]
file_name = var_config["file_name"]
ext =  var_config["ext"]
encoding = var_config["encoding"]
db_user = var_config["db_user"]
db_pw = var_config["db_pw"]
db_sv = var_config["db_sv"]
db_port = var_config["db_port"] 
db_name = var_config["db_name"]
db_table = var_config["db_table"]

file_path = local_path + file_name + ext
mysql_engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(db_user, db_pw, db_sv, db_port, db_name))
dag_describ = dag_describ + " (Read Csv and Insert in DB)."

# --------------------------------------------------------------------------------
# Create Defs
# --------------------------------------------------------------------------------

# exibe no log arquivo original
def load_file_original():
    print("Load File Name: " + file_name)
    file_original = pd.read_csv(local_path + file_name + ext, header=None)
    print(file_original)

# pega o arquivo original e formata ele
def formating_file(**kwargs):
    print("Formating File Name: " + file_name)
    format_in = str(kwargs['execution_date'].day) + str(kwargs['execution_date'].month) + str(kwargs['execution_date'].year)
    file_formated = file_name + '_' + format_in + ext
    
    file_csv = pd.read_csv(
        file_path,
        sep=';',
        decimal='.',
        encoding=encoding,
        parse_dates=['ref_date'],
        header=None,
        names=['ref_date',
               'value_per_liter_brl',
               'value_per_liter_usd',
               'weekly_variation'])

    file_csv.to_csv( local_tmp + file_formated, sep=',', index=False)
    file_formated_path = local_tmp + file_formated
    file_formated = pd.read_csv(file_formated_path)
    print(file_formated)
    return file_formated_path
 
# pega o arquivo formatado e salva os dados no db
def insert_in_db(mysql_engine, db_table_name, **kwargs):
    print("Insert data in db....\n")
    file_formated_path = kwargs['ti'].xcom_pull(task_ids='formating_file')
    file_formated = pd.read_csv(file_formated_path)
    file_formated.to_sql(db_table_name, mysql_engine, if_exists='replace', index_label='id')

# faz uma consulta no db e retorna o dados
def select_data_etanol(mysql_engine, db_table_name, **kwargs):
    print("Select data in db....\n")
    data_etanol = pd.read_sql("""
    SELECT * FROM trade.{0}
    """.format(db_table_name), mysql_engine)
    print(data_etanol.info)  
    
# --------------------------------------------------------------------------------
# Init the DAG
# --------------------------------------------------------------------------------
default_args = {
    'owner': 'thiagodf',
    'depends_on_past': False,
    'start_date': datetime(2015, 12, 1),
    'email': ['thiagodf@ciandt.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=15),
}

with DAG(
    dag_name,
    default_args=default_args,
    schedule_interval=timedelta(minutes=10),
    tags=[dag_name],
    description=dag_describ,
    catchup=False
) as dag:

    start_dag = DummyOperator(task_id='start_dag')
        
    # Test => docker-compose -f docker-compose.yml run --rm webserver airflow test trade_etanol_anidro load_file_original 2020-03-29
    # exibe no log arquivo original
    load_file_original = PythonOperator(
        task_id="load_file_original",
        python_callable=load_file_original)
      
    # Test => docker-compose -f docker-compose.yml run --rm webserver airflow test trade_etanol_anidro formating_file 2020-03-29
    # pega o arquivo original e formata ele
    formating_file = PythonOperator(
        task_id="formating_file",
        provide_context=True,
        python_callable=formating_file)
    
    # Test => docker-compose -f docker-compose.yml run --rm webserver airflow test trade_etanol_anidro insert_in_db 2020-03-29
    # pega o arquivo formatado e salva os dados no db
    insert_in_db = PythonOperator(
        task_id="insert_in_db",
        provide_context=True,
        python_callable=insert_in_db,
        op_kwargs={ 'db_table_name': db_table, 'mysql_engine': mysql_engine })
    
    # Test => docker-compose -f docker-compose.yml run --rm webserver airflow test trade_etanol_anidro select_data_etanol 2020-03-29
    # seleciona dados de etanol
    select_data_etanol = PythonOperator(
        task_id="select_data_etanol",
        provide_context=True,
        python_callable=select_data_etanol,
        op_kwargs={ 'db_table_name': db_table, 'mysql_engine': mysql_engine })
    
    end_dag = DummyOperator(task_id='end_dag')

start_dag >> load_file_original >> formating_file >> insert_in_db >> select_data_etanol >> end_dag