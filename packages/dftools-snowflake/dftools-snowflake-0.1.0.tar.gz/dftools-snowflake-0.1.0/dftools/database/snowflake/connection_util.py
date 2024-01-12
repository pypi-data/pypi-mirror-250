import snowflake.connector
from typing import List, Dict

from dftools.core.structure import Field, Structure, FieldCharacterisationStd


class SnowflakeUtil:

    @classmethod
    def get_standard_error_message(cls, error: snowflake.connector.errors.ProgrammingError) -> str:
        return 'Error {0} ({1}): {2} ({3})'.format(error.errno, error.sqlstate, error.msg, error.sfqid)

    @classmethod
    def get_field_from_result_metadata(cls, result_metadata: snowflake.connector.cursor.ResultMetadata) -> Field:
        return Field(
            name=result_metadata.name
            , desc=None
            , position=0
            , data_type=SnowflakeUtil.get_snowflake_data_type_mapping()[result_metadata.type_code]
            , length=result_metadata.internal_size
            , precision=result_metadata.scale
            , default_value=None
            , characterisations=[FieldCharacterisationStd.MANDATORY] if result_metadata.is_nullable else []
            , sourcing_info=None
        )

    @classmethod
    def get_result_error_field(cls) -> Field:
        return Field(
            name='Error Message'
            , desc=None, position=0
            , data_type='TEXT'
            , length=16777216
            , precision=0
            , default_value=None
            , characterisations=[]
            , sourcing_info=None
        )

    @classmethod
    def get_structure_from_result_metadata(cls
                                           , result_metadata_list: List[snowflake.connector.cursor.ResultMetadata]
                                           ) -> Structure:
        structure = Structure(name='ResultSet', desc=None, type='PyDataSet'
                              , row_count=0, options=None, content_type=None, fields=[], sourcing_info=None)
        for result_metadata in result_metadata_list:
            structure.add_field(new_field=SnowflakeUtil.get_field_from_result_metadata(result_metadata),
                                prevent_position_check=True)
        return structure

    @classmethod
    def get_structure_for_error_result(cls) -> Structure:
        structure = Structure(name='ResultSet', desc=None, type='PyDataSet'
                              , row_count=0, options=None, content_type=None, fields=[], sourcing_info=None)
        structure.add_field(new_field=SnowflakeUtil.get_result_error_field(), prevent_position_check=True)
        return structure

    @classmethod
    def get_snowflake_data_type_mapping(cls) -> Dict[int, str]:
        return {
            0: "NUMBER"
            , 1: "REAL"
            , 2: "TEXT"
            , 3: "DATE"
            , 4: "TIMESTAMP"
            , 5: "VARIANT"
            , 6: "TIMESTAMP_LTZ"
            , 7: "TIMESTAMP_TZ"
            , 8: "TIMESTAMP_NTZ"
            , 9: "OBJECT"
            , 10: "ARRAY"
            , 11: "BINARY"
            , 12: "TIME"
            , 13: "BOOLEAN"
        }
