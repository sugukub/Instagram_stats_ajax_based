from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from . import instagram_page_stats

session_global = None

def get_page_name(link):
    
    page_name = link.split(".com/")[1]
    if "?" in page_name:
        page_name = page_name.split("?")[0]
    if "/" in link:
        page_name = page_name.split("/")[0]
    page_name = page_name.replace("\r","")
        
    return page_name

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

            logged_in,session = instagram_page_stats.login_function(request,username,password)
            
            session_global = session

            if logged_in:
                links_array = input_links.split("\n")
                names_array = list(map(get_page_name,links_array))
                print(names_array)
                return render(request, "Instagram_page_stats/display_page_stats.html", {'names_array':names_array} )    
            else:
                return render(request, "Instagram_page_stats/display_page_stats.html", {'names_array':[]} )
            
    elif request.method == "GET":
        return render(request, "Instagram_page_stats/home_page.html", {})

def waitforit_page(request,page_name):
    
    global session_global
    page_name = page_name.replace(" ","")
    page_name,is_private,page_url,followers,average_likes,average_comments,average_engagement_rate = instagram_page_stats.get_account_stats(page_name,session_global)
    stats_dict = {
        'page_name':str(page_name),
        'private_public':is_private,
        'page_link':page_url,
        'followers':followers,
        'avg_likes':average_likes,
        'avg_comments':average_comments,
        'avg_eng_rate':average_engagement_rate
    }
    return JsonResponse(stats_dict)
