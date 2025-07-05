import glob
from datetime import datetime,timedelta,date
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Thread
import regex as re
import imaplib
import email

from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from instagrapi.exceptions import (
    BadPassword, ReloginAttemptExceeded, ChallengeRequired,
    SelectContactPointRecoveryForm, RecaptchaChallengeForm,
    FeedbackRequired, PleaseWaitFewMinutes, LoginRequired
)
from instagrapi.mixins.challenge import ChallengeChoice
import logging
import requests
from requests.exceptions import HTTPError


from data_generator import *
from info_logger import Info_Logger as il

'''
Training Module
set-up bot accounts for Ig users.

'''

def initialize():
    print('Specify file with accounts data: ')
    all_files = glob.glob(r'C:\Users\danil\PythonFiles\IronStorm\*.csv')
    for csv_file in all_files:
        csv_file = csv_file.replace(r'C:\Users\danil\PythonFiles\IronStorm', '')
        print(csv_file)
    file = input('')
    assertion = input('is it right?: ')
    if assertion == 'yes':
        il.bot_log(f'Initializing {file}...')
        return file
    else:
        quit()

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

def set_proxy():

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

    return proxy

def main():
    '''
    Main logic block for training
    '''

    #get metadata
    influancers = metadata['influancers']
    hashtags_pa = metadata['hashtags_pa']
    comments = metadata['comments']
    bot_names = metadata['bot_names']

    #load accounts, set proxy
    file = initialize()
    user_list = load_users(file) #user list * 2 (?)
    PROXY = set_proxy()

    #main
    for user, password, email_user, email_password in user_list:

        try:
            #connect to proxy
            il.bot_log(f'Connecting {user}...')
            cl = Client()
            before_ip = cl._send_public_request("https://api.ipify.org/")
            cl.set_proxy(f"{PROXY}")
            after_ip = cl._send_public_request("https://api.ipify.org/")

            if before_ip != after_ip:
                il.bot_log(f"IP before: {before_ip}")
                il.bot_log(f"IP after: {after_ip}")
                il.bot_log("Proxy server is set.")
            else:
                il.bot_log("Failed to establish connection to Proxy",30)
                continue
            
            #2 helper functions to handle challenge required error
            def get_code_from_email(username):

                mail = imaplib.IMAP4_SSL('outlook.office365.com')
                mail.login(email_user, email_password)
                mail.select("inbox")
                result, data = mail.search(None, "(UNSEEN)")
                assert result == "OK", "Error1 during get_code_from_email: %s" % result
                ids = data.pop().split()
                for num in reversed(ids):
                    mail.store(num, "+FLAGS", "\\Seen")  # mark as read
                    result, data = mail.fetch(num, "(RFC822)")
                    assert result == "OK", "Error2 during get_code_from_email: %s" % result
                    msg = email.message_from_string(data[0][1].decode())
                    payloads = msg.get_payload()
                    if not isinstance(payloads, list):
                        payloads = [msg]
                    code = None
                    for payload in payloads:
                        body = payload.get_payload(decode=True).decode()
                        if "<div" not in body:
                            continue
                        match = re.search(">([^>]*?({u})[^<]*?)<".format(u=username), body)
                        if not match:
                            continue
                        print("Match from email:", match.group(1))
                        match = re.search(r">(\d{6})<", body)
                        if not match:
                            print('Skip this email, "code" not found')
                            continue
                        code = match.group(1)
                        if code:
                            il.bot_log(f'Authentication code found in mail: {code}')
                            return code
                return False
            
            def challenge_code_handler(username, choice):
                if choice == ChallengeChoice.SMS:
                    return False
                elif choice == ChallengeChoice.EMAIL:
                    return get_code_from_email(username)
                return False

            #helper functions
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
                        cl.challenge_code_handler = challenge_code_handler(user,ChallengeChoice.EMAIL)
                        cl.login(user, password)

                        # check if session is valid
                        try:
                            cl.get_timeline_feed()
                            il.bot_log("Session is Valid.")
                        except LoginRequired:
                            il.bot_log("Session is invalid, need to login via username and password",level=30)
                            cl.login(user,password)
                            json_file = f'session_{user}.json'
                            json_dir = r'C:\Users\danil\PythonFiles\IronStorm\account_sessions'
                            json_dump = json_dir + '\\' + json_file
                            cl.dump_settings(json_dump)
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

            def random_like(media_id):
                '''
                Helper function. mimicing human behavior
                takes in media.id, likes a post randomly
                '''  

                if random.randint(0, 10) > 6:
                    cl.media_like(media_id)
                    cl.delay_range = [3,6]
                    print(f'random like on post')

            def random_follow():
                
                random_n = random.randint(1,3)
                bot_to_infulancer_r = 4
                follow_list = []

                i=0
                while i < random_n:
                    random_bot = bot_names[random.randint(0,len(bot_names)-1)]
                    follow_list.append(random_bot)
                    i+=1
                
                k=0
                while k< random_n*bot_to_infulancer_r:
                    random_influancer = influancers[random.randint(0,len(influancers)-1)]
                    follow_list.append(random_influancer)
                    k+=1

                try:
                    followers = cl.user_followers(cl.user_id)
                except Exception as e:
                    il.bot_log(f'Failed to get followers data, passing...{e}')
                
                try:
                    for username in follow_list:
                        if username not in followers.keys():
                            username_id = cl.user_id_from_username(username)
                            cl.user_follow(username_id)
                            il.bot_log(f'succesfully followed {username}')
                            cl.delay_range = [3,5]
                except Exception as e:
                    il.bot_log(f'Failed to follow {username}')
                    cl.delay_range = [3,5]

            #connect to IG API and do the action - follow,like,comment - randomly.
            try:
                login_user(user,password)
                random_follow()
            except ChallengeRequired:
                cl.challenge_code_handler = challenge_code_handler()

            comment_counter = 0
            while comment_counter < 10:
                hashtag = hashtags_pa[0]
                medias = cl.hashtag_medias_reels_v1(hashtag, amount=10)
                for media in medias:
                    try:
                        comment = comments[random.randint(0,len(comments)-1)]
                        cl.media_comment(media.id, comment)
                        comment_counter+=1
                        print(f'comment #{comment_counter} succesfuly posted: {comment}')
                        cl.delay_range = [10,20]
                        random_like(media.id)
                    except Exception as e:
                        print(f'an ERROR ooccured: {e} ')
                        comment_counter+=10
                        cl.delay_range = [10,20]
                hashtags = hashtags[1:] + hashtag

        except Exception as e:
            il.bot_log(f'An Exception occured for {user}, {e}')

if __name__ == "__main__":
    main()