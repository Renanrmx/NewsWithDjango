from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('index/', home, name='home'),
    path('index/tag=<int:tag>', home, name='home_tag'),
    path('index/category=<int:category>', home, name='home_category'),
    path('details/<int:article>/', details, name='details'),
]


