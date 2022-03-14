from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import instagram_post_stats

# Create your views here.
def home_page(request):
    if request.method == "POST":
        if request.POST.get("get_links"):    
            
            input_links = request.POST.get("links")
            username = request.POST.get("username")
            password = request.POST.get("password")
            print("calling the program")
            post_stats = instagram_post_stats.main_program(input_links, username, password)
            print("data collected")
            return render(request, "Instagram_post_stats/display_post_stats.html", {
                'post_stats':post_stats

            } ) 

    elif request.method == "GET":
        return render(request, "Instagram_post_stats/home_page.html", {})