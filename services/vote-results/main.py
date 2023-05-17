from google.cloud import bigquery
from flask import jsonify

def voting_results(request):
    # Configure BigQuery client
    project_id = 'votingadaproject'  # Replace with your project ID
    client = bigquery.Client(project=project_id)

    # Define your BigQuery query
    query = '''
        SELECT voted_for as member_id, count(*) as n_votes
        FROM `voting_db.vote`
        GROUP BY voted_for
    '''

    # Run the query
    query_job = client.query(query)
    results = query_job.result()

    rows = []
    for row in results:
        rows.append(dict(row))

    # Return the query data
    return jsonify(rows)