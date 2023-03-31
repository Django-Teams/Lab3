class Database:
    __connection = None

    def __init__(self, name="MYSQL"):
        self.name = name

    def __enter__(self):
        if self.name == "MYSQL":
            import mysql.connector
            self.__connect_mysql(mysql.connector)
            return self.__connection

        raise ValueError("Не знайдено тип підключення")

    def __connect_mysql(self, connector):
        self.__connection = connector.connect(
            host="localhost",
            user="root",
            password="",
            database="django_lab1"
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.close()
