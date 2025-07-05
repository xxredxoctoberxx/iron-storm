from datetime import datetime,timedelta
import pandas as pd
import glob

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

'''
Set Sessions
Run on a csv file with raw user data
Coutputs clean user,password data file and loggin sessions

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
    print(f'Initializing {file}...')
else:
    quit()

#laod users
def load_users(file:str):
    ''' 
    Load user data and passwrods from file
    '''

    f = file
    df = pd.read_csv(f'{f}')
    print("Passing users...")
    users = df[df.columns[0]].values.tolist()
    passwords = df[df.columns[1]].values.tolist()
    emails = df[df.columns[2]].values.tolist()
    email_passwords = df[df.columns[3]].values.tolist()

    user_list = []
    for user_tuple in zip(users,passwords,emails,email_passwords):
        user_list.append(user_tuple)

    return user_list

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

#on first login set-up, dump session data to session.json
def create_session(user_list):
    
    i=0
    users=[]
    passwords=[]
    emails = []
    email_passwords = []
    for user, password, email, email_password in user_list:

        try:
            print(f'Connecting {user} to proxy...')
            cl = Client()
            cl.set_proxy(f"{proxy}")
            print("Proxy server is set.")
            cl.login(user,password)
            json_file = f'session_{user}.json'
            json_dir = r'C:\Users\danil\PythonFiles\IronStorm\account_sessions'
            json_dump = json_dir + '\\' + json_file
            cl.dump_settings(json_dump)
            print(f"json file created for user {user}.")
            users.append(user)
            passwords.append(password)
            emails.append(email)
            email_passwords.append(email_password)
            i+=1
        except Exception as e:
            print(f"Failed to create session for {user}, {e} passing...")

    print(f'Results: created {i} sessions out of {len(user_list)}. success rate: {round(i/len(user_list)*100,2)}% ')
    df = pd.DataFrame()
    df['users'] = users
    df['passwords'] = passwords
    df['emails'] = emails
    df['email_passwords'] = email_passwords
    df.to_csv(f"clean_sessions.csv", header=False, index=False)
    print(f'clean file created.')

create_session(user_list)