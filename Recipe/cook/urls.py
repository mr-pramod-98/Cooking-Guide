from django.urls import path
from . import views


urlpatterns = [
    # MAKE "index" PAGE OF THE "cook" APP AS THE MAIN PAGE
    path('', views.index, name="index"),
    path('cook', views.cook, name="cook"),
]
