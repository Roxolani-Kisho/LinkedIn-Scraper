from __future__ import print_function
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrape import *
import datetime
import json
import time



def write_line_to_file(filename, data):
    """
    output the current job title, company, job id, then write
    the scraped data to file
    """
    if data is not None:
        job_title = data[0]["job_title"]
        company   = data[0]["company"]
        
        message = u"Writing data to file for job listing:"
        message += "\n  {}  {};\n"
        try:
            print(message.format(job_title, str(company)))
        except Exception as e:
            print("Encountered a unicode encode error while attempting to print " \
                        "the job post information;  job id {}".format(job_id))
        with open(filename, "a") as f:
            f.write(json.dumps(data) + '\n')


def robust_wait_for_clickable_element(driver, delay, selector):
    """ wait for css selector to load """
    clickable = False
    attempts = 1
    try:
        driver.find_element_by_css_selector(selector)
        #driver.find_element_by_xpath(selector)
    except Exception as e:
        print("  Selector not found: {}".format(selector))
    else:
        while not clickable:
            try:
                # wait for job post link to load
                wait_for_clickable_element(driver, delay, selector)
            except Exception as e:
                print("  {}".format(e))
                attempts += 1
                if attempts % 100 == 0:
                    driver.refresh()
                if attempts > 10**3: 
                    print("  \nrobust_wait_for_clickable_element failed " \
                                    "after too many attempts\n")
                    break
                pass
            else:
                clickable = True

def robust_click(driver, delay, selector):
    """
    use a while-looop to click an element. For stubborn links
    and general unexpected browser errors.
    """
    try:
        driver.find_element_by_css_selector(selector).click()
    except Exception as e:
        print("  The job post link was likely hidden,\n    An " \
                "error was encountered while attempting to click link" \
                "\n    {}".format(e))
        attempts = 1
        clicked = False
        while not clicked:
            try:
                driver.find_element_by_xpath(selector).click()
            except Exception as e:
                pass
            else:
                clicked = True
                print("  Successfully navigated to job post page "\
                            "after {} attempts".format(attempts))
            finally:
                attempts += 1
                if attempts % 100 == 0:
                    print("--------------  refreshing page")
                    driver.refresh()
                    time.sleep(5)
                if attempts > 10**3:
                    print(selector)
                    print("  robust_click method failed after too many attempts")
                    break 


def wait_for_clickable_element(driver, delay, selector):
    """use WebDriverWait to wait for an element to become clickable"""
    obj = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, selector)
            )
        )
    return obj  

def wait_for_clickable_element_css(driver, delay, selector):
    """use WebDriverWait to wait for an element to become clickable"""
    obj = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, selector)
            )
        )
    return obj  


def link_is_present(driver, delay, selector, index, results_page):
    """
    verify that the link selector is present and print the search 
    details to console. This method is particularly useful for catching
    the last link on the last page of search results
    """

    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, selector)
            )
        )
        y=driver.find_element_by_css_selector(selector)

        driver.execute_script("arguments[0].scrollIntoView();",y)

        print("**************************************************")
        print("\nScraping data for result  {}" \
                "  on results page  {} \n".format(index, results_page))
    except Exception as e:
        print(e)
        if index < 25:
            print("\nWas not able to wait for job_selector to load. Search " \
                    "results may have been exhausted.")
            return True
        else:
            return False
    else:
        return True 


def search_suggestion_box_is_present(driver, selector, index, results_page):
    """
    check results page for the search suggestion box,
    as this causes some errors in navigate search results.
    """
    
    return (index == 0) and (results_page == 1)
    

def next_results_page(driver, delay,index):
    """
    navigate to the next page of search results. If an error is encountered
    then the process ends or new search criteria are entered as the current 
    search results may have been exhausted.
    """
    try:
        # wait for the next page button to load
        print("  Moving to the next page of search results... \n" \
                "  If search results are exhausted, will wait {} seconds " \
                "then either execute new search or quit".format(delay))
        
        # navigate to next page
        hold = driver.find_element_by_xpath("//li[@data-test-pagination-page-btn=" + str(index)+"]")
        hold.click()
    except Exception as e:
        print ("\nFailed to click next page link; Search results " \
                                "may have been exhausted\n{}".format(e))
        raise ValueError("Next page link not detected; search results exhausted")
    else:


        # wait for the first job post button to load
        time.sleep(2)


def go_to_specific_results_page(driver, delay, results_page):
    """
    go to a specific results page in case of an error, can restart 
    the webdriver where the error occurred.
    """
    if results_page < 2:
        return
    current_page = 1
    for i in range(results_page):
        current_page += 1
        time.sleep(5)
        try:
            next_results_page(driver, delay)
            print("\n**************************************************")
            print("\n\n\nNavigating to results page {}" \
                  "\n\n\n".format(current_page))
        except ValueError:
            print("**************************************************")
            print("\n\n\n\n\nSearch results exhausted\n\n\n\n\n")

def print_num_search_results(driver, keyword, location):
    """print the number of search results to console"""
    # scroll to top of page so first result is in view
    #driver.execute_script("window.scrollTo(0, 0);")
    selector = "div.results-context div strong"

    try:
        num_results = driver.find_element_by_css_selector(selector).text
    except Exception as e:
        num_results = ''
    print("**************************************************")
    print("\n\n\n\n\nSearching  {}  results for  '{}'  jobs in  '{}' " \
            "\n\n\n\n\n".format(num_results, keyword, location))

