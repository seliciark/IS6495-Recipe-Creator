# Indgredient csv 

import db_base as db
import csv

class ingredients:
    def __init__(self, row):
        """sets the columns for the "ingredients" table"""
      self.ingredientsID = row[0]
      self.ingredientName = row[1]
      self.quantity = row[2]
      self.unit = row[3]
      self.recipeID = row[4]
      
