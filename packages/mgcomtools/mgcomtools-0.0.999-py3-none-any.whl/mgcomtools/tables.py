from google.cloud import bigquery
from datetime import datetime, timedelta
from collections import defaultdict

bq_client = bigquery.Client()

all_status = []

def get_logs(step, table_id='newageriver.config.adriver-logs-test'):

    #Получаем данные для обработки
    query = f"""
        SELECT path FROM  
            (SELECT
            time,
            path,
            step,
            is_completed,
            ROW_NUMBER() OVER(PARTITION BY path ORDER BY time DESC) as num
        FROM `{table_id}`) as t
        WHERE num = 1 and step = '{step}' and is_completed = TRUE;"""

    query_job = bq_client.query(query)
    return query_job.result()


class Logs:

    all_status = []
    
    def __init__(self, URL, step):

        parts = URL.split('/')
        self.name = parts[-2] # Название FTP рекламодателя
        self.log_type = parts[-1].split('.')[-3] # Название лога
        self.file_date = URL.split('.')[0].split('__')[-1] # дата лога, для ссылки
        self.step = step
        self.URL = URL


    def update_log(self):

        moscow_time = datetime.now() + timedelta(hours=3)
        current_timestamp = moscow_time.strftime('%Y-%m-%d %H:%M:%S') 
        
        query = f"""
            (DATE('{current_timestamp}'),
            DATETIME('{current_timestamp}'),
            '{self.name}',
            '{self.log_type}',
            DATE('{self.file_date}'),
            '{self.URL}',
            '{self.step}',
            TRUE)"""
        
        Logs.all_status.append(query)


def insert_logs(table_id='newageriver.config.adriver-logs-test'):

    all_status_string = ', '.join(Logs.all_status)

    #Обновляем таблицу
    query = f"""
        INSERT INTO `{table_id}` (date, time, ftp, log_type, log_date, path, step, is_completed)
        VALUES
        {all_status_string}"""

    bq_client.query(query)


def update_log(URL, step):
    Logs(URL, step).update_log()


def get_ftp_client_data():
    
    query = f"""
        SELECT client, ftp_names
        FROM `newageriver.config.client_ftp`
        WHERE client_status = 'on'
        GROUP BY client, ftp_names
        """  
    query_job = bq_client.query(query)
    return query_job.result()


def update_clients_table(client_name, log_date):
    
    print('clients to update:', client_name, log_date)
    query =  f"""
        DELETE FROM `newageriver.config.clients-modify`
        WHERE client = '{client_name}' AND log_date = '{log_date}';

        INSERT INTO `newageriver.config.clients-modify` (client, log_date, modified, status)
        VALUES
        ('{client_name}',
        DATE('{log_date}'),
        NULL,
        NULL);"""
    
    bq_client.query(query)