import mysql
from mysql import connector
from sys import exit
from abc import ABC, abstractmethod
from datetime import datetime


class DBConnector(object):
    def __init__(self, _db_config, db_conn = None):

        try:
            assert _db_config.get("host")
            assert _db_config.get("port")
            assert _db_config.get("database")
            assert _db_config.get("user")
            assert _db_config.get("password")

            self.db_config = _db_config

        except AssertionError:
            raise AssertionError("Database Config object must contain keys: host, port, database, user, password.")

        self.cnx = db_conn or None # just in case an empty object is passed


    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def __connect(self):
        self.cnx = mysql.connector.connect(**self.db_config)

    def getCursor(self):
        self.__connect()
        return self.cnx.cursor()

    def commit(self):
        #to-do: Create Logging
        self.cnx.commit()


    def query(self, query):
        """Execute SQL query."""

        if not self.cnx:
            print("CNX is False, connecting...")
            self.__connect()

        else:
            print("Recycling Connection.")

        try:
            assert self.cnx
            cursor = self.getCursor()
            stat = cursor.execute(query)


            try:
                return cursor.fetchall()
            except:
                return stat

        except connector.errors.IntegrityError as err:
            return "not_unique"

        except connector.Error as err:
            print(err)
            exit(1)

        except AssertionError:
            raise AssertionError("Connector has not been defined")



class DBSchema(ABC):

    """
      This is an abstract base class for schemas for mysql
    """

    SCHEMA = None

    def __init__(self, _db_info,_conn=""):
        self.connector = DBConnector(_db_info, _conn) # to-do: Pass connection object to DBSchema
        self.db_info = _db_info

    def __isSchema(self):
        if self.SCHEMA:
            return True
        return False


    def sanitizeInsert(self, _query_object):
        return _query_object


    @abstractmethod
    def createTable(self):
        assert self.__isSchema
        # to-do: validation & Logging
        frame = """
        CREATE TABLE IF NOT EXISTS {_table_name} (
          {_columns}
        ) DEFAULT CHARACTER SET=utf8;
        """ #to-do: decouple query frame from insert

        tup_schemas = self.SCHEMA.get("columns")
        mapped_cols = map(lambda i: "%s,\n" % " ".join(i) if tup_schemas.index(i) != len(tup_schemas) - 1 else "%s" % " ".join(i), tup_schemas)
        proc_cols = [col for col in mapped_cols]

        cols = "".join(proc_cols)
        query = frame.format(_table_name = self.SCHEMA.get("name"), _columns = cols)

        print("CREATING TABLE WITH: %s" % query)
        stat = self.connector.query(query)
        self.connector.commit()

        return stat


    @abstractmethod
    def insertOne(self, _insert_data_array, _insert_headers):
        # to-do: validation & Logging

        frame = """
        INSERT INTO {_table_name} ({_insert_cols}) VALUES ({_insert_items});
        """

        insert_items = ",".join(['%s' % e for e in _insert_data_array])
        insert_headers = ",".join(_insert_headers)

        query = frame.format(
            _table_name=self.SCHEMA.get("name"),
            _insert_cols=insert_headers,
            _insert_items=insert_items
        )

        #print("INSERTING: %s with %s" % (insert_items, query))
        stat = self.connector.query(query)
        self.connector.commit()

        return stat


    @abstractmethod
    def modifyOne(self, _table, _search_key, _search_value, _change_term, _change_value, _append_val=""):
        # to-do: validation & Logging
        frame = """
          UPDATE {table} SET {change_term} = '{change_value}' WHERE {search_key} = '{search_value} {append_val}';
        """

        query = frame.format(
            table = _table,
            change_term = _change_term,
            change_value = _change_value,
            search_key = _search_key,
            search_value=_search_value,
            append_val = _append_val
        )

        print("MODIFYING WITH %s" % query)

        stat = self.connector.query(query)
        self.connector.commit()

        return stat

    @abstractmethod
    def getSchema(self):
        # to-do: validation & Logging
        pass

    @abstractmethod
    def sanitizeInsert(self, _insert_dict):
        stypes = {
          "int": "{_mem}",
          "str": "'{_mem}'",
          "timestamp": "'{_mem}'"
        }

        sheads = self.SCHEMA.get("insert_headers")

        insert_array = list()
        for k in sheads:

            if k[1] == "timestamp":
                rev_insert = datetime.fromtimestamp(_insert_dict[k[0]]).strftime('%Y-%m-%d %H:%M:%S')
            else:
                rev_insert = _insert_dict[k[0]]

            insert_array.append(stypes[k[1]].format(_mem=rev_insert))

        return insert_array

    @abstractmethod
    def selectRows(self, _search_key, _search_value, _search_cols = "*", _append_val=""):
        frame = """
           SELECT {search_cols} FROM {table_name} WHERE {search_key} = '{search_value}' {append_val};
        """

        query = frame.format(search_cols= _search_cols, table_name = self.SCHEMA.get("name"), search_key = _search_key, search_value = _search_value, append_val = _append_val)

        stat = self.connector.query(query)
        return stat
