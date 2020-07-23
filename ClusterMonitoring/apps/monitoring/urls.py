from django.urls import path
from apps.monitoring.views import *

urlpatterns = [
    path('', landing, name='landing'),
    path('receive', receive, name='receive')
]
