import pandas as pd
from datetime import datetime as dt

LOCAL_PATH = '/usr/local/airflow/files/'
FILE_NAME = 'trade_etanol_anidro.csv'
FILE_FORMATED = 'trade_etanol_anidro_formated.csv'
ENCODING = 'utf-8'


def main():
    file_csv = pd.read_csv(
        LOCAL_PATH + FILE_NAME,
        sep=';',
        decimal='.',
        encoding=ENCODING,
        parse_dates=['date_trade'],
        header=None,
        names=['date_trade',
               'value_per_liter_brl',
               'value_per_liter_usd',
               'weekly_variation'])

    file_csv.to_csv(LOCAL_PATH + FILE_FORMATED, index=False)
                    
    file_save = pd.read_csv(LOCAL_PATH + FILE_FORMATED)
    print("File Save: \n", file_save)

if __name__ == '__main__':
    main()
