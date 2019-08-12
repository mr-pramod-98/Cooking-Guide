from django.shortcuts import render
import mysql.connector


class CookingGuide:

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.mydatabase = mysql.connector.connect(host='localhost', user='root', passwd='password', database='recipe_test')
        self.mycursor = self.mydatabase.cursor()

    # "fetch_data" METHOD IS USED TO FETCH DATA FROM THE SPECIFIED TABLE IN THE SPECIFIED DATABASE
    def fetch_data(self, table_name):
        
        # "cooking_recipes" CONTAINS LIST OF DICTIONARIES
        cooking_recipes = []

        # "table_name" IS NAME OF THE TABLE FROM WHICH DATA HAS TO BE FETCHED
        self.mycursor.execute(''' SELECT * FROM ''' + table_name)

        # "id", "title", "ingredients" AND "directions" ARE THE COLUMN-NAME'S IN THE TABLE
        for (id, title, ingredients, directions) in self.mycursor:
            recipes = {
                        "title": title,
                        "ingredients": ingredients,
                        "directions": directions
                       }
            cooking_recipes.append(recipes)

        # RETURNING LIST OF RECIPES AS LIST OF DICTIONARY
        return cooking_recipes


# Create your views here.

# "index" METHOD IS CALLED WHET THE USER REQUEST FOR "index" PAGE 
def index(request):
    return render(request, "index.html")


# "cook_guide" METHOD IS CALLED WHET THE USER LOGIN'S SUCCESSFULLY
def cook_guide(request, username):

    # "username" IS THE NAME OF THE TABLE
    data = CookingGuide()
    cooking_recipes = data.fetch_data(username)
    return render(request, "cook_guide.html", {'cooking_recipes': cooking_recipes})


def cook(request):
    cooking_recipes = []
    return render(request, "cook.html", {'cooking_recipes': cooking_recipes})
