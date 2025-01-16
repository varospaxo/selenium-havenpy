# main.py
import tkinter as tk
from gui import SeleniumScriptGeneratorApp
"""
input 0 = action_type
input 1 = xpath
input 2 = coords
input 3 = viewport
input 4 = timeout
unput 5 = text
input0|input1|input2|input3|input4|input5
"""
def main():
    root = tk.Tk()
    app = SeleniumScriptGeneratorApp(root)
    root.geometry("800x700")
    root.mainloop()

if __name__ == "__main__":
    main()