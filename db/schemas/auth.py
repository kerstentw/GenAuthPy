try:
    from .DBSchema import DBSchema
except:
    from DBSchema import DBSchema


# Handles Type checking, sanitation, and data availability of queries.

class AuthSchema(DBSchema):

    SCHEMA = {
      "name": "auth",
      "insert_headers": [ # NOTE: Order matters
          ("user_id", "str"),
          ("email", "str"),
          ("password", "str"),
          ("token", "str"),
          ("token_expiry", "timestamp")
      ],
      "columns" : (
        ("idx", "INT", "AUTO_INCREMENT", "PRIMARY KEY"),
        ("user_id", "varchar(100)", "NOT NULL"),
        ("email", "varchar(255)", "UNIQUE NOT NULL"),
        ("password", "TEXT", "NOT NULL"),
        ("token", "VARCHAR(255)", "NOT NULL"),
        ("token_expiry", "TIMESTAMP"),
        ("created", "TIMESTAMP", "DEFAULT","now()"),
        ("modified", "TIMESTAMP", "DEFAULT", "now() ON UPDATE now()"),
        ("KEY", "user_id (user_id)")
      )
    }

    def __init__(self, _db_info):
        super().__init__(_db_info)


    def createTable(self):
        stat = super().createTable()
        return stat


    def insertOne(self, _insert_data_array, _insert_headers):
        try:
            # to-do: Data Validation
            stat = super().insertOne(_insert_data_array, _insert_headers)
            return stat

        except:
            from traceback import print_exc
            print_exc()

    def modifyOne(self, _search_key, _search_value, _change_term, _change_value):
        #(user_id
        return super().modifyOne(self.SCHEMA.get("name"), _search_key, _search_value, _change_term, _change_value)

    def getSchema(self):
        return self.SCHEMA

    def sanitizeInsert(self, _insert_dict):
        # to-do: input validation
        stat = super().sanitizeInsert(_insert_dict)
        return stat

    def selectRows(self, _search_key, _search_value, _search_cols="*", _append_vals=""):
        """

        """
        stat = super().selectRows(_search_key, _search_value, _search_cols, _append_vals)
        return stat

    ###  Implementations ###

    def insertManyUsers(self, _insert_list):
        for entry in  _insert_list:
            self.insertOne(entry)

    # to-do: Spin out into action/service modules...
    def insertNewUser(self, _user_obj):
        insert_array = list()

        keys = [k[0] for k in self.SCHEMA.get("insert_headers")]
        insert_items = self.sanitizeInsert(_user_obj)

        for itm in insert_items:

            insert_array.append(itm) #Enforces adherence to keys

        stat = self.insertOne(insert_array, keys)

        return stat


# to-do: Move all test functions into nose-tests

def testCreate():
    TEST_CONFIG = {
      "host" : "128.199.252.53",
      "port" : "5121",
      "database": "tk_test",
      "user" : "TK",
      "password": "f543k5n34lk5Z"
    }

    auth_schema = AuthSchema(TEST_CONFIG)
    auth_schema.createTable()


def testCreateAndInsert():
    TEST_CONFIG = {
      "host" : "128.199.252.53",
      "port" : "5121",
      "database": "tk_test",
      "user" : "TK",
      "password": "f543k5n34lk5Z"
    }

    TEST_USER = {
        "user_id": "abcdefg",
        "email": "foobar@test.com",
        "password": "password_hash",
        "token": "fake.token.is",
        "token_expiry": 12345678 # Must be iso 8601
    }

    auth_schema = AuthSchema(TEST_CONFIG)
    auth_schema.createTable()
    msg = auth_schema.insertNewUser(TEST_USER)



if __name__ == "__main__":
    #testCreate()
    testCreateAndInsert()
    #print("This module cannot be accessed from rel dir.")
