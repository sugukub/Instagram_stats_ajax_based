from django.urls import path
from . import views

urlpatterns = [
path("get_stats",views.home_page)
]