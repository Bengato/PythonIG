from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import time
import configparser
import datetime
import json

# class init


class InstagramBot:
    def __init__(self, username, password):
        """
        initializes an InstagramBot object
        call login() to authenticate a user with IG

        Args:
            username:str: the instagram username to log in
            password:str: the password for said username

        Attributes:
            driver:selenium.webdriver.Firefox: used to automate browser actions
        """
        self.username = username
        self.password = password
        self.base_url = "http://www.instagram.com/"
        options = Options()
        options.add_argument('disable-infobars')
        self.driver = webdriver.Chrome(
            executable_path=r'./chromedriver.exe', options=options)
# login method - should already be logged in !!!

    def logStatus(self, state):
        line = '## '+self.username+' '
        if state == "logged in":
            line += state
        else:
            line += "started "+state
        line += " at "+str(datetime.datetime.now())+"\n"
        if os.path.isfile('./logFile.txt'):
            with open('logFile.txt', 'a') as logFile:
                logFile.write(line)
        else:
            logFile = open("logFile.txt", "a+")
            logFile.write("## Instagram Bot Log File ##\n\n"+line)

    def login(self):

        self.driver.get('{}accounts/login'.format(self.base_url))
        time.sleep(1)
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        username.clear()
        password.clear()
        username.send_keys(self.username)
        password.send_keys(self.password+Keys.RETURN)
        self.logStatus("logged in")
        time.sleep(10)
# accepts wanted hashtag and cycles through posts -> follows posting user

    def follow_tags(self, hashtag):
        self.driver.get('{}explore/tags/{}/'.format(self.base_url, hashtag))
        time.sleep(1)
        for i in range(0, 3):
            self.driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(1)
        posts = self.driver.find_elements_by_class_name('v1Nh3')
        links = list()
        for post in posts:
            links.append(post.find_element_by_xpath(
                'a').get_attribute('href'))
        self.logStatus("following tags")
        for link in links:
            self.driver.get(link)
            time.sleep(1)
            self.driver.find_elements_by_xpath(
                '//button[contains(.,"Follow")]')[0].click()
            time.sleep(1)
# accepts wanted hashtag and cycles through posts -> likes posts

    def like_tags(self, hashtag):
        self.driver.get(
            '{}explore/tags/{}/'.format(self.base_url, hashtag))
        time.sleep(1)
        for i in range(0, 3):
            self.driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(1)
        posts = self.driver.find_elements_by_class_name('v1Nh3')
        links = list()
        for post in posts:
            links.append(post.find_element_by_xpath(
                'a').get_attribute('href'))
        self.logStatus("liking tags")
        for link in links:
            self.driver.get(link)
            time.sleep(1)
            self.driver.find_elements_by_xpath(
                '//button/span[@aria-label="Like"]')[0].click()
            time.sleep(1)

    def like_user(self, username):
        self.driver.get(
            '{}{}/'.format(self.base_url, username))
        time.sleep(1)
        for i in range(0, 3):
            self.driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(1)
        posts = self.driver.find_elements_by_class_name('v1Nh3')
        links = list()
        for post in posts:
            links.append(post.find_element_by_xpath(
                'a').get_attribute('href'))
        self.logStatus("liking user posts")
        for link in links:
            self.driver.get(link)
            time.sleep(1)
            self.driver.find_elements_by_xpath(
                '//button/span[@aria-label="Like"]')[0].click()
            time.sleep(1)


def getConfig():
    user = {
        "username": "",
        "password": ""
    }
    config_path = './config.ini.un~'
    cparser = configparser.ConfigParser()
    cparser.read(config_path)
    user["username"] = cparser['AUTH']['USERNAME']
    user["password"] = cparser['AUTH']['PASSWORD']
    return user


if __name__ == '__main__':
    user = getConfig()
    print(user["username"], user["password"])
    ig_bot = InstagramBot(user["username"], user["password"])
    ig_bot.login()
    # ig_bot.like_user('garyvee') will like every post on said users account
    # ig_bot.like_tags('guitar')  # will like every post on said hashtag search
    # ig_bot.follow_tags('guitar') will follow every posting user on said hashtag search
