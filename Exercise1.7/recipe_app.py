# -*- coding: utf-8 -*-
# Import packages and methods necessary
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

# Use the credentials and details to create an engine object called engine
engine = create_engine(
    "mysql://cf-python:password@localhost/my_database")

# Make the session object that I’ll use to make changes to my database.
Session = sessionmaker(bind=engine)
session = Session()

# The Recipe class should inherit the Base class that I created earlier
Base = declarative_base()


class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Define a __repr__ method that shows a quick representation of the recipe.
    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + " Level: " + difficulty + ">"

    # Define a __str__ method that prints a well-formatted version of the recipe.
    def __str__(self):
        output = "\nName: " + str(self.name) + \
            "\nCooking time (in minutes): " + str(self.cooking_time) + \
            "\nDifficulty: " + str(self.difficulty) + \
            "\nIngredients: " + str(self.ingredients)
        return output


# Define a method called calculate_difficulty() to calculate the difficulty of a recipe

    def calc_difficulty(self, cooking_time, ingredients):
        difficulty = "Unknown"
        ingredients = self.ingredients.split(',')
        if self.cooking_time < 10 and len(ingredients) < 4:
            difficulty = "Easy"
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            difficulty = "Medium"
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            difficulty = "Hard"
        self.difficulty = difficulty

    def return_ingredients_as_list(self):
        if len(self.ingredients) == 0:
            return []

        return [i.strip() for i in self.ingredients.split(',')]


# Create the corresponding table on the database using the create_all() method
Base.metadata.create_all(engine)

# Function 1: Collect the details of the recipe (name, ingredients, cooking_time) from the user


def create_recipe():
    recipe_ingredients = []

    correct_input_name = False
    while correct_input_name == False:

        name = input("\nEnter the name of the recipe: ")
        if len(name) < 50:

            correct_input_name = True

            correct_input_cooking_time = False
            while correct_input_cooking_time == False:
                cooking_time = input(
                    "\nEnter the cooking time of the recipe (minutes): ")
                if cooking_time.isnumeric() == True:
                    correct_input_cooking_time = True

                else:
                    print("Please enter a number.")
        else:
            print("Please enter a name that contains less than 50 characters.")
        correct_input_number = False
        while correct_input_number == False:
            ing_nber = input("How many ingredients do you want to enter?: ")
            if ing_nber.isnumeric() == True:
                correct_input_number = True

                for _ in range(int(ing_nber)):
                    ingredient = input("Enter an ingredient: ")
                    recipe_ingredients.append(ingredient)

            else:
                correct_input_number = False
                print("Please enter a positive number.")

    recipe_ingredients_str = ", ".join(recipe_ingredients)
    print(recipe_ingredients_str)

    # Create a new object from the Recipe model called recipe_entry using the details above.
    recipe_entry = Recipe(
        name=name,
        cooking_time=int(cooking_time),
        ingredients=recipe_ingredients_str
    )

    print(recipe_entry)

    session.add(recipe_entry)
    session.commit()

    print("Recipe saved into the database.")

# Function 2: Retrieve all recipes from the database as a list.


def view_all_recipes():
    all_recipes = []
    all_recipes = session.query(Recipe).all()

    # If there aren’t any entries, inform the user that there aren’t any entries in your database
    if len(all_recipes) == 0:
        print("There is no recipe in the database")
        return None

    else:
        print("\nAll recipes can be found below: ")
        print("-"*40)

        # Loop through this list of recipes
        for recipe in all_recipes:
            print(recipe)

# Function 3: Check if your table has any entries.


def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("There is no recipe in the database")
        return None

    # Retrieve only the values from the ingredients column of your table, and store this into a variable called results.
    else:
        results = session.query(Recipe.ingredients).all()
        print("results: ", results)

        # Initialize an empty list called all_ingredients.
        all_ingredients = []

        # Go through each entry in results, split up the ingredients into a temporary list
        for recipe_ingredients_list in results:
            for recipe_ingredients in recipe_ingredients_list:
                recipe_ingredient_split = recipe_ingredients.split(", ")
                all_ingredients.extend(recipe_ingredient_split)

        # Display these ingredients to the user, where each ingredient has a number displayed next to it.
        print("all_ingredients after the loop: ", all_ingredients)

        all_ingredients = list(dict.fromkeys(all_ingredients))

        all_ingredients_list = list(enumerate(all_ingredients))

        print("\nAll ingredients list:")
        print("-"*40)

        for index, ingredient in all_ingredients_list:
            print(str(index+1) + ". " + ingredient)

        # The user is allowed to pick these ingredients by typing the numbers corresponding to the ingredients, separated by spaces.
        try:
            ingredient_searched_nber = input(
                "\nEnter the number corresponding to the ingredient you want to select from the above list. You can enter several numbers. In this case, numbers shall be separated by a space: ")

            ingredients_nber_list_searched = ingredient_searched_nber.split(
                " ")

            ingredient_searched_list = []

            # Check that the user’s inputs match the options available. Otherwise, inform the user and exit the function.
            for ingredient_searched_nber in ingredients_nber_list_searched:
                ingredient_searched_index = int(ingredient_searched_nber) - 1

                # make a list of ingredients to be searched for, called search_ingredients, which contains these ingredients as strings.
                ingredient_searched = all_ingredients_list[ingredient_searched_index][1]
                ingredient_searched_list.append(ingredient_searched)

            print("\nYou selected the ingredient(s): ", ingredient_searched_list)

            # Initialize an empty list called conditions. This list will contain like() conditions for every ingredient to be searched for.
            conditions = []
            for ingredient in ingredient_searched_list:
                like_term = "%"+ingredient+"%"
                condition = Recipe.ingredients.like(like_term)
                conditions.append(condition)
            print("conditions: ", conditions)
            searched_recipes = session.query(Recipe).filter(*conditions).all()

            print(searched_recipes)
        except IndexError:
            print("Sorry, the number is not in the range")

        except:
            print(
                "An unexpected error occurred. Make sure to select a number from the list.")

        else:
            print("searched_recipes: ")
            for recipe in searched_recipes:
                print(recipe)

