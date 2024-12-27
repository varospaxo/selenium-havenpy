import os
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

"""
input 0 = action_type
input 1 = xpath
input 2 = coords
input 3 = viewport
input 4 = timeout
input0|input1|input2|input3|input4
"""



class ScriptGenerator:
    DEFAULT_BROWSER = "Chrome"

    def _generate_import_statements(self):
        return (
            "import time\n"
            "import csv\n"
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
            
        variable_name = f"input_value_{index}"
        
        script = ""
        
        # Add viewport resize if dimensions are provided
        if width and height:
            script += f"set_viewport_size(driver, {width}, {height})\n"
        
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
            )

            if x and y:
                script += (
                    f"    print('Failed to find XPath. Trying coordinate click.')\n" 
                    f"    actions = ActionChains(driver)\n"
                    f"    actions.move_by_offset({x}, {y}).click().perform()\n"
                    f"    actions.move_by_offset(-{x}, -{y}).perform()\n"  # Fixed string formatting
                )
            script += "    time.sleep(1)\n"
            
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

        elif action_type == "submit":
            script += (
                f"wait = WebDriverWait(driver, {wait})\n"
                f"element = wait.until(EC.element_to_be_clickable((By.XPATH, '{xpath}')))\n"
                f"element.submit()\n"
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

import tkinter as tk
from tkinter import ttk
import os
import csv

import tkinter as tk
from tkinter import ttk

class SeleniumScriptGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Selenium Script Generator")
        self.root.configure(bg="#f0f0f0")  # Set background color
        
        # Configure grid weights for responsiveness
        for i in range(3):  # Three columns
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(12):  # Configure rows
            self.root.grid_rowconfigure(i, weight=1)

        self.script_generator = ScriptGenerator()

        # Main layout components
        self._create_browser_selection()
        self._create_url_input()
        self._create_help_button()
        self._create_actions_input()
        self._create_prefix_suffix_actions()
        self._create_folder_name_input()
        self._create_script_name_input()
        self._create_buttons_frame()
        self._create_generated_script_output()

    def _create_browser_selection(self):
        browser_label = tk.Label(self.root, text="Select a Browser:", bg="#f0f0f0", font=("Helvetica", 10))
        browser_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.browser_selection_combobox = ttk.Combobox(self.root, textvariable=tk.StringVar(), 
                                                         values=["Chrome", "Firefox"], state="readonly")
        self.browser_selection_combobox.set(ScriptGenerator.DEFAULT_BROWSER)
        self.browser_selection_combobox.grid(row=0, column=1, columnspan=2, sticky="ew", padx=10, pady=5)

    def _create_url_input(self):
        url_label = tk.Label(self.root, text="URL:", bg="#f0f0f0", font=("Helvetica", 10))
        url_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.url_input_entry = tk.Entry(self.root, font=("Helvetica", 10))
        self.url_input_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=10, pady=5)

    def _create_help_button(self):
        try:
            with open('instructions.txt', 'r') as file:
                instructions = file.read()
        except FileNotFoundError:
            instructions = "Instructions file not found. Please ensure 'instructions.txt' exists in the same directory."

        def add_placeholder():
            self.generated_script.delete("1.0", tk.END)
            self.generated_script.insert("1.0", instructions)
            self.url_input_entry.delete(0, tk.END)
            self.url_input_entry.insert(0, "Insert URL here.")
            self.actions_text.delete("1.0", tk.END)
            self.actions_text.insert("1.0", "Insert Actions here.\n")
            self.prefix_actions_text.delete("1.0", tk.END)
            self.prefix_actions_text.insert("1.0", "Insert Prefix Actions here.\n")
            self.suffix_actions_text.delete("1.0", tk.END)
            self.suffix_actions_text.insert("1.0", "Insert Suffix Actions here.\n")
            self.folder_input_entry.delete(0, tk.END)
            self.folder_input_entry.insert(0, "Folder Name")
            self.script_input_entry.delete(0, tk.END)
            self.script_input_entry.insert(0, "Script Name")

        help_button = tk.Button(self.root, text="Help", command=add_placeholder, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        help_button.grid(row=1, column=2, padx=10, pady=5, sticky="e")

    def _create_actions_input(self):
        actions_label = tk.Label(self.root, text="Main Actions:", bg="#f0f0f0", font=("Helvetica", 10))
        actions_label.grid(row=2, column=0, sticky="nw", padx=10, pady=5)

        self.actions_frame = tk.Frame(self.root)
        self.actions_frame.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=10, pady=5)

        self.actions_scrollbar = tk.Scrollbar(self.actions_frame)
        self.actions_text = tk.Text(self.actions_frame, height=6, wrap="word", yscrollcommand=self.actions_scrollbar.set, font=("Helvetica", 10))
        self.actions_scrollbar.config(command=self.actions_text.yview)
        
        self.actions_scrollbar.pack(side="right", fill="y")
        self.actions_text.pack(side="left", fill="both", expand=True)

    def _create_prefix_suffix_actions(self):
        prefix_actions_label = tk.Label(self.root, text="Prefix Actions:", bg="#f0f0f0", font=("Helvetica", 10))
        prefix_actions_label.grid(row=3, column=0, sticky="nw", padx=10, pady=5)

        self.prefix_actions_frame = tk.Frame(self.root)
        self.prefix_actions_frame.grid(row=3, column=1, sticky="nsew", padx=10, pady=5)

        self.prefix_actions_scrollbar = tk.Scrollbar(self.prefix_actions_frame)
        self.prefix_actions_text = tk.Text(self.prefix_actions_frame, height=4, wrap="word", 
                                           yscrollcommand=self.prefix_actions_scrollbar.set, font=("Helvetica", 10))
        self.prefix_actions_scrollbar.config(command=self.prefix_actions_text.yview)
        
        self.prefix_actions_scrollbar.pack(side="right", fill="y")
        self.prefix_actions_text.pack(side="left", fill="both", expand=True)

        suffix_actions_label = tk.Label(self.root, text="Suffix Actions:", bg="#f0f0f0", font=("Helvetica", 10))
        suffix_actions_label.grid(row=4, column=0, sticky="nw", padx=10, pady=5)

        self.suffix_actions_frame = tk.Frame(self.root)
        self.suffix_actions_frame.grid(row=4, column=1, sticky="nsew", padx=10, pady=5)

        self.suffix_actions_scrollbar = tk.Scrollbar(self.suffix_actions_frame)
        self.suffix_actions_text = tk.Text(self.suffix_actions_frame, height=4, wrap="word",
                                           yscrollcommand=self.suffix_actions_scrollbar.set, font=("Helvetica", 10))
        self.suffix_actions_scrollbar.config(command=self.suffix_actions_text.yview)
        
        self.suffix_actions_scrollbar.pack(side="right", fill="y")
        self.suffix_actions_text.pack(side="left", fill="both", expand=True)

    def _create_folder_name_input(self):
        folder_label = tk.Label(self.root, text="Folder Name:", bg="#f0f0f0", font=("Helvetica", 10))
        folder_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        self.folder_input_entry = tk.Entry(self.root, font=("Helvetica", 10))
        self.folder_input_entry.grid(row=5, column=1, columnspan=2, sticky="ew", padx=10, pady=5)

    def _create_script_name_input(self):
        script_label = tk.Label(self.root, text="Script Name:", bg="#f0f0f0", font=("Helvetica", 10))
        script_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)

        self.script_input_entry = tk.Entry(self.root, font=("Helvetica", 10))
        self.script_input_entry.grid(row=6, column=1, columnspan=2, sticky="ew", padx=10, pady=5)

    def _create_buttons_frame(self):
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

        self.generate_button = tk.Button(buttons_frame, text="Generate Script", command=self.generate_and_save_script, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        self.generate_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.reset_button = tk.Button(buttons_frame, text="Reset", command=self._reset_fields, bg="#f44336", fg="white", font=("Helvetica", 10, "bold"))
        self.reset_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def _create_generated_script_output(self):
        output_label = tk.Label(self.root, text="Generated Script:", bg="#f0f0f0", font=("Helvetica", 10))
        output_label.grid(row=8, column=0, sticky="nw", padx=10, pady=5)

        self.output_frame = tk.Frame(self.root)
        self.output_frame.grid(row=8, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        self.output_scrollbar = tk.Scrollbar(self.output_frame)
        self.generated_script = tk.Text(self.output_frame, height=10, wrap="word", 
                                        yscrollcommand=self.output_scrollbar.set, font=("Helvetica", 10))
        self.output_scrollbar.config(command=self.generated_script.yview)

        self.output_scrollbar.pack(side="right", fill="y")
        self.generated_script.pack(side="left", fill="both", expand=True)

    def _reset_fields(self):
        """Reset all input fields to their default state"""
        self.browser_selection_combobox.set(ScriptGenerator.DEFAULT_BROWSER)
        self.url_input_entry.delete(0, tk.END)
        self.actions_text.delete("1.0", tk.END)
        self.prefix_actions_text.delete("1.0", tk.END)
        self.suffix_actions_text.delete("1.0", tk.END)
        self.folder_input_entry.delete(0, tk.END)
        self.script_input_entry.delete(0, tk.END)
        self.generated_script.delete("1.0", tk.END)

    # def generate_and_save_script(self):
    #     selected_browser = self.browser_var.get()
    #     url = self.url_entry.get()
    #     actions_text = self.actions_text.get("1.0", tk.END).strip()
    #     print(actions_text)
    #     action_lines = [line.split('|') for line in actions_text.split('\n') if line.strip()]
    #     actions = []
    #     input_values = []

    def generate_and_save_script(self):
        selected_browser = self.browser_selection_combobox.get()
        url = self.url_input_entry.get()
        actions_text = self.actions_text.get("1.0", tk.END).strip()

        # Variables for text to add
        text_before = f'{self.prefix_actions_text.get("1.0", tk.END).strip()}'
        text_after = f'{self.suffix_actions_text.get("1.0", tk.END).strip()}'

        # Process actions_text to add the lines before and after each action
        modified_actions_text = []
        for line in actions_text.split('\n'):
            if line.strip():  # Ignore empty lines
                modified_line = f"{text_before}\n{line}\n{text_after}"
                modified_actions_text.append(modified_line)

        # Reconstruct actions_text with the modified lines
        actions_text = '\n'.join(modified_actions_text)
        # print("Modified Actions Text:\n", actions_text)

        action_lines = [line.split('|') for line in actions_text.split('\n') if line.strip()]
        actions = []
        input_values = []

        for i, action in enumerate(action_lines):
            action_type = action[0].strip() if len(action) > 0 else ""
            xpath = action[1].strip() if len(action) > 1 else ""
            coords = action[2].strip() if len(action) > 2 else ""
            viewport = action[3].strip() if len(action) > 3 else ""
            timeout = action[4].strip() if len(action) > 4 else ""
            actions.append((action_type, xpath, coords, viewport, timeout))
            if action_type in ["type", "input"]:
                input_values.append((f"input_value_{i}", coords))
        
        collection = "Generated"
        if self.folder_input_entry.get() and self.script_input_entry.get():
            folder_name = self.folder_input_entry.get()
            script_name = self.script_input_entry.get()+".py"
            csv_name = self.script_input_entry.get()+".csv"
            action_list_name = self.script_input_entry.get()+".txt"
        else:
            folder_name = "GeneratedScript"
            script_name = "script.py"
            csv_name = "inputs.csv"
            action_list_name = "actions.txt" 
        folder_path = os.path.join(collection, folder_name)
        
        if selected_browser and url and actions:
            script = self.script_generator.generate_script(selected_browser, url, actions, csv_name)
            self.generated_script.delete("1.0", tk.END)
            self.generated_script.insert(tk.END, script)

            os.makedirs(folder_path, exist_ok=True)

            script_path = os.path.join(folder_path, script_name)
            with open(script_path, "w") as script_file:
                script_file.write(script)

            action_list_path = os.path.join(folder_path, action_list_name)
            with open(action_list_path, "w") as action_list_file:
                for action in actions:
                    # Join the action tuple into a string and write it to the file
                    action_line = '|'.join(action)  # Join using '|' or any separator you want
                    action_list_file.write(action_line + "\n")

            csv_path = os.path.join(folder_path, csv_name)
            with open(csv_path, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Variable", "Value"])
                csv_writer.writerows(input_values)

            self.generated_script.insert(tk.END, f"\nScript saved to {script_path}\nCSV saved to {csv_path}\nAction list saved to {action_list_path}")
        else:
            self.generated_script.delete("1.0", tk.END)
            self.generated_script.insert(tk.END, "Please select a browser, enter a URL, and define actions.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SeleniumScriptGeneratorApp(root)
    root.geometry("800x700")  # Set initial size
    root.mainloop()