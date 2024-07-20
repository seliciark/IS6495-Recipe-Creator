# Recipe csv

import db_base as db
import csv

class Recipe:

    def __init__(self, row):
        self.recipeID = row[0]
        self.recipeName = row[1]
        self.category = row[2]
        self.description = row[3]
        self.preparationTime = row[4]
        self.cookingTime = row[5]
        self.servings = row[6]
        self.createdAt = row[7]

class CsvLab(db.DBbase):
    def reset_database(self):
        try:
            sql = """
            DROP TABLE IF EXISTS Recipe;
            CREATE TABLE Recipe (
                recipeID INTEGER PRIMARY KEY,
                recipeName TEXT NOT NULL UNIQUE,
                category TEXT,
                description TEXT,
                preparationTime INTEGER,
                cookingTime INTEGER,
                servings INTEGER,
                createdAt TIMESTAMP
            );
            """
            super().execute_script(sql)
        except Exception as e:
            print(e)

    def import_csv_file(self, file_name):

        self._recipe_list = []

        try:
            with open(file_name, "r") as record:
                csv_reader = csv.reader(record)
                next(record)
                for row in csv_reader:
                    veggie = Recipe(row)
                    self._recipe_list.append(recipe)

        except Exception as e:
            print(e)

    def save_to_database(self):

        print("Number of records to save: ", len(self._recipe_list))
        save = input("Continue? ").lower()

        if save == "y":
            for item in self._recipe_list:
                try:
                    super().get_cursor.execute("""INSERT INTO Recipe 
                        (name, common_color, peal, type)
                        VALUES(?,?,?,?,?,?,?)""",
                                               (item.recipeName, item.category, item.description, item.preparationTime, item.cookingTime, item.servings, item.createdAt)
                                               )
                    super().get_connection.commit()
                    print("Saved item", item.recipeName, item.category, item.description, item.preparationTime, item.cookingTime, item.servings, item.createdAt)
                except Exception as e:
                    print(e)


recipe_db = CsvLab("recipe.sqlite")
recipe_db.reset_database()
recipe_db.import_csv_file("recipe.csv")
recipe_db.save_to_database()
