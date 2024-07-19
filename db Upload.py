import sqlite3
from datetime import datetime

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('RecipeCreator.db')
cursor = conn.cursor()

# Creating the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Creaing the recipe table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Recipes (
    RecipeID INTEGER PRIMARY KEY AUTOINCREMENT,
    RecipeName TEXT NOT NULL,
    Description TEXT,
    PreparationTime INTEGER,  -- in minutes
    CookingTime INTEGER,  -- in minutes
    Servings INTEGER,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Creating the ingredients table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Ingredients (
    IngredientID INTEGER PRIMARY KEY AUTOINCREMENT,
    IngredientName TEXT NOT NULL,
    Quantity TEXT,
    Unit TEXT,
    RecipeID INTEGER,
    FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID)
)
''')

conn.commit()


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


# Populate the database with psuedodata
def populate_initial_data():
    users = [
        ('john_doe', 'password123', 'john.doe@example.com'),
        ('jane_smith', 'mypassword', 'jane.smith@example.com'),
        ('alex_jones', 'securepass', 'alex.jones@example.com'),
        ('emily_davis', 'emilypass', 'emily.davis@example.com'),
        ('michael_brown', 'brownie123', 'michael.brown@example.com'),
        ('sarah_lee', 'sarahpassword', 'sarah.lee@example.com'),
        ('david_clark', 'davidpass', 'david.clark@example.com'),
        ('linda_martin', 'lindapass', 'linda.martin@example.com'),
        ('robert_white', 'robertpassword', 'robert.white@example.com'),
        ('lisa_harris', 'lisapass', 'lisa.harris@example.com')
    ]

    recipes = [
        ('Spaghetti Bolognese', 'A classic Italian pasta dish.', 15, 60, 4),
        ('Chicken Curry', 'A spicy and flavorful curry.', 20, 40, 4),
        ('Vegetable Stir Fry', 'A quick and healthy stir fry.', 10, 15, 2),
        ('Beef Tacos', 'Delicious beef tacos with fresh toppings.', 20, 10, 4),
        ('Pancakes', 'Fluffy pancakes perfect for breakfast.', 10, 20, 4),
        ('Grilled Cheese Sandwich', 'A classic grilled cheese sandwich.', 5, 10, 1),
        ('Caesar Salad', 'A fresh and crispy Caesar salad.', 15, 0, 2),
        ('Tomato Soup', 'A warm and comforting tomato soup.', 10, 30, 4),
        ('Lasagna', 'A rich and hearty lasagna.', 30, 90, 6),
        ('Chocolate Cake', 'A decadent chocolate cake.', 20, 45, 8)
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

    cursor.executemany('''
    INSERT INTO Users (Username, Password, Email) VALUES (?, ?, ?)
    ''', users)

    cursor.executemany('''
    INSERT INTO Recipes (RecipeName, Description, PreparationTime, CookingTime, Servings) VALUES (?, ?, ?, ?, ?)
    ''', recipes)

    cursor.executemany('''
    INSERT INTO Ingredients (IngredientName, Quantity, Unit, RecipeID) VALUES (?, ?, ?, ?)
    ''', ingredients)

    conn.commit()



print("The database has been setup and CRUD functions are ready to go.")
