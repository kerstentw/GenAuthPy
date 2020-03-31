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
