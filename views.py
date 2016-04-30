from django.shortcuts import render, HttpResponse

from .models import Review, Item, User

# Create your views here.
def index(request):
    return HttpResponse("hey hey hey!!!")


# ==============================================================================
#                                                                    REVIEW_LIST
# ==============================================================================
def review_list(request):
    reviews = Review.objects.all()
    context = {"reviews":reviews}
    return render(request,
                  template_name="review_list_template.html",
                  context=context)

