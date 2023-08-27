# Import the pickle module
import pickle

# Define a function called take_recipe() to take recipes from the user
def take_recipe():
    name = str(input('Enter the name of the recipe: '))
    cooking_time = int(
        input('Enter the cooking time of the recipe in minutes: ')
    )
    ingredients = input('Enter the ingredients of the recipe, separated by a space: ')
    ingredients = ingredients.split()
    ingredients = [ingredient.lower() for ingredient in ingredients]
    recipe = {'Name': name, 'Cooking_Time': cooking_time, 'Ingredients': ingredients}
    difficulty = calc_difficulty(recipe)
    return recipe

# Define the function calc_diffficulty(), where the difficulty is returned as Easy, Medium, Intermediate or Hard
def calc_difficulty(recipe):
    if recipe['Cooking_Time'] < 10 and len(recipe['Ingredients']) < 4:
        recipe['Difficulty'] = 'Easy'

    elif recipe['Cooking_Time'] < 10 and len(recipe['Ingredients']) >= 4:
        recipe['Difficulty'] = 'Medium'

    elif recipe['Cooking_Time'] >= 10 and len(recipe['Ingredients']) < 4:
        recipe['Difficulty'] = 'Intermediate'

    elif recipe['Cooking_Time'] >= 10 and len(recipe['Ingredients']) >= 4:
        recipe['Difficulty'] = 'Hard'

# Have the user enter a filename, which would attempt to open a binary file in read mode.
recipes_list = []
all_ingredients = []

filename = str(input('Enter a filename with your recipes: '))
try:
    recipes_file = open(filename, 'rb')
    data = pickle.load(recipes_file)
except FileNotFoundError:
    print('File not found. Creating a new file.')
    data = {'recipes_list': [], 'all_ingredients': []}
except:
    print('Unexpected error. Creating a new file. ')
    data = {'recipes_list': [], 'all_ingredients': []}
else:
    recipes_file.close()
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

# Ask the user how many recipes they’d like to enter, and define a for loop that calls the take_recipe() function.
num = int(input('How many recipes would you like to enter? '))

for i in range(num):
    recipe = take_recipe()
    print(recipe)

    for ingredient in recipe['Ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

    recipes_list.append(recipe)

# Gather the updated recipes_list and all_ingredients into the dictionary called data.
data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

# Open a binary file with the user-defined filename and write data to it using the pickle module.
new_file_name = str(input('Enter a name for the new file.'))
new_file_name = open(new_file_name, 'wb')
pickle.dump(data, new_file_name)