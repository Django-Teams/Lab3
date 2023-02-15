class Connection:
    connected = "{dbms} | C | Successfully connected to '{db}'"
    error = "{dbms} | C | Error while connecting to '{db}' database: {e}"
    closed = "{dbms} | C | Successfully closed the connection with '{db}'"

class ImportTables:
    already_exists = "{dbms} | W | Table with name '{table}' already exists"
    success = "{dbms} | W | Table '{table}' created successfully"

class ImportData:
    unsupported_dtype = "{dbms} | W | Encountered unsupported datatype in table '{table}'. Skipping data insertion"
    no_data = "{dbms} | W | There was no data provided to '{table}' table"
    success = "{dbms} | W | Table '{table}' filled with data succsesfully"

class ExportTables:
    success = "{dbms} | R | Successfully read whole '{db}' schema"

class ExportData:
    success = "{dbms} | R | Successfully read all '{table}' rows"