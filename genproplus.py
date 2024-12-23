import os
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


"""HELP
click - click|XPath|Coordinates|Resolution
input - input|XPath|text
submit - submit|XPath(form)
sleep - sleep|seconds
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
        action_type, xpath, coords, viewport = action
        
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
                    f"    actions = ActionChains(driver)\n"
                    f"    actions.move_by_offset({x}, {y}).click().perform()\n"
                    f"    actions.move_by_offset(-{x}, -{y}).perform()\n"  # Fixed string formatting
                )
            script += "    time.sleep(1)\n"
            
        elif action_type in ["type", "input"]:
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
        return script

import tkinter as tk
from tkinter import ttk
import os
import csv

class SeleniumScriptGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Selenium Script Generator")
        # self.root.geometry("800x400")

        self.script_generator = ScriptGenerator()

        self._create_browser_selection()
        self._create_url_input()
        self._create_actions_input()
        self._create_folder_name_input()
        self._create_script_name_input()
        self._create_generate_button()
        self._create_generated_script_output()

    def _create_browser_selection(self):
        browser_label = tk.Label(self.root, text="Select a Browser:")
        browser_label.pack(anchor="w", padx=10, pady=5)

        self.browser_var = tk.StringVar()
        self.browser_var.set(ScriptGenerator.DEFAULT_BROWSER)
        browser_option = ttk.Combobox(self.root, textvariable=self.browser_var, values=["Chrome", "Firefox"])
        browser_option.pack(fill="x", padx=10)

    def _create_url_input(self):
        url_label = tk.Label(self.root, text="URL:")
        url_label.pack(anchor="w", padx=10, pady=5)

        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack(fill="x", padx=10)

    def _create_actions_input(self):
        actions_label = tk.Label(self.root, text="Actions (One per line in format 'action|XPath|Coordinates|Resolution'):")
        actions_label.pack(anchor="w", padx=10, pady=5)

        self.actions_frame = tk.Frame(self.root)
        self.actions_frame.pack(fill="both", expand=True, padx=10, pady=5)

        actions_scrollbar = tk.Scrollbar(self.actions_frame, orient="vertical")
        self.actions_text = tk.Text(self.actions_frame, height=6, wrap="word", yscrollcommand=actions_scrollbar.set)
        actions_scrollbar.config(command=self.actions_text.yview)
        actions_scrollbar.pack(side="right", fill="y")
        self.actions_text.pack(fill="both", expand=True)

    def _create_folder_name_input(self):
        folder_label = tk.Label(self.root, text="Folder Name:")
        folder_label.pack(anchor="w", padx=10, pady=5)

        self.folder_entry = tk.Entry(self.root)
        self.folder_entry.pack(fill="x", padx=10, pady=5)

    def _create_script_name_input(self):
        script_label = tk.Label(self.root, text="Script Name:")
        script_label.pack(anchor="w", padx=10, pady=5)

        self.script_entry = tk.Entry(self.root)
        self.script_entry.pack(fill="x", padx=10, pady=5)

    def _create_generate_button(self):
        generate_button = tk.Button(self.root, text="Generate Script", command=self.generate_and_save_script)
        generate_button.pack(pady=10)

    def _create_generated_script_output(self):
        output_label = tk.Label(self.root, text="Generated Script:")
        output_label.pack(anchor="w", padx=10, pady=5)

        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=5)

        output_scrollbar = tk.Scrollbar(self.output_frame, orient="vertical")
        self.generated_script = tk.Text(self.output_frame, height=6, wrap="word", yscrollcommand=output_scrollbar.set)
        output_scrollbar.config(command=self.generated_script.yview)
        output_scrollbar.pack(side="right", fill="y")
        self.generated_script.pack(fill="both", expand=True)

    def generate_and_save_script(self):
        selected_browser = self.browser_var.get()
        url = self.url_entry.get()
        actions_text = self.actions_text.get("1.0", tk.END).strip()
        action_lines = [line.split('|') for line in actions_text.split('\n') if line.strip()]
        actions = []
        input_values = []

        for i, action in enumerate(action_lines):
            action_type = action[0].strip() if len(action) > 0 else ""
            xpath = action[1].strip() if len(action) > 1 else ""
            coords = action[2].strip() if len(action) > 2 else ""
            viewport = action[3].strip() if len(action) > 3 else ""
            actions.append((action_type, xpath, coords, viewport))
            if action_type in ["type", "input"]:
                input_values.append((f"input_value_{i}", coords))
        
        collection = "Generated"
        if self.folder_entry.get() and self.script_entry.get():
            folder_name = self.folder_entry.get()
            script_name = self.script_entry.get()+".py"
            csv_name = self.script_entry.get()+".csv"
            action_list_name = self.script_entry.get()+".txt"
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
    root.geometry("600x700")
    root.mainloop()