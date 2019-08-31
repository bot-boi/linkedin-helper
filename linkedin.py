from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from constants import user1

driver = None

def is_logged_in():
    try:
        driver.find_element_by_id("profile-nav-item") # profile navigation button in menu bar   
        return True
    except NoSuchElementException:
        return False

def login(user, pw): # logs into linkedin
    driver.get("https://www.linkedin.com/login")
    if not is_logged_in():
        driver.find_element_by_id("username").send_keys(user)
        pw_field = driver.find_element_by_id("password")
        pw_field.send_keys(pw)
        pw_field.send_keys(Keys.RETURN)

def wait_user(): # waits for user to press enter
    input("Press Enter to continue...")

def open_sales_nav():
    driver.get("https://www.linkedin.com/sales/")

def open_sales_search():
    driver.get("https://www.linkedin.com/sales/search/people?viewAllFilters=true")

def get_links(): # gets a list of links to sales nav profiles
    elems = driver.find_elements_by_xpath("//*[@href]")
    elems = [elem for elem in elems if "/sales/people" in elem.get_attribute("href")]

def init():
    global driver
    driver = webdriver.Chrome()
    login(user1.email, user1.pw)
    open_sales_nav()
