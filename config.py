import CREDENTIALS
import os

connectionDSN = """"""

HOME_PATH = os.path.expanduser("~").lower()
if 'mybal' in HOME_PATH:
    connectionDSN = CREDENTIALS.DSN_MYB
elif 'mihri' in HOME_PATH:
    connectionDSN = CREDENTIALS.DSN_MIHRI
elif 'application' in HOME_PATH:
    connectionDSN = CREDENTIALS.DSN_DEPLOYMENT
else:
    connectionDSN = CREDENTIALS.DSN_OTHER
APIKEY = CREDENTIALS.APIKEY