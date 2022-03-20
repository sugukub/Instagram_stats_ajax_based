import pyperclip as pp
import json
import re
import requests
from datetime import datetime
import time

def get_post_stats(medium,media_id,session):

    if medium == 'post':
        link = "https://www.instagram.com/p/"  + media_id + "?__a=1"
    elif medium == 'reel':
        link = "https://www.instagram.com/reel/"  + media_id + "?__a=1"
    elif medium == 'igtv':
        link = "https://www.instagram.com/tv/"  + media_id + "?__a=1"
    
    link_response = session.get(link)        
    link_response = link_response.json()
    
    try:
        try:
            likes = link_response['graphql']['shortcode_media']['edge_media_preview_like']['count']
        except Exception as e:
            try:
                likes = link_response['items'][0]['like_count']        
            except:
                likes  = "Not available"
        
        if likes == -1:
            likes  = "Not available"
        
    except :
        likes  = "Not available"
        
        
    try:
        try:
            comments = link_response['graphql']['shortcode_media']['edge_media_preview_comment']['count']
        except Exception as e:
            try:
                comments = link_response['items'][0]['comment_count']        
            except:
                comments  = "Not available"
        
        if comments == -1:
            comments  = "Not available"
        
    except :
        comments  = "Not available"
    
    try:
        try:
            views_count = link_response['graphql']['shortcode_media']['edge_media_preview_like']['play_count']
        except Exception as e:
            print(e)
            try:
                views_count= link_response['items'][0]['play_count']        
            except Exception as e:
                try:
                    views_count= link_response['items'][0]['view_count']        
                except Exception as e:
                    views_count = "Not available"
                
        if views_count == -1:
            views_count = "Not available"
            
    except Exception as e:
        views_count = "Not available"
    
    link = link.replace("?__a=1","")

    return link, likes, comments, views_count
    

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