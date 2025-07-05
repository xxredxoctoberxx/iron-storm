from datetime import datetime,timedelta
import random
import time

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
Iron Storm Project
Fighting missinformation on Instagram, Supporting Israel, Educating the masses about the conflict
dedicated to the brave men and women of south Israel. 7/10/2023 NEVER FORGET :heart:


Instagram Limits:
1) 60 comments/ 1 hour
2) 80 comment/ 1 day
3) duplicate comment detection
4) 10 accounts from 1 IP
5) human behavior detection 
6) too many re-login's detection

#notes:
1)avarage scroll time for user on ig is around 25-35 minutes.

'''

with open('proxy_1.txt', 'r') as f:
    PROXY_USER, PROXY_PASSWORD = f.read().splitlines()

with open('credentials_1.txt', 'r') as f:
    USERNAME, PASSWORD = f.read().splitlines()

proxy = f"http://{PROXY_USER}:{PROXY_PASSWORD}@il.smartproxy.com:30000"

logger = logging.getLogger()

print(f'Connecting {USERNAME}...')
cl = Client()
before_ip = cl._send_public_request("https://api.ipify.org/")
cl.set_proxy(f"{proxy}")
after_ip = cl._send_public_request("https://api.ipify.org/")

if before_ip != after_ip:
    print(f"IP before: {before_ip}")
    print(f"IP after: {after_ip}")
    print("Proxy server is set.")
else:
    print("Failed to establish connection to Proxy")
    raise ConnectionError

#on first login set-up, dump session data to session.json
#cl.login(USERNAME,PASSWORD)
#cl.dump_settings("session.json") 
#print("json file created.")

def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
                print("Session is Valid.")
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

def random_like(media_id,comments_count):
    '''
    Helper function. mimicing human behavior
    takes in media.id, likes a post randomly
    '''  

    if random.randint(0, 10) > 8:
        cl.media_like(media_id)
        cl.delay_range = [0,10]
        print(f'random like on post #{comments_count}')

hashtag = 'nakba'
comments = ["Google about the arab-jewish war, and get back to me",
            "the strongest people, the stronges army, the victory - Israel!",
            "what the f*** is palestine? never heard of it lol",
            "what is a crime against humanity? HAMAS Dismember a pregnant woman and take the baby out",
            "Imagine you're sleeping in bed and terrorists break into your house and murder your children. This is not your imagination, this is the reality of hundreds of families in Israel. HAMAS is not sorry",
            "Thousands of people went out to celebrate at a party and found themselves in the middle of a massacre, without weapons and without the ability to defend themselves. Hamas celebrated over their bodies",
            "Hamas does not want peace and does not want to protect its citizens. They want death and hatred. Erase Gaza",
            "Gaza = the new amusement park",
            "ONLY ISRAEL",
            "IDF!!!!",
            "CNN news on the day of israeli attacks: Hamas tells Gaza residents to leave their homes after IDF warned civillians to evacuate. and then you say ISRAEL is the one to blame for innocent lives? what a joke.",
            "I stand with IDF!",
            "Israel Defense Forces - the most humanitrian army in the world",
            "United states, europe and the all world stand with Israel!",
            "From land to sea, Israel shall be free !",
            "I LOVE AND SUPPORT ISRAEL!",
            "There was no Palestinian prime minister, no Palestinian government and no Palestinian state It was all Established and controlled by the British army. The Jewish people were in the land of Israel before the British lived in Britain, before Mohammed was born and before jesus christ was born, and that a fact. After all, jesus was born as a jewish boy in The land of Israel, that at the time was called 'Judah' 2023 years ago... later on the roman empire came and sent most of the jewish people who lived in the land, and to erase the identity of the land completely, renamed the land as Syria Palestina, which later on became just PALESTINE 500 years later Mohammad was born, the islam raised and the Islamic empire conquered the territory. They forced some of the jews who still lived there to convert to islam, and that's where most of the arab pepole who lived in Palestine came from. just for the record, in 800 BC there were still 200 Jews who lived on that land. Over the years the numbers had changed, until In 1948 Britain and the world decided to Split the land into two countries-Israel and Palestine- the arabs didn't accept that, and went to a war with Israel, a war which they lost.",
            "USA loves Israel!",
            "peace to the middle east, peace to Israel",
            "May god protect and save Israel",
            "I love you Israel.",
            "Hamas teaches 5-year-old children to hate Jews, they don't want peace, they want blood on their hands",
            "ISRAEL",
            "I AM PROUD TO BE ISRAELI!",
            "NOW ALL THE WORLD KNOWS WHAT WE KNEW ALL ALONG. HAMAS HAS SHOWED THEIR TRUE FACE. LOVE LIVE ISRAEL",
            "#ISTANDWITHISRAEL",
            "#israelforever",
            "#onlyISRAEL",
            "#GODSAVEISRAEL",
            "Who was the first Palestinian Prime minister?",
            "When was Palestian decloration of independence?",
            "WITH ALL MY HEART AND ALL MY BRAIN - ISRAEL!!!!",
            "US STANDS WITH ISRAEL. love from NY!",
            "cant feel no sympathy for you after the horrors of 7/10",
            "supporting terrorists makes me sick to my stomach",
            "violance against innocent civiliance are never the answer",
            "the pictures of burnt babies are sutck in my head. what a brutal, horrible act of unhuman animals. I STAND WITH ISRAEL.",
            "As long as deep in the heart,The soul of a Jew yearns,And forward to the EastTo Zion, an eye looksOur hope will not be lostThe hope of two thousand years,To be a free nation in our land,The land of Zion and Jerusalem.",
            "The only front line against arab agression - The proud and strong jewish nation of Israel",
            "did we really see any freedom fighters on 7/10? i dont think so. all I saw was barabric terrorist animals. I stand with Israel.",
            "Palestinians of Gaza wake up! Israel brings you electricity, water and money. Hamas brings you wars and death. Look who is really to blame.",
            "Gaza = parking lot",
            "if the Arabs lay down their arms there will be no more war, but if Israel lays down its weapons there would be no more Israel.",
            "7/10/2023 is the new 9/11 - stop hamas terrorists!",
            "How can you claim you are the victim after causing the death of 1200 inocent citizens?",
            "God save the state of Israel !!!",
            "TERROR IS NEVER THE ANSWER! you should be ahamed of yourselfs.",
            "If Palestine exists, what is its capital?",
            "Set Gaza on fire like Hamas burned people alive inside their homes",
            "Iran sent ISIS and Al Qaeda to war in Israel",
            "Palestinians of Gaza wake up! Israel gives you the opportunity to escape to a safe place, Egypt closes the door in your face. Your Arab brothers do not want you and do not want to help you",
            "Palestinians of Gaza wake up! Hamas uses you as a human shield, your Arab brothers use you as a pond. Your Arab brothers are abandoning you",
            "Hamas sends 20-year-old terrorists to fight, they don't want peace, they want blood on their hands",
            "I stand with Israel!",
            "Why is 80% palestinians relly on foreign aid?? why they dont build a country? whos real intrest for them to stay rooted as refugees? ask yourself that",
            "Palestenian? your arab brothers care about you? so why did they blocked with cocrete walls the southeren border? what is there for them in you staying rooted as refugee?",
            "ISRAEL HAS THE RIGHT TO DEFEND ITSELF.",
            "You cannot be the VICTIM and the OPRRESOR -at the same time lol. which one actually are you?",
            "did we really see any freedom fighters on 7/10? i dont think so. all I saw was barabric terrorist animals. I stand with Israel.",
            "Palestinians of Gaza wake up! Israel brings you electricity, water and money. Hamas brings you wars and death. Look who is really to blame.",
            "Gaza = parking lot",
            "if the Arabs lay down their arms there will be no more war, but if Israel lays down its weapons there would be no more Israel.",
            "7/10/2023 is the new 9/11 - stop hamas terrorists!",
            "How can you claim you are the victim after causing the death of 1200 inocent citizens?",
            "God save the state of Israel !!!",
            "TERROR IS NEVER THE ANSWER! you should be ahamed of yourselfs.",
            "Justice for Beeri, my hearts with the families of the dead.",
            "Is this the religion of Islam? butchering innocent people...",
            "You support Hamas = you support ISIS and Al Qaeda",
            "People in Israel were sleeping in their beds and were kidnapped into Gaza, children and elderly, then murdered. stop HAMAS",
            "HAMAS launches hundreds of missiles at Israel, they don't want peace they want war. terrorists",
            "NY CITY IS WITH ISRARL!",
            "Justice to Israel",
            "HAMAS = ISIS",
            "You cant be the victim and the opressor. It dose not work like this. JUSTICE TO ISRAEL",
            "My heart with the Israeli Victims",
            "Your war is not again ISRAEL, its against the terrorist organization named HAMAS",
            "I love Israel! Israel will win!",
            "Palestinians of Gaza wake up! Why don't your Arab brothers help you? They sacrifice you, close doors in your face, abandon you! Look who is really to blame",
            "GOD SAVE ISRAEL",
            "Palestinians of Gaza wake up! Egypt, Jordan, Lebanon and Syria do not want to let you enter. They want to let you die in their political game.",
            "I love you israel!!!!!!!",
            "my #heart with #israel",
            "#fromlandtoseaisraelwillbefree",
            "#iloveisrael",
            "#israel",
            "#onlyisreal",
            "Now the all world knows the true face of the Hamas leaders and the palestinian authorities. animals.",
            "Hamas don't even respect the palestinian people smh",
            "Islam is not a religion of peace, sorry."]

login_user()
count_loops = 0
comments_count = 0
time_it = datetime.now()
while count_loops < 2: #3###############

    start = datetime.now()
    finish = start + timedelta(hours=1)
    start_str = start.strftime("%H:%M:%S")
    finish_str = finish.strftime("%H:%M:%S")

    while start_str < finish_str:
        medias = cl.hashtag_medias_reels_v1(hashtag, amount=60)
        for media, comment in zip(medias,comments):
            try:
                cl.media_comment(media.id, comment)
                comments_count += 1
                print(f'comment #{comments_count} succesfuly posted: {comment}')
                random_like(media.id,comments_count)
            except Exception as e:
                print(f'an ERROR ooccured: {e} ')
            cl.delay_range = [10,20]
        count_loops += 1
        print(f'loop #{count_loops} done. waiting...')
        time.sleep(3600)
        #add another loop here and new time object
time_it = round(datetime.now() - time_it, 2)
time_it = ((time_it)/60)/60

print(f'Done. {USERNAME} posted {comments_count} comments in {time_it} hours.')
print(f'Goodbye.')


