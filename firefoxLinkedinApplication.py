import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import json
import math


class ApplyLinkedin:
    #with open('config.json', 'r') as config_file:
    #    config_data = json.load(config_file)
    #forbidden_words = config_data.get('forbidden_words', [])

    def __init__(self, data):
        """Parameter initialization"""
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        self.driver_path = data['driver_path']
        self.driver = None
        self.forbidden_words = data.get('forbidden_words', [])

    def configure_logging(self):
        # Create a logger for geckodriver
        logger = logging.getLogger('webdriver')
        logger.setLevel(logging.DEBUG)  # Set the desired log level

        # Create separate log handlers for different log levels
        trace_handler = logging.FileHandler('geckodriver_trace.log')
        debug_handler = logging.FileHandler('geckodriver_debug.log')
        info_handler = logging.FileHandler('geckodriver_info.log')
        warn_handler = logging.FileHandler('geckodriver_warn.log')
        error_handler = logging.FileHandler('geckodriver_error.log')
        fatal_handler = logging.FileHandler('geckodriver_fatal.log')

        # Set the log level for each handler
        trace_handler.setLevel(logging.DEBUG)  # Use DEBUG level for trace
        debug_handler.setLevel(logging.DEBUG)
        info_handler.setLevel(logging.INFO)
        warn_handler.setLevel(logging.WARN)
        error_handler.setLevel(logging.ERROR)
        fatal_handler.setLevel(logging.FATAL)

        # Create a log formatter and set it for each handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        trace_handler.setFormatter(formatter)
        debug_handler.setFormatter(formatter)
        info_handler.setFormatter(formatter)
        warn_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        fatal_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(trace_handler)
        logger.addHandler(debug_handler)
        logger.addHandler(info_handler)
        logger.addHandler(warn_handler)
        logger.addHandler(error_handler)
        logger.addHandler(fatal_handler)

    def login_linkedin(self):
        """This function logs into your personal LinkedIn profile"""
        self.configure_logging()

        options = FirefoxOptions()
        
        # Initialize the FirefoxService with log_output
        service = FirefoxService(executable_path=self.driver_path, options=options)
        self.driver = webdriver.Firefox(service=service)

        # Open the LinkedIn login page
        url = 'https://www.linkedin.com/login'
        self.driver.get(url)
        time.sleep(3)
        
        #wait = WebDriverWait(self.driver, 20)

        # Enter email and password
        login_email = self.driver.find_element(By.NAME, 'session_key')
        login_email.clear()
        login_email.send_keys(self.email)

        login_pass = self.driver.find_element(By.NAME, 'session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)

        login_pass.send_keys(Keys.RETURN)
        time.sleep(10)

    def job_search(self):
        """This function goes to the 'Jobs' section and looks for jobs that match the keywords and location"""

        # Wait for the 'Jobs' link to be clickable
        wait = WebDriverWait(self.driver, 10)
        jobs_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Jobs')))
        jobs_link.click()
        time.sleep(6)

        # Enter keywords and location
        search_keywords = self.driver.find_element(By.CSS_SELECTOR, ".jobs-search-box__text-input")
        search_keywords.click()
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        time.sleep(1)

        search_location = self.driver.find_element(By.CSS_SELECTOR, '[aria-label*="City, state, or zip code"]')
        search_location.clear()
        search_location.send_keys(self.location)
        time.sleep(1)
        search_location.send_keys(Keys.RETURN)

    def filter(self):
        """This function filters job results by 'Most recent' and other filters as needed"""

        wait = WebDriverWait(self.driver, 10)

        # Wait for the 'Easy Apply' filter button to be clickable
        button_easy_apply = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label*="Easy Apply filter."]')))
        button_easy_apply.click()
        time.sleep(3)

        # Click 'All filters'
        button_filter_text = 'All filters'
        all_filters_button = self.driver.find_element(By.XPATH, f"//button[text()='{button_filter_text}']")
        all_filters_button.click()
        time.sleep(2)

        # Select 'Most recent'
        radio_button_label_for_most_recent = 'Most recent'
        most_recent_radio_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{radio_button_label_for_most_recent}']")))
        most_recent_radio_button.click()
        time.sleep(2)

        # Apply filters
        apply_filters_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-reusables__secondary-filters-show-results-button')))
        apply_filters_button.click()

    def go_throw_results(self):
        # Find the li element with the desired class
        li_element = self.driver.find_element(By.CSS_SELECTOR, 'li.scaffold-layout__list-item')

        # Navigate to the parent ul of this li element
        ul_element = li_element.find_element(By.XPATH, './ancestor::ul')
        # Locate the list items (individual elements) within the <ul>
        results = ul_element.find_elements(By.TAG_NAME, 'li')
        counter = 0
        # Iterate over the individual list items, is dynamic because annoying LinkedIn tries to block bots
        for index, result in enumerate(results):
            try:
                # Dynamically re-locate the result element before performing actions
                result = results[index]

                # Perform hover action (only once)
                hover = ActionChains(self.driver).move_to_element(result)
                hover.perform()
                time.sleep(1)

                # Increment the counter
                counter += 1

                # Locate titles within the current result
                titles = result.find_elements(By.CLASS_NAME, 'job-card-list__title--link')

                # Check if the counter is a multiple of 2, and if so, scroll
                if counter % 2 == 0:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", result)

                for title in titles:
                    try:
                        # Find the hidden span and check for forbidden words
                        hidden_span = title.find_element(By.CLASS_NAME, 'visually-hidden')
                        span_text = hidden_span.text

                        if not any(word in span_text for word in self.forbidden_words):
                            self.submit_apply(title)
                    except StaleElementReferenceException:
                        print(f"Stale element in title processing. Skipping: {title.text}")
                        continue  # Skip this title and move to the next one
            except StaleElementReferenceException:
                print(f"Stale element encountered for result {index}. Skipping...")
                continue  # Skip this result and move to the next one

    def find_offers(self):
        """This function finds and processes job offers"""

        wait = WebDriverWait(self.driver, 10)

        # Find the total number of job results
        total_results = self.driver.find_element(By.CLASS_NAME, "jobs-search-results-list__subtitle")
        total_results_int = int(total_results.text.split(' ', 1)[0].replace(",", ""))
        print(total_results_int)
        time.sleep(1)
        
        # Retrive all the results that we get from first page, get results
        # Every 25 jobs the page change 25 the last part of the url is gonna tell in wich page we are 
        current_page = self.driver.current_url
        
        self.go_throw_results()
        
        # if there is more than one page, find the pages and apply to the results of each page
        if total_results_int > 25:
        # go throw all pages and job offers and apply
            try:
                #  iterates through numbers starting from 25 and increasing by 25 in each iteration until it reaches total_results_int (429)
                for page_number in range(25, total_results_int, 25):
                    self.driver.get(current_page+"&start="+str(page_number))
                    time.sleep(5)
                    self.go_throw_results()
            except NoSuchElementException:
                self.close_session()
        else: 
            self.close_session()

    def discard_application(self):
        """This function handles discarding the application."""
        wait = WebDriverWait(self.driver, 3)
        try:
            discard = self.driver.find_element(By.CSS_SELECTOR, f'button[aria-label*="Dismiss"]')
            discard.send_keys(Keys.RETURN)
            time.sleep(1)
            discard_confirm = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']")))
            discard_confirm.send_keys(Keys.RETURN)
            time.sleep(1)
        except TimeoutException:
            # Handle TimeoutException
            print("A TimeoutException occurred.")
            pass
        except NoSuchElementException:
            # Handle NoSuchElementException
            print("A NoSuchElementException occurred.")
            pass
        except StaleElementReferenceException:
            print("A StaleElementReferenceException occurred. Retrying...")
            # Retry locating and interacting with the elements
            self.discard_application()

    def close_modal_post_apply(self):
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.jobs-loader')))
            button_close_modal = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[aria-label*="Dismiss"]')))
            #button_close_modal.click()
            self.driver.execute_script("arguments[0].click();", button_close_modal)              
            print("Modal dismissed successfully.")
        except NoSuchElementException:
            print('No modal post application')
            pass

    def try_to_submit_application(self):
        wait = WebDriverWait(self.driver, 3)
        try:
            # Loop to handle multiple "Next" buttons
            while True:
                try:
                    # Check for the "Next" button
                    button_next = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label*="Continue to next step"]'))
                    )
                    button_next.send_keys(Keys.RETURN)
                    time.sleep(1)  # Optional, can adjust or remove based on application responsiveness
                except TimeoutException:
                    # Break the loop if no "Next" button is found
                    print("No more 'Next' buttons found.")
                    break
            # If "Submit application" button is not found, look for and click the "Review your application" button
            button_review = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[aria-label*="Review your application"]')))
            button_review.send_keys(Keys.RETURN)
            time.sleep(1)

            button_submit_apply = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[aria-label*="Submit application"]')))
            button_submit_apply.send_keys(Keys.RETURN)
            time.sleep(1)    

            self.close_modal_post_apply()

        except NoSuchElementException:
            print('No direct application found. Proceeding to discard...')
            self.discard_application()
        except TimeoutException:
            # Handle TimeoutException
            print('No direct application (timeout) found. Proceeding to discard...')
            self.discard_application()

    def submit_apply(self,job_add):
        """This function submits the application for the job add found"""
        #Retrive the name of the job offer
        wait = WebDriverWait(self.driver, 10)
        print('you are aplying to the position of: ', job_add.text )
        job_add.click()
        time.sleep(2)
        try:
            # Locate and click the "Easy Apply" button
            in_apply = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'jobs-apply-button')))
            in_apply.click()
            print("Clicked the Easy Apply button successfully.")
            time.sleep(1)
             # Check if the "jobs-apply-button" element is still displayed
            try:
                modal_to_scroll = self.driver.find_element(By.CLASS_NAME, 'jobs-easy-apply-modal')
                modal_to_scroll.send_keys(Keys.PAGE_UP)
                self.try_to_submit_application()
            except NoSuchElementException:
                print('Element reference is stale after clicking. Proceeding to submit application.')
                # Locate and click the "Easy Apply" button
                in_apply = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'jobs-apply-button')))
                in_apply.click()
                print("Clicked the Easy Apply button successfully.")
                time.sleep(1)
                modal_to_scroll = self.driver.find_element(By.CLASS_NAME, 'jobs-easy-apply-modal')
                modal_to_scroll.send_keys(Keys.PAGE_UP)
                self.try_to_submit_application()
        except TimeoutException:
            print('Easy Apply button not found. You already applied or encountered an issue.')
            pass

        time.sleep(1)

    def close_session(self):
        """This function closes the actual session"""
        
        print('End of the session, see you later!')
        self.driver.close()
    
    def apply(self):
        """Apply to job offers"""
        #to maximaze the window and not have problem such as is out of bounds of viewport 

        self.login_linkedin()
        time.sleep(5)
        
        self.driver.maximize_window()
        self.job_search()
        time.sleep(5)
        self.filter()
        time.sleep(5)
        self.find_offers()
        time.sleep(5)
        self.close_session()

if __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = ApplyLinkedin(data)
    bot.apply()

    # Keep the WebDriver open until user input
    input("Press Enter to close the WebDriver...")

    # Close the WebDriver
    bot.driver.quit()
