'''
This file establishes the basic scraper class. 
Scrapers save essential information from online job listings to a Google Sheets database.
'''
import re
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from database_interaction import upload_during_scrape
from selenium.webdriver.common.keys import Keys


class Scraper(object):
    def __init__(self, url_to_scrape:str, page_results_xpath:str, content_xpath:str, 
                jobtitle_html:str,company_html:str, location_html:str, posted_html:str,
                body_html:str, salary_html:str, page_turn_xpath:str, result_count:str):
        # Several xpaths are required to properly configure a scraper. See scraper_instances.py for two successful examples.
        self.url_to_scrape = url_to_scrape # Cannot be a landing page; needs to be a search results page for a job type.
        self.page_results_xpath = page_results_xpath # Refers to the element containing total number of search results, e.g. '250 results found'.
        self.content_xpath = content_xpath # Clickable search results page link to a job listing. 
        self.jobtitle_html = jobtitle_html
        self.company_html = company_html
        self.location_html = location_html
        self.posted_html = posted_html
        self.body_html = body_html
        self.salary_html = salary_html
        self.page_turn_xpath = page_turn_xpath # Points to a clickable page-turn button, often found at the bottom of the search results page.
        self.result_count = result_count # Refers to the element containing number of search results being currently displayed.
    
    # Download driver and open a Chrome window to the desired webpage.
    def _configure_driver(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.url_to_scrape)
        return driver
    
    # Scroll page to desired element and place cursor on top of it.
    def _scroll_to_element(self, driver:webdriver, element:str):
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

    # Calculate number of results per page and total pages.
    def _find_total_page_results(self, driver:webdriver):
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        result_numbers = driver.find_element_by_xpath(self.page_results_xpath)
        res_list = re.split('-| ', result_numbers.text.replace('Showing\n','').replace(',',''))
        cleaned_res_list = [int(i) for i in res_list if i.isdigit()]
        results_per_page = len(driver.find_elements_by_xpath(self.result_count))
        total_pages = round(max(cleaned_res_list) / results_per_page)
        return [results_per_page, total_pages]
    
    # Swats away various banners and other impediments. The 'element' needs to be a clickable xpath.
    def _element_swat(self, driver:webdriver, element:str):
        if element == None:
            pass
        else:
            try:
                swat_me = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, element)))
                self._scroll_to_element(driver=driver, element=swat_me)
                swat_me.click()
                swat_me.click()
                sleep(1)
            except WebDriverException:
                print('Unable to click specified element to swat.')
            except NoSuchElementException:
                print('One or more specified elements to swat could not be found. Please check the xpath.')

    # Retrieves all desired information from a job listing.
    def _get_data(self, driver:webdriver):
        jobdetails = []
        elements_to_search = [self.jobtitle_html, self.company_html, self.location_html, self.posted_html, self.body_html, self.salary_html]
        for element in elements_to_search:
            try:
                element_to_append_raw = driver.find_element_by_xpath(element)
                element_to_append_clean = element_to_append_raw.get_attribute('innerHTML')
                element_to_append_parsed = BeautifulSoup(element_to_append_clean, 'html5lib').text
                jobdetails.append(element_to_append_parsed.replace('"', "'")
                                                          .replace('Posted by: ', '')
                                                          .replace('Posted:', ''))
            except NoSuchElementException:
                jobdetails.append('NA')
                pass
        return jobdetails

    # Scrapes all results and pages.
    def run(self, element_to_swat:str=None, upload:bool=False):
        self.upload = upload
        t = 1.5 # Regulates scraping speed in sleep functions.
        driver = self._configure_driver()
        link = 1 # Determines which link to click, where n is the nth link.
        tabs = self._find_total_page_results(driver)[0] # Number of results on the page.
        pages = self._find_total_page_results(driver)[1] # Number of pages.
        while pages >= 1:
            try:
                while tabs >= 1:
                    try:
                        self._element_swat(driver=driver, element=element_to_swat)      
                        job = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, self.content_xpath.format(link))))
                        self._scroll_to_element(driver=driver, element=job)
                        sleep(t)
                        job.click()
                        sleep(t)
                        jobdetails = self._get_data(driver=driver)
                        if self.upload == True:
                            upload_during_scrape(jobdetails)
                            print(f'{jobdetails[0]} at {jobdetails[1]} uploaded.')
                        else:
                            print(f'{jobdetails[0]} at {jobdetails[1]} found.')  
                        tabs -= 1
                        link += 1
                        driver.back()
                    except TimeoutException:
                        print('Timeout exception caught during result-finding.')
                        try:
                            self._get_data(driver=driver)
                        finally:
                            tabs -= 1
                            link += 1
                            continue
                    except NoSuchElementException:
                        print('NoSuchElement exception caught during result-finding.')
                        try:
                            self._get_data(driver=driver)
                        finally:
                            tabs -= 1
                            link += 1
                            continue
            finally:
                link = 1
                tabs = self._find_total_page_results(driver)[0]
                try:
                    self._element_swat(driver=driver, element=element_to_swat)
                    sleep(t)      
                    pagecheck = WebDriverWait(driver, 10).until(ec.presence_of_element_located((
                        By.XPATH, self.page_turn_xpath)))
                    self._scroll_to_element(driver=driver, element=pagecheck)
                except TimeoutException:
                    print('Timeout exception occurred during page-turn')
                    pages = 0
                    driver.quit()
                    print('Scrape aborted.')
                except NoSuchElementException:
                    print('NoSuchElement exception caught during page-turn.')
                    pages = 0
                    driver.quit()
                    print('Scrape aborted.')
                pagecheck.click()
                pages -= 1
                sleep(t)
        driver.quit()
        print('Scraping complete.')
