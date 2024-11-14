import azure.functions as func
import logging
from azure.data.tables import TableServiceClient, UpdateMode
import os


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# Initialize the Table Service Client
connection_string = os.getenv("AzureWebJobsStorage")  # Ensure this is set in app settings
table_name = "userquery"
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = table_service.get_table_client(table_name=table_name)

@app.route(route="Httptrigger1")
def Httptrigger1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve query parameters for name, partition_key, and row_key
    name = req.params.get('name')
    partition_key = "default_partition"
    row_key = "001"

    
    
    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    try:
        # Retrieve the entity by partition_key and row_key
        entity = table_client.get_entity(partition_key=partition_key, row_key=row_key)

        # Update the Name field with the new value
        entity['Name'] = name
        table_client.update_entity(entity=entity, mode=UpdateMode.REPLACE)

        return func.HttpResponse(f"Entity updated successfully with Name: {name}", status_code=200)

    except Exception as e:
        logging.error(f"Error updating entity: {e}")
        return func.HttpResponse(f"Failed to update entity: {str(e)}", status_code=500)