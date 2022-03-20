from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from . import instagram_post_stats

session_global = None

# Create your views here.
def home_page(request):    
    global session_global

    if request.method == "POST":
        if request.POST.get("get_links"):    

            input_links = request.POST.get("links")
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            request.session['username'] = username
            request.session['password'] = password

            logged_in,session = instagram_post_stats.login_function(request,username,password)
            
            session_global = session
            links_array = input_links.split("\n")
            
            
            if logged_in:
                links_array = input_links.split("\n")
                return render(request, "Instagram_post_stats/display_post_stats.html", {'links_array':links_array} )    
            else:
                return render(request, "Instagram_post_stats/display_post_stats.html", {'links_array':[]} )
            
    elif request.method == "GET":
        return render(request, "Instagram_post_stats/home_page.html", {})


def waitforit_page(request):

    medium = request.GET.get('medium', None)
    media_id = request.GET.get('media_id', None)
        
    global session_global
    print(medium,media_id)
    medium = medium.replace(" ","")
    media_id = media_id.replace(" ","")
    
    if medium == 'None':
        stats_dict = {
            'post_link':'Not available',
            'likes':'Not available',
            'comments':'Not available',
            'views':'Not available'
        }    
        
        return JsonResponse(stats_dict)


    post_link,likes,comments,views = instagram_post_stats.get_post_stats(medium,media_id,session_global)
    stats_dict = {
        'post_link':post_link,
        'likes':likes,
        'comments':comments,
        'views':views
    }
    return JsonResponse(stats_dict)
