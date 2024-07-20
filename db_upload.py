import db_base as db
import sqlite3
import csv
from datetime import datetime


class InitializeDB(db.DBbase):
    def createDBTables(self):

        # Create DB Tables ***-->>currently set to drop and reset database for Testing<<----g****
        try:
            sql = """

            CREATE TABLE IF NOT EXISTS Recipes (
                recipeID INTEGER PRIMARY KEY AUTOINCREMENT,
                recipeName TEXT NOT NULL,
                category TEXT,
                description TEXT,
                preparationTime INTEGER,  -- in minutes
                cookingTime INTEGER,  -- in minutes
                servings INTEGER,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            DROP TABLE IF EXISTS Users;
            
            CREATE TABLE IF NOT EXISTS Users (
                userID INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS Ingredients (
                ingredientID INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredientName TEXT NOT NULL,
                quantity TEXT,
                unit TEXT,
                recipeID INTEGER,
                FOREIGN KEY (recipeID) REFERENCES Recipes(recipeID)
            );
            """
            super().execute_script(sql)
            print("Default Database Created Successfully")

        except Exception as e:
            print("Error Creating DB Tables", e)

    def populateDB(self):
        # populates default data to database
        try:

            recipes = [
                ('Spaghetti Bolognese', 'Dinner', 'A classic Italian pasta dish.', 15, 60, 4),
                ('Chicken Curry', 'Dinner', 'A spicy and flavorful curry.', 20, 40, 4),
                ('Vegetable Stir Fry', 'Dinner', 'A quick and healthy stir fry.', 10, 15, 2),
                ('Beef Tacos', 'Lunch', 'Delicious beef tacos with fresh toppings.', 20, 10, 4),
            ]

            ingredients = [
                ('Spaghetti', '200', 'g', 1),
                ('Ground Beef', '500', 'g', 1),
                ('Tomato Sauce', '400', 'ml', 1),
                ('Onion', '1', 'pcs', 1),
                ('Garlic', '2', 'cloves', 1),
                ('Chicken Breast', '400', 'g', 2),
                ('Curry Powder', '2', 'tbsp', 2),
                ('Coconut Milk', '400', 'ml', 2),
                ('Carrot', '1', 'pcs', 2),
                ('Bell Pepper', '1', 'pcs', 2),
                ('Broccoli', '200', 'g', 3),
                ('Soy Sauce', '2', 'tbsp', 3),
                ('Olive Oil', '2', 'tbsp', 3),
                ('Beef', '500', 'g', 4),
                ('Taco Shells', '8', 'pcs', 4),
                ('Lettuce', '100', 'g', 4),
                ('Cheddar Cheese', '100', 'g', 4),
                ('Flour', '200', 'g', 5),
                ('Milk', '300', 'ml', 5),
                ('Eggs', '2', 'pcs', 5),
                ('Bread', '2', 'slices', 6),
                ('Butter', '1', 'tbsp', 6),
                ('Romaine Lettuce', '1', 'head', 7),
                ('Caesar Dressing', '100', 'ml', 7)
            ]


            super().get_cursor.executemany('''
                INSERT INTO Recipes (recipeName, category, description, preparationTime, cookingTime, servings) 
                VALUES (?, ?, ?, ?, ?, ?)
                ''', recipes)

            super().get_cursor.executemany('''
                INSERT INTO Ingredients (ingredientName, quantity, unit, recipeID) 
                VALUES (?, ?, ?, ?)
                ''', ingredients)

            super().get_connection.commit()

            print("Default Data Population Successful")

        except Exception as e:
            print("error populating default database: ", e)


