---
title: Web testing with Selenium
theme: moon
revealOptions:
    transition: 'none'
css: slides.css
---

## Web testing with Selenium

---

## What is Selenium?

- Automate interaction with browsers
- Bindings for Python, Java...
- Drivers for all major browsers & platforms

See:
- <https://selenium.dev/>
- <https://selenium-python.readthedocs.io/getting-started.html>

---

## Installation

- `sudo apt install python3-selenium`
- `pip install selenium` (or `pipenv`)
- Download Chrome & Firefox drivers and copy to `/usr/local/bin`
  - <https://sites.google.com/a/chromium.org/chromedriver/downloads>
  - <https://github.com/mozilla/geckodriver/releases>

---

## Simple usage

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox() # or Chrome() - open browser window
driver.get("http://python.org") #          - load page

assert "Python" in driver.title #          - interrogate browser state

elem = driver.find_element_by_name("q") #  - interrogate the DOM
elem.clear() #                             - clear form field
elem.send_keys("pycon") #                  - insert data into form field
elem.send_keys(Keys.RETURN) #              - submit form
assert "No results found." not in driver.page_source # - search page content
driver.close() #                           - close browser window

```

---

## Do the same thing in a test

(This uses `unittest` but obviously `pytest` would work too.)

```python
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(object):

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
```

---

## Test continued...

```python
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
```

---

## Test CS analyzer login page

As above, except:

```python
    def test_cs_login_bad_pw(self):
        driver = self.driver
        driver.get("https://analyzer.cryptosense.com/")
        self.assertIn("Cryptosense", driver.title)
        elem = driver.find_element_by_name("username")
        elem.send_keys("ian@cryptosense.com")
        elem = driver.find_element_by_name("password")
        elem.send_keys("not-my-password")
        elem.send_keys(Keys.RETURN)
        self.assertIn("Bad login or password", driver.page_source)
```

---

## So... that doesn't work

- Chrome passes, Firefox fails
- Fresh copy of the login page hasn't loaded yet when it checks for the "Bad
  login..." message
- Instead the page contains the message "Please log in to access this page."
  (Why?)
- Need to wait for page load?

And that's where things start to get complicated...

- Selenium has no way to know that you've triggered a new page load.
- Maybe your click or "Return" triggered some Javascript within the page.

---

## Waiting for page load

See <http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html>

- Use a context manager
- Wait (with timeout limit) for old page to get stale
- Only then check the condition

---

## Revised code... should work?

```python
class PythonOrgSearch(object):

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.driver, timeout).until(staleness_of(old_page))

    def test_cs_login_bad_pw(self):
        driver = self.driver
        driver.get("https://analyzer.cryptosense.com/")
        self.assertIn("Cryptosense", driver.title)
        elem = driver.find_element_by_name("username")
        elem.send_keys("ian@cryptosense.com")
        elem = driver.find_element_by_name("password")
        elem.send_keys("not-my-password")
        elem.send_keys(Keys.RETURN)
        with self.wait_for_page_load(timeout=10):
            self.assertIn("Bad login or password", driver.page_source)
```

... but still fails with same error

---

## Try clicking the submit button

```python
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
```

... and now the test passes on both browsers

---

## Further possibilities

- Alternative called `puppeteer`, haven't tried it
- Selenium IDE: Record actions and turn them into scripts
- Selenium Grid: Run tests on multiple remote machines
  - Different operating systems
  - Potentially works on VMs
  - In principle could automate cross-browser testing

---
