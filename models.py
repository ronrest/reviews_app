from django.db import models
import numpy as np


# ##############################################################################
#                                                                           ITEM
# ##############################################################################
class Item(models.Model):
    name = models.CharField(max_length=200)

    # ==========================================================================
    #                                                                __UNICODE__
    # ==========================================================================
    def __unicode__(self):
        return self.name

    # ==========================================================================
    #                                                                    __STR__
    # ==========================================================================
    def __str__(self):
        return self.name

    # ==========================================================================
    #                                                             AVERAGE_RATING
    # ==========================================================================
    def average_rating(self):
        # Get a list of all the Review objects that reference this item, and
        # extract the rating value given
        all_ratings = [x.rating for x in self.review_set.all()]

        # Return the average value of those ratings
        # (return None if there are no reviews. None is used instead of np.nan
        # it is easier to check for None in Jinja templates )
        return np.mean(all_ratings) if len(all_ratings) > 0 else None

    # ==========================================================================
    #                                                                NUM_REVIEWS
    # ==========================================================================
    def num_reviews(self):
        """
        Returns the number of reviews this item has received.
        """
        return len(self.review_set.all())


# ##############################################################################
#                                                                           USER
# ##############################################################################
class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, blank=True, null=False)

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __unicode__(self):
        return self.full_name()

    def __str__(self):
        return self.full_name()


# ##############################################################################
#                                                                         REVIEW
# ##############################################################################
class Review(models.Model):
    # Restrict ratings to be categorical
    RATING_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(max_length=250)
    pub_date = models.DateTimeField(auto_now=False,
                                    auto_now_add=False,
                                    verbose_name="date published")

    # ==========================================================================
    #                                                         CONDENSED_REVIEW()
    # ==========================================================================
    def condensed_review(self, max_len=40):
        """
        Return a condensed version of the review so that it does not exceed some
        specified length. Includes ellipses to indicate that the text continues
        if it is longer than the max length.
        """
        if len(self.review) > max_len:
            return self.review[:max_len-3] + "..."
        else:
            return self.review[:max_len]

    # ==========================================================================
    #                                                                  __STR__()
    # ==========================================================================
    def __str__(self):
        return str(self.rating) + " (" + self.author.full_name() + ") " + self.item.name

    # ==========================================================================
    #                                                              __UNICODE__()
    # ==========================================================================
    def __unicode__(self):
        return str(self.rating) + " (" + self.author.full_name() + ") " + self.item.name

