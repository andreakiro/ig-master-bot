from selenium import webdriver
from selenium import common
from time import sleep, time
from datetime import datetime
from os import path as pth, mkdir

class InstaBot:
    def __init__(self, username, password, headless = False):
        intro = 'InstaBot session started ' + str(datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S'))
        if headless:
            intro += ' (headless)'
        else:
            intro += ' (head)'
        print intro

        # attributes
        self.username = username
        self.unfollowers = []
        self.headless = headless
        self.legal = True

        if self.headless:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1200x600') # optional 
            self.driver = webdriver.Chrome(executable_path = './chromedriver', chrome_options = options)
        else:
            self.driver = webdriver.Chrome('./chromedriver')

        # driving
        self.driver.get("https://instagram.com")
        sleep(2)

        if self.headless:
            self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]").click()
        else:
            self.driver.find_element_by_xpath("//a[contains(text(), 'Connectez-vous')]").click()
        
        sleep(2)

        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password)
        try:
            self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        except common.exceptions.ElementClickInterceptedException:
            print 'Credentials are wrong'
            self.legal = False
            self.close_session()
            return

        sleep(4)

        if not self.headless:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Plus tard')]").click()

        self._refresh()

    def unfollow(self):
        old = self._read_from_file('./awaitlist/{}/unfollow.txt'.format(self.username))
        for person in old:
            self.driver.get("https://www.instagram.com/{}/".format(person))
            sleep(2)
            try:
                self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button').click()
                self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[1]').click()
            except common.exceptions.NoSuchElementException:
                continue

    def follow(self):
        old = self._read_from_file('./awaitlist/{}/follow.txt'.format(self.username))
        for person in old:
            self.driver.get("https://www.instagram.com/{}/".format(person))
            sleep(2)
            try:
                self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/button').click()
            except common.exceptions.NoSuchElementException:
                continue

    def remove_followers(self):
        return

    def get_unfollowers(self):
        old = []
        if pth.exists('./archives/{}'.format(self.username)):
            old = self._read_from_file('./archives/{}/last.txt'.format(self.username))
        self._get_unfollowers()
        temp = self._read_from_file('./archives/{}/last.txt'.format(self.username))
        new = [item for item in temp if item not in old]
        self._write_into_file(False, new)

    def close_session(self):
        if self.legal:
            # log out
            self._refresh()
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div/button').click()
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/button[9]').click()
        self.driver.quit()
        print 'Successfully closed the driver'
        print 'InstaBot session closed ' + str(datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S'))

    def _get_unfollowers(self):
        # drive to account page
        self.driver.get("https://www.instagram.com/{}/".format(self.username))
        sleep(2)

        # following list
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        print 'Searching following names'
        following = self._get_names()
        #print str(len(following)) + ' list of following'

        # follower list
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        print 'Searching followers names'
        followers = self._get_names()
        #print str(len(followers)) + ' list of followers'

        self.unfollowers = [user for user in following if user not in followers]
        self._write_into_file()
        #print str(len(self.unfollowers)) + ' list unfollowers'

    def _get_names(self):
        sleep(5)
        # scroll the name box
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht, check, ct = 0, 1, -1, -10
        while last_ht != check:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
            if last_ht == ht:
                ct += 1
                #print 'check + 1 ' + str(datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S'))
                if ct == 0:
                    check = ht
        links = scroll_box.find_elements_by_tag_name('a')
        #print 'size of links ' + str(len(links)) + ' ' + str(datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S'))
        names = [name.text for name in links if name.text != '']

        # drive to account page
        self.driver.get("https://www.instagram.com/{}/".format(self.username))
        sleep(2)
        return names

    def _refresh(self):
        self.driver.get("https://www.instagram.com/{}/".format(self.username))
        sleep(2)

    def _write_into_file(self, bool = True, newlist = None):
        if bool:
            filename = str(datetime.fromtimestamp(time()).strftime('%Y-%m-%d*%H:%M:%S')) + '.txt'
            path = './archives/{}/history/'.format(self.username) + filename
            if not pth.exists('./archives'):
                mkdir('./archives')
            if not pth.exists('./archives/{}'.format(self.username)):
                mkdir('./archives/{}'.format(self.username))
                mkdir('./archives/{}/history'.format(self.username))
            with open(path, 'w') as f:
                for item in self.unfollowers:
                    f.write("%s\n" % item)
            with open('./archives/{}/last.txt'.format(self.username), 'w') as f:
                for item in self.unfollowers:
                    f.write("%s\n" % item)
            print 'Find text file in ./archives/{}/history'.format(self.username)
        else:
            with open('./archives/{}/new.txt'.format(self.username), 'w') as f:
                for item in newlist:
                    f.write("%s\n" % item)

    def _read_from_file(self, filename):
        return [line.rstrip('\n') for line in open(filename)]