import os
import time
import random
from dotenv import load_dotenv
import linkedin_script

load_dotenv()

USER = os.getenv('EMAIL')
PASSWORD = os.getenv(f"PASSWORD")
LOGIN_TYPE = int(os.getenv(f"LOGIN_TYPE", 0))

scrapper = linkedin_script.LINKEDIN(user=USER, password=PASSWORD, login_type=LOGIN_TYPE)

time.sleep(random.uniform(5,10))
json_response=scrapper.fetch_connection_profile()

time.sleep(random.uniform(5,10))
connections_list = ['provide the list for making connections']
scrapper.add_connection(connections_list)

scrapper.quit()