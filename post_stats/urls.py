from django.urls import path
from . import views

urlpatterns = [
path("",views.home_page),
path("waitforit/",views.waitforit_page)
]