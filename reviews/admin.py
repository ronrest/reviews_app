from django.contrib import admin

from .models import Review, Item, KmeansCluster


# ==============================================================================
#                                                                     ITEM ADMIN
# ==============================================================================
class ItemAdmin(admin.ModelAdmin):
    """
    Customise the admin page for the Item Model so it displays id and name.

    Also has filtering and search features.
    """
    list_display = ('id', 'name')
    list_filter = ("name",)
    search_fields = ("name", "id")
    ordering = ("name",)


# ==============================================================================
#                                                                   REVIEW ADMIN
# ==============================================================================
class ReviewAdmin(admin.ModelAdmin):
    """
    Customise the admin page for the User Model so it displays first and
    last names as separate columns, as well as email.

    Also has filtering and search features.
    """
    # TODO: Try settin gup pretty date as a @property in the Model
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
    # TODO: COnsider seting up condensed review as a @property in the Model
    list_display = ('item', 'rating', "author","condensed_review", 'pretty_date')

    # Filtering widget
    list_filter = ("pub_date", "rating")

    # Search bar to filter for values in the following fields
    search_fields = ("item__name",)

    # Ordering of rows using these columns (pubdate order the pretty_date colum)
    ordering = ("-pub_date", "-rating", "item")


# ==============================================================================
#                                                                  CLUSTER ADMIN
# ==============================================================================
class KmeansClusterAdmin(admin.ModelAdmin):
    """
    Customise the admin page for the KmeansCluster Model.
    """
    list_display = ('name', 'get_members')
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)



# ==============================================================================
#                                                                REGISTER MODELS
# ==============================================================================
admin.site.register(Review, ReviewAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(KmeansCluster, KmeansClusterAdmin)



