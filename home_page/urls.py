from django.urls import path

import page_stats
from . import views

urlpatterns = [
path("",views.home_page),
]
