from django.urls import path

from .views import *

urlpatterns = [
    *AccountView.get_url_patterns(),
]
