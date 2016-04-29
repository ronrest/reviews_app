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


# ==============================================================================
#                                                                           USER
# ==============================================================================
class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
