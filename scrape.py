from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import json
import time
import urllib.request, urllib.error, urllib.parse
import re
from selenium.common.exceptions import NoSuchElementException

"""
useing selenium scrape job application
"""

def job_id(driver):
    """
    grabs the meta linkedin unique job id from the url
    e.g. url = https://www.linkedin.com/jobs/view/161251904
    returns https://www.linkedin.com/jobs/view/161251904
    """
    elem = driver.find_element_by_xpath("//a[@data-control-name='two_pane_job_title']")
    url = elem.get_attribute('href')
    url = url[:45]

    return url



def job_data(driver):
    """
    scrapes the posting info for title, company, post age, location,
    and page views. Have seen many strange errors surrounding the
    job tite, company, location data, so have used many try-except
    statements to avoid potential errors with unicode, etc.
    """
    job_info = {
        "job_title": "//h2[@class='jobs-details-top-card__job-title t-20 t-black t-normal']",
        "employment_type": "//p[@class='jobs-box__body js-formatted-employment-status-body']",
        "industry": "//li[@class='jobs-box__list-item jobs-description-details__list-item']",
        "experience": "//p[@class='jobs-box__body js-formatted-exp-body']",
        "job_function": "//li[@class='jobs-box__list-item jobs-description-details__list-item']",
        "description": "//div[@class='jobs-box__html-content jobs-description-content__text t-14 t-normal']",
        "base_salary": "//p[@class='salary-main-rail__data-amount t-24 t-black t-normal']",
        "company": "",
        "location": "//a[@class='jobs-details-top-card__exact-location t-black--light link-without-visited-state']",
        "temploc": "//div[@class='jobs-commute-module__company-location ml2 t-14 t-black t-normal']",
        "contact info": "//p[@class='jobs-poster__name t-14 t-black t-bold mb0']",
        "contact title": ""
    }

    for key, selector in job_info.items():
        try:
            job_info[key] = driver.find_element_by_xpath(selector).text
        except NoSuchElementException:
            if key == "company":

                hold = driver.find_element_by_css_selector("a[class~=jobs-details-top-card__company-url]")
                job_info[key] = hold.text

            else:
                job_info[key] = ""
            pass

    if job_info["location"] == "":
        job_info["location"] = driver.find_element_by_xpath("//span[@class='jobs-details-top-card__bullet']").text
    if job_info["temploc"] != "":
        job_info["location"] = job_info["temploc"]
    try:
        html = driver.execute_script("return document.body.outerHTML;")
        html2 = driver.execute_script("return document.body.innerHTML;")
        t = driver.find_element_by_css_selector("div[class*='jobs-commute-module__company-location'")
        job_info["location"] = driver.find_element_by_css_selector("div[class*='jobs-commute-module__company-location'").text
        h=0
    except NoSuchElementException:
        pass
    job_info["location"] = job_info["location"].replace(",", "-")
    return job_info


def num_applicants(driver):
    """
    Grabs number of applicants from either the header of the 
    applicants-insights div, or within the applicants-table in the same 
    div element. Returns empty string if data is not available.
    """

    num_applicant_selectors = [
        "//span[@class='jobs-details-job-summary__text--ellipsis']"
    ]
    for selector in num_applicant_selectors:
        try:
            num_applicants = driver.find_element_by_xpath(selector).text
        except Exception as e:
            pass
        else:
            return ''.join(list(filter(lambda c: c.isdigit(), num_applicants)))
    return ''


def nameRound2(driver, job_info,selector):
    """
    look for the name of a hiring manager not specfic
    """
    driver.find_element_by_css_selector("a[class~=jobs-details-top-card__company-url]").click()
    waittoclick(driver, 60, "a[data-control-name=page_member_main_nav_people_tab]").click()
    hold = waittoclick(driver, 60, "input[id=people-search-keywords]")
    hold.send_keys("talent")
    hold.send_keys(Keys.RETURN)
    time.sleep(2)
    hold = re.findall(r'\d+', driver.find_element_by_css_selector("span[class='t-20 t-black']").text)

    if int(hold[0]) < 50:
        try:
            hold = driver.find_element_by_css_selector(
                "div[class='org-people-profile-card__profile-title t-black lt-line-clamp lt-line-clamp--single-line ember-view']")
            job_info["contact info"] = hold.text

        except Exception as e:
            pass
    driver.back()
    driver.back()
    driver.back()
    while True:
        scroll =300
        try:
            y = driver.find_element_by_css_selector(selector)
            break
        except:
            driver.execute_script("window.scrollTo(0,"+str(scroll)+")")
            scroll=scroll + 300
    driver.execute_script("arguments[0].scrollIntoView();", y)
    return job_info


