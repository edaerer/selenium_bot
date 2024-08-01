from selenium import webdriver, common
import selenium.webdriver.common.by as by
import time
from info import version, chromedriver, chrome, username, password

def getChromeBrowser(version, path_to_chromedriver, path_to_chrome):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = path_to_chrome.format(version)
    service_options = webdriver.ChromeService(executable_path=path_to_chromedriver.format(version))
    driver = webdriver.Chrome(options=chrome_options, service=service_options)
    return driver

class Github:
    def __init__(self, username, password):
        self.browser = getChromeBrowser(version, chromedriver, chrome)
        self.username = username
        self.password = password
        self.followers = []
    
    # will not work if user has 2FA
    def signIn(self):
        self.browser.get("https://github.com/login")
        self.browser.find_element(by.By.ID, "login_field").send_keys(self.username)
        self.browser.find_element(by.By.ID, "password").send_keys(self.password)
        self.browser.find_element(by.By.XPATH, "//*[@id='login']/div[4]/form/div/input[13]").click()

    def getFollowers(self):
        self.browser.get(f"https://github.com/{self.username}?page=1&tab=followers")
        elems = self.browser.find_elements(by.By.CSS_SELECTOR, ".d-table.table-fixed")
        for elem in elems:
            self.followers.append(elem.find_element(by.By.CLASS_NAME, 'Link--secondary').text)

        while True:
            try:
                next_button = self.browser.find_element(by.By.XPATH, "//a[@rel='nofollow' and contains(text(), 'Next')]")
                if next_button:
                    next_button.click()
                    time.sleep(2)
                    elems = self.browser.find_elements(by.By.CSS_SELECTOR, ".d-table.table-fixed")
                    for elem in elems:
                        self.followers.append(elem.find_element(by.By.CLASS_NAME, 'Link--secondary').text)
                else:
                    break
            except (common.exceptions.NoSuchElementException, common.exceptions.StaleElementReferenceException):
                break


github = Github(username, password)
# github.signIn()
github.getFollowers()
print(github.followers)
print(len(github.followers))