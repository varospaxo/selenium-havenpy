import tkinter as tk
from tkinter import messagebox, simpledialog
import base64
import re
import pyperclip

class CurlEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("cURL Editor and Base64 Converter")

        # Input cURL command
        tk.Label(root, text="Input cURL Command:").pack(anchor="w")
        self.curl_entry = tk.Text(root, height=8, width=80)
        self.curl_entry.pack(pady=5)

        # Parse and Edit button
        tk.Button(root, text="Parse cURL", command=self.parse_curl).pack(pady=5)

        # Edit fields
        self.url_label = tk.Label(root, text="URL:")
        self.url_entry = tk.Entry(root, width=80)

        self.headers_label = tk.Label(root, text="Headers (Key: Value):")
        self.headers_text = tk.Text(root, height=8, width=80)

        self.data_label = tk.Label(root, text="Data:")
        self.data_entry = tk.Entry(root, width=80)

        # Convert and Copy buttons
        self.convert_button = tk.Button(root, text="Convert to Base64", command=self.convert_to_base64)
        self.copy_button = tk.Button(root, text="Copy Base64 Data", command=self.copy_to_clipboard)

        self.base64_output = tk.Text(root, height=5, width=80, state="disabled")

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
            # Debugging (optional: remove these later)
            print("Extracted URL:", url)
            print("Extracted Headers:", headers)
            print("Extracted Data:", data)

            # Populate GUI fields
            self.url_label.pack(anchor="w")
            self.url_entry.pack(pady=5)
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)

            self.headers_label.pack(anchor="w")
            self.headers_text.pack(pady=5)
            self.headers_text.delete("1.0", tk.END)
            self.headers_text.insert("1.0", "\n".join(headers))

            self.data_label.pack(anchor="w")
            self.data_entry.pack(pady=5)
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, data)

            self.convert_button.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse cURL command: {e}")

import tkinter as tk
from tkinter import messagebox, simpledialog
import base64
import re
import pyperclip

class CurlEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("cURL Editor and Base64 Converter")

        # Input cURL command
        tk.Label(root, text="Input cURL Command:").pack(anchor="w")
        self.curl_entry = tk.Text(root, height=8, width=80)
        self.curl_entry.pack(pady=5)

        # Parse and Edit button
        tk.Button(root, text="Parse cURL", command=self.parse_curl).pack(pady=5)

        # Edit fields
        self.url_label = tk.Label(root, text="URL:")
        self.url_entry = tk.Entry(root, width=80)

        self.headers_label = tk.Label(root, text="Headers (Key: Value):")
        self.headers_text = tk.Text(root, height=8, width=80)

        self.data_label = tk.Label(root, text="Data:")
        self.data_entry = tk.Entry(root, width=80)

        # Convert and Copy buttons
        self.convert_button = tk.Button(root, text="Convert to Base64", command=self.convert_to_base64)
        self.copy_button = tk.Button(root, text="Copy Base64 Data", command=self.copy_to_clipboard)

        self.base64_output = tk.Text(root, height=5, width=80, state="disabled")

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
            # Debugging (optional: remove these later)
            print("Extracted URL:", url)
            print("Extracted Headers:", headers)
            print("Extracted Data:", data)

            # Populate GUI fields
            self.url_label.pack(anchor="w")
            self.url_entry.pack(pady=5)
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)

            self.headers_label.pack(anchor="w")
            self.headers_text.pack(pady=5)
            self.headers_text.delete("1.0", tk.END)
            self.headers_text.insert("1.0", "\n".join(headers))

            self.data_label.pack(anchor="w")
            self.data_entry.pack(pady=5)
            self.data_entry.delete(0, tk.END)
            self.data_entry.insert(0, data)

            self.convert_button.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse cURL command: {e}")


    def convert_to_base64(self):
        url = self.url_entry.get()
        headers = self.headers_text.get("1.0", tk.END).strip().split("\n")
        data = self.data_entry.get()

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
            self.base64_output.pack(pady=5)

            self.copy_button.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to Base64: {e}")

    def copy_to_clipboard(self):
        base64_data = self.base64_output.get("1.0", tk.END).strip()
        if base64_data:
            pyperclip.copy(base64_data)
            messagebox.showinfo("Copied", "Base64 data copied to clipboard.")
        else:
            messagebox.showerror("Error", "No Base64 data to copy.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurlEditorApp(root)
    root.mainloop()
