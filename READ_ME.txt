IronStorm Project README

How to start:

1. get a .csv with account data in the format account,password,email,passswrod
for example 'test.csv', and .txt with proxy information in the format user,
password,host,port. for example'proxy.txt'

2. run 'set_session.py' -> 'test.csv_clean'
creates and save .json of session for accounts that logged-in succesfuly

3. run 'avataring.py' -> 'avatared_batch.csv'
creates a .csv with profile info, and new human-friendly user tag.

4. run 'set_session.py' -> 'avatared_batch.csv_clean'
workable avatared bots with sessions set for new user tag.