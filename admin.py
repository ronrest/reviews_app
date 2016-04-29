from django.contrib import admin

from .models import Review, User, Item

# ==============================================================================
#                                                                     USER ADMIN
# ==============================================================================
class UserAdmin(admin.ModelAdmin):
    """
    Customise the admin page for the User Model so it displays first and
    last names as separate columns, as well as email.

    Also has filtering and search features.
    """
    list_display = ('first_name', 'last_name', 'email')
    list_filter = ("last_name",)
    search_fields = ("last_name", "first_name")


# ==============================================================================
#                                                                   REVIEW ADMIN
# ==============================================================================
class ReviewAdmin(admin.ModelAdmin):
    """
    Customise the admin page for the User Model so it displays first and
    last names as separate columns, as well as email.

    Also has filtering and search features.
    """
    list_display = ('item', 'rating', "author","condensed_review", 'time_condensed')
    list_filter = ("pub_date", "rating")
    search_fields = ("item__name",)

    def time_condensed(self, obj):
        return obj.pub_date.strftime("%Y_%m_%d %H:%M")


# ==============================================================================
#                                                                REGISTER MODELS
# ==============================================================================
admin.site.register(Review, ReviewAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Item)

