from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.review_list, name="review_list"),
    url(r'^(?P<review_id>[0-9]+)/$', views.single_review, name="single_review"),

    url(r'^item/$', views.item_list, name="item_list"),
    url(r'^item/(?P<item_id>[0-9]+)/$', views.single_item, name="single_item"),

    url(r'^add_review/(?P<item_id>[0-9]+)/$', views.add_review, name="add_review"),

    url(r'^user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    url(r'^user/$', views.user_review_list, name='user_review_list'),

    # User Authentication Pages
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'template_name': 'registration/logout.html'},
        name="logout"),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {"template_name": "registration/login.html"},
        name="login"),
]
