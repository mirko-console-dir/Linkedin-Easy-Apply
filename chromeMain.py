from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import json

class EasyApplyLinkedin:

    def __init__(self, data):
        """Parameter initialization"""

        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver_path = data['driver_path']
        self.driver = None

    def login_linkedin(self):
        """This function logs into your personal LinkedIn profile"""
     # Initialize the WebDriver with Chrome
        service = ChromeService(self.driver_path)
        self.driver = webdriver.Chrome(service=service)

        # Open a website to test the driver
        url = 'https://www.linkedin.com/login'
        self.driver.get(url)
        time.sleep(3)
        # introduce email and password and hit enter to remove the sospicous activity det on linkedin remove the following
        login_email = self.driver.find_element(By.NAME, 'session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element(By.NAME, 'session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)

    def job_search(self):
        """This function goes to the 'Jobs' section a looks for all the jobs that matches the keywords and location"""
       
        # go to Jobs
        jobs_link = element = self.driver.find_element(By.LINK_TEXT, 'Jobs')
        jobs_link.click()
        # search based on keywords and location and hit enter
        # Click on an input element with class 'jobs-search-box__text-input'
        search_keywords = self.driver.find_element(By.CSS_SELECTOR, ".jobs-search-box__text-input")
        search_keywords.click()
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_keywords.send_keys(Keys.RETURN)

        time.sleep(5)
        # Find an input element with title 'Search by title, skill, or company'
        search_location = self.driver.find_element(By.CSS_SELECTOR, '[aria-label*="City, state, or zip code"]')
        search_location.clear()
        
        search_location.send_keys(self.location)
        button_search =  self.driver.find_element(By.CSS_SELECTOR, '.jobs-search-box__submit-button')
        button_search.click()


    def filter(self):
        """This function filters all the job results by 'Most recent'"""
        #Easy apply 
        button_easy_apply = self.driver.find_element(By.CSS_SELECTOR, '[aria-label*="Easy Apply filter."]')
        button_easy_apply.click()
        time.sleep(1)
        
        # select all filters, click on Easy Apply and apply the filter
        button_filter_text = 'All filters'
        all_filters_button = self.driver.find_element(By.XPATH, f"//button[text()='{button_filter_text}']")
        all_filters_button.click()
        time.sleep(1)

        radio_button_label_for_most_recent = 'Most recent'
        most_recent_radio_button = self.driver.find_element(By.XPATH, f"//span[text()='{radio_button_label_for_most_recent}']")
        most_recent_radio_button.click()
        time.sleep(1)

        apply_filters_button =  self.driver.find_element(By.CSS_SELECTOR, '.search-reusables__secondary-filters-show-results-button')
        apply_filters_button.click()
    
    def find_offers(self):
        """This function finds all the offers through all the pages result of the search and filter"""

        # find the total amount of results of the job offers (if the results are above 25-more than one page-, we will scroll trhough all available pages) if more classes with space in python the space is a dot class1 class2 class3 = class1.class2.class3 ecc..
        total_results = self.driver.find_element_by_class_name("jobs-search-results-list__subtitle")
        #retrive the number of pages to convert the data from the webdriver to a number we can use
        total_results_int = int(total_results.text.split(' ',1)[0].replace(",",""))
        print(total_results_int)

       

    def apply(self):
        """Apply to job offers"""

        #self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(5)
        self.job_search()
        time.sleep(2)
        self.filter()
        time.sleep(2)
        self.find_offers()



if __name__ == '__main__':

    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)
    bot.apply()
        # Keep the WebDriver open until user input
    input("Press Enter to close the WebDriver...")

    # Close the WebDriver
    bot.driver.quit()