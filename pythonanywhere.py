from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# List of account credentials
# List of account credentials
accounts = [
    {"username": "u1", "password": "p1"},
    {"username": "u2", "password": "p2"},
    {"username": "u3", "password": "p3"},
    {"username": "u4", "password": "p4"}
]

# Loop through each account
for account in accounts:
    # Initialize the Chrome driver with options
    driver = webdriver.Chrome(options=chrome_options)

    # Open the PythonAnywhere login page
    driver.get("https://www.pythonanywhere.com/login/")

    try:
        # Wait until the username field is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "auth-username"))
        )

        # Enter the username
        username_field = driver.find_element(By.NAME, "auth-username")
        username_field.send_keys(account["username"])

        # Enter the password
        password_field = driver.find_element(By.NAME, "auth-password")
        password_field.send_keys(account["password"])
        password_field.send_keys(Keys.RETURN)

        # Wait for a successful login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "navbar"))
        )
        print ("Login Successful for user:", account["username"])
        
        # Navigate to the webapps page
        driver.get(f"https://www.pythonanywhere.com/user/{account['username']}/webapps/")

        # Wait for and click the "Run until 3 months from today" button
        extend_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "webapp_extend"))
        )
        extend_button.click()
        print ("Webapp extended for user:", account["username"])
        
        # Navigate to tasks page
        driver.get(f"https://www.pythonanywhere.com/user/{account['username']}/tasks_tab/")

        # Wait for and click the "Extend Expiry" button
        expiry_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "extend_scheduled_task"))
        )
        expiry_button.click()
        print ("Scheduled Task extended for user:", account["username"])
        
        # Log out
        logout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "logout_link"))
        )
        logout_button.click()

        print ("Logout successful for user:", account["username"])

    except Exception as e:
        print(f"An error occurred with account {account['username']}: {e}")
    
    finally:
        # Close the browser instance for this account
        driver.quit()

print("Process completed for all accounts.")
