from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^main/$', views.main, name='webfrontend.main'),
    url(r'^main/(?P<team_hash>.*)/(?P<user_hash>.*)/$', views.details, name='webfrontend.details'),
    url(r'^logout/$', views.logout),
]