import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Constants
SCROLL_PAUSE_TIME = 1.0
WAIT_TIME = 3  # Timeout for explicit waits
DELAY_BETWEEN_ACTIONS = 2  # Delay between actions to mimic human behavior

# User credentials
username = "glucosecho482@gmail.com"
password = "Perceptiviti@1234"

# Connection list
connection_list = ['pramod-singh-b284b7a7']

# Configure Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, WAIT_TIME)

# Login to LinkedIn
try:
    driver.get("https://www.linkedin.com")
    try:
        email_sign_in_button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Sign in with email')]")))
        email_sign_in_button.click()
        print("Clicked on 'Sign in with email'.")
    except TimeoutException:
        print("Sign in with email button not found, proceeding with manual login.")
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    username_field.send_keys(username)
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_field.send_keys(password)
    sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    sign_in_button.click()
    print("Successfully logged in.")
except TimeoutException:
    print("Login failed. Check credentials or LinkedIn page structure.")
    driver.quit()
    exit()

# Visit each profile and send a connection request
for connection in connection_list:
    try:
        profile_url = f"https://www.linkedin.com/in/{connection}/"
        driver.get(profile_url)
        print(f"Visiting profile: {profile_url}")

        # Wait for the "Connect" button and click it
        try:
            connect_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button'))
            )
            connect_button.click()
            print(f"Clicked 'Connect' button for {connection}.")
        except TimeoutException:
            print("No 'Connect' button found. Skipping to next profile.")
            continue

        # Handle the "Add a note" pop-up
        try:
            add_note_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[3]/button[1]'))
            )
            add_note_button.click()
            note_field = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[3]/div[1]/textarea')))
            note_field.send_keys("Hi, I'd like to connect with you on LinkedIn!")
            send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[4]/button[2]")))
            send_button.click()
            print("Connection request sent with a note.")
        except TimeoutException:
            try:
                send_without_note = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[3]/button[2]')))
            except TimeoutException:
                print('Unable to send connection request.')                    

        # Delay between requests
        time.sleep(DELAY_BETWEEN_ACTIONS)

    except TimeoutException:
        print(f"Error processing profile: {connection}. Check screenshot for details.")
        driver.save_screenshot(f"screenshot_{connection}.png")
    except NoSuchElementException:
        print(f"Could not find the 'Connect' button for {connection}.")

# Close WebDriver
driver.quit()