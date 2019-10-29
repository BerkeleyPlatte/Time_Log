from django.conf.urls import url, include
from timelog4app.views import *
from django.urls import path

app_name = "timelog4app"

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^activities$', activity_list, name='activities'),
    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^register/$', register_user, name='register'),
    url(r'^activity/form$', activity_form, name='activity_form'),
    path('activities/<int:activity_id>/', activity_details, name='activity'),
    url(r'^activities/(?P<activity_id>[0-9]+)/form$', activity_edit_form, name='activity_edit_form'),
]
