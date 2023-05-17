from google.cloud import bigquery

bigquery_client = bigquery.Client(project="votingadaproject")
dataset_id = 'notification_service'
table_id = 'party_admin_message'

def create_table_if_not_exists():
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    schema = [
        bigquery.SchemaField('message', 'STRING'),
        bigquery.SchemaField('timestamp', 'TIMESTAMP')
    ]
    table = bigquery.Table(table_ref, schema=schema)
    try:
        bigquery_client.create_table(table)
        print(f"Table '{dataset_id}.{table_id}' created.")
    except:
        print(f"Table '{dataset_id}.{table_id}' already exists.")


def export_to_bigquery(message, timestamp):
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    rows_to_insert = [
        {'message': message, 'timestamp': timestamp}
    ]

    errors = bigquery_client.insert_rows(table_ref, rows_to_insert)
    if errors == []:
        print(f"Message exported to BigQuery: '{message}'")
    else:
        print(f"Error occurred while exporting message: '{message}'")