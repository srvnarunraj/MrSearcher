from django.urls import path
from . import views
urlpatterns = [
    path('',views.startup),
    path('search',views.search),
    path('videos',views.videos),
    path('images',views.images),
    path('books',views.books),
    path('all',views.all),
]
