from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")
firefox = webdriver.Firefox(options=firefox_options)
dx, dy = firefox.execute_script("var w=window; return [w.outerWidth - w.innerWidth, w.outerHeight - w.innerHeight];")
firefox.set_window_size(1024 + dx, 768 + dy)
firefox.get("https://analyzer.cryptosense.com/")
firefox.save_screenshot("firefox-login.png")
assert "Cryptosense" in firefox.title
elem = firefox.find_element_by_name("username")
elem.send_keys("ian@cryptosense.com")
elem = firefox.find_element_by_name("password")
elem.send_keys("not-my-password")
elem = firefox.find_element_by_name("submit")
elem.click()
firefox.save_screenshot("firefox-bad-pw.png")
assert "Bad login or password" in firefox.page_source
firefox.close()

chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")
chrome = webdriver.Chrome(options=chrome_options)
chrome.set_window_size(1024, 768)
chrome.get("https://analyzer.cryptosense.com/")
chrome.save_screenshot("chrome-login.png")
assert "Cryptosense" in chrome.title
elem = chrome.find_element_by_name("username")
elem.send_keys("ian@cryptosense.com")
elem = chrome.find_element_by_name("password")
elem.send_keys("not-my-password")
elem = chrome.find_element_by_name("submit")
elem.click()
chrome.save_screenshot("chrome-bad-pw.png")
assert "Bad login or password" in chrome.page_source
chrome.close()
