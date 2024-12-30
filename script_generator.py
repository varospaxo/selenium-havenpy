import base64
import json
import re

# script_generator.py
class ScriptGenerator:
    DEFAULT_BROWSER = "Chrome"

    def _generate_import_statements(self):
        return (
            "import time\n"
            "import csv\n"
            "import requests\n"
            "import json\n"
            "from selenium import webdriver\n"
            "from selenium.webdriver.common.by import By\n"
            "from selenium.webdriver.support.ui import WebDriverWait\n"
            "from selenium.webdriver.support import expected_conditions as EC\n"
            "from selenium.webdriver.common.action_chains import ActionChains\n"
        )

    def generate_script(self, browser, url, actions, csv_name):
        script = self._generate_import_statements()
        script += "input_values = {}\n"
        script += (
            f"with open('{csv_name}', 'r') as csv_file:\n"
            "    csv_reader = csv.DictReader(csv_file)\n"
            "    for row in csv_reader:\n"
            "        input_values[row['Variable']] = row['Value']\n\n"
        )
        script += f"driver = webdriver.{browser}()\n"
        
        # Add viewport resize function
        script += (
            "try:\n"
            "   def set_viewport_size(driver, width, height):\n"
            "       window_size = driver.execute_script(\"\"\"\n"
            "           return [window.outerWidth - window.innerWidth + arguments[0],\n"
            "                   window.outerHeight - window.innerHeight + arguments[1]];\n"
            "           \"\"\", width, height)\n"
            "       driver.set_window_size(*window_size)\n\n"
            "except: pass\n"
        )
        
        script += f"driver.get('{url}')\n"
        script += self._generate_actions(actions)
        script += "time.sleep(5)\n"
        script += "driver.quit()\n"
        return script

    def _generate_actions(self, actions):
        action_script = ""
        for i, action in enumerate(actions):
            action_script += self._generate_action(i, action)
        return action_script

    def _generate_action(self, index, action):
        wait = 5
        action_type, xpath, coords, viewport, timeout = action
            
        variable_name = f"input_value_{index}"
        action_type = action_type.replace("'", '"')
        xpath = xpath.replace("'", '"')
        coords = coords.replace("'", '"')
        viewport = viewport.replace("'", '"')
        timeout = timeout.replace("'", '"')
        
        script = ""
        # Add viewport resize if dimensions are provided
        if action_type == "click":
            script += (
                f"time.sleep(2)\n"
                f"try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, \"//ion-spinner[@id='spinner']\")))\n"
                "except: pass\n"
                "try:\n"
                f"    wait = WebDriverWait(driver, {wait})\n"
                f"    element = wait.until(EC.element_to_be_clickable((By.XPATH, '{xpath}')))\n"
                "    element.click()\n"
                "except Exception as e:\n"
                "    # Fallback to coordinates if XPath click fails\n"
                    f"    print('Failed to find XPath. Trying coordinate click.')\n" 
            )
            # Parse coordinates and viewport
            if coords and ',' in coords:
                x, y = coords.split(',')
                x, y = x.strip(), y.strip()
            else:
                x, y = None, None
                
            if viewport and 'x' in viewport.lower():
                width, height = viewport.lower().split('x')
                width, height = width.strip(), height.strip()
            else:
                width, height = None, None

            if width and height:
                script += f"    set_viewport_size(driver, {width}, {height})\n"
            else:
                print("Viewport not provided or invalid.")

            if x and y:
                script += (
                    f"    actions = ActionChains(driver)\n"
                    f"    actions.move_by_offset({x}, {y}).click().perform()\n"
                    f"    actions.move_by_offset(-{x}, -{y}).perform()\n"  # Fixed string formatting
                )
            else:
                print("Coordinates not provided or invalid.")
           
        elif action_type in ["type", "input"]:
            if timeout == "encoded":
                # Multi-line input
                script += (
                    f"import base64\n"
                    f"wait = WebDriverWait(driver, {wait})\n"
                    f"element = wait.until(EC.presence_of_element_located((By.XPATH, '{xpath}')))\n"
                    f"element.clear()\n"
                    f"decoded_value = base64.b64decode(input_values['{variable_name}']).decode('utf-8')\n"
                    f"element.send_keys(decoded_value)\n"
                )
            else:
                # Single-line input
                script += (
                    f"wait = WebDriverWait(driver, {wait})\n"
                    f"element = wait.until(EC.presence_of_element_located((By.XPATH, '{xpath}')))\n"
                    f"element.clear()\n"
                    f"element.send_keys(input_values['{variable_name}'])\n"
                )

        elif action_type == "submit":
            script += (
                f"wait = WebDriverWait(driver, {wait})\n"
                f"element = wait.until(EC.element_to_be_clickable((By.XPATH, '{xpath}')))\n"
                f"element.submit()\n"
            )
        elif action_type == "#" or action_type == "comment" or action_type == "":
            script += (
                f"# {xpath}\n"
            )
        elif action_type == "sleep":
            script += (
                f"time.sleep({xpath})\n"
            )
        elif action_type == "wait":
            timeout = timeout if timeout else 5  # Set timeout default if not specified
            script += f"try:\n"
            script += f"    wait = WebDriverWait(driver, {timeout})\n"
            condition_map = {
                "visible": "visibility_of_element_located",
                "invisible": "invisibility_of_element_located",
                "clickable": "element_to_be_clickable",
                "presence": "presence_of_element_located",
                "staleness": "staleness_of",
                "selected": "element_to_be_selected",
                "deselected": "element_to_be_deselected",
                "text_to_be_present": "text_to_be_present_in_element",
                "text_to_be_present_in_value": "text_to_be_present_in_element_value",
                "frame_to_be_available": "frame_to_be_available_and_switch_to_it",
                "alert_is_present": "alert_is_present",
                "title_contains": "title_contains",
                "title_is": "title_is",
                "url_contains": "url_contains",
                "url_matches": "url_matches",
                "url_to_be": "url_to_be",
                "url_changes": "url_changes",
                "number_of_windows_to_be": "number_of_windows_to_be",
                "new_window_is_opened": "new_window_is_opened",
                "element_located_to_be_selected": "element_located_to_be_selected",
                "element_selection_state_to_be": "element_selection_state_to_be",
                "element_located_selection_state_to_be": "element_located_selection_state_to_be"   
            }
            if viewport in condition_map:
                condition = condition_map[viewport]
                if coords == "until":
                    script += f"    wait.until(EC.{condition}((By.XPATH, '{xpath}')))\n"
                elif coords == "until_not":
                    script += f"    wait.until_not(EC.{condition}((By.XPATH, '{xpath}')))\n"
            script += f"except: print('Wait element failed')\n"
        
        elif action_type == "request":
            curl_command = base64.b64decode(xpath).decode('utf-8')

                # Extract the HTTP method (default to GET)
            method_match = re.search(r"-X\s+(\w+)", curl_command)
            method = method_match.group(1) if method_match else "GET"

            # Override method if --data or --form is present and method is not explicitly defined
            if method == "GET" and ("--data" in curl_command or "--form" in curl_command):
                method = "POST"

            # Extract the URL
            url_match = re.search(r"curl --location '(.*?)'", curl_command)
            url = url_match.group(1) if url_match else None

            # Extract headers
            headers = {}
            for header_match in re.finditer(r"--header '(.*?): (.*?)'", curl_command):
                headers[header_match.group(1)] = header_match.group(2) if header_match else None

            # Extract payload
            payload_match = re.search(r"--data '(.*?)'", curl_command, re.DOTALL)
            payload = payload_match.group(1) if payload_match else None

            # Format payload as JSON string if it exists
            if payload:
                try:
                    payload = json.dumps(json.loads(payload), indent=2)
                except json.JSONDecodeError:
                    print("Payload is not valid JSON, skipping payload.")
                    payload = f''

            # Generate Python code
            script +=(
            f"url = '{url}'\n"
            f"method = '{method}'\n"
            f"payload = json.dumps({payload})\n"
            f"headers = {json.dumps(headers, indent=2)}\n"
            )
            if payload is not None and headers is not None:
                script +=f"response = requests.request(method, url, headers=headers, data=payload)\n"
            elif payload is not None and headers is None:
                script +=f"response = requests.request(method, url, data=payload)\n"
            elif payload is None and headers is not None:
                script +=f"response = requests.request(method, url, headers=headers)\n"
            else:  # payload is None and headers are absent
                script +=f"response = requests.request(method, url)\n"
            script +=f"print(response.text)\n"
            
        elif action_type == "scroll":
            script += f"driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')\n"
        elif action_type == "scroll_up":
            script += f"driver.execute_script('window.scrollTo(0, 0)')\n"
        elif action_type == "scroll_to":
            script += f"element = driver.find_element_by_xpath('{xpath}')\n"
            script += f"driver.execute_script('arguments[0].scrollIntoView(true);', element)\n"
        elif action_type == "scroll_by":
            script += f"driver.execute_script('window.scrollBy({xpath}, {coords})')\n"
        elif action_type == "hover":
            script += f"element = driver.find_element_by_xpath('{xpath}')\n"
            script += f"actions = ActionChains(driver)\n"
            script += f"actions.move_to_element(element).perform()\n"
        elif action_type == "right_click":
            script += f"element = driver.find_element_by_xpath('{xpath}')\n"
            script += f"actions = ActionChains(driver)\n"
            script += f"actions.context_click(element).perform()\n"
        elif action_type == "double_click":
            script += f"element = driver.find_element_by_xpath('{xpath}')\n"
            script += f"actions = ActionChains(driver)\n"
            script += f"actions.double_click(element).perform()\n"
        elif action_type == "drag_and_drop":
            script += f"source = driver.find_element_by_xpath('{xpath}')\n"
            script += f"target = driver.find_element_by_xpath('{coords}')\n"
            script += f"actions = ActionChains(driver)\n"
            script += f"actions.drag_and_drop(source, target).perform()\n"
        elif action_type == "drag_and_drop_by":
            script += f"element = driver.find_element_by_xpath('{xpath}')\n"
            script += f"actions = ActionChains(driver)\n"
            script += f"actions.drag_and_drop_by_offset(element, {coords}, {viewport}).perform()\n"
        elif action_type == "accept_alert":
            script += f"driver.switch_to.alert.accept()\n"
        elif action_type == "dismiss_alert":
            script += f"driver.switch_to.alert.dismiss()\n"
        elif action_type == "send_keys_alert":
            script += f"driver.switch_to.alert.send_keys('{xpath}')\n"
        elif action_type == "get_alert_text":
            script += f"alert_text = driver.switch_to.alert.text\n"
        elif action_type == "set_alert_text":
            script += f"driver.execute_script(\"alert('{xpath}')\")\n"
        elif action_type == "get_attribute":
            script += f"element = driver.find_element_by_xpath('{xpath}')\n"
            script += f"attribute = element.get_attribute('{coords}')\n"
        elif action_type == "get_css_value":
            script += f"element = driver.find_element_by_xpath('{xpath}')\n"
            script += f"css_value = element.value_of_css_property('{coords}')\n"
        elif action_type == "get_property":
            script += f"element = driver.find_element_by_xpath('{xpath}')\n"
            script += f"property = element.get_property('{coords}')\n"
        elif action_type == "get_text":
            script += f"element = driver.find_element_by_xpath('{xpath}')\n"
            script += f"text = element.text\n"
        elif action_type == "get_title":
            script += f"title = driver.title\n"
        elif action_type == "get_url":
            script += f"url = driver.current_url\n"
        elif action_type == "get_page_source":
            script += f"page_source = driver.page_source\n"
        elif action_type == "get_cookies":
            script += f"cookies = driver.get_cookies()\n"
        elif action_type == "add_cookie":
            script += f"driver.add_cookie({xpath})\n"
        elif action_type == "delete_cookie":
            script += f"driver.delete_cookie('{xpath}')\n"
        elif action_type == "delete_all_cookies":  
            script += f"driver.delete_all_cookies()\n"
        return script