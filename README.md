# LinkedIn Scraper

**NOTE:** This script is to be used for educational purposes only.

## Description
This Python script allows you to scrape your LinkedIn connection profiles and send connection requests to multiple users. The script uses LinkedIn's web interface to automate the process, and it can work in both automatic and manual login modes.

**Important Note:** The script relies on XPath expressions to identify elements on the LinkedIn page. These XPaths may change over time as LinkedIn updates its page structure. You may need to update the XPaths accordingly to ensure the script continues to work.

## Features
- Scrapes Your LinkedIn connection profiles and their contact info.
- Sends connection requests automatically.
- Logs actions for debugging.
- Configurable login options (automatic or manual).
- Adjustable time delays to mimic human interactions.

## Prerequisites
Make sure you have the following before running the script:
- Python 3.11 installed on your machine.
- A LinkedIn account for scraping.
- LinkedIn profile IDs to scrape.
- Necessary libraries installed via `pip install -r requirements.txt`.

## Installation
1. Clone the repository:
        git clone "https://github.com/Gatecoders/linkedin_scrapper.git"

2. Navigate to the project directory:
        cd linkedin_scrapper

3. Create a .env file with the following variables:
        EMAIL='Your LinkedIn Email ID'
        PASSWORD='LinkedIn Password'
        LOGIN_TYPE=0  # 0 for automatic login, 1 for manual login
        BASE_URL='https://www.linkedin.com'
        SCROLL_PAUSE_TIME=1.0
        WAIT_TIME=10
        DELAY_BETWEEN_ACTIONS=5
        LOG_FILE='Path to your log file'

4. Install the required dependencies:
        pip install -r requirements.txt

## Usage
1. Open the scraper.py file and add the profile IDs of the people you wish to connect with. You can get the profile ID from the URL of their LinkedIn profile (e.g., https://www.linkedin.com/in/testid/ where testid is the profile ID).
2. Run the scraper script:
        python scrapper.py

## Log file
The script generates a log file for debugging purposes. Make sure to specify the path to the log file in your .env file under LOG_FILE.