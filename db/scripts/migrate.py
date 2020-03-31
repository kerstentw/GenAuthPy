"""
This module creates Database and tables necessary for running the application.
"""

import sys

sys.path.append("..")

import schemas

TEST_CONFIG = {
  "host" : "localhost",
  "port" : "5121",
  "database": "tk_test",
  "user" : "admin",
  "password": "change_me"
}

schema_handlers = [
  schemas.auth.AuthSchema,
]

for s in schema_handlers:
    tc = s(TEST_CONFIG)
    tc.createTable()

print("Finished Migration")
