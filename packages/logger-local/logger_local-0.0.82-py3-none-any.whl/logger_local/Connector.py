import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connections_pool = {}


# We are using the database directly to avoid cyclic dependency
def get_connection(schema_name: str) -> mysql.connector:
    if (schema_name in connections_pool and
            connections_pool[schema_name] and
            connections_pool[schema_name] and
            connections_pool[schema_name].is_connected()):
        return connections_pool[schema_name]
    else:
        connection = mysql.connector.connect(
            host=os.getenv('RDS_HOSTNAME'),
            user=os.getenv('RDS_USERNAME'),
            password=os.getenv('RDS_PASSWORD'),
            database=schema_name
        )
        connections_pool[schema_name] = connection
        return connection
