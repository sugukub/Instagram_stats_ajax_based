from django.urls import path
from . import views

urlpatterns = [
    path("",views.home_page),
    path("waitforit/<str:page_name>",views.waitforit_page)
    ]