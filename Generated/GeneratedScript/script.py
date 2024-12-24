import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
input_values = {}
with open('inputs.csv', 'r') as csv_file:
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
set_viewport_size(driver, 1877, 926)
time.sleep(2)
try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
except: pass
try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, 'id("username")')))
    element.click()
except Exception as e:
    # Fallback to coordinates if XPath click fails
    print('Failed to find XPath. Trying coordinate click.')
    actions = ActionChains(driver)
    actions.move_by_offset(578, 167).click().perform()
    actions.move_by_offset(-578, -167).perform()
    time.sleep(1)
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("username")')))
element.clear()
element.send_keys(input_values['input_value_1'])
set_viewport_size(driver, 1877, 926)
time.sleep(2)
try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
except: pass
try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, 'id("password")')))
    element.click()
except Exception as e:
    # Fallback to coordinates if XPath click fails
    print('Failed to find XPath. Trying coordinate click.')
    actions = ActionChains(driver)
    actions.move_by_offset(479, 242).click().perform()
    actions.move_by_offset(-479, -242).perform()
    time.sleep(1)
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("password")')))
element.clear()
element.send_keys(input_values['input_value_3'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("password")')))
element.clear()
element.send_keys(input_values['input_value_4'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("password")')))
element.clear()
element.send_keys(input_values['input_value_5'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("password")')))
element.clear()
element.send_keys(input_values['input_value_6'])
set_viewport_size(driver, 1877, 926)
time.sleep(2)
try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
except: pass
try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/form/button')))
    element.click()
except Exception as e:
    # Fallback to coordinates if XPath click fails
    print('Failed to find XPath. Trying coordinate click.')
    actions = ActionChains(driver)
    actions.move_by_offset(343, 291).click().perform()
    actions.move_by_offset(-343, -291).perform()
    time.sleep(1)
set_viewport_size(driver, 1877, 864)
time.sleep(2)
try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
except: pass
try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/form[1]/div/textarea')))
    element.click()
except Exception as e:
    # Fallback to coordinates if XPath click fails
    print('Failed to find XPath. Trying coordinate click.')
    actions = ActionChains(driver)
    actions.move_by_offset(550, 195).click().perform()
    actions.move_by_offset(-550, -195).perform()
    time.sleep(1)
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/form[1]/div/textarea')))
element.clear()
element.send_keys(input_values['input_value_9'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/form[1]/div/textarea')))
element.clear()
element.send_keys(input_values['input_value_10'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/form[1]/div/textarea')))
element.clear()
element.send_keys(input_values['input_value_11'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/form[1]/div/textarea')))
element.clear()
element.send_keys(input_values['input_value_12'])
set_viewport_size(driver, 1877, 864)
time.sleep(2)
try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
except: pass
try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/form[1]/button')))
    element.click()
except Exception as e:
    # Fallback to coordinates if XPath click fails
    print('Failed to find XPath. Trying coordinate click.')
    actions = ActionChains(driver)
    actions.move_by_offset(451, 340).click().perform()
    actions.move_by_offset(-451, -340).perform()
    time.sleep(1)
wait = WebDriverWait(driver, 5)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/form[1]')))
element.submit()
set_viewport_size(driver, 1877, 864)
time.sleep(2)
try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
except: pass
try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/form[1]/a')))
    element.click()
except Exception as e:
    # Fallback to coordinates if XPath click fails
    print('Failed to find XPath. Trying coordinate click.')
    actions = ActionChains(driver)
    actions.move_by_offset(551, 345).click().perform()
    actions.move_by_offset(-551, -345).perform()
    time.sleep(1)
set_viewport_size(driver, 1877, 926)
time.sleep(2)
try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
except: pass
try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/form[2]/button')))
    element.click()
except Exception as e:
    # Fallback to coordinates if XPath click fails
    print('Failed to find XPath. Trying coordinate click.')
    actions = ActionChains(driver)
    actions.move_by_offset(507, 408).click().perform()
    actions.move_by_offset(-507, -408).perform()
    time.sleep(1)
wait = WebDriverWait(driver, 5)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/form[2]')))
element.submit()
set_viewport_size(driver, 1877, 926)
time.sleep(2)
try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
except: pass
try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, 'id("confirmation")')))
    element.click()
except Exception as e:
    # Fallback to coordinates if XPath click fails
    print('Failed to find XPath. Trying coordinate click.')
    actions = ActionChains(driver)
    actions.move_by_offset(454, 621).click().perform()
    actions.move_by_offset(-454, -621).perform()
    time.sleep(1)
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("confirmation")')))
element.clear()
element.send_keys(input_values['input_value_19'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("confirmation")')))
element.clear()
element.send_keys(input_values['input_value_20'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("confirmation")')))
element.clear()
element.send_keys(input_values['input_value_21'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("confirmation")')))
element.clear()
element.send_keys(input_values['input_value_22'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("confirmation")')))
element.clear()
element.send_keys(input_values['input_value_23'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("confirmation")')))
element.clear()
element.send_keys(input_values['input_value_24'])
wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, 'id("confirmation")')))
element.clear()
element.send_keys(input_values['input_value_25'])
set_viewport_size(driver, 1877, 926)
time.sleep(2)
try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
except: pass
try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/form[3]/button')))
    element.click()
except Exception as e:
    # Fallback to coordinates if XPath click fails
    print('Failed to find XPath. Trying coordinate click.')
    actions = ActionChains(driver)
    actions.move_by_offset(390, 687).click().perform()
    actions.move_by_offset(-390, -687).perform()
    time.sleep(1)
wait = WebDriverWait(driver, 5)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/form[3]')))
element.submit()
set_viewport_size(driver, 1877, 926)
time.sleep(2)
try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))
except: pass
try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/div[1]/div[2]/a')))
    element.click()
except Exception as e:
    # Fallback to coordinates if XPath click fails
    print('Failed to find XPath. Trying coordinate click.')
    actions = ActionChains(driver)
    actions.move_by_offset(650, 123).click().perform()
    actions.move_by_offset(-650, -123).perform()
    time.sleep(1)
time.sleep(5)
driver.quit()
