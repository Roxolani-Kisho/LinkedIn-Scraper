from selenium import webdriver
from client import LIClient
from settings import search_keys
import time

"""
linkedin job scrapper
can be combined with python script to generate cover letters
"""
# initialize Selenium Web Driver
driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/uas/login")
# initialize LinkedIn web client
liclient = LIClient(driver, **search_keys)
liclient.login()
# wait for page load
time.sleep(3)

liclient.keyword  = "Computer science"
liclient.location = "greater seattle area"
liclient.navigate_to_jobs_page()
liclient.enter_search_keys()
liclient.sent_experience_level()
liclient.navigate_search_results()
liclient.driver_quit()
