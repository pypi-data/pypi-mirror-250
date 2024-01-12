from datetime import datetime
import snowflake

from dftools.events import StandardErrorEvent
from dftools.database.query import QueryExecResult, QueryWrapper
from dftools.database.base import BaseConnectionAdapterManager
from dftools.database.snowflake.connection_util import SnowflakeUtil as SnowUtil
from dftools.database.snowflake.connection import SnowflakeConnectionWrapper, SnowflakeCredentials
from dftools.database.snowflake.connection_metadata import SnowflakeConnectionMetadataService


class SnowflakeConnectionAdapterManager(BaseConnectionAdapterManager):
    def __init__(self):
        super().__init__(SnowflakeConnectionMetadataService())

    def log_execution_error(self, error: snowflake.connector.errors.ProgrammingError) -> None:
        """
        Logs an error event for a snowflake error

        Parameters
        ----------
        error : snowflake.connector.errors.ProgrammingError
            The snowflake error
        """
        self.log_event(StandardErrorEvent(SnowUtil.get_standard_error_message(error)))

    @classmethod
    def get_active_cursor(cls, conn_wrapper: SnowflakeConnectionWrapper):
        """
        Get the active cursor on the connection wrapper

        Parameters
        ----------
        conn_wrapper : SnowflakeConnectionWrapper
            The snowflake connection wrapper

        Returns
        ----------
            The connection cursor
        """
        return conn_wrapper.connection.cursor()

    def execute_query(self, conn_name: str, query_wrapper: QueryWrapper) -> QueryExecResult:
        conn_wrapper: SnowflakeConnectionWrapper = self.get_connection(conn_name)
        cur = self.get_active_cursor(conn_wrapper)
        start_tst = datetime.now()
        query_wrapper.update_interpreted_query()
        try:
            cur.execute(query_wrapper.interpreted_query)
            return QueryExecResult(query_wrapper.name, QueryExecResult.SUCCESS, query_wrapper.interpreted_query
                                   , cur.sfqid, list(cur)
                                   , SnowUtil.get_structure_from_result_metadata(cur.description), start_tst,
                                   datetime.now())
        except snowflake.connector.errors.ProgrammingError as e:
            self.log_execution_error(e)
            query_wrapper.raise_runtime_exception()
            return QueryExecResult(query_wrapper.name, QueryExecResult.ERROR, query_wrapper.interpreted_query
                                   , e.sfqid, [SnowUtil.get_standard_error_message(e)]
                                   , SnowUtil.get_structure_for_error_result(), start_tst, datetime.now())
        finally:
            cur.close()

    def update_connection_schema_info(self, conn_name: str):
        """
        Update the connection schema information stored in this wrapper and updates the connection.

        Parameters
        ----------
        conn_name : str
            The connection name

        """
        credentials: SnowflakeCredentials = self.get_connection(conn_name).credentials
        if credentials.role is None:
            return

        self.execute_query(conn_name
                           , query_wrapper=QueryWrapper(query="USE ROLE {role}", params={"role": credentials.role}
                                                        , runtime_exception_message="Role {role} cannot be set"))

        if credentials.warehouse is not None:
            self.execute_query(conn_name
                               , query_wrapper=QueryWrapper(query="USE WAREHOUSE {warehouse}"
                                                            , params={"warehouse": credentials.warehouse}
                                                            , runtime_exception_message="Role {role} cannot be set"))

        if credentials.catalog is not None:
            self.execute_query(conn_name
                               , query_wrapper=QueryWrapper(
                                    query="USE DATABASE {catalog}"
                                    , params={"catalog": credentials.catalog}
                                    , runtime_exception_message="Database {catalog} cannot be set"))

            if credentials.schema is not None:
                self.execute_query(conn_name
                                   , query_wrapper=QueryWrapper(
                                        query="USE SCHEMA {schema}"
                                        , params={"schema": credentials.schema}
                                        , runtime_exception_message="Schema {schema} cannot be set"))

    def retrieve_current_session_id(self, conn_name: str) -> str:
        session_id = self.execute_query_for_single_value_output(conn_name
            , query_wrapper=QueryWrapper(query='SELECT CURRENT_SESSION() AS SESSION_ID', name='Get Session ID'))
        self.get_connection(conn_name).session_id = session_id
        return session_id

    def get_ddl(self, conn_name: str, obj_type: str, obj_name: str, output_file_path: str = None) -> str:
        """
        Get the DDL from the database connection provided for a single object of the type and name provided

        Params
        -------
        conn_name : str
            The connection name
        obj_type : str
            The object type (should be one of the following : TABLE, VIEW, PROCEDURE, SCHEMA, DATABASE)
        obj_name : str
            The object name
        output_file_path : str, optional
            The output file path for the DDL statement
            
        Returns
        -------
            The DDL statement retrieved from the database connection
        """
        get_ddl_query = QueryWrapper(query=f'SELECT GET_DDL(\'{obj_type}\', \'{obj_name}\');')
        return self.execute_query_for_single_value_output(conn_name, get_ddl_query, output_file_path)
