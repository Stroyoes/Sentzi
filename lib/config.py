# for handle configs and environment files
import os
from dotenv import load_dotenv

load_dotenv()
DEV_EMAIL_ID = os.getenv('DEV_EMAIL_ID') # get the developer email id
DEV_PASS = os.getenv('DEV_PASS') # get the password 



