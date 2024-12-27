# gui.py
import tkinter as tk
from tkinter import ttk
import os
import csv
from script_generator import ScriptGenerator

class SeleniumScriptGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Selenium Script Generator")
        self.root.configure(bg="#f0f0f0")
        
        # Main container frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid weights for main frame
        self.main_frame.grid_columnconfigure(1, weight=1)  # Make middle column expandable
        self.main_frame.grid_columnconfigure(2, weight=0)  # Keep right column fixed
        
        self.script_generator = ScriptGenerator()

        # Initialize UI components
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
        browser_label = tk.Label(self.main_frame, text="Select a Browser:", bg="#f0f0f0", font=("Helvetica", 10))
        browser_label.grid(row=0, column=0, sticky="w", pady=5)

        self.browser_selection_combobox = ttk.Combobox(self.main_frame, textvariable=tk.StringVar(), 
                                                     values=["Chrome", "Firefox"], state="readonly")
        self.browser_selection_combobox.set(ScriptGenerator.DEFAULT_BROWSER)
        self.browser_selection_combobox.grid(row=0, column=1, columnspan=2, sticky="ew", pady=5)

    def _create_url_input(self):
        url_label = tk.Label(self.main_frame, text="URL:", bg="#f0f0f0", font=("Helvetica", 10))
        url_label.grid(row=1, column=0, sticky="w", pady=5)

        self.url_input_entry = tk.Entry(self.main_frame, font=("Helvetica", 10))
        self.url_input_entry.grid(row=1, column=1, sticky="ew", pady=5)

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

        help_button = tk.Button(self.main_frame, text="Help", command=add_placeholder, 
                              bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        help_button.grid(row=1, column=2, pady=5, padx=(5, 0))

    def _create_actions_input(self):
        actions_label = tk.Label(self.main_frame, text="Main Actions:", bg="#f0f0f0", font=("Helvetica", 10))
        actions_label.grid(row=2, column=0, sticky="nw", pady=5)

        # Frame for actions with proper weight configuration
        self.actions_frame = tk.Frame(self.main_frame)
        self.actions_frame.grid(row=2, column=1, columnspan=2, sticky="nsew", pady=5)
        self.actions_frame.grid_columnconfigure(0, weight=1)
        self.actions_frame.grid_rowconfigure(0, weight=1)

        # Create text widget and scrollbar with increased height
        self.actions_text = tk.Text(self.actions_frame, height=12, wrap="none", font=("Helvetica", 10))  # Increased height from 6 to 12
        self.actions_h_scrollbar = tk.Scrollbar(self.actions_frame, orient="horizontal", command=self.actions_text.xview)
        self.actions_v_scrollbar = tk.Scrollbar(self.actions_frame, orient="vertical", command=self.actions_text.yview)
        self.actions_text.configure(xscrollcommand=self.actions_h_scrollbar.set, 
                                  yscrollcommand=self.actions_v_scrollbar.set)

        # Grid layout for text widget and scrollbars
        self.actions_text.grid(row=0, column=0, sticky="nsew")
        self.actions_h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.actions_v_scrollbar.grid(row=0, column=1, sticky="ns")

        # Give more weight to the actions row
        self.main_frame.grid_rowconfigure(2, weight=2)  # Increased weight for actions row

    def _create_prefix_suffix_actions(self):
        # Similar pattern for prefix actions
        prefix_actions_label = tk.Label(self.main_frame, text="Prefix Actions:", bg="#f0f0f0", font=("Helvetica", 10))
        prefix_actions_label.grid(row=3, column=0, sticky="nw", pady=5)

        self.prefix_actions_frame = tk.Frame(self.main_frame)
        self.prefix_actions_frame.grid(row=3, column=1, columnspan=2, sticky="nsew", pady=5)
        self.prefix_actions_frame.grid_columnconfigure(0, weight=1)
        self.prefix_actions_frame.grid_rowconfigure(0, weight=1)

        self.prefix_actions_text = tk.Text(self.prefix_actions_frame, height=4, wrap="none", font=("Helvetica", 10))
        self.prefix_h_scrollbar = tk.Scrollbar(self.prefix_actions_frame, orient="horizontal", 
                                             command=self.prefix_actions_text.xview)
        self.prefix_v_scrollbar = tk.Scrollbar(self.prefix_actions_frame, orient="vertical", 
                                             command=self.prefix_actions_text.yview)
        self.prefix_actions_text.configure(xscrollcommand=self.prefix_h_scrollbar.set, 
                                        yscrollcommand=self.prefix_v_scrollbar.set)

        self.prefix_actions_text.grid(row=0, column=0, sticky="nsew")
        self.prefix_h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.prefix_v_scrollbar.grid(row=0, column=1, sticky="ns")

        # Similar pattern for suffix actions
        suffix_actions_label = tk.Label(self.main_frame, text="Suffix Actions:", bg="#f0f0f0", font=("Helvetica", 10))
        suffix_actions_label.grid(row=4, column=0, sticky="nw", pady=5)

        self.suffix_actions_frame = tk.Frame(self.main_frame)
        self.suffix_actions_frame.grid(row=4, column=1, columnspan=2, sticky="nsew", pady=5)
        self.suffix_actions_frame.grid_columnconfigure(0, weight=1)
        self.suffix_actions_frame.grid_rowconfigure(0, weight=1)

        self.suffix_actions_text = tk.Text(self.suffix_actions_frame, height=4, wrap="none", font=("Helvetica", 10))
        self.suffix_h_scrollbar = tk.Scrollbar(self.suffix_actions_frame, orient="horizontal", 
                                             command=self.suffix_actions_text.xview)
        self.suffix_v_scrollbar = tk.Scrollbar(self.suffix_actions_frame, orient="vertical", 
                                             command=self.suffix_actions_text.yview)
        self.suffix_actions_text.configure(xscrollcommand=self.suffix_h_scrollbar.set, 
                                        yscrollcommand=self.suffix_v_scrollbar.set)

        self.suffix_actions_text.grid(row=0, column=0, sticky="nsew")
        self.suffix_h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.suffix_v_scrollbar.grid(row=0, column=1, sticky="ns")

    def _create_folder_name_input(self):
        folder_label = tk.Label(self.main_frame, text="Folder Name:", bg="#f0f0f0", font=("Helvetica", 10))
        folder_label.grid(row=5, column=0, sticky="w", pady=5)

        self.folder_input_entry = tk.Entry(self.main_frame, font=("Helvetica", 10))
        self.folder_input_entry.grid(row=5, column=1, columnspan=2, sticky="ew", pady=5)

    def _create_script_name_input(self):
        script_label = tk.Label(self.main_frame, text="Script Name:", bg="#f0f0f0", font=("Helvetica", 10))
        script_label.grid(row=6, column=0, sticky="w", pady=5)

        self.script_input_entry = tk.Entry(self.main_frame, font=("Helvetica", 10))
        self.script_input_entry.grid(row=6, column=1, columnspan=2, sticky="ew", pady=5)

    def _create_buttons_frame(self):
        buttons_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        buttons_frame.grid(row=7, column=0, columnspan=3, pady=10, sticky="ew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

        self.generate_button = tk.Button(buttons_frame, text="Generate Script", 
                                       command=self.generate_and_save_script,
                                       bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        self.generate_button.grid(row=0, column=0, padx=5, sticky="ew")

        self.reset_button = tk.Button(buttons_frame, text="Reset", command=self._reset_fields,
                                    bg="#f44336", fg="white", font=("Helvetica", 10, "bold"))
        self.reset_button.grid(row=0, column=1, padx=5, sticky="ew")

    def _create_generated_script_output(self):
        output_label = tk.Label(self.main_frame, text="Generated Script:", bg="#f0f0f0", font=("Helvetica", 10))
        output_label.grid(row=8, column=0, sticky="nw", pady=5)

        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.grid(row=8, column=0, columnspan=3, sticky="nsew", pady=5)
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)

        self.generated_script = tk.Text(self.output_frame, height=10, wrap="none", font=("Helvetica", 10))
        self.output_h_scrollbar = tk.Scrollbar(self.output_frame, orient="horizontal", 
                                             command=self.generated_script.xview)
        self.output_v_scrollbar = tk.Scrollbar(self.output_frame, orient="vertical", 
                                             command=self.generated_script.yview)
        self.generated_script.configure(xscrollcommand=self.output_h_scrollbar.set,
                                     yscrollcommand=self.output_v_scrollbar.set)

        self.generated_script.grid(row=0, column=0, sticky="nsew")
        self.output_h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.output_v_scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure row weight for output frame
        self.main_frame.grid_rowconfigure(8, weight=1)

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

        # Process actions
        text_before = self.prefix_actions_text.get("1.0", tk.END).strip()
        text_after = self.suffix_actions_text.get("1.0", tk.END).strip()

        modified_actions_text = []
        for line in actions_text.split('\n'):
            if line.strip():
                modified_line = f"{text_before}\n{line}\n{text_after}"
                modified_actions_text.append(modified_line)

        actions_text = '\n'.join(modified_actions_text)
        action_lines = [line.split('|') for line in actions_text.split('\n') if line.strip()]
        
        # Process actions and save files
        self._process_and_save_files(selected_browser, url, action_lines)

    def _process_and_save_files(self, selected_browser, url, action_lines):
        actions = []
        input_values = []

        for i, action in enumerate(action_lines):
            action_tuple = self._process_action_line(action)
            actions.append(action_tuple)
            if action_tuple[0] in ["type", "input"]:
                input_values.append((f"input_value_{i}", action_tuple[2]))

        self._save_generated_files(selected_browser, url, actions, input_values)

    def _process_action_line(self, action):
        action_type = action[0].strip() if len(action) > 0 else ""
        xpath = action[1].strip() if len(action) > 1 else ""
        coords = action[2].strip() if len(action) > 2 else ""
        viewport = action[3].strip() if len(action) > 3 else ""
        timeout = action[4].strip() if len(action) > 4 else ""
        return (action_type, xpath, coords, viewport, timeout)

    def _save_generated_files(self, selected_browser, url, actions, input_values):
        # Get file paths
        folder_path, script_name, csv_name, action_list_name = self._get_file_paths()
        
        if selected_browser and url and actions:
            # Generate and save script
            script = self.script_generator.generate_script(selected_browser, url, actions, csv_name)
            self._save_files(folder_path, script_name, csv_name, action_list_name,
                           script, actions, input_values)
            self._update_output(folder_path, script_name, csv_name, action_list_name, script)
        else:
            self.generated_script.delete("1.0", tk.END)
            self.generated_script.insert(tk.END, "Please select a browser, enter a URL, and define actions.")

    def _get_file_paths(self):
        collection = "Generated"
        if self.folder_input_entry.get() and self.script_input_entry.get():
            folder_name = self.folder_input_entry.get()
            script_name = f"{self.script_input_entry.get()}.py"
            csv_name = f"{self.script_input_entry.get()}.csv"
            action_list_name = f"{self.script_input_entry.get()}.txt"
        else:
            folder_name = "GeneratedScript"
            script_name = "script.py"
            csv_name = "inputs.csv"
            action_list_name = "actions.txt"
        
        folder_path = os.path.join(collection, folder_name)
        return folder_path, script_name, csv_name, action_list_name

    def _save_files(self, folder_path, script_name, csv_name, action_list_name,
                   script, actions, input_values):
        os.makedirs(folder_path, exist_ok=True)
        
        # Save script
        with open(os.path.join(folder_path, script_name), "w") as script_file:
            script_file.write(script)
        
        # Save action list
        with open(os.path.join(folder_path, action_list_name), "w") as action_list_file:
            for action in actions:
                action_list_file.write('|'.join(action) + "\n")
        
        # Save CSV
        with open(os.path.join(folder_path, csv_name), "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Variable", "Value"])
            csv_writer.writerows(input_values)

    def _update_output(self, folder_path, script_name, csv_name, action_list_name, script):
        self.generated_script.delete("1.0", tk.END)
        self.generated_script.insert(tk.END, f"Files saved successfully:\n")
        self.generated_script.insert(tk.END, f"Script: {os.path.join(folder_path, script_name)}\n")
        self.generated_script.insert(tk.END, f"CSV: {os.path.join(folder_path, csv_name)}\n")
        self.generated_script.insert(tk.END, f"Action list: {os.path.join(folder_path, action_list_name)}\n")
        self.generated_script.insert(tk.END, f"\nGenerated script:\n{script}")