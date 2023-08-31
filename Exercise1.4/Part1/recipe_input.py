# Import the pickle module
import pickle

# Define a function called take_recipe() to take recipes from the user


def take_recipe():
    name = str(input('Enter the name of the recipe: '))
    cooking_time = int(
        input('Enter the cooking time of the recipe in minutes: ')
    )
    ingredients = input(
        'Enter the ingredients of the recipe, separated by a space: ')
    ingredients = ingredients.split()
    ingredients = [ingredient.lower() for ingredient in ingredients]
    difficulty = calc_difficulty(cooking_time, ingredients)
    recipe = {'name': name, 'cooking_Time': cooking_time,
              'ingredients': ingredients, 'difficulty': difficulty}
    return recipe

# Define the function calc_diffficulty(), where the difficulty is returned as Easy, Medium, Intermediate or Hard
# takes params cooking_time and ingredients


def calc_difficulty(cooking_time, ingredients):
    difficalty = None
    if (cooking_time < 10) and (len(ingredients) < 4):
        difficulty = 'Easy'
    elif (cooking_time < 10) and (len(ingredients) >= 4):
        difficulty = 'Medium'
    elif (cooking_time >= 10) and (len(ingredients) < 4):
        difficulty = 'Intermediate'
    elif (cooking_time >= 10) and (len(ingredients) >= 4):
        difficulty = 'Hard'
    else:
        print('Something bad happened, please try again')

    return difficulty


# Have the user enter a filename, which would attempt to open a binary file in read mode.
recipes_list = []
all_ingredients = []

filename = str(input('Enter a filename with your recipes without extension: '))
filename = filename + '.bin'
try:
    recipes_file = open(filename, 'rb')
    data = pickle.load(recipes_file)
    print('Loaded file successfully.')
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

    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

    recipes_list.append(recipe)

# Open a binary file with the user-defined filename and write data to it using the pickle module.
filename = open(filename, 'wb')
pickle.dump(data, filename)
