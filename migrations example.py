import migrations.mysql_interface as mysql_interface
import migrations.postgresql_interface as pg_interface
import migrations.sqlite_interface as sqlite_interface

# Connect to all the databases
mysql_db = mysql_interface.MySQL("localhost", 3306, "root", "admin", "djangolab1")
pg_db = pg_interface.PostgreSQL("localhost", 5432, "postgres", "admin", "djangolab1")
sqlite_db = sqlite_interface.SQLite("sqlite.db")

# Juggle the data around
try:
    mysql_tables = mysql_db.export_tables()
    for table in mysql_tables:
        pg_db.import_tables(table)
        pg_db.import_data(table, mysql_db.export_data(table["name"]))
        
    pg_tables = pg_db.export_tables()
    for table in pg_tables:
        sqlite_db.import_tables(table)
        sqlite_db.import_data(table, pg_db.export_data(table["name"]))

except (Exception) as error:
    print(error.with_traceback())

# Always remember to close the connections
mysql_db.close_conn()
pg_db.close_conn()
sqlite_db.close_conn()