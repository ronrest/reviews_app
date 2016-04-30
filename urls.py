from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.review_list, name="review_list"),
    url(r'^item/$', views.item_list, name="item_list"),
    url(r'^(?P<review_id>[0-9]+)/$', views.single_review, name="single_review"),
]
