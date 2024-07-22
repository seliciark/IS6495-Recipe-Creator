import db_base as db
import sqlite3
import csv


class InitializeDB(db.DBbase):

    def createDBTables(self):

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
            #print("Default Database Created Successfully")

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
                ('Omelette', 'Breakfast', 'A hearty start to the day', 10, 3, 1),
                ('Greek Salad','Lunch','A refreshing Greek salad with feta cheese.',10,0,2),
                ('Chocolate Cake','Dessert','A decadent chocolate cake.',20,45,8)
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
                INSERT OR IGNORE INTO Recipes (recipeName, category, description, preparationTime, cookingTime, servings) 
                VALUES (?, ?, ?, ?, ?, ?)
                ''', recipes)

            super().get_cursor.executemany('''
                INSERT OR IGNORE INTO Ingredients (ingredientName, quantity, unit, recipeID) 
                VALUES (?, ?, ?, ?)
                ''', ingredients)

            super().get_connection.commit()

            #print("Default Data Population Successful")
        except Exception as e:
            print("error populating default database: ", e)


#CRUD operations on User:
class Users(db.DBbase):
    def __init__(self):
        super(Users, self).__init__("RecipeCreator.sqlite")

    def update_user(self, username, userID):
        try:
            super().get_cursor.execute("UPDATE Users set username = ? where userID = ?;", (username, userID))
            super().get_connection.commit()
            print(f"Updated User: {username}, {userID} successfully")
        except Exception as e:
            print("An error occurred updating user: ", e)

    def add_user(self, username, email):
        try:
            super().get_cursor.execute("INSERT INTO Users (username, email) values(?,?);", (username, email))
            super().get_connection.commit()
            print(f"New user added successfully: {username}, {email}")
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                print("This user already exists")
        except Exception as e:
            print("An error occurred adding user: ", e)


    def delete_user(self, userID):
        try:
            super().get_cursor.execute("DELETE FROM Users where userID = ?;", (userID,))
            super().get_connection.commit()
            print(f"Deleted User: {userID} successfully")
            return True
        except Exception as e:
            print("An error occurred deleting User.", e)

    def fetch_user(self, userID=None, username=None):
        # if Id is null (or None), then get everything, else get by id
        try:
            if userID is not None:
                return super().get_cursor.execute("SELECT * FROM Users WHERE userID = ?", (userID,)).fetchone()
            elif username is not None:
                return super().get_cursor.execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchone()
            else:
                return super().get_cursor.execute("SELECT * FROM Users").fetchall()

        except Exception as e:
            print("An error occurred finding Users.", e)


class Ingredients(db.DBbase):
    def __init__(self):
        super(Ingredients, self).__init__("RecipeCreator.sqlite")

    def update_ingrd(self, ingredientID, ingredientName):
        try:
            super().get_cursor.execute("UPDATE Ingredients set ingredientName = ? where ingredientID = ?;",
                                       (ingredientName, ingredientID))
            super().get_connection.commit()
            print(f"Updated {ingredientName} successfully")
        except Exception as e:
            print("An error occurred.", e)

    def add_ingrd(self, ingredientName, quantity, unit):  #recipeID is being ignored for now
        try:
            super().get_cursor.execute(
                "INSERT OR IGNORE INTO Ingredients  (ingredientName, quantity, unit) values(?, ?, ?);",
                (ingredientName, quantity, unit))
            super().get_connection.commit()
            print(f"Added {ingredientName} successfully")
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
                return super().get_cursor.execute("SELECT * FROM Ingredients WHERE ingredientId = ?",
                                                  (ingredientId,)).fetchone()
            elif ingredientName is not None:
                return super().get_cursor.execute("SELECT * FROM Ingredients WHERE ingredientName = ?",
                                                  (ingredientName,)).fetchone()
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
    def __init__(self, db_name):
        super().__init__(db_name)
        self.recipe_list = []

    def read_recipes(self, file_name):

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
        save = input("Continue? (y/n) ").lower()

        if save == "y":
            for item in self.recipe_list:
                item.recipeName = item.recipeName.replace("NaN", "No Name Supplied")

                try:
                    super().get_cursor.execute(""" 
                    INSERT INTO Recipes
                    (recipeName, category, description, preparationTime, cookingTime, servings)
                        VALUES(?,?,?,?,?,?)""",
                                               (item.recipeName, item.category, item.description, item.preparationTime,
                                                item.cookingTime, item.servings))
                    super().get_connection.commit()

                    print(f"Recipe Saved:{item.recipeName}")

                except Exception as e:
                    print(e)

        else:
            print("save to DB aborted")


class Recipes(db.DBbase):
    def __init__(self):
        super(Recipes, self).__init__("RecipeCreator.sqlite")

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


    def fetch_recipe_by_category(self, category):
        try:
            return super().get_cursor.execute("SELECT recipeName FROM Recipes WHERE category = ?", (category,)).fetchone()
        except Exception as e:
            print("An error occurred finding Recipes by category.", e)


    def fetch_recipes_by_ingredient(self, ingredientName):
        try:
            query = """
            SELECT Recipes.recipeName
            FROM Recipes
            JOIN Ingredients ON Recipes.recipeID = Ingredients.recipeID
            WHERE Ingredients.ingredientName = ?;
            """
            return super().get_cursor.execute(query, (ingredientName,)).fetchall()
        except Exception as e:
            print("An error occurred finding Recipes by ingredient.", e)



class InteractiveMenu:

    def user_display(self):

        user1 = Users()
        results = user1.fetch_user()
        if len(results) == 1:
            print(f"\nWelcome to the Recipe Manager!")
            self.display_menu()
        elif len(results) == 0:
            print(f"\nWelcome to the Recipe Manager!")
            print("Please create a user to get started: ")
            username = input("Enter a username: ")
            email = input("Enter an email: ")
            user1.add_user(username, email)
            self.display_menu()

    def display_menu(self):
        while True:
            print("\nMain Menu Options")
            print("1. Manage Users")
            print("2. Manage Recipes")
            print("3. Manage Ingredients")
            print("4. Exit")
            choice = input("Please choose an option: ")

            if choice == '1':
                self.user_options()
            elif choice == '2':
                self.recipe_options()
            elif choice == '3':
                self.ingredient_options()
            elif choice == '4':
                print("Goodbye!")
                break
            else:
                print("Invalid option, please try again.")

    def user_options(self):
        while True:
            print("\nUser Management")
            print("1. Add User")
            print("2. Update User")
            print("3. Delete User")
            print("4. List Users")
            print("5. Back to Main Menu")
            choice = input("Please choose an option: ")

            #creates instance of the class for user
            user = Users()

            if choice == '1':
                username = input("Enter username: ")
                email = input("Enter email: ")
                user.add_user(username, email)
            elif choice == '2':
                userID = int(input("Enter user ID: "))  # handle data type error int #TODO
                username = input("Enter new username: ")
                user.update_user(username, userID)
            elif choice == '3':
                userID = int(input("Enter user ID: "))
                user.delete_user(userID)
            elif choice == '4':
                users = user.fetch_user()
                for user in users:
                    print(user)
            elif choice == '5':
                break
            else:
                print("Invalid option, please try again.")

    def recipe_options(self):
        while True:
            print("\nRecipe Management")
            print("1. Add Recipe")
            print("2. Update Recipe")
            print("3. Delete Recipe")
            print("4. List Recipes")
            print("5. Find Recipes by Category")
            print("6. Find Recipes by Ingredient")
            print("7. Import Recipes")
            print("8. Back to Main Menu")
            choice = input("Please choose an option: ")

            # this creates an instance for recipe
            recipe = Recipes()

            if choice == '1':
                recipeName = input("Enter recipe name: ")
                category = input("Enter category: ")
                description = input("Enter description: ")
                preparationTime = int(input("Enter preparation time (in minutes): "))
                cookingTime = int(input("Enter cooking time (in minutes): "))
                servings = int(input("Enter number of servings: "))
                recipe.add_recipe(recipeName, category, description, preparationTime, cookingTime, servings)
            elif choice == '2':
                recipeID = int(input("Enter recipe ID: "))
                recipeName = input("Enter new recipe name: ")
                category = input("Enter new category: ")
                description = input("Enter new description: ")
                preparationTime = int(input("Enter new preparation time (in minutes): "))
                cookingTime = int(input("Enter new cooking time (in minutes): "))
                servings = int(input("Enter new number of servings: "))
                recipe.update_recipe(recipeID, recipeName, category, description, preparationTime, cookingTime,
                                     servings)
            elif choice == '3':
                recipeID = int(input("Enter recipe ID: "))
                recipe.delete_recipe(recipeID)
            elif choice == '4':
                recipes = recipe.fetch_recipe()
                for recipe in recipes:
                    print(recipe)

            elif choice == '5':
                categoryinput = input("Choose a category: ('Breakfast', 'Lunch', 'Dinner', or 'Dessert')").title()
                recipesbyCategory = recipe.fetch_recipe_by_category(categoryinput)
                for recipe in recipesbyCategory:
                    print(recipe)

            elif choice == '6':
                ingredient_name = input("Enter an Ingredient: ").title()
                recipes_with_ingredient = recipe.fetch_recipes_by_ingredient(ingredient_name)
                if recipes_with_ingredient:
                    print(f"Recipes containing {ingredient_name}:")
                    for recipe in recipes_with_ingredient:
                        print(recipe)
                else:
                    print(f"No recipes found with the ingredient {ingredient_name}.")

            elif choice == '7':
                importYN = input("Would you like to import more Recipes? (y/n): ").lower()

                if importYN == "y":
                    recipeImport = RecipeImport("RecipeCreator.sqlite")
                    recipeImport.read_recipes("recipes_csv.csv")
                    recipeImport.save_to_database()
                elif importYN == "n":
                    break
                else:
                    print("Please input `y` or `n`")

            elif choice == '8':
                break
            else:
                print("Invalid option, please try again.")

    def ingredient_options(self):
        while True:
            print("\nIngredient Management")
            print("1. Add Ingredient")
            print("2. Update Ingredient")
            print("3. Delete Ingredient")
            print("4. List Ingredients")
            print("5. Back to Main Menu")
            choice = input("Please choose an option: ")

            # this creates an instance for ingredients
            ingredient = Ingredients()

            if choice == '1':
                ingredientName = input("Enter ingredient name: ")
                quantity = input("Enter quantity: ")
                unit = input("Enter unit: ")
                # recipeID = int(input("Enter recipe ID: "))
                ingredient.add_ingrd(ingredientName, quantity, unit)  # deleted , recipeID
            elif choice == '2':
                ingredientID = int(input("Enter ingredient ID: "))
                ingredientName = input("Enter new ingredient name: ")
                ingredient.update_ingrd(ingredientID, ingredientName)
            elif choice == '3':
                ingredientID = int(input("Enter ingredient ID: "))
                ingredient.delete_ingrd(ingredientID)
            elif choice == '4':
                ingredients = ingredient.fetch_ingrd()
                for ingredient in ingredients:
                    print(ingredient)
            elif choice == '5':
                break
            else:
                print("Invalid option, please try again.")



#code below executes application

#create database and populate default data
# createDB = InitializeDB("RecipeCreator.sqlite")
# createDB.createDBTables()
# createDB.populateDB()

#call interactive menu
menu = InteractiveMenu()
menu.user_display()

