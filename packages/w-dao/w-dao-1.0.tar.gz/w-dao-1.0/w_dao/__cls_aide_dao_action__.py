class cls_aide_dao_action:
	def __init__(self, table_name: str):
		self._table = table_name
		self.insert_dict = {}
		self.update_list = []
		self.sql_where = ""

	def where(self, sql_where):
		self.sql_where = " WHERE " + sql_where

	def and_where(self, sql_where):
		self.sql_where = self.sql_where + " AND " + sql_where

	def or_where(self, sql_where):
		self.sql_where = self.sql_where + " OR " + sql_where

	def add(self, data: str, new_value: str = None):

		# if data.find("="):
		# 	split_index = data.find("=")
		# 	column = data[:split_index]
		# 	value = data[split_index + 1:]
		# else:
		# 	column = data
		# 	value = new_value
		column = data
		if isinstance(new_value, int):
			pass
		elif new_value is None:
			new_value = 'NULL'
		else:
			new_value = new_value.replace("'", "''")
			new_value = f"'{new_value}'"

		value = new_value

		self.insert_dict[column] = value

	def update(self, column_value: str):
		self.update_list.append(column_value)

	@property
	def sql_to_add(self):

		sql_columns = None
		sql_values = None

		print(self.insert_dict)

		for column in self.insert_dict:
			value = self.insert_dict[column]

			if sql_columns is None:
				sql_columns = column
				sql_values = value
			else:
				sql_columns = f'{sql_columns},{column}'
				sql_values = f"{sql_values},{value}"

		sql = f"INSERT " \
			  + f" INTO {self._table}" \
			  + f" ({sql_columns}) VALUES ({sql_values})" + self.sql_where

		self.insert_dict = {}

		return sql

	@property
	def sql_to_update(self):
		self.update_list = []
		sql=""
		return sql
