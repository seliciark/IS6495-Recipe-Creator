import db_base as db
import sqlite3
import csv
from datetime import datetime

class Recipes(db.DBbase):
    def __init__(self, row):
        super(Recipes, self).__init__("RecipeCreator.db")
        self.recipeID = None
        self.recipeName = row[0]
        self.category = row[1]
        self.description = row[2]
        self.preparationTime = row[3]
        self.cookingTime = row[4]
        self.servings = row[5]

    def update_recipe(self, recipeID, recipeName, category, description, preparationTime, cookingTime, servings):
        try:
            super().get_cursor.execute("""
                UPDATE Recipes 
                SET recipeName = ?, category = ?, description = ?, preparationTime = ?, cookingTime = ?, servings = ?
                WHERE recipeID = ?;
            """, (recipeName, category, description, preparationTime, cookingTime, servings, recipeID))
            super().get_connection.commit()
            print(f"Updated {recipeName} successfully")
        except Exception as e:
            print("An error occurred.", e)

    def add_recipe(self, recipeName, category, description, preparationTime, cookingTime, servings):
        try:
            super().get_cursor.execute("""
                INSERT OR IGNORE INTO Recipes (recipeName, category, description, preparationTime, cookingTime, servings) 
                VALUES (?, ?, ?, ?, ?, ?);
            """, (recipeName, category, description, preparationTime, cookingTime, servings))
            super().get_connection.commit()
            print(f"Added {recipeName} successfully")
        except Exception as e:
            print("An error occurred.", e)

    def delete_recipe(self, recipeID):
        try:
            super().get_cursor.execute("DELETE FROM Recipes WHERE recipeID = ?;", (recipeID,))
            super().get_connection.commit()
            print(f"Deleted recipe with ID {recipeID} successfully")
            return True
        except Exception as e:
            print("An error occurred.", e)

    def fetch_recipe(self, recipeID=None, recipeName=None):
        try:
            if recipeID is not None:
                return super().get_cursor.execute("SELECT * FROM Recipes WHERE recipeID = ?", (recipeID,)).fetchone()
            elif recipeName is not None:
                return super().get_cursor.execute("SELECT * FROM Recipes WHERE recipeName = ?", (recipeName,)).fetchone()
            else:
                return super().get_cursor.execute("SELECT * FROM Recipes").fetchall()
        except Exception as e:
            print("An error occurred finding Recipes.", e)





