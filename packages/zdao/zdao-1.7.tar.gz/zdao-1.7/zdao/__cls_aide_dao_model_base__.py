from .__cls_aide_dao_model_column__ import __cls_aide_dao_model_column__
from .__cls_aide_dao_db_types__ import __cls_aide_dao_db_types__


class __cls_aide_dao_model_base__:
    def __init__(self):
        self.__dict_all = {}

        self.__db_type = None

        self.schema_name = None

        self.table_name = None

        self.table = f'{self.schema_name}.{self.table_name}'

        self.all_columns = f"{self.table}.*"

    def set_base(self, db_type, schema_name, table_name):
        self.__dict_all = {}

        self.set_db_type(db_type)

        self.schema_name = f'"{schema_name}"'

        self.table_name = f'"{table_name}"'

        self.table = f'{self.schema_name}.{self.table_name}'

        self.all_columns = f"{self.table}.*"

    @property
    def db_type(self):
        return self.__db_type

    def set_db_type(self, db_type: str):
        self.__db_type = __cls_aide_dao_db_types__.get_db_type(db_type)

    def column(self, new_pure_col_name: str,
               new_mask_name: str = None,
               new_map_code: str = None,
               new_value=None,
               new_default_value=None,
               is_key: bool = False,
               not_null: bool = False, ):
        return __cls_aide_dao_model_column__(new_pure_db_table_name=self.table_name,
                                             new_pure_col_name=new_pure_col_name,
                                             new_mask_name=new_mask_name,
                                             new_map_code=new_map_code,
                                             new_value=new_value,
                                             new_default_value=new_default_value,
                                             is_key=is_key,
                                             not_null=not_null,
                                             dict_all=self.__dict_all,
                                             db_type=self.__db_type)

    @property
    def all(self):
        return self.__dict_all

    @property
    def dict_map_code(self):
        return {self.__dict_all[column_name]["map_code"]: column_name for column_name in self.__dict_all
                if self.__dict_all[column_name]["map_code"] is not None}

    # # 动态添加属性,可行，但是在IDE里无法自动提示和补全还有检测
    # def add_column(self, column_name):
    #     column = column_model(self.table, column_name, db_type=self.db_type)
    #     setattr(cls_dao_model_base, column_name, column)
