# Define a class Recipe
class Recipe(object):

    # Data attributes
    def __init__(self, name):
        self.name = name # the name of a recipe
        self.ingredients = [] # a list containing the ingredients for a recipe
        self.cooking_time = int(0) # the time taken in minutes to carry out a recipe
        self.difficulty = '' # an auto-generated attribute that says whether the recipe is Easy, Medium, Intermediate, or Hard

    #  method that takes in the name for the recipe
    def get_name(self): # Getter method for name
        output = 'Recipe name: ' + str(self.name)
        return output

    def set_name(self, name): # Setter method for name
        self.name = str(name)

    def get_cooking_time(self): # Getter method for cooking_time
        output = 'Cooking time: ' + str(self.cooking_time)
        return output

    def set_cooking_time(self, cooking_time): # Setter method for cooking_time
        self.cooking_time = int(cooking_time)

    # A method called add_ingredients that takes in variable-length arguments for the recipe’s ingredients.
    def add_ingredients(self, *args):
        self.ingredients = args
        self.update_all_ingredients()

    # A getter method for ingredients that returns the list itself.
    def get_ingredients(self):
        print('\nIngredients: ')
        print('---------------------------')
        for ingredient in self.ingredients:
            print(' - ' + str(ingredient))
        print('\n')

    # Updated difficalty with this method
    def calc_difficulty(self, cooking_time, ingredients): # takes params cooking_time and ingredients
        if (cooking_time < 10) and (len(ingredients) < 4):
            difficulty_level = 'Easy'
        elif (cooking_time < 10) and (len(ingredients) >= 4):
            difficulty_level = 'Medium'
        elif (cooking_time >= 10) and (len(ingredients) < 4):
            difficulty_level = 'Intermediate'
        elif (cooking_time >= 10) and (len(ingredients) >= 4):
            difficulty_level = 'Hard'
        else:
            print('Something bad happened, please try again')

        return difficulty_level

    # A getter method for difficulty which also calls calculate_difficulty() if difficulty hasn’t been calculated.
    def get_difficulty(self):
        difficulty = self.calc_difficulty(self.cooking_time, self.ingredients)
        output = 'Difficulty: ' + str(self.cooking_time)
        self.difficulty = difficulty
        return output

    # A search method that takes an ingredient as an argument
    def search_ingredient(self, ingredient, ingredients):
        if (ingredient in ingredients):
            return True
        else:
            return False
      

     # a list containing all of the ingredients
    all_ingredients = []

    # A method goes through the current object´s ingredients and adds them to all_ingredients container
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in self.all_ingredients:
                self.all_ingredients.append(ingredient)
    
    # A string representation the entire recipe 
    def __str__(self):
        output = '\nName: ' + str(self.name) + \
            '\nCooking time in minutes: ' + str(self.cooking_time) + \
            '\nDifficulty: ' + str(self.difficulty) + \
            '\nIngredients:' + \
            '\n-------------------- \n'
        for ingredient in self.ingredients:
            output += '- ' + ingredient + '\n'
        return output


    # A search method that takes recipe as an argument
    def recipe_search(self, recipes_list, ingredient):
        data = recipes_list
        search_term = ingredient
        for recipe in data: # Run a for loop that traverses through data
            if self.search_ingredient(search_term, recipe.ingredients):
                print(recipe)  


# Wrap the recipes into a list called recipes_list.
recipes_list = []

# Initialize an object named tea
tea = Recipe('Tea')
tea.add_ingredients('Tea Leaves', 'Sugar', 'Water')
tea.set_cooking_time(5)
tea.get_difficulty()

recipes_list.append(tea) # add tea to the recipes_list

# Initialize an object named coffee
coffee = Recipe('Coffee')
coffee.add_ingredients('Coffee Powder', 'Sugar', 'Water')
coffee.set_cooking_time(5)
coffee.get_difficulty()

recipes_list.append(coffee) # add coffee to the recipes_list

# Initialize an object named cake
cake = Recipe('Cake')
cake.add_ingredients('Sugar', 'Butter', 'Eggs',
                     'Vanilla Essence', 'Flour', 'Baking Powder', 'Milk')
cake.set_cooking_time(50)
cake.get_difficulty()

recipes_list.append(cake) # add cake to the recipes_list

# Initialize an object named banana_smoothie
banana_smoothie = Recipe('Banana Smoothie')
banana_smoothie.add_ingredients(
    'Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes')
banana_smoothie.set_cooking_time(5)
banana_smoothie.get_difficulty()

recipes_list.append(banana_smoothie) # add banana_smoothie to the recipes_list


# Display the string representation of objects
print('------------- ')
print('Recipes list: ')
print('------------- ')
for recipe in recipes_list:
    print(recipe)

# A method to search for recipes that contain ingredient "Water"
print('------------------------------------- ')
print('Results for recipe_search with Water: ')
print('------------------------------------- ')
tea.recipe_search(recipes_list, 'Water')

# A method to search for recipes that contain ingredient "Sugar"
print('------------------------------------- ')
print('Results for recipe_search with Sugar: ')
print('------------------------------------- ')
tea.recipe_search(recipes_list, 'Sugar')

# A method to search for recipes that contain ingredient "Bananas"
print('--------------------------------------- ')
print('Results for recipe_search with Bananas: ')
print('--------------------------------------- ')
tea.recipe_search(recipes_list, 'Bananas')

