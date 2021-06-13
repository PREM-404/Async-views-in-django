from django.contrib import admin
from .models import Article, Subscriber

admin.site.register([Article, Subscriber])