#CRUD operations on User:
class Users(db.DBbase):
    def __init__(self):
        super(Users, self).__init__("RecipeCreator.db")

    def update_user(self, username, userID):
        try:
            super().get_cursor.execute("UPDATE Users set username = ? where userID = ?;", (username, userID))
            super().get_connection.commit()
            print(f"Updated User: {username}, {userID} successfully")
        except Exception as e:
            print("An error occurred updating user: ", e)

    def add_user(self, username, email):
        try:
            super().get_cursor.execute("INSERT OR IGNORE INTO Users (username, email) values(?,?);", (username, email))
            super().get_connection.commit()
            print(f"New user added successfully: {username}, {email}")
        except Exception as e:
            print("An error occurred adding user: ", e)

    def delete_user(self, userID):
        try:
            super().get_cursor.execute("DELETE FROM Users where userID = ?;", (userID,))
            super().get_connection.commit()
            print(f"deleted {userID} successfully")
            return True
        except Exception as e:
            print("An error occurred deleting User.", e)

    # I think we can use this function to determine if a user exists or not
    def fetch_user(self, userID=None, username=None):
        # if Id is null (or None), then get everything, else get by id
        try:
            if userID is not None:
                return super().get_cursor.execute("SELECT * FROM Users WHERE userID = ?",(userID,)).fetchone()
            elif username is not None:
                return super().get_cursor.execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchone()
            else:
                return super().get_cursor.execute("SELECT * FROM Users").fetchall()

        except Exception as e:
            print("An error occurred finding Users.", e)



class Ingredients(db.DBbase):
    def __init__(self):
        super(Ingredients, self).__init__("RecipeCreator.db")

    def update_ingrd(self, ingredientID, ingredientName):
        try:
            super().get_cursor.execute("UPDATE Ingredients set name = ? where id = ?;", (ingredientName, ingredientID))
            super().get_connection.commit()
            print(f"Updated {ingredientName} successfully")
        except Exception as e:
            print("An error occurred.", e)

    def add_ingrd(self, ingredientName):
        try:
            super().get_cursor.execute("INSERT OR IGNORE INTO Ingredients  (ingredientName) values(?);", (ingredientName,))
            super().get_connection.commit()
            print(f"Add {ingredientName} successfully")
        except Exception as e:
            print("An error occurred.", e)

    def delete_ingrd(self, ingredientID):
        try:
            super().get_cursor.execute("DELETE FROM Ingredients where ingredientID = ?;", (ingredientID,))
            super().get_connection.commit()
            print(f"deleted {ingredientID} successfully")
            return True
        except Exception as e:
            print("An error occurred.", e)

    def fetch_ingrd(self, ingredientId=None, ingredientName=None):
        # if Id is null (or None), then get everything, else get by id
        try:
            if ingredientId is not None:
                return super().get_cursor.execute("SELECT * FROM Ingredients WHERE ingredientId = ?",(ingredientId,)).fetchone()
            elif ingredientName is not None:
                return super().get_cursor.execute("SELECT * FROM Ingredients WHERE ingredientName = ?", (ingredientName,)).fetchone()
            else:
                return super().get_cursor.execute("SELECT * FROM Ingredients").fetchall()

        except Exception as e:
            print("An error occurred finding Ingredients.", e)

class RecipeRows:
    def __init__(self, row):
        self.recipeID = None
        self.recipeName = row[0]
        self.category = row[1]
        self.description = row[2]
        self.preparationTime = row[3]
        self.cookingTime = row[4]
        self.servings = row[5]

