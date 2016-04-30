from django.shortcuts import render, HttpResponse

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
    reviews = Review.objects.all()
    context = {"reviews":reviews,
               "page_title":"Latest Reviews",
               }
    return render(request,
                  template_name= template_sub_dir + "review_list_template.html",
                  context=context)

