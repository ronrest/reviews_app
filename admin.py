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
#                                                                REGISTER MODELS
# ==============================================================================
admin.site.register(Review)
admin.site.register(User, UserAdmin)
admin.site.register(Item)
