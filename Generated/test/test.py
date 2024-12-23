import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
input_values = {}
with open('test.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        input_values[row['Variable']] = row['Value']

driver = webdriver.Chrome()
try:
   def set_viewport_size(driver, width, height):
       window_size = driver.execute_script("""
           return [window.outerWidth - window.innerWidth + arguments[0],
                   window.outerHeight - window.innerHeight + arguments[1]];
           """, width, height)
       driver.set_window_size(*window_size)

except: pass
driver.get('https://vedantfar.pythonanywhere.com/pastebinlogin')
set_viewport_size(driver, 1920, 1080)
time.sleep(2)
try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
except: pass
try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="submit"]')))
    element.click()
except Exception as e:
    # Fallback to coordinates if XPath click fails
    print('Failed to find XPath. Trying coordinate click.')
    actions = ActionChains(driver)
    actions.move_by_offset(100, 200).click().perform()
    actions.move_by_offset(-100, -200).perform()
    time.sleep(1)
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
element.clear()
element.send_keys(input_values['input_value_1'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '//form[@id="loginForm"]')))
element.submit()
time.sleep(5)
try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="loading"]')))
except: print('Wait element failed')
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
driver.execute_script('window.scrollTo(0, 0)')
element = driver.find_element_by_xpath('//div[@id="content"]')
driver.execute_script('arguments[0].scrollIntoView(true);', element)
driver.execute_script('window.scrollBy(0, 500)')
element = driver.find_element_by_xpath('//button[@class="menu"]')
actions = ActionChains(driver)
actions.move_to_element(element).perform()
element = driver.find_element_by_xpath('//div[@id="context-menu"]')
actions = ActionChains(driver)
actions.context_click(element).perform()
element = driver.find_element_by_xpath('//button[@class="edit"]')
actions = ActionChains(driver)
actions.double_click(element).perform()
source = driver.find_element_by_xpath('//div[@id="item"]')
target = driver.find_element_by_xpath('//div[@id="target"]')
actions = ActionChains(driver)
actions.drag_and_drop(source, target).perform()
element = driver.find_element_by_xpath('//div[@id="item"]')
actions = ActionChains(driver)
actions.drag_and_drop_by_offset(element, 100, 200).perform()
driver.switch_to.alert.accept()
driver.switch_to.alert.dismiss()
driver.switch_to.alert.send_keys('username123')
alert_text = driver.switch_to.alert.text
driver.execute_script("alert('Hello World')")
element = driver.find_element_by_xpath('//input[@id="username"]')
attribute = element.get_attribute('value')
element = driver.find_element_by_xpath('//div[@id="box"]')
css_value = element.value_of_css_property('color')
element = driver.find_element_by_xpath('//input[@id="checkbox"]')
property = element.get_property('checked')
element = driver.find_element_by_xpath('//p[@id="message"]')
text = element.text
title = driver.title
url = driver.current_url
page_source = driver.page_source
cookies = driver.get_cookies()
driver.add_cookie({"name": "session", "value": "12345"})
driver.delete_cookie('session')
driver.delete_all_cookies()
time.sleep(5)
driver.quit()
