# Recipe csv 

import db_base as db
import csv

class recipe:
    def __init__(self, row):
        """sets the columns for the "recipe" table"""
      self.recipeID = row[0]
      self.recipeName = row[1]
      self.description = row[2]
      self.preperationTime = row[3]
      self.cookingTime = row[4]
      self.servings = row[5]
      self.createdAt = row[6]
