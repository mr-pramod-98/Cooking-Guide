# -*- coding: utf-8 -*-
import scrapy
from ..spiders.user_input import UserInput
from ..spiders.user_input import Filter
from ..items import RecipesItem


class RecipesSpider(scrapy.Spider):
    
    name = 'recipes'
    start_urls = ['https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/?page=1']

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
            next_page = 'https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/?page=' + str(
                RecipesSpider.page_number)

            if RecipesSpider.page_number <= 43:
                RecipesSpider.page_number += 1
                yield response.follow(next_page, callback=self.parse)

            # ADDING TO "reference"
            RecipesSpider.reference[title[0]] = url[0]

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
