import sys
import getopt
import json
import tweepy
from selenium import webdriver


class TwitterCreator:

    def start(self, callbacks, inputFile, fromRow, toRow, driverType):
        try:
            rows = json.loads(open(inputFile).read())
            numElements = len(rows)
        except:
            numElements = 0
        if numElements > 0:
            if toRow == -1:
                toRow = numElements
            else:
                if toRow > numElements:
                    toRow = numElements
            fromRow -= 1
            if fromRow < numElements:
                self.driver = self.getWebdriver(driverType)
                for numRow in range(fromRow, toRow):
                    row = rows[numRow]
                    print('Processing row: ' + str(numRow))
                    for callback in callbacks:
                        callback(row)
                    print('Processed.')
                self.close()
            else:
                print('Index out of bounds')
        else:
            print('Data could not be extracted')

    def getWebdriver(self, driverType):
        if driverType == 'proxy':
            profile = webdriver.FirefoxProfile()
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.socks", "127.0.0.1")
            profile.set_preference("network.proxy.socks_port", 9150)
            profile.set_preference("network.proxy.socks_remote_dns", True)
            profile.set_preference("places.history.enabled", False)
            profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
            profile.set_preference("privacy.clearOnShutdown.passwords", True)
            profile.set_preference(
                "privacy.clearOnShutdown.siteSettings", True)
            profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
            profile.set_preference("signon.rememberSignons", False)
            profile.set_preference("network.cookie.lifetimePolicy", 2)
            profile.set_preference("network.dns.disablePrefetch", True)
            profile.set_preference("network.http.sendRefererHeader", 0)
            profile.set_preference("javascript.enabled", False)
            profile.set_preference("permissions.default.image", 2)
            return webdriver.Firefox(profile)
        elif driverType == 'headless':
            return webdriver.PhantomJS()
        else:
            return webdriver.Firefox()

    def desktopCreateUserPhone(self, row):
        consumer_key = 'emubaipEDnjyLM1jhG2Kb17Ny'
        consumer_secret = 'GeGrxYbHhqeOQxgfpA39nTbHAPOzRsEL2IgHwju4xrEXcngstC'
        access_token = '1041594267964256257-OUt3QJZf0aUEHyp2HoTcoRqGuGJ8gF'
        access_token_secret = 'ebHRgfrU4abL9x9xHqqk5AlhLxMBszondRIOeBECnvOqh'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        # Register a new user on desktop
        self.driver.get('https://twitter.com/i/flow/signup')
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath(
            "//span[text()='Use email instead']").click()
        self.driver.find_element_by_name('email').send_keys(row['Email'])
        self.driver.find_element_by_name('password').send_keys(row['Password'])
        self.driver.find_element_by_name('name').send_keys(row['FullName'])
        self.driver.find_element_by_xpath("//span[text()='Next']").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_name(
            'phone_number').send_keys(row['PhoneNumber'])
        self.driver.find_element_by_xpath("//span[text()='Next']").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//span[text()='Next']").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//span[text()='Sign up']").click()
        self.driver.implicitly_wait(5)

        # Verify the email address
        verification_link = self.getVerificationLink(row['Email'])
        if verification_link:
            self.driver.get(verification_link)
            self.driver.implicitly_wait(2)
            self.driver.find_element_by_xpath("//span[text()='Next']").click()
            self.driver.implicitly_wait(2)
            self.driver.find_element_by_xpath(
                "//span[text()='Let's go']").click()
            self.driver.implicitly_wait(5)
            print('Account created for ' + row['Email'])
            api.update_status(
                "Hello, world! This is my first tweet with Python and Tweepy!")
        else:
            print('Could not get verification link for ' + row['Email'])

    def getVerificationLink(self, email):
        # This function should retrieve the verification link from the email sent to the user's email address
        # You can use a third-party library like BeautifulSoup or lxml to parse the email
        # and retrieve the verification link from the email's HTML content
        # However, this is beyond the scope of this code template and requires additional configuration and setup
        # For testing purposes only, this function returns a dummy verification link
        return 'https://twitter.com/i/flow/signup/complete?flow_data=%7B%22show_sms_verification_dialog%22%3Atrue%2C%22search_surface%22%3A%22signup_flow%22%2C%22email%22%3A%22' + email + '%22%2C%22flow_origin%22%3A%22web%22%2C%22prefill_phone_number%22%3Atrue%2C%22phone_number%22%3A%22%22%7D'

    def close(self):
        self.driver.quit()


def main(argv):
    fromRow = 1
    toRow = -1
    inputFile = 'D:\\TAC\\AA.csv'
    driverType = 'proxy'
    opts, args = getopt.getopt(argv, "f:t:i:d:")
    if opts:
        for o, a in opts:
            if o in ("-f"):
                fromRow = int(a)
            elif o in ("-t"):
                toRow = int(a)
            elif o in ("-i"):
                inputFile = a
            elif o in ("-d"):
                driverType = a
    while not inputFile:
        inputFile = input('Input file path: ')
    creator = TwitterCreator()
    print('Process started')
    creator.start(callbacks=[creator.desktopCreateUserPhone],inputFile=inputFile, fromRow=fromRow, toRow=toRow, driverType=driverType)
    # print(inputFile)

    print('Process ended')


with open('/TAC/AA.csv', 'r') as file:
    contents = file.read()
    print(contents)
if __name__ == "__main__":
    main(sys.argv[1:])
