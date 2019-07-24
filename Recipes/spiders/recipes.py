# -*- coding: utf-8 -*-
import scrapy
from ..spiders.user_input import UserInput
from ..spiders.user_input import Filter
from ..items import RecipesItem


class RecipesSpider(scrapy.Spider):

    name = 'recipes'

    def start_requests(self):

        urls = [
                #'https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/?page=1',
                'https://www.allrecipes.com/recipes/1874/world-cuisine/asian/indian/appetizers/?internalSource=hub%20nav&referringId=233&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202&page=1',
                'https://www.allrecipes.com/recipes/1879/world-cuisine/asian/indian/desserts/?internalSource=hub%20nav&referringId=233&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202&page=1',
                'https://www.allrecipes.com/recipes/1876/world-cuisine/asian/indian/bread/?internalSource=hub%20nav&referringId=233&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202&page=1',
                'https://www.allrecipes.com/recipes/1877/world-cuisine/asian/indian/side-dishes/?internalSource=hub%20nav&referringId=233&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202&page=1'
               ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # "url_to_total_pages" HOLDS THE TOTAL NUMBER OF PAGES OF THE CORRESPONDING URL
    url_to_total_pages = {
                'https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/?': 43,
                'https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/': 43,
                'https://www.allrecipes.com/recipes/1874/world-cuisine/asian/indian/appetizers/?internalSource=hub%20nav&referringId=233&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202': 3,
                'https://www.allrecipes.com/recipes/1876/world-cuisine/asian/indian/bread/?internalSource=hub%20nav&referringId=233&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202': 2,
                'https://www.allrecipes.com/recipes/1877/world-cuisine/asian/indian/side-dishes/?internalSource=hub%20nav&referringId=233&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202': 5,
                'https://www.allrecipes.com/recipes/1879/world-cuisine/asian/indian/desserts/?internalSource=hub%20nav&referringId=233&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202': 3
               }

    # "page_number" CONTAINS THE NEXT PAGE INDEX IN THE URL TO BE CRAWLED
    page_number = 2

    # "reference" IS A DICT THAT HOLDS THE "title" AS KEY AND "url" AS ITS VALUE
    reference = {}

    # CREATING AN OBJECT OF CLASS "RecipesItem"
    item = RecipesItem()

    # CREATING AN OBJECT OF CLASS "Filter"
    filter = Filter()

    # GETTING USER INPUT
    user = UserInput()
    item_name = user.read()

    def parse(self, response):

        # SELECT THE LIST OF BLOCKS
        recipes_list = response.css('.fixed-recipe-card')

        # LOOP THROUGH EACH BLOCK AND SCRAP THE "title" AND "url" OF THAT BLOCK
        for recipe in recipes_list:

            title = recipe.css('span.fixed-recipe-card__title-link::text').extract()
            url = recipe.css('.fixed-recipe-card__h3 a').xpath("@href").extract()

            # OBTAINING THE URL OF NEXT PAGE
            next_page = response.url[:-1] + str(RecipesSpider.page_number)

            # "response.url" HOLDS THE URL OF THE CURRENT CRAWLING PAGE
            # "URL" TAKES A CORY OF THE CURRENT PAGE URL
            URL = str(response.url)

            # REMOVING "&page=?" SUB-STRING FROM THE MAIN STRING
            URL = URL[:-7]

            # CRAWL THE NEXT PAGE IF "page_number" AS NOT EXCEDED TOTAL PAGE NUMBER
            # IF "page_number" AS  EXCEDED TOTAL PAGE NUMBER THEN RESET THE "page_number"
            if RecipesSpider.page_number <= RecipesSpider.url_to_total_pages[URL]:
                RecipesSpider.page_number += 1
                yield response.follow(next_page, callback=self.parse)

            else:
                # RESET THE "page_number"
                RecipesSpider.page_number = 2

            # ADDING TO "reference"
            RecipesSpider.reference[title[0]] = url[0]

        # FILTERING THE URL's WHICH ARE NOT REQURIED
        result = RecipesSpider.filter.optimize_search_result(RecipesSpider.item_name, RecipesSpider.reference)

        # CALLING "parse_recipe" METHOD FOR "result"
        for item in result.keys():
            yield response.follow(result[item], callback=self.parse_recipe)

    # "parse_recipe" METHOD CRAWL'S THE SUB-PAGES PRESENT A SINGLE PAGE
    def parse_recipe(self, responce):

        # SCRAP THE NAME TO THE ITEM
        title = responce.css('#recipe-main-content::text').get()

        # SCRAP THE RECIPE OF THE ITEM
        ingredients = responce.css('.added::text').extract()

        # ADDING SCRAPED ELEMENTS TO ITEM'S LIST
        RecipesSpider.item['ingredients'] = ingredients
        RecipesSpider.item['title'] = title
        yield RecipesSpider.item
