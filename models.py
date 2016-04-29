from django.db import models


# ==============================================================================
#                                                                           ITEM
# ==============================================================================
class Item(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
