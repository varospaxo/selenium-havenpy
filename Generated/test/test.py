import time
import csv
import sys
import requests
import json
import logging
import os
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
start_time = datetime.now()
start_time = start_time.strftime('%d%m%Y_%H%M%S')
print('Start time:', start_time)
step=0
if not os.path.exists(start_time):
    os.makedirs(start_time)
logging.basicConfig(
filename='run.log',
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s')
force_clicks=0
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

def capture_screenshot(filename=None):
   if filename:
       file_name = filename + '.png' if not filename.endswith('.png') else filename
       filepath = os.path.join(start_time, file_name)
       driver.save_screenshot(filepath)
   else:
       current_time = datetime.now()
       filename = current_time.strftime('Screenshot-%d%m%y_%H%M%S') + '.png'
       filepath = os.path.join(start_time, filename)
       driver.save_screenshot(filepath)
       time.sleep(1)

def click_action(xpath, vpx, vpy, x, y):
   global force_clicks
   time.sleep(2)
   try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
   except: pass
   try:
       if force_clicks > 3:
           print('Force clicks exceeded limit. Exiting script.')
           logging.info(f'Failed to find XPath: {xpath}. Trying coordinate click.')
           sys.exit()
       wait = WebDriverWait(driver, 5)
       element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
       element.click()
       force_clicks=0
   except Exception as e:
       print(f'Failed to find XPath: {xpath}. Trying coordinate click.')
       logging.info(f'Failed to find XPath: {xpath}. Trying coordinate click.')
       force_clicks+=1
       set_viewport_size(driver, vpx, vpy)
       actions = ActionChains(driver)
       actions.move_by_offset(x, y).click().perform()
       actions.move_by_offset(-(x), -(y)).perform()


response_text = "Hello World" 
variable1 = "Hello World"
variableX = "Hello World"

driver.get('https://example.com')
# Prefix text
logging.warning(response_text)
# Suffix text
# Prefix text
logging.info('Hello World')
# Suffix text
# Prefix text
logging.debug(variable1)
# Suffix text
# Prefix text
logging.critical('Deprecated module found')
# Suffix text
# Prefix text
logging.error(variableX)
# Suffix text
# Prefix text
capture_screenshot()
# Suffix text
# Prefix text
capture_screenshot('test')
# Suffix text
# Prefix text
# Suffix text
# Prefix text
# Comment Text
# Suffix text
# Prefix text
# Comment Text
# Suffix text
# Prefix text
click_action('//button[@id=submit]', 1920, 780, 70, 200)
# Suffix text
# Prefix text
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name=username]')))
element.clear()
element.send_keys(input_values['input_value_34'])
# Suffix text
# Prefix text
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@id=description]')))
element.clear()
decoded_value = base64.b64decode(input_values['input_value_37']).decode('utf-8')
element.send_keys(decoded_value)
# Suffix text
# Prefix text
wait = WebDriverWait(driver, 5)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '//form[@id=loginForm]')))
element.submit()
# Suffix text
# Prefix text
time.sleep(5)
# Suffix text
# Prefix text
# Format: wait
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="example"]')))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.invisibility_of_element_located((By.XPATH, '//div[@id="example"]')))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="submit"]')))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="status"]')))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    status_element = driver.find_element(By.XPATH, '//div[@id="staleElement"]')
    wait.until(EC.staleness_of(status_element))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.element_to_be_selected((By.XPATH, '//input[@id="checkbox"]')))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.element_to_be_deselected((By.XPATH, '//input[@id="checkbox"]')))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="message"]'), 'Hello World'))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.text_to_be_present_in_element_value((By.XPATH, '//input[@id="textbox"]'), 'Example Value'))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@id="frame"]')))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.alert_is_present())
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.title_contains('Page Title'))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until_not(EC.title_is('Exact Page Title'))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.url_contains('example.com'))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.url_matches('https://example.com'))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.url_to_be('https://example.com/home'))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.url_changes(''))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until_not(EC.number_of_windows_to_be(2))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.new_window_is_opened())
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.element_located_to_be_selected((By.XPATH, '//input[@id="checkbox"]')))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.element_selection_state_to_be((By.XPATH, '//input[@id="checkbox"]'), True))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
try:
    wait = WebDriverWait(driver, 7)
    wait.until(EC.element_located_selection_state_to_be((By.XPATH, '//input[@id="checkbox"]'), False))
