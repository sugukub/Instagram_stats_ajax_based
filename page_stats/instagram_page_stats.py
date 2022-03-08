import pyperclip as pp
import json
import re
import requests
from datetime import datetime
import time


def get_account_stats(link,session):
    
    link = link.replace("\r","")
    link = link.replace("\n","")
    
    page_name = link.split(".com/")[1]
    if "?" in page_name:
        page_name = page_name.split("?")[0]
    if "/" in link:
        page_name = page_name.split("/")[0]
    
    page_url = "https://www.instagram.com/" + page_name
    print(page_url)
    link = "https://www.instagram.com/"  + page_name + "?__a=1"
    
    link_response = session.get(link)        
    link_response = link_response.json()
    
    likes_array = []
    comments_array = []
    
    
    try:
        is_private = link_response['graphql']['user']['is_private']
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
        
    except:
        
        average_likes = "Not available"
        average_comments = "Not available"
        average_engagement_rate = "Not available"
    
    return full_name,is_private,page_url,followers,average_likes,average_comments,average_engagement_rate 
    
def main_program(input_links, username, password):
    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    userAgent= "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

    time = int(datetime.now().timestamp())
    print("Remember, 200 requests per hour only :) ")
    username = username
    password = password
    payload = {
    'username': username,
    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
    'queryParams': {},
    'optIntoOneTap': 'false'
    }

    #links_array =  pp.paste()
    links_array = input_links
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
            if login_response_dict['authenticated']:
                print("Login successful")
                final_string = ""
                for link in links_array:   
                    full_name,is_private,page_url,followers,average_likes,average_comments,average_engagement_rate  = get_account_stats(link,session)
                    final_string += full_name + "\t" + str(is_private)  + "\t" + page_url + "\t" + str(followers) + "\t" + str(average_likes )+ "\t" + str(average_comments )+ "\t" + str(average_engagement_rate) + "\n" 
                    #final_string += full_name + "\n" + str(is_private)  + "\n" + page_url + "\n" + str(followers) + "\n" + str(average_likes )+ "\n" + str(average_comments )+ "\n" + str(average_engagement_rate) + "\n" 
                arr = []
                final_string = final_string.split("\n")
                for row in final_string:
                    arr.append(row.split("\t"))
                #pp.copy(final_string)
                return arr
                
            else:
                print("Login failed")
                return None
        else:
            print("Login failed")
            return None