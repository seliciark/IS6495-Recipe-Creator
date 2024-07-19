# user csv

import db_base as db
import csv

class user:
    def __init__(self, row):
        """sets the columns for the "user" table"""
      self.UserID = row[0]
      self.Username = row[1]
      self.Password = row[2]
      self.Email = row[3]
      self.CreatedAt = row[4]
