from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from . import instagram_post_stats

session_global = None

def get_post_link(link):

    if '/p/' in link:
        media_id = link.split('/p/')[1]
        
        if '/' in media_id:
            media_id = media_id.split("/")[0]
        if '?' in media_id:
            media_id = media_id.split("?")[0]
        
        link = "https://www.instagram.com/p/" + media_id

    elif '/tv/' in link:
        media_id = link.split('/tv/')[1]
        
        if '/' in media_id:
            media_id = media_id.split("/")[0]
        if '?' in media_id:
            media_id = media_id.split("?")[0]
        
        link = "https://www.instagram.com/tv/" + media_id

    elif '/reel/' in link:
        media_id = link.split('/reel/')[1]
        
        if '/' in media_id:
            media_id = media_id.split("/")[0]
        if '?' in media_id:
            media_id = media_id.split("?")[0]
        
        link = "https://www.instagram.com/reel/" + media_id
    
    return link
        
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
            
            if logged_in:
                links_array = input_links.split("\n")
                links_array = list(map(get_post_link, links_array))
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
