import os
from dotenv import load_dotenv
import time
import json
from progress.bar import IncrementalBar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging

load_dotenv('/Users/parivat/Desktop/scripts/linkedin_scrapper/.env')

BASE_URL = os.getenv(f"BASE_URL")
SCROLL_PAUSE_TIME = float(os.getenv(f"SCROLL_PAUSE_TIME", 1.0))
WAIT_TIME = int(os.getenv(f"WAIT_TIME", 10))  # Convert to int
DELAY_BETWEEN_ACTIONS = int(os.getenv(f"DELAY_BETWEEN_ACTIONS", 5))
LOG_FILE = os.getenv(f"LOG_FILE")

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

log_dir = os.path.dirname(LOG_FILE)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler(LOG_FILE, mode='a')  # Output to file
    ]
)
logger = logging.getLogger()



class LINKEDIN(object):
    def __init__(self, user, password, login_type):
        self.username = user
        self.password = password
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, WAIT_TIME)
        self.login_wait = WebDriverWait(self.driver, 300)
        self.login(login_type)


    def quit(self):
            logger.info("Closing the browser.")
            self.driver.quit()


    def premimum_popup(self):
        try:
            # Wait for the pop-up modal to appear
            premium_popup = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "artdeco-modal--layer-default"))
            )
            if premium_popup:
                try:
                    # Find the close button inside the modal using its ID
                    close_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'artdeco-modal__dismiss')]")
                    close_button.click()
                    print("Premium pop-up closed.")
                    return "Popup closed"
                except NoSuchElementException:
                    print("Close button not found, pop-up may have a different structure.")
                    return "Button not found"
        except TimeoutException:
            print("No Premium pop-up detected.")
            return "No pop-up detected"


    def login_pincode(self):
        try:
            login_code = input("Please enter the login code: ")
            pin_input = self.driver.find_element(By.ID, "input__phone_verification_pin")
            pin_input.clear()  # Clear any existing value in the field
            pin_input.send_keys(login_code)  # Enter the provided login code
            submit_button = self.driver.find_element(By.ID, "two-step-submit-button")
            submit_button.click()
        except NoSuchElementException:
            logger.error("Login code input field not found.")


    def automatic_login(self):
        try:
            self.driver.get(BASE_URL)
            try:
                email_sign_in_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Sign in with email')]")))
                email_sign_in_button.click()
                logger.info("Clicked on 'Sign in with email'.")
            except TimeoutException:
                logger.warning("Sign in with email button not found, proceeding with manual login.")
            username_field = self.wait.until(EC.presence_of_element_located((By.ID, 'username')))
            username_field.send_keys(self.username)
            password_field = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
            password_field.send_keys(self.password)
            sign_in_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            sign_in_button.click()
            try:
                form_element = self.driver.find_element(By.ID, "two-step-challenge")
                if form_element:
                    logger.info("Two-factor authentication required. Please complete the login process.")
                    self.login_pincode()
                    logger.info("Login code submitted. Proceeding with login.")
            except NoSuchElementException:
                logger.info("No two-factor authentication found. Proceeding with login.")
            logger.info("Successfully logged in.")
        except TimeoutException:
            logger.error("Login failed. Check credentials or LinkedIn page structure.")
            self.driver.quit()
            exit()


    def manual_login(self):
        try:
            self.driver.get(BASE_URL)
            logger.info("Please log in manually. Waiting for you to complete the login process.")
            try:
                self.login_wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='global-nav-search']"))
                )
                logger.info("Login successful. Proceeding with the script...")
            except TimeoutException:
                logger.error("Login process timed out. Please ensure you log in within the given time.")
                self.driver.quit()
                exit()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            self.driver.quit()
            exit()


    def add_note(self, connection):
        try:
            add_note_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[3]/button[1]'))
            )
            add_note_button.click()
            note_field = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[3]/div[1]/textarea')))
            note_field.send_keys("Hi, I'd like to connect with you on LinkedIn!")
            send_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[4]/button[2]")))
            send_button.click()
            logger.info("Connection request sent with a note.")
        except Exception as e:
            logger.error('Failed to add note, trying without note.')
            response = self.premimum_popup()
            try:
                connect_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button'))
                )
                connect_button.click()
                logger.info(f"Clicked 'Connect' button for {connection}.")
                send_without_note = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[3]/button[2]')))
                send_without_note.click()
            except TimeoutException:
                logger.error('Unable to send connection request.')


    def send_message(self, connection):
        message = input('Please provide the message you want to send.')
        default_message = "Hi, I'd like to connect with you on LinkedIn!"
        if message is None:
            message = default_message
        try:
            message_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="ember541"]'))
                        )
            message_button.click()
            response = self.premimum_popup()
            if response == "Popup closed" or "Button not found":
                logger.info(f"Unable to send message to connection {connection}") 
        except TimeoutException:
            logger.error(f"Unable to send message to connection {connection}")


    def login(self, login_type):
        logger.info(f"Logging in as {self.username}...")
        if login_type == 0:
            self.automatic_login()
        else:
            self.manual_login()


    def add_connection(self, connections_list):
        for connection in connections_list:
            try:
                profile_url = f"{BASE_URL}/in/{connection}/"
                self.driver.get(profile_url)
                logger.info(f"Visiting profile: {profile_url}")
                # Wait for the "Connect" button and click it
                try:
                    connect_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button'))
                    )
                    connect_button.click()
                    logger.info(f"Clicked 'Connect' button for {connection}.")
                except Exception as e:
                    logger.warning("No 'Connect' button found. Searcing in more options.")
                    try:
                        more_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button'))
                        )
                        more_button.click()
                        logger.info("Clicked 'More' button to see more options.")
                        connect_button = self.wait.unitl(
                            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div'))
                        )
                        connect_button.click()
                        logger.info(f"Clicked 'Connect' button for {connection}.")
                    except Exception as e:
                        logger.error(f"No connection button found. Skipping to next profile")
                        continue
                    continue
                self.add_note(connection) # Handle the "Add a note" pop-up
                self.send_message(connection)  # Trying to send message to the connection.      
                time.sleep(DELAY_BETWEEN_ACTIONS)  # Delay between requests
            except TimeoutException:
                logger.error(f"Error processing profile: {connection}.")
                # self.driver.save_screenshot(f"screenshot_{connection}.png")


    def fetch_connection_profile(self):
        try:
            connection_url = f"{BASE_URL}/mynetwork/invite-connect/connections"
            self.driver.get(connection_url)
            logger.info(f"Visiting Connections Page: {connection_url}")
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            cards = self.driver.find_elements(By.CLASS_NAME, 'mn-connection-card__link')
            links = [card.get_attribute('href') for card in cards]
            bar = IncrementalBar('Fetching Connections', max=len(links))
            contacts_list = []
            for link in links:
                self.driver.get(link + 'overlay/contact-info')
                # Extract contact information
                def extract_element_text(by, value, attr=None):
                    try:
                        element = self.driver.find_element(by, value)
                        # Return the attribute value if 'attr' is specified, else return the text
                        return element.get_attribute(attr) if attr else element.text
                    except NoSuchElementException:
                        return "NA"
                contact_info = {
                    'phone' : extract_element_text(By.XPATH, "//ul[@class='list-style-none']/li/span[@class='t-14 t-black t-normal']"),
                    'email' : extract_element_text(By.XPATH, "//a[contains(@href, 'mailto:')]", "href").replace("mailto:", ""),
                    'name' : extract_element_text(By.ID, 'pv-contact-info'),
                    'headline' : extract_element_text(By.CLASS_NAME, 'text-body-medium'),
                    'location' : extract_element_text(By.CLASS_NAME, 'text-body-small')
                }
                contacts_list.append(contact_info)
                bar.next()
                time.sleep(0.2)
            bar.finish()
            response = {
                "status": 200,
                "data": contacts_list
            }
            return json.dumps(response,indent=4)
        except TimeoutException:
            logger.error(f"Error fetching connection profile.")
            response = {
                "status": 200,
                "data": ''
            }
            return json.dumps(response, indent=4)
            # self.driver.save_screenshot(f"screenshot_{connection}.png")