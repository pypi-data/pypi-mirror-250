from pyspark.sql.functions import col
from google.cloud import bigquery
import pandas as pd
import pyspark

bq_client = bigquery.Client()

class UpdateSchema:
    _query_already_got = dict()


    def __init__(self, df, path):
        self.path = path
        print(path)
        self.df = df


    def __call__(self):
        if not self.path in UpdateSchema._query_already_got.keys():
            UpdateSchema._query_already_got[self.path] = self.get_schema_from_bq()
        self.schema = UpdateSchema._query_already_got[self.path]
        self.transform()
        print(UpdateSchema._query_already_got)
        print('Schema has been updated succesfully')
        
        return self.df


    def get_schema_from_bq(self):

        query = f"""
        SELECT field_name, table_path, {self.dataframe_type} FROM `newageriver.config.fields`
        WHERE table_path LIKE '{self.path}%'
        """      
        query_job = bq_client.query(query).result()
        schema_dict = dict()
        print(query)

        for row in query_job:
            column_name = row['field_name']
            column_type = row[self.dataframe_type]
            column_type = 'timestamp' if column_type == 'timestamp_ntz' else column_type
                
            schema_dict[column_name] = column_type

        return schema_dict

class PandasDataFrame(UpdateSchema):
    def __init__(self, df, path):
        super().__init__(df, path)
        self.dataframe_type = 'pandas_type'

    def transform(self):

        for column in self.df.columns:
            if column in self.schema.keys():
                if self.schema[column] != 'date':
                    try:
                        self.df[column] = self.df[column].astype(self.schema[column])
                    except Exception as e:
                        print(column, e)
                else:
                    # Проверить на загрузку в BigQuery
                    self.df[column] = pd.to_datetime(self.df[column]).dt.date
        return self.df


class PySparkDataFrame(UpdateSchema):
    def __init__(self, df, path):
        super().__init__(df, path)
        self.dataframe_type = 'pyspark_type'

    def transform(self):
        
        for column in self.df.schema.names:
            try:
                self.df = self.df.withColumn(column, col(column).cast(self.schema[column]))
            except Exception as e:
                print('Ошибка:', column, e)
            
        return self.df


def transform(data, path):

    if isinstance(data, pd.DataFrame):
        print("Это pandas DataFrame")
        df_obj = PandasDataFrame(data, path)
        
    # Проверка типа для PySpark DataFrame
    if isinstance(data, pyspark.sql.dataframe.DataFrame):
        df_obj = PySparkDataFrame(data, path)
    
    result = df_obj()
    del df_obj.df

    return result