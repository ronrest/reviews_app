from django.contrib import admin

from .models import Review, User, Item

# Register your models here.
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Item)
