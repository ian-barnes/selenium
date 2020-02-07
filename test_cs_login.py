import unittest
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of


class PythonOrgSearch(object):

    def test_cs_login_bad_pw(self):
        driver = self.driver
        driver.get("https://analyzer.cryptosense.com/")
        self.assertIn("Cryptosense", driver.title)
        elem = driver.find_element_by_name("username")
        elem.send_keys("ian@cryptosense.com")
        elem = driver.find_element_by_name("password")
        elem.send_keys("not-my-password")
        # elem.send_keys(Keys.RETURN)
        elem = driver.find_element_by_name("submit")
        elem.click()
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
