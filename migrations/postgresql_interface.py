from . import messages as msg

from datetime import datetime
from typing import Iterator
import psycopg2 as pg

class PostgreSQL:
    
    dbms_name = "PostgreSQL"
    database = None
    conn = None
    
    def __init__(self, host:str, port:int, user:str, password:str, database:str) -> None:        
        try:
            self.conn = pg.connect(host=host,
                              port=port,
                              user=user,
                              password=password,
                              database=database)
            
            cur = self.conn.cursor()

            cur.execute('SELECT current_database()')
            self.database = cur.fetchone()[0]
            print(msg.Connection.connected.format(dbms=self.dbms_name,db=self.database))
            
            cur.close()
            
        except (Exception, pg.DatabaseError) as error:
            print(msg.Connection.error.format(dbms=self.dbms_name,db=database,e=error))
        
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
        cur = self.conn.cursor()

        # Check if there isn't already table with the same name
        cur.execute("SELECT tablename FROM pg_catalog.pg_tables "+
                         "WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
        table_list = [item[0] for item in cur.fetchall()]
        curr_table_name = schema["name"]
        if curr_table_name in table_list:
            print(msg.ImportTables.already_exists.format(dbms=self.dbms_name,table=curr_table_name))
            return
        
        # Create table
        # Query start
        query = f"CREATE TABLE {curr_table_name} ("
        
        # Write columns into query
        # column -> dict[ name, type, null, key, extra ]
        for column in schema["columns"]:
            name = column["name"]
            
            if column["type"] == "datetime":
                dtype = "TIMESTAMP"
            else:
                dtype = column["type"]
            
            if column["null"] == "NO":
                null = "NOT NULL"
            else:
                null = ""
            
            if column["key"] == "PRI":
                null = ""
                key = f"CONSTRAINT {curr_table_name}_pk PRIMARY KEY"
            else:
                key = ""
            
            if column["extra"] != None:
                # Reserved for future
                pass
            
            column_query = f"{name} {dtype} {key}{null},"
            query += column_query
        
        # End of the query
        query = query[:-1]
        query += ");"
        
        cur.execute(query)
        self.conn.commit()
        print(msg.ImportTables.success.format(dbms=self.dbms_name,table=curr_table_name))
        cur.close()
    
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
        
        cur = self.conn.cursor()
        table_name = table["name"]
        columns = ""
        for item in table['columns']:
            columns += f"{item['name']},"
        columns = columns[:-1]
        
        # Empty the table in case it already has data in it
        cur.execute(f"TRUNCATE {table_name}")
        
        query = ""
        for row in data:
            values = ""
            for value in row:
                dtype = type(value)
                # str and datetime
                if dtype in [str, datetime]:
                    values += f"$${value}$$,"
                # int and float
                elif dtype in [int, float]:
                    values += f"{value},"
                # None of those
                else:
                    print(msg.ImportData.unsupported_dtype.format(dbms=self.dbms_name,table=table_name))
                    return

            # Truncate redundant comma
            values = values[:-1]
            query += f"INSERT INTO {table_name} ({columns}) VALUES ({values});\n"
        
        # Check if any data was provided
        if query == "":
            print(msg.ImportData.no_data.format(dbms=self.dbms_name,table=table_name))
            return
        
        cur.execute(query)
        self.conn.commit()
        print(msg.ImportData.success.format(dbms=self.dbms_name,table=table_name))
        cur.close()
    
    def export_tables(self) -> Iterator[dict]:
        """DB schema generator

        Yields:
            Iterator [{
                "name": str,
                "columns": list[ dict[ name, type, null, key, default ] ]
            }]
        """
        cur = self.conn.cursor()
        
        # Get the table list
        cur.execute(
            "SELECT tablename FROM pg_catalog.pg_tables "+
            "WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
            )
        table_list = [item[0] for item in cur.fetchall()]

        for table in table_list:
            # Get only relevant data of the columns
            cur.execute(f"""
                SELECT
                    f.attname as column,  
                    t.typname AS data_type_name,
                    f.attnotnull as not_null,
                    CASE  
                        WHEN p.contype = 'p' THEN 't'  
                        ELSE 'f'  
                    END AS is_primary_key,  
                    CASE
                        WHEN f.atthasdef = 't' THEN pg_get_expr(d.adbin, d.adrelid)
                    END AS default_value
                FROM pg_attribute f  
                    JOIN pg_class c ON c.oid = f.attrelid  
                    JOIN pg_type t ON t.oid = f.atttypid  
                    LEFT JOIN pg_attrdef d ON d.adrelid = c.oid AND d.adnum = f.attnum  
                    LEFT JOIN pg_namespace n ON n.oid = c.relnamespace  
                    LEFT JOIN pg_constraint p ON p.conrelid = c.oid AND f.attnum = ANY (p.conkey)  
                    LEFT JOIN pg_class AS g ON p.confrelid = g.oid  
                WHERE c.relkind = 'r'::char  
                    AND f.attisdropped = false
                    AND n.nspname = 'public'  -- Replace with Schema name  
                    AND c.relname = '{table}'  -- Replace with table name  
                    AND f.attnum > 0 
                ORDER BY f.attnum
                """)
            desc_raw = cur.fetchall()
            
            columns = []
            for column_desc in desc_raw:
                columns.append({
                    "name": column_desc[0],
                    "type": column_desc[1],
                    "null": column_desc[2],
                    "key": column_desc[3],
                    "default": column_desc[4],
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
        cur = self.conn.cursor()
        
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