class RecipeImport(db.DBbase):

    #Recipes will be the CSV file import we use in the demo "Would you like to import additional recipes?"

    def read_recipes(self, file_name):
        self.recipe_list = []

        try:
            with open(file_name, 'r') as record:
                csv_contents = csv.reader(record)
                next(csv_contents)
                for row in csv_contents:
                    # print(row)
                    recipe = RecipeRows(row)
                    self.recipe_list.append(recipe)

        except Exception as e:
            print(e)

    def save_to_database(self):
        print("Number of records to save: ", len(self.recipe_list))
        save = input("Continue? ").lower()

        if save == "y":
            for item in self.recipe_list:
                item.recipeName = item.recipeName.replace("NaN", "No Name Supplied")

                # recipeName, category, description, preparationTime, cookingTime, servings
                """
                Recipes (
                    recipeID INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipeName TEXT NOT NULL,
                    category TEXT,
                    description TEXT,
                    preparationTime INTEGER,  -- in minutes
                    cookingTime INTEGER,  -- in minutes
                    servings INTEGER,
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                try:
                    super().get_cursor.execute(""" 
                    INSERT INTO Recipes
                    (recipeName, category, description, preparationTime, cookingTime, servings)
                        VALUES(?,?,?,?,?,?)""",
                            (item.recipeName, item.category, item.description, item.preparationTime, item.cookingTime, item.servings))
                    super().get_connection.commit()

                    print(f"Recipe Saved:{item.recipeName}")

                except Exception as e:
                    print(e)
        else:
            print("save to DB aborted")







#create database and populate default data:

# createDB = InitializeDB("RecipeCreator.db")
# createDB.createDBTables()
# createDB.populateDB()


#import recipes .csv

# recipe_manager = RecipeImport("RecipeCreator.db")
# recipe_manager.read_recipes("recipes_csv.csv")
# recipe_manager.save_to_database()


#to use in interactive menu for user:
class App:
    def run(self):
        user1 = Users()
        results = user1.fetch_user()
        if len(results) > 0:
            for item in results:
                print(item)
        elif len(results) == 0:
            print("Please create a new user to get started: ")
            username = input("Enter a username: ")
            email = input("Enter an email: ")
            user1.add_user(username, email)
            print("Done\n")
            input("Press return to continue")

apptest = App()
apptest.run()










#Below are previous version CRUD. preserved for reference, update variables to the current names if using (see InitializeDB class):

"""
# CRUD Functions for the users table
def create_user(username, password, email):
    cursor.execute('''
    INSERT INTO Users (Username, Password, Email) VALUES (?, ?, ?)
    ''', (username, password, email))
    conn.commit()


def retrieve_user(user_id):
    cursor.execute('''
    SELECT * FROM Users WHERE UserID = ?
    ''', (user_id,))
    return cursor.fetchone()


def update_user(user_id, username, password, email):
    cursor.execute('''
    UPDATE Users SET Username = ?, Password = ?, Email = ? WHERE UserID = ?
    ''', (username, password, email, user_id))
    conn.commit()


def delete_user(user_id):
    cursor.execute('''
    DELETE FROM Users WHERE UserID = ?
    ''', (user_id,))
    conn.commit()


# CRUD Functions for the recipes table
def create_recipe(recipe_name, description, prep_time, cook_time, servings):
    cursor.execute('''
    INSERT INTO Recipes (RecipeName, Description, PreparationTime, CookingTime, Servings) VALUES (?, ?, ?, ?, ?)
    ''', (recipe_name, description, prep_time, cook_time, servings))
    conn.commit()


def retrieve_recipe(recipe_id):
    cursor.execute('''
    SELECT * FROM Recipes WHERE RecipeID = ?
    ''', (recipe_id,))
    return cursor.fetchone()


def update_recipe(recipe_id, recipe_name, description, prep_time, cook_time, servings):
    cursor.execute('''
    UPDATE Recipes SET RecipeName = ?, Description = ?, PreparationTime = ?, CookingTime = ?, Servings = ? WHERE RecipeID = ?
    ''', (recipe_name, description, prep_time, cook_time, servings, recipe_id))
    conn.commit()


def delete_recipe(recipe_id):
    cursor.execute('''
    DELETE FROM Recipes WHERE RecipeID = ?
    ''', (recipe_id,))
    conn.commit()


# CRUD Functions for the Ingredients table
def create_ingredient(ingredient_name, quantity, unit, recipe_id):
    cursor.execute('''
    INSERT INTO Ingredients (IngredientName, Quantity, Unit, RecipeID) VALUES (?, ?, ?, ?)
    ''', (ingredient_name, quantity, unit, recipe_id))
    conn.commit()


def retrieve_ingredient(ingredient_id):
    cursor.execute('''
    SELECT * FROM Ingredients WHERE IngredientID = ?
    ''', (ingredient_id,))
    return cursor.fetchone()


def update_ingredient(ingredient_id, ingredient_name, quantity, unit, recipe_id):
    cursor.execute('''
    UPDATE Ingredients SET IngredientName = ?, Quantity = ?, Unit = ?, RecipeID = ? WHERE IngredientID = ?
    ''', (ingredient_name, quantity, unit, recipe_id, ingredient_id))
    conn.commit()


def delete_ingredient(ingredient_id):
    cursor.execute('''
    DELETE FROM Ingredients WHERE IngredientID = ?
    ''', (ingredient_id,))
    conn.commit()
"""
