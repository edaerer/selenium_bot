from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import by
from time import sleep
from info import version, chromedriver, chrome, username, password

def getChromeBrowser(version, path_to_chromedriver, path_to_chrome):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = path_to_chrome.format(version)
    service_options = webdriver.ChromeService(executable_path=path_to_chromedriver.format(version))
    driver = webdriver.Chrome(options=chrome_options, service=service_options)
    return driver

class Instagram:
    def __init__(self, username, password):
        self.browser = getChromeBrowser(version, chromedriver, chrome)
        self.username = username
        self.password = password
        self.followers = []

    def signIn(self):
        self.browser.get("https://www.instagram.com/")
        sleep(3)
        self.browser.find_element(by.By.CSS_SELECTOR, 'input[aria-label="Phone number, username, or email"]').send_keys(self.username)
        self.browser.find_element(by.By.CSS_SELECTOR, 'input[aria-label="Password"]').send_keys(self.password)
        self.browser.find_element(by.By.CSS_SELECTOR, "._acan._acap._acas._aj1-._ap30").click()
        # if user has 2FA, manually enter the code.
        # print("Please enter the 2FA code manually in the browser.")
        # sleep(30)
        sleep(10)

    def getFollowers(self):
        self.browser.get(f"https://www.instagram.com/{self.username}")
        sleep(3)
        self.browser.find_element(by.By.XPATH, f"//a[@href='/{self.username}/followers/' and @role='link']").click()
        sleep(3)

        # Get follower count to calculate spaces to be clicked.
        counts = self.browser.find_elements(by.By.CLASS_NAME, "_ac2a")
        temp = []
        for count in counts:
            temp.append(count.text)
        follower_count = int(temp[1])
        space_count = int(follower_count / 3)
        sleep(2)

        # Scroll down to the end.
        action = webdriver.ActionChains(self.browser)
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        for i in range(space_count):
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            sleep(1)

        # Iterate through each div to get user links.
        divs = self.browser.find_elements(by.By.XPATH, "/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div")
        for div in divs:
            links = div.find_elements(by.By.XPATH, "//a[@role='link']")
            for link in links:
                if link.text:
                    self.followers.append(link.text)

        # Crop the list to only get followers.
        self.followers = self.followers[12:]
        self.followers = self.followers[:-1]



insta = Instagram(username, password)
insta.signIn()
insta.getFollowers()
print(insta.followers, len(insta.followers))