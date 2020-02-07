import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(object):

    def test_cs_login_bad_pw(self):
        driver = self.driver
        driver.get("https://analyzer.cryptosense.com/")
        self.assertIn("Cryptosense", driver.title)
        sleep(1)
        elem = driver.find_element_by_name("username")
        elem.send_keys("ian@cryptosense.com")
        sleep(1)
        elem = driver.find_element_by_name("password")
        elem.send_keys("not-my-password")
        sleep(1)
        elem = driver.find_element_by_name("submit")
        elem.click()
        sleep(1)
        self.assertIn("Bad login or password", driver.page_source)

class FirefoxTest(PythonOrgSearch, unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()


class ChromeTest(PythonOrgSearch, unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
