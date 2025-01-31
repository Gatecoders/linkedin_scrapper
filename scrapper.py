import os
import time
from dotenv import load_dotenv
import linkedin_script

load_dotenv()

USER = os.getenv('EMAIL')
PASSWORD = os.getenv(f"PASSWORD")
LOGIN_TYPE = int(os.getenv(f"LOGIN_TYPE", 0))

scrapper = linkedin_script.LINKEDIN(user=USER, password=PASSWORD, login_type=LOGIN_TYPE)
time.sleep(5)
# json_response=scrapper.fetch_connection_profile()
# print('printing the dataframe')
# print(json_response)
# time.sleep(5)
connections_list = ['ayushkasara']
scrapper.add_connection(connections_list)

scrapper.quit()