except:
    print('Wait condition failed')
    logging.info('Wait condition failed')
# Suffix text
# Prefix text
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# Suffix text
# Prefix text
driver.execute_script('window.scrollTo(0, 0)')
# Suffix text
# Prefix text
element = driver.find_element(By.XPATH, '//div[@id=content]')
driver.execute_script('arguments[0].scrollIntoView(true);', element)
# Suffix text
# Prefix text
set_viewport_size(driver, 1920, 780)
driver.execute_script('window.scrollBy(0, 500)')
# Suffix text
# Prefix text
set_viewport_size(driver, 1920, 780)
driver.execute_script('window.scrollBy(0, -500)')
# Suffix text
# Prefix text
element = driver.find_element(By.XPATH, '//button[@class=menu]')
actions = ActionChains(driver)
actions.move_to_element(element).perform()
# Suffix text
# Prefix text
element = driver.find_element(By.XPATH, '//button[@class=edit]')
actions = ActionChains(driver)
actions.double_click(element).perform()
# Suffix text
# Prefix text
element = driver.find_element(By.XPATH, '//button[@class=edit]')
actions = ActionChains(driver)
actions.double_click(element).perform()
# Suffix text
# Prefix text
source = driver.find_element(By.XPATH,'//div[@id=item]')
target = driver.find_element(By.XPATH,'//div[@id=arget]')
actions = ActionChains(driver)
actions.drag_and_drop(source, target).perform()
# Suffix text
# Prefix text
element = driver.find_element(By.XPATH, '//div[@id=item]')
actions = ActionChains(driver)
actions.drag_and_drop_by_offset(element, 70, 200).perform()
# Suffix text
# Prefix text
driver.switch_to.alert.accept()
# Suffix text
# Prefix text
driver.switch_to.alert.dismiss()
# Suffix text
# Prefix text
driver.switch_to.alert.send_keys('username123')
# Suffix text
# Prefix text
alert_text = driver.switch_to.alert.text
# Suffix text
# Prefix text
driver.execute_script("alert('Hello World')")
# Suffix text
# Prefix text
element = driver.find_element(By.XPATH, '//input[@id=username]')
attribute = element.get_attribute('value')
# Suffix text
# Prefix text
element = driver.find_element(By.XPATH, '//div[@id=box]')
css_value = element.value_of_css_property('color')
# Suffix text
# Prefix text
element = driver.find_element(By.XPATH, '//input[@id=checkbox]')
property = element.get_property('checked')
# Suffix text
# Prefix text
element = driver.find_element(By.XPATH, '//p[@id=message]')
text = element.text
# Suffix text
# Prefix text
title = driver.title
# Suffix text
# Prefix text
url = driver.current_url
# Suffix text
# Prefix text
page_source = driver.page_source
# Suffix text
# Prefix text
cookies = driver.get_cookies()
# Suffix text
# Prefix text
driver.add_cookie({"name": "John Doe", "value": 12345})
# Suffix text
# Prefix text
driver.delete_cookie('session')
# Suffix text
# Prefix text
driver.delete_all_cookies()
# Suffix text
# Prefix text
url = 'https://jsonplaceholder.typicode.com/posts'
method = 'POST'
payload_body = '''{
  "title": "foo",
  "body": "bar",
  "userId": 1
}'''
payload = json.dumps(json.loads(payload_body))
headers = {
  "Content-Type": "application/json",
  "Accept": "application/json"
}
response = requests.request(method, url, headers=headers, data=payload)
print(response.text)
logging.info(response.text)
# Suffix text
time.sleep(5)
driver.quit()
