from django.shortcuts import render
from .models import RecipesDjango


# Create your views here.
def index(request):
    return render(request, "index.html")


def cook(request):

    # FETCHING DATA FROM DATABASE
    cooking_recipes = RecipesDjango.objects.all()
    return render(request, "cook.html", {'cooking_recipes': cooking_recipes})
