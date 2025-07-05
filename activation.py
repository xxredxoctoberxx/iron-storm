import glob
from datetime import datetime,timedelta,date
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Thread

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
set-up bot accounts for Ig users.

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

    user_list = []
    for user_tuple in zip(users,passwords):
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

#definitions
NOW_BOT = 'None'
NOW_TAG = 'None'
today = str(date.today())
comments_counter = [0] 
time_values = [0]
influancers = metadata['influancers']
hashtags_pa = metadata['hashtags_pa']
comments = metadata['comments']
bot_names = metadata['bot_names']

def main():
    '''
    Main defense logic block
    '''
    
    global comments_counter
    global time_values
    global NOW_BOT
    global NOW_TAG
    global user_list

    user_list = user_list * 2

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
        
    def random_like(media_id,comments_count):
        '''
        Helper function. mimicing human behavior
        takes in media.id, likes a post randomly
        '''  

        if random.randint(0, 10) > 6:
            cl.media_like(media_id)
            cl.delay_range = [0,10]
            print(f'random like on post #{comments_count}')

    for user, password in user_list:

        try:
            NOW_BOT = user
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

            #do the action:
            hashtag = hashtags[0]
            NOW_TAG = hashtag
            medias = cl.hashtag_medias_reels_v1(hashtag, amount=10)
            for media in medias:
                try:
                    comment = comments[random.randint(0,len(comments)-1)]
                    cl.media_comment(media.id, comment)
                    comments_counter.append(comments_counter[-1] + 1)
                    print(f'comment #{comments_counter[-1]} succesfuly posted: {comment}')
                    cl.delay_range = [10,20]
                    random_like(media.id,comments_counter[-1])
                except Exception as e:
                    print(f'an ERROR ooccured: {e} ')
                    cl.delay_range = [10,20]
            hashtags = hashtags[1:] + hashtag

        except Exception as e:
            il.bot_log(f'An Exception occured for {user}, {e}')

def comment_graph():
    '''Graphing the impv for the equity.'''

    plt.style.use("dark_background") #dark theme
    fig = plt.figure(f'Iron Storm Defense Bots {today}')
    ax1 = fig.add_subplot(1,1,1)
    ax1.set_title(f'Total bots:{len(user_list)}')
    ax1.set_xlabel(f'Now running: {NOW_BOT} hashtag:{NOW_TAG}')
    ax1.set_ylabel(f'comments = {len(comments_counter)-1}')
    fig.suptitle(f'{today}', fontsize=14)

    def animate(i):
        pullData = open("comcounter.txt","r").read()
        dataArray = pullData.split('\n')
        xar = []
        yar = []
        for eachLine in dataArray:
            if len(eachLine)>1:
                x,y = eachLine.split(',')
                xar.append(int(x))
                yar.append(int(y))

        ax1.clear()
        ax1.set_title(f'Total bots:{len(user_list)}')
        ax1.set_xlabel(f'Now running: {NOW_BOT} hashtag:{NOW_TAG}')
        ax1.set_ylabel(f'comments = {len(comments_counter)-1}')
        ax1.plot(xar,yar)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

def comment_counter():
    '''This part updates the graph'''
    
    t = time_values[-1]
    time_values.append(t+1)
    t = str(t)
    comment = comments_counter[-1]
    comment = round(float(comment)*100)
    comment = str(comment)

    dot = t + "," + comment

    def storedot():

        hs = open("comcounter.txt","a")
        hs.write(dot + "\n")
        hs.close() 
        time.sleep(2)

    storedot()

def reset_comment():
    '''This helper function deletes all data inside impv file.'''

    f = open("comcounter.txt", "w")
    f.close()

#run this
reset_comment()
thread = Thread(target = main)
thread.start()    
comment_graph()