def extract_transform_load(driver, delay, selector, date, 
                           keyword, location, filename):
    """
    using the next job posting selector on a given results page, wait for
    the link to become clickable, then navigate to it. Wait for the job 
    posting page to load, then scrape the page and write the data to file.
    Finally, go back to the search results page
    """
    # wait for the job post to load then navigate to it
    try:
        wait_for_clickable_element(driver, delay, selector)
        robust_click(driver, delay, selector)
    except Exception as e:
        print("error navigating to job post page")
        print(e)
        # scrape page and prepare to write the data to file
    data = scrape_page(driver, keyword=keyword, location=location, dt=date,selector = selector)

        # write data to file
    write_line_to_file(filename, data)

    if not ("Search | LinkedIn" in driver.title):
        driver.execute_script("window.history.go(-1)")


class LIClient(object):
    def __init__(self, driver, **kwargs):
        self.driver         =  driver
        self.username       =  kwargs["username"]
        self.password       =  kwargs["password"]
        self.filename       =  kwargs["filename"]
        self.date_range     =  kwargs["date_range"]
        self.search_radius  =  kwargs["search_radius"]
        self.sort_by        =  kwargs["sort_by"]
        self.salary_range   =  kwargs["salary_range"]
        self.results_page   = 1 

    def driver_quit(self):
        self.driver.quit()

    def login(self):
        """login to linkedin then wait 3 seconds for page to load"""
        # Enter login credentials
        
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable(
                (By.ID, "username")
            )
        )
        elem = self.driver.find_element_by_id("username")
        elem.send_keys(self.username)

        elem = self.driver.find_element_by_id("password")
        elem.send_keys(self.password)

        # Enter credentials with Keys.RETURN
        elem.send_keys(Keys.RETURN)
        # Wait a few seconds for the page to load
        time.sleep(2)

    def navigate_to_jobs_page(self):
        """
        navigate to the 'Jobs' page since it is a convenient page to 
        enter a custom job search.
        """
        # Click the Jobs search page
        jobs_link_clickable = False
        attempts = 1
        url = "https://www.linkedin.com/jobs/?trk=nav_responsive_sub_nav_jobs"
        while not jobs_link_clickable:
            try:
                self.driver.get(url)
            except Exception as e:
                attempts += 1
                if attempts > 10**3: 
                    print("  jobs page not detected")
                    break
                pass
            else:
                print("**************************************************")
                print ("\n\n\nSuccessfully navigated to jobs search page\n\n\n")
                jobs_link_clickable = True
    def sent_experience_level(self):
        """
        set search to only look for entry level postions using linkedin features

        """
        driver = self.driver

        elem = driver.find_element_by_xpath("//button[@aria-label='Experience Level filter. Clicking this button displays all Experience Level filter options.']")
        elem.click()
        elem = driver.find_element_by_xpath("//label[@for='experience-2']") # entry level postions set here
        elem.click()
        elem = driver.find_element_by_xpath("//button[@class='jobs-search-box__submit-button artdeco-button artdeco-button--inverse artdeco-button--2 artdeco-button--secondary']")
        elem.click()

    def enter_search_keys(self):
        """
        execute the job search by entering job and location information.
        The location is pre-filled with text, so we must clear it before
        entering our search.
        """
        driver = self.driver
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located(
                (By.ID, "jobs-search-box-keyword-id-ember17")
            )
        )
        # Enter search criteria
        time.sleep(1)
        elem = driver.find_element_by_id("jobs-search-box-keyword-id-ember17")
        elem.send_keys(self.keyword)
        # clear the text in the location box then enter location
        elem = driver.find_element_by_id("jobs-search-box-location-id-ember17").clear()
        elem = driver.find_element_by_id("jobs-search-box-location-id-ember17")
        elem.send_keys(self.location)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)


    def navigate_search_results(self):
        """
        scrape postings for all pages in search results
        """
        driver = self.driver
        search_results_exhausted = False
        results_page = self.results_page
        delay = 60
        date = get_date_time()
        # css elements to view job pages
        list_element_tag = "div[class*=viewport-tracking-"
        print_num_search_results(driver, self.keyword, self.location)
        # go to a specific results page number if one is specified
        go_to_specific_results_page(driver, delay, results_page)
        results_page = results_page if results_page > 1 else 1
        index = 1;
        

        while not search_results_exhausted:
            index+=1
            for i in range(1,26):  # 25 results per page
                
                job_selector = list_element_tag + str(i-1) +"]"
                #temp = driver.find_element_by_css_selector(job_selector)
                if search_suggestion_box_is_present(driver,
                                                    job_selector, i, results_page):

                    continue
                    # wait for the selector for the next job posting to load.
                    # if on last results page, then throw exception as job_selector
                    # will not be detected on the page


                if not link_is_present(driver, delay,
                                       job_selector, i, results_page):
                    continue
                robust_wait_for_clickable_element(driver, delay, job_selector)
                extract_transform_load(driver,
                                       delay,
                                       job_selector,
                                       date,
                                       self.keyword,
                                       self.location,
                                       self.filename)

            try:
                next_results_page(driver, delay,index)
                print("\n**************************************************")
                print("\n\n\nNavigating to results page  {}" \
                      "\n\n\n".format(results_page + 1))
            except ValueError:
                search_results_exhausted = True
                print("**************************************************")
                print("\n\n\n\n\nSearch results exhausted\n\n\n\n\n")
            else:
                results_page += 1
