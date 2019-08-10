from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import configparser

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
        self.base_url = "https://www.instagram.com/"
        self.driver = webdriver.Chrome(
            executable_path=r'./chromedriver.exe')
# login method - should already be logged in !!!

    def login(self):
        self.driver.get('{}accounts/login'.format(self.base_url))
        time.sleep(2)
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        username.clear()
        password.clear()
        username.send_keys(self.username)
        password.send_keys(self.password+Keys.RETURN)
        time.sleep(25)
# accepts wanted hashtag and cycles through posts -> follows posting user

    def follow_tags(self, hashtag):
        self.driver.get('{}explore/tags/{}/'.format(self.base_url, hashtag))
        time.sleep(2)
        for i in range(0, 3):
            self.driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        posts = self.driver.find_elements_by_class_name('v1Nh3')
        links = list()
        for post in posts:
            links.append(post.find_element_by_xpath(
                'a').get_attribute('href'))
        for link in links:
            self.driver.get(link)
            time.sleep(2)
            self.driver.find_elements_by_xpath(
                '//button[contains(.,"Follow")]')[0].click()
            time.sleep(2)
# accepts wanted hashtag and cycles through posts -> likes posts

    def like_tags(self, hashtag):
        self.driver.get(
            '{}explore/tags/{}/'.format(self.base_url, hashtag))
        time.sleep(2)
        for i in range(0, 3):
            self.driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        posts = self.driver.find_elements_by_class_name('v1Nh3')
        links = list()
        for post in posts:
            links.append(post.find_element_by_xpath(
                'a').get_attribute('href'))
        for link in links:
            self.driver.get(link)
            time.sleep(2)
            self.driver.find_elements_by_xpath(
                '//button/span[@aria-label="Like"]')[0].click()
            time.sleep(2)

    def like_user(self, username):
        self.driver.get(
            '{}{}/'.format(self.base_url, username))
        time.sleep(2)
        for i in range(0, 3):
            self.driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        posts = self.driver.find_elements_by_class_name('v1Nh3')
        links = list()
        for post in posts:
            links.append(post.find_element_by_xpath(
                'a').get_attribute('href'))
        for link in links:
            self.driver.get(link)
            time.sleep(2)
            self.driver.find_elements_by_xpath(
                '//button/span[@aria-label="Like"]')[0].click()
            time.sleep(2)


if __name__ == '__main__':
    config_path = './config.ini.un~'
    cparser = configparser.ConfigParser()
    cparser.read(config_path)
    username = cparser['AUTH']['USERNAME']
    password = cparser['AUTH']['PASSWORD']
    print(username, password)
    ig_bot = InstagramBot(username, password)
    ig_bot.login()
    # ig_bot.like_user('garyvee') will like every post on said users account
    # ig_bot.like_tags('guitar') will like every post on said hashtag search
    # ig_bot.follow_tags('guitar') will follow every posting user on said hashtag search
