import tkinter as tk
from tkinter import messagebox
import base64
import re
import pyperclip
from gui import SeleniumScriptGeneratorApp as sa
import json

import tkinter as tk

class CurlEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("cURL Editor and Base64 Converter")

        # Configure grid layout
        self.root.rowconfigure(1, weight=1)  # cURL input box
        self.root.rowconfigure(6, weight=1)  # Headers input box
        self.root.rowconfigure(8, weight=1)  # Data input box
        self.root.rowconfigure(10, weight=1)  # Base64 output box
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        # Input cURL command
        tk.Label(root, text="Input cURL Command:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.curl_entry = tk.Text(root, height=5, wrap="word")
        self.curl_entry.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Parse button
        tk.Button(root, text="Parse cURL", command=self.parse_curl).grid(row=2, column=0, columnspan=2, pady=5)

        # Editable fields
        self.url_label = tk.Label(root, text="URL:")
        self.url_label.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.url_entry = tk.Entry(root)
        self.url_entry.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=2)

        self.headers_label = tk.Label(root, text="Headers (Key: Value):")
        self.headers_label.grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.headers_text = tk.Text(root, height=8, wrap="word")
        self.headers_text.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.data_label = tk.Label(root, text="Data:")
        self.data_label.grid(row=7, column=0, sticky="w", padx=5, pady=2)
        self.data_entry = tk.Text(root, height=6, wrap="word")
        self.data_entry.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=5, pady=2)

        # Convert, Copy, and Add to Actions buttons
        self.convert_button = tk.Button(root, text="Convert to Action Format", command=self.convert_to_base64)
        self.convert_button.grid(row=9, column=0, pady=5)

        self.copy_button = tk.Button(root, text="Copy Action", command=self.copy_to_clipboard)
        self.copy_button.grid(row=9, column=1, pady=5)

        # Base64 output
        self.base64_output = tk.Text(root, height=5, wrap="word", state="disabled")
        self.base64_output.grid(row=10, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Adjust column configuration for responsiveness
        for col in range(2):
            root.columnconfigure(col, weight=1)


    def parse_curl(self):
        curl_command = self.curl_entry.get("1.0", tk.END).strip()
        if not curl_command:
            messagebox.showerror("Error", "Please enter a valid cURL command.")
            return

        try:
            # Extract URL
            url_match = re.search(r"--location '(.*?)'", curl_command)
            url = url_match.group(1) if url_match else ""

            # Extract Headers
            headers = re.findall(r"--header\s+'([^']+)'", curl_command)

            # Extract Data
            data_match = re.search(r"--data\s+'([^']+)'", curl_command, re.DOTALL)
            data = data_match.group(1) if data_match else ""
            # data = json.dumps(data)

            # Populate GUI fields
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)

            self.headers_text.delete("1.0", tk.END)
            self.headers_text.insert("1.0", "\n".join(headers))

            self.data_entry.delete("1.0", tk.END)
            self.data_entry.insert("1.0", data)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse cURL command: {e}")

    def convert_to_base64(self):
        url = self.url_entry.get()
        headers = self.headers_text.get("1.0", tk.END).strip().split("\n")
        data = self.data_entry.get("1.0", tk.END)

        if not url:
            messagebox.showerror("Error", "URL cannot be empty.")
            return

        try:
            # Construct the cURL command
            curl_command = f"curl --location '{url}'"

            # Add headers
            for header in headers:
                curl_command += f" --header '{header.strip()}'"

            # Add data if available
            if data:
                curl_command += f" --data '{data.strip()}'"

            # Encode the cURL command to Base64
            base64_data = base64.b64encode(curl_command.encode("utf-8")).decode("utf-8")

            # Display Base64 output
            self.base64_output.config(state="normal")
            self.base64_output.delete("1.0", tk.END)
            self.base64_output.insert("1.0", base64_data)
            self.base64_output.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to Base64: {e}")

    def copy_to_clipboard(self):
        base64_data = self.base64_output.get("1.0", tk.END).strip()
        if base64_data:
            pyperclip.copy("request|"+base64_data)
            messagebox.showinfo("Copied", "Base64 data copied to clipboard.")
        else:
            messagebox.showerror("Error", "No Base64 data to copy.")

    # def add_to_actions(self):
    #     sa.hehe.actions_text.insert(tk.END, self.base64_output.get("1.0", tk.END))
    

if __name__ == "__main__":
    root = tk.Tk()
    app = CurlEditorApp(root)
    root.mainloop()