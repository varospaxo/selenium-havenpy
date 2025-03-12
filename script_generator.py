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
            "import sys\n"
            "import requests\n"
            "import json\n"
            "import logging\n"
            "import os\n"
            "import base64\n"
            "from selenium import webdriver\n"
            "from selenium.webdriver.common.by import By\n"
            "from selenium.webdriver.support.ui import WebDriverWait\n"
            "from selenium.webdriver.support import expected_conditions as EC\n"
            "from selenium.webdriver.common.action_chains import ActionChains\n"
            "from datetime import datetime\n"
            "start_time = datetime.now()\n"
            "start_time = start_time.strftime('%d%m%Y_%H%M%S')\n"
            "print('Start time:', start_time)\n"
            "step=0\n"
            "if not os.path.exists(start_time):\n"
            "    os.makedirs(start_time)\n"
            "logging.basicConfig(\n"
            "filename='run.log',\n"
            "level=logging.INFO,\n"
            "format='%(asctime)s - %(levelname)s - %(message)s')\n"
            "force_clicks=0\n"
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
            "       driver.set_window_size(*window_size)\n"
            "except: pass\n\n"
        )

        script += (
            "def capture_screenshot(filename=None):\n"
            "   if filename:\n"
            "       file_name = filename + '.png' if not filename.endswith('.png') else filename\n"
            "       filepath = os.path.join(start_time, file_name)\n"
            "       driver.save_screenshot(filepath)\n"
            "   else:\n"
            "       current_time = datetime.now()\n"
            "       filename = current_time.strftime('Screenshot-%d%m%y_%H%M%S') + '.png'\n"
            "       filepath = os.path.join(start_time, filename)\n"
            "       driver.save_screenshot(filepath)\n"
            "       time.sleep(1)\n\n"
        )

        script += (
            "def click_action(xpath, vpx, vpy, x, y):\n"
            "   global force_clicks\n"
            "   time.sleep(2)\n"
            """   try: WebDriverWait(driver, 5).until_not(EC.presence_of_element_located((By.XPATH, "//ion-spinner[@id='spinner']")))\n"""
            "   except: pass\n"
            "   try:\n"
            "       if force_clicks > 3:\n"
            "           print('Force clicks exceeded limit. Exiting script.')\n"
            "           logging.info(f'Failed to find XPath: {xpath}. Trying coordinate click.')\n"
            "           sys.exit()\n"
            "       wait = WebDriverWait(driver, 5)\n"
            "       element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))\n"
            "       element.click()\n"
            "       force_clicks=0\n"
            "   except Exception as e:\n"
            "       print(f'Failed to find XPath: {xpath}. Trying coordinate click.')\n"
            "       logging.info(f'Failed to find XPath: {xpath}. Trying coordinate click.')\n"
            "       force_clicks+=1\n"
            "       set_viewport_size(driver, vpx, vpy)\n"
            "       actions = ActionChains(driver)\n"
            "       actions.move_by_offset(x, y).click().perform()\n"
            "       actions.move_by_offset(-(x), -(y)).perform()\n\n"
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
        action_type, xpath, coords, viewport, timeout, text = action
        # print(text)
        variable_name = f"input_value_{index}"
        action_type = action_type.replace("'", '"')
        xpath = xpath.replace("'", '"')
        coords = coords.replace("'", '"')
        viewport = viewport.replace("'", '"')
        timeout = timeout.replace("'", '"')
        
        script = ""
        # Add viewport resize if dimensions are provided
        if action_type == "click":
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
                pass
            else:
                print("Viewport not provided or invalid.")

            if x and y:
                pass
            else:
                print("Coordinates not provided or invalid.")
            script += f"click_action('{xpath}', {width}, {height}, {x}, {y})\n"
           
        elif action_type in ["type", "input"]:
            if timeout == "encoded":
                # Multi-line input
                script += (
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
        elif action_type == "paste":
            if xpath not in ["", " "]:
                script += (
                    f"wait = WebDriverWait(driver, {wait})\n"
                    f"element = wait.until(EC.presence_of_element_located((By.XPATH, '{xpath}')))\n"
                    f"element.clear()\n"
                    f"element.send_keys(Keys.CONTROL, 'v')\n"
                )
            else:
                script += (
                    f"element = driver.switch_to.active_element\n"
                    f"element.clear()\n"
                    f"element.send_keys(Keys.CONTROL, 'v')\n"
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

            try:
                if viewport in condition_map:
                    condition = condition_map[viewport]
                    timeout_value = int(timeout) if isinstance(timeout, (int, str)) else 5
                    script += f"try:\n"
                    script += f"    wait = WebDriverWait(driver, {timeout_value})\n"
                    if coords == "until":
                        if condition in ["text_to_be_present_in_element", "text_to_be_present_in_element_value"]:
                            script += f"    wait.until(EC.{condition}((By.XPATH, '{xpath}'), '{text}'))\n"
                        elif condition == "staleness_of":
                            script += f"    status_element = driver.find_element(By.XPATH, '{xpath}')\n"
                            script += f"    wait.until(EC.{condition}(status_element))\n"
                        elif condition in ["number_of_windows_to_be"]:
                            script += f"    wait.until(EC.{condition}({text}))\n"
                        elif condition in ["element_selection_state_to_be", "element_located_selection_state_to_be"]:
                            script += f"    wait.until(EC.{condition}((By.XPATH, '{xpath}'), {text}))\n"
                        elif condition == "alert_is_present":
                            script += f"    wait.until(EC.{condition}())\n"
                        elif condition in ["title_contains", "title_is", "url_contains", "url_matches", "url_to_be", "url_changes"]:
                            script += f"    wait.until(EC.{condition}('{text}'))\n"
                        elif condition == "new_window_is_opened":
                            script += f"    wait.until(EC.{condition}())\n"
                        elif condition == "frame_to_be_available":
                            script += f"    wait.until(EC.{condition}((By.XPATH, '{xpath}')))\n"
                        else:
                            script += f"    wait.until(EC.{condition}((By.XPATH, '{xpath}')))\n"
                    if coords == "until_not":
                        if condition in ["text_to_be_present_in_element", "text_to_be_present_in_element_value"]:
                            script += f"    wait.until_not(EC.{condition}((By.XPATH, '{xpath}'), '{text}'))\n"
                        elif condition == "staleness_of":
                            script += f"    status_element = driver.find_element(By.XPATH, '{xpath}')\n"
                            script += f"    wait.until_not(EC.{condition}(status_element))\n"
                        elif condition in ["number_of_windows_to_be"]:
                            script += f"    wait.until_not(EC.{condition}({text}))\n"
                        elif condition in ["element_selection_state_to_be", "element_located_selection_state_to_be"]:
                            script += f"    wait.until_not(EC.{condition}((By.XPATH, '{xpath}'), {text}))\n"
                        elif condition == "alert_is_present":
                            script += f"    wait.until_not(EC.{condition}())\n"
                        elif condition in ["title_contains", "title_is", "url_contains", "url_matches", "url_to_be", "url_changes"]:
                            script += f"    wait.until_not(EC.{condition}('{text}'))\n"
                        elif condition == "new_window_is_opened":
                            script += f"    wait.until_not(EC.{condition}())\n"
                        elif condition == "frame_to_be_available":
                            script += f"    wait.until_not(EC.{condition}((By.XPATH, '{xpath}')))\n"
                        else:
                            script += f"    wait.until_not(EC.{condition}((By.XPATH, '{xpath}')))\n"
                    script += "except:\n"
                    script += "    print('Wait condition failed')\n"
                    script += "    logging.info('Wait condition failed')\n"
                else:
                    raise ValueError("Unsupported viewport condition")

            except Exception as e:
                script += f"# Error: {str(e)}\n"

        elif action_type == "request":
            curl_command = base64.b64decode(xpath).decode('utf-8')

                # Extract the HTTP method (default to GET)
            method_match = re.search(r"-X\s+['\"](\w+)['\"]", curl_command)
            if method_match:
                method = method_match.group(1)
            else:
                print("HTTP Method not found")

            # # Override method if --data or --form is present and method is not explicitly defined
            # if method == "GET" and ("--data" in curl_command or "--form" in curl_command):
            #     method = "POST"

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
            if payload == '':
                payload = None

            # Format payload as JSON string if it exists
            if payload:
                try:
                    payload = json.dumps(json.loads(payload), indent=2)
                except json.JSONDecodeError:
                    print("Payload is not valid JSON, skipping payload.")
                    payload = None
            # Generate Python code

            script +=f"url = '{url}'\n"
            script +=f"method = '{method}'\n"
            script +=f"payload_body = '''{payload}'''\n"
            script +=f"payload = json.dumps(json.loads(payload_body))\n"
            script +=f"headers = {json.dumps(headers, indent=2)}\n"
            if payload is not None and headers is not None:
                script +=f"response = requests.request(method, url, headers=headers, data=payload)\n"
            elif payload is not None and headers is None:
                script +=f"response = requests.request(method, url, data=payload)\n"
            elif payload is None and headers is not None:
                script +=f"response = requests.request(method, url, headers=headers)\n"
            else:  # payload is None and headers are absent
                script +=f"response = requests.request(method, url)\n"
            script +=f"print(response.text)\n"
            script +=f"logging.info(response.text)\n"
        
        elif action_type == "log":
            if xpath == "info":
                if coords == "var":
                    script += f"logging.info({viewport})\n"
                else:
                    script += f"logging.info('{viewport}')\n"
            elif xpath == "warning":
                if coords == "var":
                    script += f"logging.warning({viewport})\n"
                else:
                    script += f"logging.warning('{viewport}')\n"
            elif xpath == "error":
                if coords == "var":
                    script += f"logging.error({viewport})\n"
                else:
                    script += f"logging.error('{viewport}')\n"
            elif xpath == "debug":
                if coords == "var":
                    script += f"logging.debug({viewport})\n"
                else:
                    script += f"logging.debug('{viewport}')\n"
            elif xpath == "critical":
                if coords == "var":
                    script += f"logging.critical({viewport})\n"
                else:
                    script += f"logging.critical('{viewport}')\n"
        elif action_type == "scroll":
            script += f"driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')\n"
        elif action_type == "scroll_up":
            script += f"driver.execute_script('window.scrollTo(0, 0)')\n"
        elif action_type == "scroll_to":
            script += f"element = driver.find_element(By.XPATH, '{xpath}')\n"
            script += f"driver.execute_script('arguments[0].scrollIntoView(true);', element)\n"
        elif action_type == "scroll_by":
            if viewport and 'x' in viewport.lower():
                width, height = viewport.lower().split('x')
                width, height = width.strip(), height.strip()
            else:
                width, height = None, None

            if width and height:
                script += f"set_viewport_size(driver, {width}, {height})\n"
            else:
                print("Viewport not provided or invalid.")
            xpath = int(float(xpath))
            coords = int(float(coords))
            script += f"driver.execute_script('window.scrollBy({xpath}, {coords})')\n"
        elif action_type == "hover":
            script += f"element = driver.find_element(By.XPATH, '{xpath}')\n"
            script += f"actions = ActionChains(driver)\n"
            script += f"actions.move_to_element(element).perform()\n"
        elif action_type == "right_click":
            script += f"element = driver.find_element(By.XPATH, '{xpath}')\n"
            script += f"actions = ActionChains(driver)\n"
            script += f"actions.context_click(element).perform()\n"
        elif action_type == "double_click":
            script += f"element = driver.find_element(By.XPATH, '{xpath}')\n"
            script += f"actions = ActionChains(driver)\n"
            script += f"actions.double_click(element).perform()\n"
        elif action_type == "drag_and_drop":
            script += f"source = driver.find_element(By.XPATH,'{xpath}')\n"
            script += f"target = driver.find_element(By.XPATH,'{coords}')\n"
            script += f"actions = ActionChains(driver)\n"
            script += f"actions.drag_and_drop(source, target).perform()\n"
        elif action_type == "drag_and_drop_by":
            script += f"element = driver.find_element(By.XPATH, '{xpath}')\n"
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
            script += f"element = driver.find_element(By.XPATH, '{xpath}')\n"
            script += f"attribute = element.get_attribute('{coords}')\n"
        elif action_type == "get_css_value":
            script += f"element = driver.find_element(By.XPATH, '{xpath}')\n"
            script += f"css_value = element.value_of_css_property('{coords}')\n"
        elif action_type == "get_property":
            script += f"element = driver.find_element(By.XPATH, '{xpath}')\n"
            script += f"property = element.get_property('{coords}')\n"
        elif action_type == "get_text":
            script += f"element = driver.find_element(By.XPATH, '{xpath}')\n"
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
        elif action_type == "step":
            script += f"print((step := step + 1))\n"
        elif action_type == "ss" or action_type == "screenshot":
            if xpath:
                script += f"capture_screenshot('{xpath}')\n"
            else:
                script += f"capture_screenshot()\n"
        return script