from django.conf.urls import url, include
from timelog4app.views import *

app_name = "timelog4app"

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^activities$', activity_list, name='activities'),
    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^register/$', register_user, name='register'),
]
