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
        ("user_num", "INT", "AUTO_INCREMENT", "PRIMARY KEY"),
        ("user_id", "varchar(100)", "NOT NULL"),
        ("email", "TEXT", "NOT NULL"),
        ("password", "TEXT", "NOT NULL"),
        ("token", "VARCHAR(100)", "NOT NULL"),
        ("token_expiry", "TIMESTAMP"),
        ("created", "TIMESTAMP", "DEFAULT", "CURRENT_TIMESTAMP"),
        ("modified", "TIMESTAMP", "DEFAULT", "CURRENT_TIMESTAMP")
      )
    }
