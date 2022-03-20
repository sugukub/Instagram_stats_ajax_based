import pyperclip as pp
import json
import re
import requests
from datetime import datetime
import time
from sqlalchemy import over

def numbers_into_k(val):
    val = str(val.replace(",",""))
    try:
        val = float(val)
        if val > 10000:
            val = val/1000
            val = float("{:.1f}".format(val))
            if val > 1000:
                val = float(val/1000)
                val = float("{:.1f}".format(val))
                val = str(val) + "m"
            else:
                val = str(val) + "k"
        else:
            val = str(val)
    except:
        val = str(val)
    
    return val


def get_account_stats(page_name,session):
    
    page_url = "https://www.instagram.com/" + page_name
    link = "https://www.instagram.com/"  + page_name + "?__a=1"
    
    link_response = session.get(link)        
    link_response = link_response.json()
    
    likes_array = []
    comments_array = []
    
    try:
        is_private = link_response['graphql']['user']['is_private']
        if is_private:
            is_private = "Private"
        else:
            is_private = "Public"

    except:
        is_private = "Not available"

    try:
        followers = link_response['graphql']['user']['edge_followed_by']['count']    
    except:
        followers = "Not available"
    
    try:
        full_name = link_response['graphql']['user']['full_name']
    except:
        full_name = "Not available"
    
    try:
        for post in link_response['graphql']['user']['edge_owner_to_timeline_media']['edges']:
            likes_array.append(post['node']['edge_liked_by']['count'])
        
        average_likes = int(sum(likes_array)/len(likes_array))
        for post in link_response['graphql']['user']['edge_owner_to_timeline_media']['edges']:
            comments_array.append(post['node']['edge_media_to_comment']['count'])
        
        average_comments = int(sum(comments_array)/len(comments_array))
        average_engagement_rate = (average_comments + average_likes) / followers * 100
        average_engagement_rate = round(average_engagement_rate, 2)

    except:    
        average_likes = "Not available"
        average_comments = "Not available"
        average_engagement_rate = "Not available"
    
    followers = numbers_into_k(str(followers))
    
    return page_name,is_private,page_url,followers,average_likes,average_comments,average_engagement_rate 

def login_function(request,username,password):
            
    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    userAgent= "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

    time = int(datetime.now().timestamp())
    payload = {
    'username': username,
    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
    'queryParams': {},
    'optIntoOneTap': 'false'
    }

    with requests.Session() as session:

        session.headers= {"user-agent":userAgent}
        session.headers.update({"Referer":link})
        r = session.get(link)
        csrf = re.findall(r"csrf_token\":\"(.*?)\"",r.text)[0]
        login_response = session.post(login_url,data=payload,headers={
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken":csrf
        })
        
        login_response_dict = json.loads(login_response.text)
        
        if 'authenticated' in login_response_dict:
            if login_response_dict['authenticated']:
                return True,session
            else:
                return False,None
        else:
            return False,None