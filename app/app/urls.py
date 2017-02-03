
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^slack/', include('django_slack_oauth.urls')),

    url('', include('webfrontend.urls')),
]
