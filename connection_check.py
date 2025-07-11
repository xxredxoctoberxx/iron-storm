import requests

#check Internet connection
def internet_connection():
    try:
        response = requests.get("https://nataliliser.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False    
    
if internet_connection():
    print("The Internet is connected.")
else:
    print("The Internet is not connected.")

#check IP
response = requests.get("https://ipinfo.io/json")
print(response.text)
print('done')

#Instagram log-in function
def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """
    
    def json_helper():

        try:
            session = cl.load_settings("session.json")
            return True, session
        except Exception:
            session = None
            return False, session
    
    session_status, session = json_helper()
    login_via_session = False
    login_via_pw = False

    if session_status:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
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
            logger.info(f"Attempting to login via username and password. username: {USERNAME}")
            response = cl.login(USERNAME, PASSWORD)
            print(response)
            login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")
