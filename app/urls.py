from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('article/create/', views.create_article, name='article_create'),
]