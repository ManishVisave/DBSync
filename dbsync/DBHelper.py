from sqlalchemy import create_engine


class DBHelper:

    def __init__(self, config_helper):
        self.config_helper = config_helper
        self.group = 'DATABASE'
        self.username = self.config_helper.get_config(self.group, 'USERNAME')
        self.password = self.config_helper.get_config(self.group, 'PASSWORD')
        self.host = self.config_helper.get_config(self.group, 'HOST')
        self.database = self.config_helper.get_config(self.group, 'DB')
        self.con = create_engine(f"mysql+mysqldb://{self.username}:{self.password}@{self.host}/{self.database}")

    def add_base_tenant(self):
        self.con.connect()
        self.con.execute("UPDATE tenant SET tenant_id = 0 where tenant_name = 'Agilone Base'")

    def save_data_to_DB(self, data, table_name) -> None:
        self.con.connect()
        self.con.execute('SET FOREIGN_KEY_CHECKS = 0')
        self.con.execute(f'TRUNCATE TABLE {table_name}')
        data.to_sql(con=self.con, name=table_name, if_exists='append', index=False)
        print(f'{data.shape[0]} records saved in table {table_name}')
        self.con.execute('SET FOREIGN_KEY_CHECKS = 1')
        if table_name == 'tenant':
            self.add_base_tenant()
