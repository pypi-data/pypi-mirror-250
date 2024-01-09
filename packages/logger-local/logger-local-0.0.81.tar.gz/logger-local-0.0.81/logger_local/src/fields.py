import sys

from database_infrastructure_local.Connector import get_connection

from .MessageSeverity import MessageSeverity
from .SendToLogzIo import SendTOLogzIo

COMPUTER_LANGUAGE = "Python"
COMPONENT_ID = 102
COMPONENT_NAME = 'Logger Python'
Logzio_handler = SendTOLogzIo()

cache = []


class Fields:
    @staticmethod
    def getFieldsSingelton():
        global cache
        if cache:
            return cache
        sql_query = f"DESCRIBE logger.logger_table"
        try:
            object1 = {
                'record': {'severity_id': MessageSeverity.Information.value,
                           'severity_name': MessageSeverity.Information.name, 'component_id': COMPONENT_ID,
                           'component_name': COMPONENT_NAME, 'computer_language': COMPUTER_LANGUAGE,
                           'message': "get_logger_table_fields activated"},
                'severity_id': MessageSeverity.Information.value,
                'component_id': COMPONENT_ID,
                'severity_name': MessageSeverity.Information.name,
                'component_name': COMPONENT_NAME,
                'COMPUTER_LANGUAGE': COMPUTER_LANGUAGE,
                'message': "get_logger_table_fields activated",
            }
            Logzio_handler.send_to_logzio(object1)
            con = get_connection(schema_name="logger")
            cursor = con.cursor()
            cursor.execute(sql_query)
            columns_info = cursor.fetchall()
            columns = [column[0] for column in columns_info]
            cache = columns
            return columns

        except Exception as e:
            print("logger-local-python-package LoggerService.py sql(self) Exception caught SQL=" +
                  sql_query + " Exception=" + str(e), file=sys.stderr)
            return
