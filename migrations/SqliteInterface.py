from . import Messages as msg

from typing import Iterator
from datetime import datetime
import sqlite3

class SQLite:
    
    dbms_name = "SQLite    "
    database = None
    conn = None
    
    def __init__(self, path:str) -> None:        
        try:
            self.conn = sqlite3.connect(path)

            cur = self.conn.execute('PRAGMA database_list;')
            database_path = cur.fetchone()[2]
            # splt path to db by "/"
            # get only last element
            # get only left item in the list
            # throw away extension from the name
            self.database = database_path.split("\\")[-1:][0][:-3]
            print(msg.Connection.connected.format(dbms=self.dbms_name,db=self.database))
            
        except (Exception) as error:
            print(msg.Connection.error.format(dbms=self.dbms_name,db=path,e=error))
        
        pass
    
    def import_tables(self, schema:Iterator) -> None:
        """Create tables

        Args:
            schema (dict):
            {
                "name": str,
                "columns": list[ dict[ name, type, null, key, extra ] ]
            }
        """

        # Check if there isn't already table with the same name
        cur = self.conn.execute("SELECT name FROM sqlite_schema "+
                    "WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
        table_list = [item[0] for item in cur.fetchall()]
        curr_table_name = schema["name"]
        if curr_table_name in table_list:
            print(msg.ImportTables.already_exists.format(dbms=self.dbms_name,table=curr_table_name))
            return
        
        # Create table
        # Query start
        query = f"CREATE TABLE {curr_table_name} ("
        
        # Write columns into query
        # column -> dict[ name, type, null, key, default ]
        convert = {
            "int4": "INT",
            "timestamp": "TEXT",
            "varchar": "TEXT",
            "float8": "REAL"
        }
        for column in schema["columns"]:
            name = column["name"]
            dtype = convert[column["type"]]
            
            if column["null"]:
                # wierd right?
                null = "NOT NULL"
            else:
                null = ""
            
            if column["key"] == "t":
                null = ""
                key = "PRIMARY KEY"
            else:
                key = ""
            
            if column["default"] != None:
                # Reserved for future
                pass
            
            column_query = f"{name} {dtype} {key} {null},"
            query += column_query
        
        # End of the query
        query = query[:-1]
        query += ");"

        self.conn.execute(query)
        self.conn.commit()
        print(msg.ImportTables.success.format(dbms=self.dbms_name,table=curr_table_name))
    
    def import_data(self, table:dict, data:Iterator) -> None:
        """Write data to the table

        Args:
            table (dict): 
            {
                "name": str,
                "columns": list[ dict[ name, type, null, key, extra ] ]
            }
            data (Iterator): MySQL.import_data() yield
        """
        
        table_name = table["name"]
        columns = ""
        for item in table['columns']:
            columns += f"{item['name']},"
        columns = columns[:-1]
        
        # Empty the table in case it already has data in it
        self.conn.execute(f"DELETE FROM {table_name}")
        
        query = ""
        values = ""
        for row in data:
            values += "("
            for value in row:
                dtype = type(value)
                # str and datetime
                if dtype in [str, datetime]:
                    if dtype == str:
                        value = value.replace("'", "''")
                    values += f"'{value}',"
                # int and float
                elif dtype in [int, float]:
                    values += f"{value},"
                # None of those
                else:
                    print(msg.ImportData.unsupported_dtype.format(dbms=self.dbms_name,table=table_name))
                    return
            # Truncate redundant comma
            values = values[:-1] + "),"
        # Truncate redundant comma
        values = values[:-1]
        
        query += f"INSERT INTO {table_name} ({columns}) VALUES {values}"
        
        # Check if any data was provided
        if values == "":
            print(msg.ImportData.no_data.format(dbms=self.dbms_name,table=table_name))
            return
        
        self.conn.execute(query)
        self.conn.commit()
        print(msg.ImportData.success.format(dbms=self.dbms_name,table=table_name))

    def close_conn(self) -> None:
        """Close DB connection
        """
        self.conn.close()
        print(msg.Connection.closed.format(dbms=self.dbms_name,db=self.database))