
from django.conf.urls import url, include
import views

urlpatterns = [
	url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.add),
    url(r'^addtrip$', views.addtrip),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^travels/destination/(?P<id>\d+)$', views.showtrip)
    # url(r'^books/(?P<id>\d+)$', views.showbook),
    # url(r'^getuser$', views.getuser),
    # url(r'^users/(?P<id>\d+)$', views.showusers),
    # url(r'^books/(?P<id>\d+)/addreview$', views.addreview),
    # url(r'^books/(?P<bookid>\d+)/delete/(?P<reviewid>\d+)$', views.delete)
]