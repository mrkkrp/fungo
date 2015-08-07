from django.conf.urls import patterns, url
from fungo import views

urlpatterns = [
    url(r'^$',         views.index, name='index'),
    url(r'^category/(?P<category_name_url>[\w\-]+)/$',
        views.category, name='category'),
    url(r'^about/',    views.about, name='about'),
]
