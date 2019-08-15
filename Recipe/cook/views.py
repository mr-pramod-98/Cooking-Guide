from django.shortcuts import render, redirect
import mysql.connector
from .ScrapyProject.Recipes.Recipes.spiders.user_input import UserInput
import os


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
        query = "SELECT * FROM " + table_name
        self.mycursor.execute(query)

        # "title", "ingredients" AND "directions" ARE THE COLUMN-NAME'S IN THE TABLE
        for (title, ingredients, directions) in self.mycursor:
            recipes = {
                        "title": title,
                        "ingredients": ingredients,
                        "directions": directions
                       }
            cooking_recipes.append(recipes)

        # RETURNING LIST OF RECIPES AS LIST OF DICTIONARY
        return cooking_recipes


class RunCrawler:

    def crawler(self):

        # MOVING TO THE DIRECTORY WHERE THE "spiders" ARE PRESENT
        os.chdir('cook/ScrapyProject/Recipes')

        # INITIATING THE CRAWLER
        os.system('scrapy crawl recipes')

        # MOVING BACK TO THE PREVIOUS WORKING DIRECTORY
        os.chdir('../../..')


# Create your views here.

# "index" METHOD IS CALLED WHET THE USER REQUEST FOR "index" PAGE
def index(request):
    return render(request, "index.html")


# "cook_guide" METHOD IS CALLED WHET THE USER LOGIN'S SUCCESSFULLY AND EVERY-TIME USER CLICK'S CRAWL BUTTON
def cook_guide(request, username):

    # IF THE REQUEST METHOD IS POST EXECUTE if BLOCK
    if request.method == "POST":

        item = request.POST['item name']

        # WRITE THE "item" AND "username" ON TO THE "connector" FILE USING THE "set_itenm_and_tablename" METHOD
        connector = UserInput()
        UserInput.set_item_and_tablename(connector, item, username)

        # RUN THE WEB-CRAWLER BY CALLING THE "crawler" METHOD
        crawl = RunCrawler()
        crawl.crawler()

        # REDIRECTING BACK TO THE SAME PAGE AFTER CRAWLING
        return redirect('/cook_guide/' + username)

    # IF THE REQUEST METHOD IS GET EXECUTE else BLOCK
    else:

        # "username" IS THE NAME OF THE TABLE
        data = CookingGuide()
        cooking_recipes = data.fetch_data(username)
        return render(request, "cook_guide.html", {'cooking_recipes': cooking_recipes})
