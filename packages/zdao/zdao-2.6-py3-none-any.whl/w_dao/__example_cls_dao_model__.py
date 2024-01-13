import zdao


class cls_dao_model:
	# noinspection PyMissingConstructor
	def __init__(self):
		pass

	dict_map_code = {}

	schema_name = '"SYNC_YOUZHAI"'

	table_name = '"MYSMSAPP_SMS_RECORD"'

	table = f'{schema_name}.{table_name}'

	all_columns = f"{table}.*"

	MODIFY_LOG = zdao.model(table, "MODIFY_LOG")

	MODIFY_UID = zdao.model(table, "MODIFY_UID")

	MODIFY_TIME_GMT0 = zdao.model(table, "MODIFY_TIME_GMT0")

	CREATE_UID = zdao.model(table, "CREATE_UID")

	CREATE_TIME_GMT0 = zdao.model(table, "CREATE_TIME_GMT0")

	OBSOLETE = zdao.model(table, "OBSOLETE")

	# ####

	ID = zdao.model(table, "ID")