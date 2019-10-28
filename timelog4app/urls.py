from django.conf.urls import url
from timelog4app.views import *

app_name = "timelog4app"

urlpatterns = [
    url(r'^$', activity_list, name='home'),
    url(r'^activities$', activity_list, name='activities'),
]
