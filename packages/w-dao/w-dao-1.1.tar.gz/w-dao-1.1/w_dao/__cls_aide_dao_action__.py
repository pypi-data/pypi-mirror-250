class cls_aide_dao_action:
    def __init__(self, table_name: str):
        self._table = table_name
        self._dict_select = {}
        self._dict_insert_upidate = {}
        self.sql_where = ""

    def get_value(self, key):
        return self._dict_insert_upidate[key]

    def where(self, sql_where):
        self.sql_where = " WHERE " + sql_where

    def and_where(self, sql_where):
        self.sql_where = self.sql_where + " AND " + sql_where

    def or_where(self, sql_where):
        self.sql_where = self.sql_where + " OR " + sql_where

    def select(self, data: str, new_value: str = None):
        column = data

        if isinstance(new_value, int):
            pass
        elif new_value is None:
            new_value = None
        else:
            new_value = new_value.replace("'", "''")
            new_value = f"'{new_value}'"

        value = new_value

        self._dict_select[column] = value

    def add(self, data: str, new_value: str = None):

        if data.find("=") > 0:
            split_index = data.find("=")
            column = data[:split_index]
            value = data[split_index + 1:]
        else:
            column = data
            if isinstance(new_value, int):
                pass
            elif new_value is None:
                new_value = 'NULL'
            else:
                new_value = new_value.replace("'", "''")
                new_value = f"'{new_value}'"

            value = new_value

        self._dict_insert_upidate[column] = value

    def update(self, data: str, new_value: str = None):
        self.add(data=data, new_value=new_value)

    @property
    def SQL_add(self):

        sql_columns = None
        sql_values = None

        for column in self._dict_insert_upidate:
            value = self._dict_insert_upidate[column]

            if sql_columns is None:
                sql_columns = column
                sql_values = value
            else:
                sql_columns = f'{sql_columns},{column}'
                sql_values = f"{sql_values},{value}"

        sql = f"INSERT " \
              + f" INTO {self._table}" \
              + f" ({sql_columns}) VALUES ({sql_values})" + self.sql_where

        self._dict_insert_upidate = {}

        return sql

    @property
    def SQL_update(self):
        sql_update_item = None

        for column in self._dict_insert_upidate:
            value = self._dict_insert_upidate[column]

            if sql_update_item is None:
                sql_update_item = f"{column}={value}"
            else:
                sql_update_item = f'{sql_update_item},f"{column}={value}"'

        sql = f"UPDATE " \
              + f" {self._table} SET {sql_update_item}" \
              + self.sql_where

        self._dict_insert_upidate = {}

        return sql

    @property
    def SQL_select(self):
        sql_select_item = None

        for column in self._dict_select:

            value = self._dict_select[column]

            if value in [None, '', ]:
                pass
            else:
                column = f'{column} AS "{value}"'

            if sql_select_item is None:
                sql_select_item = column
            else:
                sql_select_item = f'{sql_select_item},{column}'

        sql = f"SELECT {sql_select_item}" \
              + f" FROM {self._table}" \
              + self.sql_where

        self._dict_select = {}

        return sql
