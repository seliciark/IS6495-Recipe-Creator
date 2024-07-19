# Indgredient csv 

import DBbase as db
import csv

class ingredients:
    def __init__(self, row):
        """sets the columns for the "ingredients" table"""
      self.IngredientsID = row[0]
      self.IngredientName = row[1]
      self.Quantity = row[2]
      self.Unit = row[3]
      self.RecipeID = row[4]
      
