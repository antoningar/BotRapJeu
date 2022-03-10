import time
import requests

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#import helpers.loggerhelper as loggerhelper

URL_SPOTIFY_DASHBOARD = 'https://developer.spotify.com/dashboard/'
URL_CONSOLE = 'https://developer.spotify.com/console/get-users-currently-playing-track/'

def start_browser():
    options = Options()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    options.add_argument("--headless")
    driver = webdriver.Firefox(
        executable_path='C:\\dev\\bot_rap_jeu\\geckodriver.exe',
        options=options)

    return driver

def click(driver, element):
    ActionChains(driver).click(element).perform()

def check_cookies(driver):
    try:
        cookies_button = driver.find_element_by_id('onetrust-accept-btn-handler')
        click(driver, cookies_button)
    except Exception:
        pass

def get_token(username, password):
    driver = None
    driver = start_browser()
    driver.get(URL_SPOTIFY_DASHBOARD)
    time.sleep(2)
    check_cookies(driver)
    login_button = driver.find_elements_by_xpath("//button[contains(@class, 'btn') and " +
                                            "contains(@class, 'btn-sm') and " +
                                            "contains(@class, 'btn-primary')]")[0]        
    driver.execute_script("window.scrollTo(0, 711)")
    click(driver, login_button)

    time.sleep(4)
    main_window = driver.window_handles[0]
    auth_window = driver.window_handles[1]
    
    driver.switch_to.window(auth_window)
    
    login_username_field = driver.find_element_by_id('login-username')
    login_password_field = driver.find_element_by_id('login-password')
    login_username_field.send_keys(username)
    login_password_field.send_keys(password)
    login_password_field.send_keys(Keys.RETURN)

    driver.switch_to.window(main_window)
    driver.get(URL_CONSOLE)
        
    driver.execute_script("window.scrollTo(0, 675)")
    token_popup_button = driver.find_element_by_xpath("//button[contains(@class, 'btn') and " +
                                                "contains(@class, 'btn-green')]")
    click(driver, token_popup_button)

    time.sleep(2)
    check_cookies(driver)    
    token_button = driver.find_element_by_id('oauthRequestToken')
    print(token_button.click())
    #click(driver, token_button)

    '''
    time.sleep(2)
    auth_button = driver.find_element_by_id('auth-accept')
    click(driver, auth_button)
    '''

    time.sleep(3)
    token_input = driver.find_element_by_id('oauth-input')        
    driver.execute_script("window.scrollTo(0, 500)")
    token = token_input.get_attribute('value')

    return token

def get_current(token):
    spotify_headers = {
        "Authorization": f"Bearer {token}"
    }

    url = 'https://api.spotify.com/v1/me/player/currently-playing'
    r = requests.get(url, headers=spotify_headers)
    print(r.json())

if __name__ == "__main__":
    token = get_token("antoningaranto@gmail.com", "KVv)6wpQaK8Bmtwz")
    get_current(token)
