from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.review_list, name="review_list"),
]
