from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from pynput.keyboard import Key, Controller
# import pdfkit # https://wkhtmltopdf.org/downloads.html for windows installer, sudo apt install wkhtmltopdf for linux

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

def scroll_once():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scroll_to_bottom():
    SCROLL_PAUSE_TIME = 1 #seconds
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height

def open_sales_nav():
    driver.get("https://www.linkedin.com/sales/")

def open_sales_search():
    driver.get("https://www.linkedin.com/sales/search/people?viewAllFilters=true")

def get_links_on_page(): # gets a list of links to sales nav profiles on a given page
    elems = []
    for n in range(2):
       elems += driver.find_elements_by_xpath("//*[@href]")
       scroll_once()
       time.sleep(3)

    links = [elem.get_attribute("href") for elem in elems] # convert elems to string
    links = [link for link in links if "/sales/people" in link] # filter links to profiles
    links = set(links) # remove any duplicates
    return links

def next_page(): # goto next page in sales nav search
    btn =  driver.find_element_by_xpath("//button[@class='search-results__pagination-next-button']");
    if btn.is_enabled():
        btn.click()
        time.sleep(3)
        return True
    else:
        return False

def get_all_links(links): # gets all links in a sales nav search (recursive! wow cool!)
    links += get_links_on_page()
    if next_page():
        get_all_links(links)

def nav_to_linkedin(profile_url): # opens nav profile and jumps to regular linkedin profile, returns linkedin profile URL
    driver.get(profile_url)     # TODO: modify tags on sales nav profile
    dropdown_menu = driver.find_element_by_xpath("//artdeco-dropdown-trigger[@role='button' and @class='button-round-tertiary-medium-muted block ml1 ember-view']")
    dropdown_menu.click()
    time.sleep(1) # this shouldnt be a static wait
    open_linkedin = driver.find_element_by_xpath("//artdeco-dropdown-item[@data-control-name='view_linkedin']")
    open_linkedin.click()
    driver.close() # close the sales nav tab
    driver.switch_to_window(driver.window_handles[0]) # switch to the tab that just opened, not sure if done auto cus only tab left
    return driver.current_url

def navs_to_linkedins(links): # convert a bunch of nav profile links to linkedin profile links
    return [nav_to_linkedin(link) for link in links]

# print using chrome print dialogue
# window must be focused for this to work
# assumes you are using print to pdf
def print_dialog(waitManualFocus = False):
    # def focus_chrome_win
    # def focus_chrome_linux
    def expand_seemore_tags(): # TODO: finish dis. click on all the see more buttons so we get all the bs ppl have written
        elems = driver.find_elements_by_xpath("//a[@href='#' and @class='lt-line-clamp__more']")

    if waitManualFocus:
        print("you've got 5 seconds to focus chrome ok homie?")
        time.sleep(5)

    keyboard = Controller()
    keyboard.press(Key.ctrl_l)
    keyboard.press('p')
    keyboard.release(Key.ctrl_l)
    keyboard.release('p')
    time.sleep(2) # wait for dialogue to open
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(5) # wait for download dialogue to open
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(2)

def print_profiles(links):
    waitManualFocus = True
    for link in links:
        if not driver.current_url == link:
            driver.get(link)
        print_dialog(waitManualFocus)
        if waitManualFocus: # first print needs manual focus until i automate it
            waitManualFocus = False

def init():
    global driver
    driver = webdriver.Chrome()
    login(user1.email, user1.pw)
    open_sales_search()

init()
