import time

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import cred
import locators

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 2,
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 2,
    "profile.default_content_setting_values.notifications": 2
})

driver = webdriver.Chrome(options=opt, executable_path="chromedriver")
driver.maximize_window()


def gotosite(url):
    driver.get(url)
    driver.implicitly_wait(10)


def login(username, password):
    driver.find_element_by_xpath(locators.email).send_keys(username)
    driver.find_element_by_xpath(locators.password).send_keys(password)
    driver.find_element_by_xpath(locators.login_button).click()


def searchforgroup(keyword):
    driver.find_element_by_xpath(locators.groups).click()
    driver.implicitly_wait(10)
    driver.find_element_by_xpath(locators.search_groups).send_keys(keyword, Keys.ENTER)
    # driver.find_element_by_xpath(locators.see_all_groups).click()
    driver.find_element_by_link_text('See all').click()

def post(status):
    driver.implicitly_wait(100)
    for i in range(1, 100):
        print(i)
        try:
            driver.find_element_by_xpath(locators.group_dynamic_start+str(i)+locators.group_dynamic_end).click()
            try:
                driver.find_element_by_xpath(locators.create_public_post).click()
                driver.find_element_by_xpath(locators.public_post_text).send_keys('this is a automated post !')
                if status:
                    driver.find_element_by_xpath(locators.post_button).click()
                    time.sleep(10)
                else:
                    driver.find_element_by_xpath(locators.close_posting).click()
            except selenium.common.exceptions.NoSuchElementException:
                print('group '+str(i)+'message: you have to join this group before post!')
        except selenium.common.exceptions.NoSuchElementException:
            print('group selection failed!!')
            break

        driver.implicitly_wait(10)
        driver.back()


if __name__ == "__main__":
    gotosite("https://www.facebook.com/")
    login(cred.username, cred.password)
    searchforgroup("car")
    post(False)
