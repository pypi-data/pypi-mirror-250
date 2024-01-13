import zdao


class cls_dao_model(zdao.model):
    # noinspection PyMissingConstructor
    def __init__(self):
        self.set_base(db_type="SQLite", schema_name="SYNC_YOUZHAI", table_name="MYSMSAPP_SMS_RECORD")

        self.MODIFY_LOG = self.column("MODIFY_LOG")

        self.MODIFY_UID = self.column("MODIFY_UID")

        self.MODIFY_TIME_GMT0 = self.column("MODIFY_TIME_GMT0")

        self.CREATE_UID = self.column("CREATE_UID")

        self.CREATE_TIME_GMT0 = self.column("CREATE_TIME_GMT0")

        self.OBSOLETE = self.column("OBSOLETE")

        # ####

        self.ID = self.column("ID")

# class cls_dao_model:
# 	# noinspection PyMissingConstructor
# 	def __init__(self):
# 		pass
#
# 	dict_map_code = {}
#
# 	schema_name = '"SYNC_YOUZHAI"'
#
# 	table_name = '"MYSMSAPP_SMS_RECORD"'
#
# 	table = f'{schema_name}.{table_name}'
#
# 	all_columns = f"{table}.*"
#
# 	MODIFY_LOG = zdao.column(table, "MODIFY_LOG")
#
# 	MODIFY_UID = zdao.column(table, "MODIFY_UID")
#
# 	MODIFY_TIME_GMT0 = zdao.column(table, "MODIFY_TIME_GMT0")
#
# 	CREATE_UID = zdao.column(table, "CREATE_UID")
#
# 	CREATE_TIME_GMT0 = zdao.column(table, "CREATE_TIME_GMT0")
#
# 	OBSOLETE = zdao.column(table, "OBSOLETE")
#
# 	# ####
#
# 	ID = zdao.column(table, "ID")
