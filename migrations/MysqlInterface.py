from . import Messages as msg

from typing import Iterator
import mysql.connector as mysql

class MySQL:
    
    dbms_name = "MySQL     "
    database = None
    conn = None

    def __init__(self, host:str, port:int, user:str, password:str, database:str) -> None:
        try:
            self.conn = mysql.connect(host=host,
                                      port=port,
                                      user=user,
                                      password=password,
                                      database=database)
            if self.conn.is_connected():
                cur = self.conn.cursor(buffered=True)
                cur.execute("select database()")
                self.database = cur.fetchone()[0]
                print(msg.Connection.connected.format(dbms=self.dbms_name,db=self.database))
                cur.close()

        except mysql.Error as error:
            print(msg.Connection.error.format(dbms=self.dbms_name,db=database,e=error))

        pass

    def export_tables(self) -> Iterator[dict]:
        """DB schema generator

        Yields:
            Iterator [{
                "name": str,
                "columns": list[ dict[ name, type, null, key, extra ] ]
            }]
        """
        cur = self.conn.cursor(buffered=True)
        # Get table list
        cur.execute(
            "SELECT table_name FROM information_schema.tables "+
            f"WHERE table_schema = '{self.database}'"
            )
        table_list = [item[0] for item in cur.fetchall()]

        # Get column data per table
        for table in table_list:
            cur.execute(f"DESCRIBE {table}")
            desc_raw = cur.fetchall()
            columns = []
            for column_desc in desc_raw:
                columns.append({
                    "name": column_desc[0],
                    "type": column_desc[1].decode("utf-8"),
                    "null": column_desc[2],
                    "key": column_desc[3],
                    "extra": column_desc[4],
                })

            yield {
                "name": table,
                "columns": columns
            }
        cur.close()
        print(msg.ExportTables.success.format(dbms=self.dbms_name,db=self.database))

    def export_data(self, table:str) -> Iterator[tuple]:
        """Table data generator

        Args:
            table (str): Table name

        Yields:
            Iterator[tuple]: Table data
        """
        cur = self.conn.cursor(buffered=True)
        
        cur.execute(f"SELECT * FROM {table}")
        for row in cur.fetchall():
            yield row
        cur.close()
        print(msg.ExportData.success.format(dbms=self.dbms_name,table=table))

    def close_conn(self) -> None:
        """Close DB connection
        """
        self.conn.close()
        print(msg.Connection.closed.format(dbms=self.dbms_name,db=self.database))