import glob
from datetime import datetime,timedelta
import time
import random
import pandas as pd

from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from instagrapi.exceptions import (
    BadPassword, ReloginAttemptExceeded, ChallengeRequired,
    SelectContactPointRecoveryForm, RecaptchaChallengeForm,
    FeedbackRequired, PleaseWaitFewMinutes, LoginRequired
)
import logging
import requests
from requests.exceptions import HTTPError

from data_generator import *
from info_logger import Info_Logger as il


'''
Avataring Module
set bot accounts for Ig users.

'''
#initialization
print('Specify file with accounts data: ')
all_files = glob.glob(r'C:\Users\danil\PythonFiles\IronStorm\*.csv')
for csv_file in all_files:
    csv_file = csv_file.replace(r'C:\Users\danil\PythonFiles\IronStorm', '')
    print(csv_file)
file = input('')
assertion = input('is it right?: ')
if assertion == 'yes':
    il.bot_log(f'Initializing {file}...')
else:
    quit()

#laod users
def load_users(file:str):
    ''' 
    Load user data and passwrods from file
    '''

    f = file
    df = pd.read_csv(f'{f}',header=None)
    il.bot_log("Passing users...")
    users = df[df.columns[0]].values.tolist()
    passwords = df[df.columns[1]].values.tolist()
    emails = df[df.columns[2]].values.tolist()
    email_passwords = df[df.columns[3]].values.tolist()

    user_list = []
    for user_tuple in zip(users,passwords,emails,email_passwords):
        user_list.append(user_tuple)

    return user_list

#load clean csv file
user_list = load_users(file)

#set proxy
proxy_name = input('Specify Proxy: ')
if proxy_name == 'smartproxy':
    proxy_file = 'proxy_1.txt'
elif proxy_name == 'socialproxy':
    proxy_file = 'proxy_2.txt'
else:
    quit()

with open(proxy_file, 'r') as f:
    PROXY_USER, PROXY_PASSWORD, HOST, PORT = f.read().splitlines()

proxy = f"http://{PROXY_USER}:{PROXY_PASSWORD}@{HOST}:{PORT}"

#loop through each account and set it up

def login_user(user,password):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    json_file = f'session_{user}.json'
    json_dir = r'C:\Users\danil\PythonFiles\IronStorm\account_sessions'
    json_load = json_dir + '\\' + json_file    
    session = cl.load_settings(json_load)

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(user, password)

            # check if session is valid
            try:
                cl.get_timeline_feed()
                il.bot_log("Session is Valid.")
            except LoginRequired:
                il.bot_log("Session is invalid, need to login via username and password",level=30)

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(user, password)
            login_via_session = True
        except Exception as e:
            il.bot_log("Couldn't login user using session information: %s" % e,level=30)

    if not login_via_session:
        try:
            il.bot_log("Attempting to login via username and password. username: %s" % user)
            if cl.login(user, password):
                login_via_pw = True
        except Exception as e:
            il.bot_log("Couldn't login user using username and password: %s" % e,level=30)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

avatared_user = []
avatared_password= []
avatared_email = []
avatared_email_pass = []
avatared_pfp= []
avatared_tag= []
avatared_privet= []
avatared_name= []
avatared_bio = []
avatared_link = []
avatared_old_user = []

for user, password,email,email_password in user_list:

    try:
        il.bot_log(f'Connecting {user}...')
        cl = Client()
        before_ip = cl._send_public_request("https://api.ipify.org/")
        cl.set_proxy(f"{proxy}")
        after_ip = cl._send_public_request("https://api.ipify.org/")

        if before_ip != after_ip:
            il.bot_log(f"IP before: {before_ip}")
            il.bot_log(f"IP after: {after_ip}")
            il.bot_log("Proxy server is set.")
        else:
            il.bot_log("Failed to establish connection to Proxy",30)
            continue
        #add some kind of iter continue, or wrap it all in try block at the end
        
        login_user(user,password)

        #set profile picture, write caption, random photo upload, follow some people, follow some bots, upload story, set profile to privet, set name, set tag.

        #set pfp
        try:
            cl.account_change_picture(pfp_generator(dir = r'C:\Users\danil\PythonFiles\IronStorm\accounts_pfps\all'))
            avatared_pfp.append(1)
            cl.delay_range = [1,3]
        except Exception:
            avatared_pfp.append(0)
            il.bot_log(f'Failed to set pfp for user {user}',level=30)
            cl.delay_range = [1,3]
        
        #set account to privet
        try:
            cl.account_edit(is_privet=True)
            avatared_privet.append(1)
            cl.delay_range = [1,3]
        except Exception:
            avatared_privet.append(0)
            il.bot_log(f'Failed to set user {user} privet',level=30)
            cl.delay_range = [1,3]
        
        #set full-name
        try:
            random_n = random.randint(0, 10)
            if random_n < 9:
                rand_name = name_generator()
                cl.account_edit(full_name = rand_name)
                avatared_name.append(rand_name)
                cl.delay_range = [1,3]
            else:
                avatared_name.append(0)
                cl.delay_range = [1,3]
        except Exception:
            avatared_name.append(0)
            il.bot_log(f'Failed to set full-name {user}',level=30)
            cl.delay_range = [1,3]

        #set bio
        try:
            random_n = random.randint(0, 10)
            if random_n < 4:
                rand_bio = bio_generator()
                cl.account_edit(biography = rand_bio)
                avatared_bio.append(rand_bio)
                cl.delay_range = [1,3]
            else:
                avatared_bio.append(0)
                cl.delay_range = [1,3]
        except Exception:
            avatared_bio.append(0)
            il.bot_log(f'Failed to set bio {user}',level=30)
            cl.delay_range = [1,3]
        
        #set link
        try:
            random_n = random.randint(0, 10)
            if random_n < 3:
                rand_link = link_generator()
                cl.account_edit(external_url = rand_link)
                avatared_link.append(rand_link)
                cl.delay_range = [1,3]
            else:
                avatared_link.append(0)
                cl.delay_range = [1,3]
        except Exception:
            avatared_link.append(0)
            il.bot_log(f'Failed to set link {user}',level=30)
            cl.delay_range = [1,3]     

        #set tag
        try:
            new_username = tag_generator()
            cl.account_edit(username = new_username)
            il.bot_log(f'username chagnged from {user} to {new_username}')
            avatared_user.append(new_username)
            avatared_password.append(password)
            avatared_email.append(email)
            avatared_email_pass.append(email_password)
            avatared_tag.append(1)
            avatared_old_user.append(user)
        except Exception:
            avatared_user.append(user)
            avatared_password.append(password)
            avatared_tag.append(0)
            avatared_old_user.append(user)     
            il.bot_log(f'Failed to set tag for user {user}',level=30)

        index = user_list.index((user,password))
        progress = round(index/len(user_list)*100,2)
        il.bot_log(f'Progress...{progress}%')
    except Exception as e:
        il.bot_log(f'An Exception occured for {user}, {e}')

il.bot_log(f'Progress...100% done') 

#save new data to file
df = pd.DataFrame()
df['user'] = avatared_user
df['password'] = avatared_password
df['email'] = avatared_email
df['email_passwrod'] = avatared_email_pass
df['name'] = avatared_name
df['tag'] = avatared_tag
df['pfp'] = avatared_pfp
df['privet'] = avatared_privet
df['bio'] = avatared_bio
df['link'] = avatared_link
df['old_user'] = avatared_old_user
df.to_csv("avatared_batch.csv", index=False)   

il.bot_log('Done, avatared_batch.csv created.')
il.bot_log('goodbye')
  


