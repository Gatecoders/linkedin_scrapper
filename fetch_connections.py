from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from progress.bar import IncrementalBar
import time, csv

# Constants
SCROLL_PAUSE_TIME = 1.0


# User credentials (replace with actual credentials)
username = "glucosecho482@gmail.com"
password = "Perceptiviti@1234"

# Configure Chrome Options for headless mode
options = Options()
# options.headless = True  # Ensure that headless mode is enabled
# options.add_argument("--disable-gpu")  # Disable GPU (required for some platforms)
# options.add_argument("--no-sandbox")  # Disable sandboxing (required for some platforms)
# options.add_argument("--start-maximized")  # Start maximized (not really needed for headless)
# options.add_argument("--disable-dev-shm-usage")  # Solve some issues with resource allocation
# options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging if needed
# options.add_argument("--window-size=1920x1080")  # Set window size for headless mode (optional)

# chrome_options.add_experimental_option("detach", True)
options.add_argument("--headless")  # Enable headless mode
options.add_argument("--disable-gpu")  # Disable GPU for headless mode
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("--window-size=1920,1080")

# Initialize WebDriver with headless mode
driver = webdriver.Chrome(options=options)

# Wait object for explicit waits
wait = WebDriverWait(driver, 20)  # Increased wait time

# Login to LinkedIn
driver.get("https://www.linkedin.com")

try:
    # Check if the "Sign in with email" button is present and click it
    try:
        email_sign_in_button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Sign in with email')]")))
        email_sign_in_button.click()
        print("Clicked on 'Sign in with email'.")
    except TimeoutException:
        print("Sign in with email button not found, proceeding with manual login.")
    
    # Wait for and enter username (standard LinkedIn login form)
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    username_field.send_keys(username)

    # Wait for and enter password (updated ID)
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))  # Updated ID
    password_field.send_keys(password)

    # Wait for and click the 'Sign in' button
    sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn__primary--large from__button--floating' and @aria-label='Sign in']")))
    sign_in_button.click()

except TimeoutException as e:
    print("Error: Timeout while waiting for elements", e)
    driver.save_screenshot("screenshot.png")
    driver.quit()

# Navigate to the Connections page
driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections")

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
# Scroll down to load all connections
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract connection links
cards = driver.find_elements(By.CLASS_NAME, 'mn-connection-card__link')
links = [card.get_attribute('href') for card in cards]
# Write connection details to a CSV file
with open("connections.csv", "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['Name', 'Headline', 'Location', 'Link', 'Website', 'Phone', 'Address', 'E-mail', 'Twitter'])
    writer.writeheader()

    bar = IncrementalBar('Fetching Connections', max=len(links))

    for link in links:
        driver.get(link + 'overlay/contact-info')

        # Extract contact information
        def extract_element_text(by, value, attr=None):
            try:
                element = driver.find_element(by, value)
                # Return the attribute value if 'attr' is specified, else return the text
                return element.get_attribute(attr) if attr else element.text
            except NoSuchElementException:
                return "NA"


        phone = extract_element_text(By.XPATH, "//ul[@class='list-style-none']/li/span[@class='t-14 t-black t-normal']")
        email = extract_element_text(By.XPATH, "//a[contains(@href, 'mailto:')]", "href").replace("mailto:", "")
        name = extract_element_text(By.ID, 'pv-contact-info')
        headline = extract_element_text(By.CLASS_NAME, 'text-body-medium')
        location = extract_element_text(By.CLASS_NAME, 'text-body-small')

        writer.writerow({
            'Name': name,
            'Headline': headline,
            'Location': location,
            'Link': link,
            'Phone': phone,
            'E-mail': email
        })
        bar.next()
        time.sleep(0.2)

    bar.finish()

# Close the driver
driver.quit()