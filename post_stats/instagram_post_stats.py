import pyperclip as pp
import json
import re
import requests
from datetime import datetime
import time

def get_post_stats(link,session):
    
    link = link.replace("\r","")
    link = link.replace("\n","")
        
    if '/reel/' in link:
        media_id = link.split("/reel/")[1]
    elif '/p/' in link:
        media_id = link.split("/p/")[1]
    elif '/tv/' in link:
        media_id = link.split("/tv/")[1]
    else:
        media_id = link.split(".com/")[1]
        media_id = media_id.split("/")[1]
        
        
    if "?" in media_id:
        media_id = media_id.split("?")[0]
    if "/" in link:
        media_id = media_id.split("/")[0]
    
    if '/p/' in link:
        link = "https://www.instagram.com/p/"  + media_id + "?__a=1"
    elif '/reel/' in link:
        link = "https://www.instagram.com/reel/"  + media_id + "?__a=1"
    elif '/tv/' in link:
        link = "https://www.instagram.com/tv/"  + media_id + "?__a=1"
    else:
        link = "https://www.instagram.com/"  + media_id + "?__a=1"
    
    print(link)
    
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
        
    return likes, comments, views_count
    

def main_program(input_links, username, password):
    print("main program called")
    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    userAgent= "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    
    time = int(datetime.now().timestamp())
    
    username = username
    password = password
    
    payload = {
    'username': username,
    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
    'queryParams': {},
    'optIntoOneTap': 'false'
    }
    
    links_array =  input_links
    links_array = links_array.split("\n")
    
    with requests.Session() as session:
        session.headers= {"user-agent":userAgent}
        session.headers.update({"Referer":link})
        r = session.get(link)
        print(r)
        csrf = re.findall(r"csrf_token\":\"(.*?)\"",r.text)[0]
        login_response = session.post(login_url,data=payload,headers={
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken":csrf
        })
        
        login_response_dict = json.loads(login_response.text)
            
        if 'authenticated' in login_response_dict:
            print("Login successful")
            if login_response_dict['authenticated']:
                final_string = ""
                for link in links_array:   
                    likes, comments, views_count = get_post_stats(link,session)
                    final_string += str(likes) + "\t" + str(comments) + "\t" + str(views_count ) + "\n" 
                arr = []
                final_string = final_string.split("\n")
                for row in final_string:
                    arr.append(row.split("\t"))
                return arr
                
            else:
                print("Login failed")
                return None
        else:
            print("Login failed")
            return None