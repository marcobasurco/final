from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^wishes/$', views.wishes),
    url(r'^wishes/new/$', views.newWish),
    url(r'^wishes/wishHandler/$', views.wishHandler),
    url(r'^wishes/editor/$', views.editor),
    url(r'^wishes/edit/(?P<id>\d+)$', views.editWish),
    url(r'^wishes/like/(?P<id>\d+)$', views.like),
    url(r'^wishes/remove/(?P<id>\d+)$', views.remove),
    url(r'^wishes/grantWish/(?P<id>\d+)$', views.grantWish),
    url(r'^wishes/stats/$', views.stats),
    url(r'^logout/$', views.logout),

]



