# Recipe csv 

import DBbase as db
import csv

class recipe:
    def __init__(self, row):
        """sets the columns for the "recipe" table"""
      self.RecipeID = row[0]
      self.RecipeName = row[1]
      self.Description = row[2]
      self.PreperationTime = row[3]
      self.CookingTime = row[4]
      self.Servings = row[5]
      self.CreatedAt = row[6]
