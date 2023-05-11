class Database:
    __connection = None

    def __init__(self, name="MYSQL"):
        self.name = name

    def __enter__(self):
        if self.name == "MYSQL":
            import mysql.connector
            self.__connect_mysql(mysql.connector)
            return self.__connection
        elif self.name == "MONGO":
            self.__connect_mongo()
            db = self.__connection['django']
            return db

        raise ValueError("Не знайдено тип підключення")

    def __connect_mysql(self, connector):
        self.__connection = connector.connect(
            host="localhost",
            user="root",
            password="",
            database="django_lab1"
        )

    def __connect_mongo(self):
        from pymongo import MongoClient
        self.__connection = MongoClient()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.close()
