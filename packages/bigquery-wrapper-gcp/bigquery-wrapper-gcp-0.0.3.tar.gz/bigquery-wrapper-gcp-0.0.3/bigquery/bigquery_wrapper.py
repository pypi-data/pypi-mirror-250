from google.cloud import bigquery
from google.oauth2 import service_account

class BigQueryWrapper:
    def __init__(self, credentials):
        credentials = service_account.Credentials.from_service_account_info(credentials)
        
        # Construct a BigQuery client object.
        self.client = bigquery.Client(credentials=credentials)
    
    def call_with_error_handling(self, func, *args, **kwargs):
        """
        A generic wrapper function that calls the specified function with the provided arguments
        and handles any exceptions that occur.

        :param func: The function to call.
        :param args: Positional arguments to pass to the function.
        :param kwargs: Keyword arguments to pass to the function.
        :return: A tuple containing the result of the function call and any errors encountered.
        """
        errors = None
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred: {e}")
            errors = e
        return result, errors


    def insert_rows_json(self, table_id, rows_to_insert):
        _, errors = self.call_with_error_handling(
            self.client.insert_rows_json(
                table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert)
            ))
        return errors
    
    def insert_rows_dataframe(self, table_id, dataframe):

        table = self.client.get_table(table_id)  
        schema = table.schema

        _, errors = self.call_with_error_handling(
            self.client.insert_rows_from_dataframe, table_id, dataframe, selected_fields=schema, chunk_size=5000
            )
        return errors
