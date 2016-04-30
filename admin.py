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
    # --------------------------------------------------------------------------
    #                                            Specify a custom Formatted Date
    # --------------------------------------------------------------------------
    def pretty_date(self, obj):
        return obj.pub_date.strftime("%Y_%m_%d %H:%M")

    # Specify the underlying Model field (Required if we want to order using
    # this column )
    pretty_date.admin_order_field = 'pub_date'

    # Give it a friendly name to display in the column
    pretty_date.short_description = 'Published'


    # --------------------------------------------------------------------------
    #                                                       NOW ORGANISE COLUMNS
    # --------------------------------------------------------------------------
    # Columns to display
    list_display = ('item', 'rating', "author","condensed_review", 'pretty_date')

    # Filtering widget
    list_filter = ("pub_date", "rating")

    # Search bar to filter for values in the following fields
    search_fields = ("item__name",)

    # Ordering of rows using these columns (pubdate order the pretty_date colum)
    ordering = ("-pub_date", "-rating", "item")



# ==============================================================================
#                                                                REGISTER MODELS
# ==============================================================================
admin.site.register(Review, ReviewAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Item)


