"""
Determines if class is open, full, waitlist, or invalid given class number
Features checklist:
[ ] Support online classes
[ ] Support classes with TBD as time
IMPORTANT
This module imports spire_cred, a module
I made that contains username and password to log into spire_cred
You have to create your own module with your own credentials
to make it work.
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import sys
import time
import re
import json
from SpireBackEnd.Lecture import Lecture
from SpireBackEnd.Course import Course
from SpireBackEnd.Discussion import Discussion

courses = []

# gathers all the courses
def get_all_data(class_type, class_num):
    # Create a chrome webdriver
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)

    # Go to the spire webpage
    browser.get('https://www.spire.umass.edu/')

    # Locate text fields
    browser.implicitly_wait(2)
    username = browser.find_element_by_css_selector("#userid")
    password = browser.find_element_by_css_selector("#pwd")

    # Input info in text fields
    username.send_keys("INSERT NAME HERE")
    password.send_keys("INSERT PASSWORD HERE")

    # Press log in
    browser.find_element_by_css_selector('#login > p:nth-child(5) > input[type="submit"]').submit()

    # Give it two more seconds to process, then grab course data
    time.sleep(2)
    get_course_data(browser, class_type, class_num)

# grabs course data
def get_course_data(browser, class_type, class_num):
    browser.implicitly_wait(2)

    # Directly go to this link for searching class
    search_link = 'https://www.spire.umass.edu/' \
                  'psc/heproda/EMPLOYEE/HRMS/c/' \
                  'SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?' \
                  'Page=SSR_CLSRCH_ENTRY&Action=U'

    browser.implicitly_wait(2)
    browser.get(search_link)

    # Click the drop down menu to select the type of class (EG: Computer Science)
    browser.implicitly_wait(2)
    classselect = Select(browser.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SUBJECT$108$"]'))
    classselect.select_by_visible_text(class_type)
    time.sleep(1)


    # find class number field (EG: 250)
    browser.implicitly_wait(2)
    classnumber = (browser.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_CATALOG_NBR$8$"]'))

    #select class number
    classnumber.send_keys(class_num)

    # Submit the search to find the class
    browser.implicitly_wait(2)
    browser.find_element_by_css_selector('#CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()

    num_credits = browser.find_element_by_id('UM_DERIVED_SR_UNITS_RANGE$0').text
    # add course to the array
    new_course = Course(class_type, class_num, num_credits)

    try:
        counter = 0
        while(True):
            # Checks whether or not it is a lecture or lab/discussion in the first element
            string = "DERIVED_CLSRCH_SSR_CLASSNAME_LONG$" + str(counter)
            browser.implicitly_wait(1)
            section_num = browser.find_element_by_id(string).text
            lecture_string = "LEC"
            lab_string = "LAB"
            disc_string = "DIS"
            sem_string = "SEM"
            # If there is an available lecture, add it and its information
            if lecture_string in section_num or sem_string in section_num:
                prof_name = browser.find_element_by_id('MTG_INSTR$' + str(counter)).text
                # get times
                time_string = browser.find_element_by_id("MTG_DAYTIME$" + str(counter)).text
                timevals = list(map(int, re.findall('\d+', time_string)))
                if "PM" in time_string:
                    if "AM" in time_string:
                        hour_end = timevals[2]
                        if (hour_end != 12):
                            hour_end += 12
                        end_time = get_time(hour_end, timevals[3])
                        start_time = get_time(timevals[0], timevals[1])
                    else:
                        hour_end = timevals[2]
                        if (hour_end != 12):
                            hour_end += 12
                        hour_start = timevals[0]
                        if (hour_start != 12):
                            hour_start += 12
                        end_time = get_time(hour_end, timevals[3])
                        start_time = get_time(hour_start, timevals[1])
                else:
                    end_time = get_time(timevals[2], timevals[3])
                    start_time = get_time(timevals[0], timevals[1])

                new_lecture = Lecture(start_time, end_time, prof_name, findProfessor(browser, prof_name))

                counter += 1
                #add corresponding discussions
                try:
                    while(lab_string in browser.find_element_by_id("DERIVED_CLSRCH_SSR_CLASSNAME_LONG$" + str(counter)).text or disc_string in browser.find_element_by_id("DERIVED_CLSRCH_SSR_CLASSNAME_LONG$" + str(counter)).text):
                        time_string = browser.find_element_by_id("MTG_DAYTIME$" + str(counter)).text
                        timevals = list(map(int, re.findall('\d+', time_string)))
                        if "PM" in time_string:
                            if "AM" in time_string:
                                hour_end = timevals[2]
                                if (hour_end != 12):
                                    hour_end += 12
                                end_time = get_time(hour_end, timevals[3])
                                start_time = get_time(timevals[0], timevals[1])
                            else:
                                hour_end = timevals[2]
                                if(hour_end != 12):
                                    hour_end += 12
                                hour_start = timevals[0]
                                if(hour_start != 12):
                                    hour_start += 12
                                end_time = get_time(hour_end, timevals[3])
                                start_time = get_time(hour_start, timevals[1])
                        else:
                            end_time = get_time(timevals[2], timevals[3])
                            start_time = get_time(timevals[0], timevals[1])

                        new_disc = Discussion(start_time, end_time)
                        new_lecture.add_disc(new_disc)
                        counter += 1
                except NoSuchElementException:
                    pass
                new_course.add_lecture(new_lecture)

    except NoSuchElementException:
        if (new_course.size() != 0):
            courses.append(new_course)


    print("course 1 size")
    print(courses[0].size())
    for i in range(0, len(courses)):
        print_course = courses[i]
        for j in range(0, print_course.size()):
            print_lecture = print_course.get_lecture(j)
            print(print_lecture.get_prof())
            print(print_lecture.get_start())
            print(print_lecture.get_rating())
            for k in range(0, print_lecture.size()):
                print_disc = print_lecture.get_disc(k)
                print("disc start time")
                print(print_disc.get_start())
    browser.quit()



def get_time(hour, minute):
    return hour*60 + minute

#find the professor rating
def findProfessor(browser, namePro):

    # For my Windows
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    # Go to RateMyProfessor
    rateMyProfessor = 'http://www.ratemyprofessors.com/'
    browser.get(rateMyProfessor)
    browser.find_element_by_xpath("""//*[@id="cookie_notice"]/a[2]""").click()
    # Clicks on the available text options
    school = browser.find_element_by_xpath("""//*[@id="findProfessorOption"]""").click()

    try:
        schoolName = browser.find_element_by_id('searchProfessorSchool2')
        name = browser.find_element_by_id('searchProfessorName')

        # Input info in text fields
        schoolName.send_keys("University of Massachusetts")
        name.send_keys(namePro)
        browser.implicitly_wait(1)
        element = browser.find_element_by_id("prof-name-btn")
        element.submit()
        browser.implicitly_wait(1)
        #element = browser.find_element_by_xpath("""//*[@id="searchResultsBox"]/div[2]/ul/li/a""")
        #prof_string = element.get_attribute("href")
        #browser.get(prof_string)
        try:
            browser.set_page_load_timeout(2)
            element = browser.find_element_by_xpath("""//*[@id="searchResultsBox"]/div[2]/ul/li/a/span[1]""")
            element.click()
        except TimeoutException:
            pass
        #webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
        browser.implicitly_wait(1)
        element = browser.find_element_by_xpath("""//*[@id="mainContent"]/div[1]/div[3]/div[1]/div/div[1]/div/div/div""")
        quality = element.text
        browser.quit()
        return quality
    except NoSuchElementException:
        browser.quit()
        return None

#find a valid schedule
