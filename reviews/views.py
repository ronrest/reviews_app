from django.shortcuts import render, HttpResponse, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from registration.backends.default.views import RegistrationView

from .models import Review, Item, KmeansCluster #, User
from django.contrib.auth.models import User
from .forms import ReviewForm

import datetime


template_sub_dir = "reviews/"   # Used for locating templates for this app
static_sub_dir = "reviews/"   # Used for locating static files for this app


# ==============================================================================
#                                                                    REVIEW_LIST
# ==============================================================================
def review_list(request):
    """
    Show the 9 latest reviews
    """
    reviews = Review.objects.order_by("-pub_date")[:9]
    context = {"reviews":reviews,
               "page_title":"Latest Reviews",
               }
    return render(request,
                  template_name= template_sub_dir + "review_list.html",
                  context=context)


# ==============================================================================
#                                                               USER_REVIEW_LIST
# ==============================================================================
def user_review_list(request, username=None):
    """
    Show the reviews by the user
    """
    if username is None:
        username = request.user.username  # get_object_or_404(User, pk=current_user)

    reviews = Review.objects.filter(author=username).order_by("-pub_date")
    context = {"reviews":reviews,
               "page_title":"Your Reviews",
               "username":username}
    return render(request,
                  template_name= template_sub_dir + "user_review_list.html",
                  context=context)



# ==============================================================================
#                                                       USER_RECOMMENDATION_LIST
# ==============================================================================
@login_required
def user_recommendation_list(request):
    """
    Show recomendations to the user
    Currently just shows the user a list of All the items.
    """
    username = request.user.username
    # --------------------------------------------------------------------------
    #                                         Get Items Reviewed by current user
    # --------------------------------------------------------------------------
    user_reviews = Review.objects.filter(author=username).prefetch_related("item")
    user_items_reviewed_ids = {review.item.id for review in user_reviews}
    #user_items_not_reviewed = Item.objects.exclude(id__in=items_reviewed).order_by("name")

    # --------------------------------------------------------------------------
    #                                                          Get Similar Users
    # --------------------------------------------------------------------------
    # Get the cluster that the current user belongs to
    cluster = User.objects.get(username=username).kmeanscluster_set.first()

    # --------------------------------------------------------------------------
    #         Handle situation where user has not been assigned to a cluster yet
    # --------------------------------------------------------------------------
    if cluster is None:
        context = {"items": [],
                   "page_title": "No recomendations available for you yet",
                   }

    # --------------------------------------------------------------------------
    # Generate recommendations based on reviews from other users in same cluster
    # --------------------------------------------------------------------------
    else:
        # Get the other users from that cluster (then their names)
        similar_users = cluster.users.exclude(username=username)
        similar_users_names = {user.username for user in similar_users}

        # ----------------------------------------------------------------------
        #                                                     Create Suggestions
        # ----------------------------------------------------------------------
        # get the reviews by those other users
        # (excluding ones already reviewed by current user)
        other_users_reviews = Review.objects.filter(author__in=similar_users_names)\
            .exclude(item__id__in=user_items_reviewed_ids)

        # Get the items reviewed by the other users
        other_users_items_reviewed = {review.item for review in other_users_reviews}

        # Use these items reviewed by the other users as the suggestions, order
        # them based on average rating of that item.
        # TODO: consider ranking them by the ratings given by the similar users
        #       instead of ratings from all users.
        suggestions = sorted(other_users_items_reviewed,
                             key=lambda x: x.average_rating(),
                             reverse=True)

        #[item.average_rating() for item in suggestions] # verify sorting worked

        # ----------------------------------------------------------------------
        #                                                         Create Context
        # ----------------------------------------------------------------------
        context = {"items": suggestions,
                   "page_title":"List of Recomentations",
                   }

    # ----------------------------------------------------------------------
    #                                                        Render the Page
    # ----------------------------------------------------------------------
    return render(request,
                  template_name= template_sub_dir + "recommendations.html",
                  context=context)



# ==============================================================================
#                                                                  SINGLE_REVIEW
# ==============================================================================
def single_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    context = {"review":review,
               "page_title":"Review for " + review.item.name,
               }
    return render(request,
                  template_name= template_sub_dir + "review.html",
                  context=context)


# ==============================================================================
#                                                                      ITEM_LIST
# ==============================================================================
def item_list(request):
    """
    Show all items
    """
    items = Item.objects.order_by("name")
    context = {"items":items,
               "page_title":"List of Items",
               }
    return render(request,
                  template_name= template_sub_dir + "item_list.html",
                  context=context)


# ==============================================================================
#                                                                    SINGLE_ITEM
# ==============================================================================
def single_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    author = request.user.username

    # --------------------------------------------------------------------------
    #                    Check if the user has already reviewed this item before
    # --------------------------------------------------------------------------
    if item.review_set.filter(author=author).count() > 0:
        form = "done"
        user_review = item.review_set.filter(author=author)[0]
    else:
        form = ReviewForm()
        user_review = None

    # --------------------------------------------------------------------------
    #                                                                Render Page
    # --------------------------------------------------------------------------
    context = {"item": item,
               "reviews": item.review_set.all().order_by("-pub_date"),
               "user_review": user_review,
               "form": form}
    return render(request, 'reviews/item.html', context=context)


# ==============================================================================
#                                                                     ADD_REVIEW
# ==============================================================================
@login_required
def add_review(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    author = request.user.username
    # --------------------------------------------------------------------------
    #                    Check if the user has already reviewed this item before
    # --------------------------------------------------------------------------
    if item.review_set.filter(author=author).count() > 0:
        already_reviewed = True
    else:
        already_reviewed = False

    # If person has already reviewed, then show a message that they have reviewed
    # -  Maybe Populate the form with their existing values
    # If not alredy reviewed, then show empty form.

    if already_reviewed:
        form = "done"
        return render(request, template_sub_dir + 'add_review.html',{'item': item, 'form': form})

    # --------------------------------------------------------------------------
    #                    Check if the user has already reviewed this item before
    # --------------------------------------------------------------------------
    if (request.method == "POST"):
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Get the filled in data from the form
            clean_data = form.cleaned_data
            rating = clean_data['rating']
            comment = clean_data['review']

            # Populate a database entry based on form data and other generated data
            review = Review(item=item,          # Got this from the url
                            author=author,      # Got this from the environment
                            rating=rating,      # Got this from the form
                            review=comment,     # Got this from the form
                            pub_date= datetime.datetime.now() # Auto generated
                            )
            review.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            # Reverse URL lookup
            return HttpResponseRedirect(reverse('reviews:single_item', args=(item.id,)))
        else:
            pass # form is not valid. SImply dont process it.
    else:
        # No POST information has been sent, which means the user is coming in
        # Fresh, so create a blank form.
        form = ReviewForm()

    return render(request, template_sub_dir + 'add_review.html', {'item': item, 'form': form})


# ==============================================================================
#                                                                       REGISTER
# ==============================================================================
class register(RegistrationView):
    template_name = "registration/registration_form.html"
    success_url = "/"
    # TODO: BUG: Throws error after registration. Something to do with not
    #            Finding the reverse lookup for registration_complete
    #            But i still continue getting this error even if i add a
    #            url field in the urls.py with that name. Find out if there is
    #            a way around this.