# Function 4: Check if any recipes exist on your database, and continue only if there are any. Otherwise, exit this function.


def edit_recipe():
    if not session.query(Recipe).count():
        print("No recipe entries")
        return None

    # Retrieve the id and name for each recipe from the database, and store them into results.
    results = session.query(Recipe.id, Recipe.name).all()

    # From each item in results, display the recipes available to the user.
    print("Recipes:")
    for result in results:
        print(f"{result[0]}: {result[1]}")

    # The user gets to pick a recipe by its id. If the chosen id doesn’t exist, exit the function
    num = input("Enter number corresponding to the recipe to update: ")

    # Retrieve the entire recipe that corresponds to this id from the database into a variable called recipe_to_edit.
    try:
        num = int(num)
        recipe_to_edit = session.get(Recipe, num)
        if not recipe_to_edit:
            raise
    except:
        print('Invalid entry. Exiting...')
        return None

    # Display the recipe, including only name, ingredients and cooking_time. difficulty isn’t editable since it is a calculated value.
    # Display a number next to each attribute so that the user gets to pick one.
    print("Item to edit")
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Cooking Time: {recipe_to_edit.cooking_time}")
    print(f"3. Ingredients: {recipe_to_edit.ingredients}")

    # Ask the user which attribute they’d like to edit by entering the corresponding number.
    num = input("Enter number corresponding to the attribute you want to edit: ")
    if num not in ['1', '2', '3']:
        print('Invalid entry. Exiting...')
        return None

    # Based on the input, use if-else statements to edit the respective attribute inside the recipe_to_edit object.
    if num == '1':
        name = input("Enter updated name: ")
        recipe_to_edit.name = name
    elif num == '2':
        cooking_time = input("Enter updated cooking time: ")
        if not cooking_time.isnumeric():
            print('Invalid entry. Exiting...')
            return None
        recipe_to_edit.cooking_time = int(cooking_time)
    elif num == '3':
        ingredients = input(
            "Enter updated list of comma separated ingredients: ")
        if not ingredients:
            print('Invalid entry. Exiting...')
            return None
        recipe_to_edit.ingredients = ingredients

    # Recalculate the difficulty using the object’s calculate_difficulty() method.
    recipe_to_edit.calc_difficulty(
        recipe_to_edit.cooking_time, recipe_to_edit.ingredients)

    # Commit these changes to the database.
    session.commit()
    print("Modification done.")

# Function 5:


def delete_recipe():
    # Check if any recipes exist on our database, and continue only if there are any. Otherwise, exit this function.
    if session.query(Recipe).count() == 0:
        print("There is no recipe in the database")
        return None
    # Retrieve the id and name of every recipe in the database. List these out to the user to choose from.
    else:
        results = session.query(Recipe).with_entities(
            Recipe.id, Recipe.name).all()
        print("results: ", results)
        print("Lits of available recipes: ")
        for recipe in results:
            print("\nId: ", recipe[0])
            print("Name: ", recipe[1])

        # Ask the user which recipe they’d like to delete by entering the corresponding id. Verify inputs here.
        recipe_id_for_deletion = (
            input("\nEnter the ID of the recipe you want to delete: "))

        # Based on the selected id, retrieve the corresponding object that exists on the database.
        recipe_to_be_deleted = session.query(Recipe).filter(
            Recipe.id == recipe_id_for_deletion).one()

        # Ask the user if they’re sure that they’d like to delete this entry.
        # If it’s a ‘yes’, perform the delete operation and commit this change. Otherwise, exit the function.
        print("\nWARNING: You are about to delete the following recipe: ")
        print(recipe_to_be_deleted)
        deletion_confirmed = input(
            "\nPlease confirm you want to delete the entry above (y/n): ")
        if deletion_confirmed == "y":
            session.delete(recipe_to_be_deleted)
            session.commit()
            print("\nRecipe successfully deleted from the database.")
        else:
            return None

# Inside this loop, lay out print statements that display six options


def main_menu():
    choice = ""
    while (choice != "quit"):
        print("\n" + "="*50)
        print("\nMain Menu:")
        print("-"*30)
        print("Pick a choice:")
        print("   1. Create a new recipe")
        print("   2. Search for a recipe by ingredient")
        print("   3. Edit an existing recipe")
        print("   4. Delete a recipe")
        print("   5. View all recipes")
        print("\n   Type 'quit' to exit the program.")
        choice = input("\nYour choice: ")
        print("\n" + "="*50)

        # Using if-elif statements, launch the corresponding function based on the user’s input.
        if choice == "1":
            create_recipe()
        elif choice == "2":
            search_by_ingredients()
        elif choice == "3":
            edit_recipe()
        elif choice == "4":
            delete_recipe()
        elif choice == "5":
            view_all_recipes()
        else:
            if choice == "quit":
                session.close()
                print("Bye~ Have a good day.\n")
            else:
                print("WARNING... Wrong entry, please try again.")


# close session and engine with their respective close() methods
main_menu()