def waittoclick(driver, delay, css):
    hold = WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, css)
        )
    )
    return hold


def peak(driver, job_info,selector):
    """
    check job descrpiton for keywords
    """
    content = job_info['description']
    if "Machine Learning" not in job_info["job_title"]:
        # bachelor postions
        if ("achelor" not in content and "B.S." not in content and "BS" not in content) and (
                "Phd" in content or "MS" in content or "Ph.D" in content or "asters" in content):
            return None
        # no professional experience
        if "years of professional experience" in content and "0 years of professional experience" not in content:
            return None

    if (job_info["job_title"].find("\\") != -1):
        job_info["job_title"] = job_info["job_title"][:job_info["job_title"].find("\\")]

    job_info["job_title"] = job_info["job_title"][0].upper() + job_info["job_title"][1:].lower()
    
    job_info = nameRound2(driver, job_info,selector)

    # get email address
    #email = "@"
    #if content.find('@') != -1:
    #    index = content.find('@')
    #    while content[index - 1] != " ":
    #        email = content[index - 1] + email
    #        index = index - 1
    #    index = content.find('@')
    #    while content[index + 1] != " " or content[index + 1] != "\\":
    #        email = email + content[index + 1]
    #        index = index + 1
    #    job_info["contact info"] = email

    # get salary
    #if content.find('$') != -1:
    #    salary = ""
    #    index = content.find('$')
    #    while content[index + 1] != " " or content[index + 1] != "K":
    #        salary = salary + content[index + 1]
    #        index = index + 1
    #    job_info["contact info"] = salary

    # get lanugage
    language = []
    if content.find("Java") != -1:
        language.append("Java")
    if content.find("Python") != -1:
        language.append("Python")
    if content.find("C++") != -1:
        language.append("C++")
    if content.find("C#") != -1:
        language.append("C#")
    if content.find("SQL") != -1:
        language.append("SQL")

    # if content.find("JavaScript") != -1:
    #    language.append("JavaScript")
    # if content.find("CSS") != -1:
    #    language.append("CSS")
    # if content.find("HTML") != -1:
    #    language.append("HTML")

    # get tools
    tools = []
    if content.find("TensorFlow") != -1:
        tools.append("TensorFlow")
    if content.find("API") != -1 or content.find("REST") != -1:
        tools.append("API")
    if content.find("machine learning") != -1:
        tools.append("Machine Learning")
    if content.find("NLP")!=-1:
        tools.append("NLP")
    if content.find("React") != -1 or content.find("JavaScript") != -1 or content.find("HTML") != -1 or content.find(
            "CSS") != -1:
        tools.append("React")
    if content.find("Git") or content.find("Version control") != -1:
        tools.append("Git")
    if content.find("multi-threading") != -1:
        tools.append("Multi-Threading")
    if content.find("communication skills") != -1:
        tools.append("Communication Skills")
    if content.find("Andriod") != -1:
        tools.append("Andriod")

    coverLetter = {
        "Language": language,
        "Tools-": tools,
    }
    return coverLetter


def scrape_page(driver, **kwargs):
    """
    scrapes single job page after the driver loads a new job posting.
    Returns data as a dictionary
    """
    # wait ~1 second for elements to be dynamically rendered
    time.sleep(1.2)
    start = time.time()

    applicant_info = {
        "num_applicants": num_applicants(driver),
    }
    job_info = {
        "job_info": job_id(driver),

    }
    temp2 = job_data(driver)
    job_info.update(temp2)
    job_info.update(applicant_info)
    skills = peak(driver, job_info,kwargs["selector"])
    if skills is None:
        return None
    job_info["description"] = ""
    data = [

        job_info,
        skills,

    ]
    print("scraped page in  {}  seconds\n".format(time.time() - start))

    return data
