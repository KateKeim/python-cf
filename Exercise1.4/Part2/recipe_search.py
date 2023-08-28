# Import the pickle module.
import pickle

# Define a function to display a recipe called display_recipe(), 
# which takes in one recipe (of the dictionary type) as an argument 
# and prints all of its attributes including the recipe name, cooking time, ingredients, and difficulty.
def display_recipe(recipe):
    print('Name: ', recipe['Name'])
    print('Cooking time in minutes: ', recipe['Cooking_Time'])
    print('Ingredients: ', ', '.join(recipe['Ingredients']))
    print('Difficulty: ', recipe['Difficulty'])


# Define another function called search_ingredient() to search for an ingredient in the given data.
def search_ingredient(data):
    ingredients_list = data['all_ingredients']
    indexed_ingredients_list = list(enumerate(ingredients_list, 1))

    for ingredient in indexed_ingredients_list:
        print('No.', ingredient[0], ' - ', ingredient[1])

    try:
        chosen_num = int(
            input('Enter the corresponding number of chosen ingredient:   '))
        index = chosen_num - 1
        ingredient_searched = ingredients_list[index]
        ingredient_searched = ingredient_searched.lower()
    except IndexError:
        print('The number you entered is not on the list.')
    except ValueError:
        print('Please enter only number.')    
    except:
        print('An error occurred while finding your ingredient.')
    else:
        for recipe in data['recipes_list']:
            for recipe_ing in recipe['Ingredients']:
                if (recipe_ing == ingredient_searched):
                    print('\nThe following recipe includes the searched ingredient: ')
                    print('------------------------------------------------------')
                    display_recipe(recipe)

# Ask the user for the name of the file that contains your recipe data.
filename = str(
    input('Enter the filename where you\'ve stored your recipes:  '))

# Use a try block to open the file, and then extract its contents into data using the pickle module.
try:
    recipes_file = open(filename, 'rb')
    data = pickle.load(recipes_file)

# For when the try block fails, add an except block to warn the user that the file hasn’t been found.
except FileNotFoundError:
    print('File doesn\'t exist in the current directory')
    data = {'recipes_list': [], 'all_ingredients': []}

except:
    print('An unexpected error occurred')
    data = {'recipes_list': [], 'all_ingredients': []}

# Define an else block that calls search_ingredient() while passing data into it as an argument.
else:
    search_ingredient(data)                        