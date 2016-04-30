from django.shortcuts import render, HttpResponse, get_object_or_404

from .models import Review, Item, User

template_sub_dir = "reviews/"   # Used for locating templates for this app
static_sub_dir = "reviews/"   # Used for locating static files for this app


# Create your views here.
def index(request):
    return HttpResponse("hey hey hey!!!")


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
                  template_name= template_sub_dir + "review_list_template.html",
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
                  template_name= template_sub_dir + "review_template.html",
                  context=context)
