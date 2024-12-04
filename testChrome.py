from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By  # Import By
from selenium.webdriver.common.keys import Keys
import time

import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # You can adjust the logging level

class EasyApplyLinkedin:

    def __init__(self, data):
        # Parameter initialization
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver_path = data['driver_path']
        self.driver = None

    def test_driver(self):
        try:
            # Initialize the WebDriver with Chrome
            service = ChromeService(self.driver_path)
            self.driver = webdriver.Chrome(service=service)

            # Open a website to test the driver
            url = 'https://www.google.com'
            self.driver.get(url)
            text_area = self.driver.find_element(By.ID, 'APjFqb')
            text_area.clear()
            text_area.send_keys('mirko saponaro full stack developer')
            
        
            text_area.send_keys(Keys.RETURN)
            time.sleep(5) 
            # Specify the text you want to find
            text_to_find_for_h3_element = 'Mirko Saponaro | Fullstack Developer'

            # Use XPath to find the h3 element with the specific text
            h3_element = self.driver.find_element(By.XPATH, f"//h3[text()='{text_to_find_for_h3_element}']")

            h3_element.click()


        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)

    # Run the test
    bot.test_driver()

    # Keep the WebDriver open until user input
    input("Press Enter to close the WebDriver...")

    # Close the WebDriver
    bot.driver.quit()
    # Close the WebDriver
    #bot.close()
