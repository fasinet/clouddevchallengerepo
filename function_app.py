import azure.functions as func
from azure.data.tables import TableServiceClient, UpdateMode
from azure.core.exceptions import ResourceNotFoundError
import os
import json

app = func.FunctionApp()

@app.route(route="VisitCounter", auth_level=func.AuthLevel.ANONYMOUS)
def VisitCounter(req: func.HttpRequest) -> func.HttpResponse:
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        return func.HttpResponse("Missing AZURE_STORAGE_CONNECTION_STRING", status_code=500)
    table_name = "visitorcounttable"
    partition_key = "counter"
    row_key = "siteVisits"

    try:
        service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
        table_client = service_client.get_table_client(table_name=table_name)

        try:
            entity = table_client.get_entity(partition_key=partition_key, row_key=row_key)
            entity["Count"] += 1
            table_client.update_entity(entity, mode=UpdateMode.REPLACE)
            return func.HttpResponse(
                json.dumps({ "count": entity["Count"] }),
                mimetype="application/json",
                status_code=200
)
        except ResourceNotFoundError:
            entity = {
                "PartitionKey": partition_key,
                "RowKey": row_key,
                "Count": 1
            }
            table_client.create_entity(entity)
            return func.HttpResponse(
                json.dumps({ "count": 1 }),
                mimetype="application/json",
                status_code=200
)

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)