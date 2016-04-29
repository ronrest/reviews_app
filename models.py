from django.db import models
import numpy as np

# ==============================================================================
#                                                                           ITEM
# ==============================================================================
class Item(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def average_rating(self):
        # Get a list of all the Review objects that reference this item, and
        # extract the rating value given
        all_ratings = map(lambda x: x.rating, self.review_set.all())

        # Return the average value of those ratings
        return np.mean(all_ratings)


# ==============================================================================
#                                                                           USER
# ==============================================================================
class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, blank=True, null=False)

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __unicode__(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()


# ==============================================================================
#                                                                         REVIEW
# ==============================================================================
class Review(models.Model):
    # Restrict ratings to be categorical
    RATING_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    item = models.ForeignKey(Item, on_delete="CASCADE")
    author = models.ForeignKey(User, on_delete="CASCADE")
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(max_length=250)
    pub_date = models.DateTimeField(auto_now=False,
                                    auto_now_add=False,
                                    verbose_name="date published")


