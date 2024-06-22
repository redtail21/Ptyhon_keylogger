import tkinter as tk
from tkinter import filedialog, messagebox
from pynput import keyboard
from datetime import datetime

class KeyLoggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Logger")
        
        self.text_area = tk.Text(root, wrap='word', height=20, width=50)
        self.text_area.pack(padx=10, pady=10)
        
        self.start_button = tk.Button(root, text="Start Logging", command=self.start_logging)
        self.start_button.pack(side=tk.LEFT, padx=(10, 0))
        
        self.stop_button = tk.Button(root, text="Stop Logging", command=self.stop_logging)
        self.stop_button.pack(side=tk.LEFT, padx=(10, 0))
        
        self.display_button = tk.Button(root, text="Display Output", command=self.display_output)
        self.display_button.pack(side=tk.LEFT, padx=(10, 0))
        
        self.save_button = tk.Button(root, text="Save to File", command=self.save_to_file)
        self.save_button.pack(side=tk.LEFT, padx=(10, 0))
        
        self.timestamp_var = tk.BooleanVar(value=True)
        self.timestamp_checkbutton = tk.Checkbutton(root, text="Include Timestamps", variable=self.timestamp_var)
        self.timestamp_checkbutton.pack(side=tk.LEFT, padx=(10, 0))
        
        self.listener = None

    def start_logging(self):
        if self.listener is None:
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
        
    def stop_logging(self):
        if self.listener is not None:
            self.listener.stop()
            self.listener = None

    def on_press(self, key):
        if self.timestamp_var.get():
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                self.text_area.insert(tk.END, f'{timestamp}: {key.char}\n')
            except AttributeError:
                self.text_area.insert(tk.END, f'{timestamp}: {key}\n')
        else:
            try:
                self.text_area.insert(tk.END, f'{key.char}\n')
            except AttributeError:
                self.text_area.insert(tk.END, f'{key}\n')
    
    def display_output(self):
        output_window = tk.Toplevel(self.root)
        output_window.title("Logged Keys")
        
        output_text_area = tk.Text(output_window, wrap='word', height=20, width=50)
        output_text_area.pack(padx=10, pady=10)
        
        output_text_area.insert(tk.END, self.text_area.get("1.0", tk.END))

    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.text_area.get("1.0", tk.END))
                messagebox.showinfo("Success", "Log saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerGUI(root)
    root.mainloop()
