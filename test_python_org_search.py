import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(object):

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        sleep(1)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        sleep(1)
        elem.send_keys(Keys.RETURN)
        sleep(1)
        assert "No results found." not in driver.page_source


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
