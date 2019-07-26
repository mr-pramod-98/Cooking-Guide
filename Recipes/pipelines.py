# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector


class RecipesPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.mydatabase = mysql.connector.connect(host='localhost', user='root', passwd='password', database='recipe_test')
        self.mycursor = self.mydatabase.cursor()

    # "create_table" METHOD CREATE's A TABLE AND IF THE TABLE IS ALREADY PRESENT THEN IT DROP THE TABLE AND THEN CREATE
    def create_table(self):
        self.mycursor.execute("""DROP TABLE IF EXISTS Recipes""")
        self.mycursor.execute("""create table Recipes(
                              title varchar(100),
                              ingredients text(500),
                              procedures text
                             )""")

    def store_to_database(self, item):

        # CONVERTING THE LIST OF INGREDIENTS INTO STRING
        ingredients = ''
        for ingredient in item['ingredients']:
            ingredients = ingredients + ingredient + "\n"

        # CONVERTING THE LIST COOKING PROCEDURE INTO STRING
        procedures = ''
        for procedure in item['procedures']:
            procedures = procedures + procedure

        query = "insert into Recipes(title, ingredients, procedures) values(%s, %s, %s)"
        values = (item['title'], ingredients, procedures)

        self.mycursor.execute(query, values)
        self.mydatabase.commit()

        print(self.mycursor.rowcount, "record inserted")

    def process_item(self, item, spider):
        self.store_to_database(item)
        return item
