class __cls_aide_dao_db_types__:
    class _cls_db_type:
        def __init__(self, type_name: str, list_alias=None):

            if list_alias is None:
                list_alias = [type_name]
            elif isinstance(list_alias, list):
                list_alias.append(type_name)
            else:
                list_alias = list_alias.splite(",")

            self.__dict = {"type_name": type_name,
                           "aliases": list_alias,
                           "sql": None}

        @property
        def dict(self):
            return self.__dict

        @property
        def type_name(self):
            return self.__dict["type_name"]

        @property
        def aliases(self):
            return self.__dict["aliases"]

        @property
        def sql(self):
            return self.__dict["sql"]

        def set_sql(self, new_sql):
            self.__dict["sql"] = new_sql

    DB2 = _cls_db_type(type_name="DB2")
    PostgreSQL = _cls_db_type(type_name="PostgreSQL", list_alias=['pgs', 'postgres'])
    SQLite = _cls_db_type(type_name="SQLite")

    @classmethod
    def get_db_type(cls, db_alias: str):
        if db_alias is None:
            return cls.PostgreSQL.type_name
        else:
            for attr in dir(cls):
                inst = getattr(cls, attr)
                if isinstance(inst, cls._cls_db_type):
                    if db_alias.upper() in [alias.upper() for alias in inst.aliases]:
                        return inst.type_name
