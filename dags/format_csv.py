import pandas as pd
import airflow
from airflow.models import Variable
from datetime import datetime as dt

var_config = Variable.get("trade_etanol_variables", deserialize_json=True)
local_path = var_config["local_path"]
local_tmp = var_config["local_tmp"]
file_name = var_config["file_name"]
ext =  var_config["ext"]
encoding = var_config["encoding"]

file_original_path = local_path + file_name + ext
file_formated_path = local_tmp + file_name + '_formated' + ext

def main():
    file_csv = pd.read_csv(
        file_original_path,
        sep=';',
        decimal='.',
        encoding=encoding,
        parse_dates=['ref_date'],
        header=None,
        names=['ref_date',
               'value_per_liter_brl',
               'value_per_liter_usd',
               'weekly_variation'])

    file_csv.to_csv(file_formated_path, index=False)
                    
    file_save = pd.read_csv(file_formated_path)
    print("File Save: \n", file_save)

if __name__ == '__main__':
    main()
