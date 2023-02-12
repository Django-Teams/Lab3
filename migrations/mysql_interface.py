import mysql.connector as mysql

class MySQL:

    def __init__(self, host:str, port:int, user:str, password:str, database:str) -> None:
        self.database = database

        try:
            self.conn = mysql.connect(host=host,
                                      port=port,
                                      user=user,
                                      password=password,
                                      database=database)
            if self.conn.is_connected():
                # Перевірка, чи успішне підключення + діагностичні повідомлення
                db_Info = self.conn.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.cur = self.conn.cursor(buffered=True)
                self.cur.execute("select database();")
                record = self.cur.fetchone()
                print("You're connected to database: ", record[0])

        except mysql.Error as e:
            # Виникла якась помилка
            print("Error while connecting to MySQL", e)

        finally:
            if self.conn.is_connected():
                # Отримання списку таблиць
                self.cur.execute(f"SELECT table_name FROM information_schema.tables \
                                WHERE table_schema = '{self.database}'")
                self.table_list = [item[0] for item in self.cur.fetchall()]

        pass

    def get_tables(self) -> dict[any]:
        """Генератор для отримання структури БД

        Yields:
            Iterator[ {
                "name": str,
                "columns": list[ dict[ name, type, null, key, extra ] ],
                "data": list[ tuple[ any ] ]
            } ]
        """

        for table in self.table_list:
            # Отримання та обробка даних про колонки в таблиці
            self.cur.execute(f"DESCRIBE {table}")
            desc_raw = self.cur.fetchall()
            columns = []
            for column_desc in desc_raw:
                columns.append({
                    "name": column_desc[0],
                    "type": column_desc[1],
                    "null": column_desc[2],
                    "key": column_desc[3],
                    "extra": column_desc[4],
                })

            yield {
                "name": table,
                "columns": columns
            }

    def get_data(self, table:str) -> tuple[any]:
        """Генератор для отримання даних БД

        Args:
            table (str): Назва таблиці

        Yields:
            Iterator[tuple[any]]: Дані таблиці
        """
        self.cur.execute(f"SELECT * FROM {table}")
        for row in self.cur.fetchall():
            yield row

    def close_all(self) -> None:
        """Закриває підключення та курсор
        """
        self.cur.close()
        self.conn.close()
        print("MySQL connection is closed")