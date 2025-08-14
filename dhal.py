import tkinter as tk
from tkinter import ttk, messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Python")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.current_number = ""
        self.first_number = 0
        self.operation = ""
        self.should_reset = False
        
        # Create display
        self.create_display()
        
        # Create buttons
        self.create_buttons()
        
        # Style configuration
        self.style_buttons()
    
    def create_display(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg="#f0f0f0", height=100)
        display_frame.pack(fill="x", padx=10, pady=10)
        
        # Display label
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#333333",
            anchor="e",
            padx=20,
            pady=20,
            relief="sunken",
            bd=2
        )
        self.display.pack(fill="both", expand=True)
    
    def create_buttons(self):
        # Button frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        
        # Button definitions
        buttons = [
            ("C", 0, 0, "#ff6b6b"), ("±", 0, 1, "#ffa726"), ("%", 0, 2, "#ffa726"), ("÷", 0, 3, "#ff9800"),
            ("7", 1, 0, "#e0e0e0"), ("8", 1, 1, "#e0e0e0"), ("9", 1, 2, "#e0e0e0"), ("×", 1, 3, "#ff9800"),
            ("4", 2, 0, "#e0e0e0"), ("5", 2, 1, "#e0e0e0"), ("6", 2, 2, "#e0e0e0"), ("-", 2, 3, "#ff9800"),
            ("1", 3, 0, "#e0e0e0"), ("2", 3, 1, "#e0e0e0"), ("3", 3, 2, "#e0e0e0"), ("+", 3, 3, "#ff9800"),
            ("0", 4, 0, "#e0e0e0", 2), (".", 4, 2, "#e0e0e0"), ("=", 4, 3, "#4caf50"),
            ("√", 5, 0, "#2196f3"), ("x²", 5, 1, "#2196f3"), ("1/x", 5, 2, "#2196f3"), ("⌫", 5, 3, "#ff6b6b")
        ]
        
        # Create buttons
        for button_info in buttons:
            if len(button_info) == 5:  # Button with colspan
                text, row, col, color, colspan = button_info
                btn = tk.Button(
                    button_frame,
                    text=text,
                    font=("Arial", 16, "bold"),
                    bg=color,
                    fg="white" if color in ["#ff6b6b", "#ff9800", "#4caf50", "#2196f3"] else "#333333",
                    relief="flat",
                    bd=0,
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2, sticky="nsew")
            else:
                text, row, col, color = button_info
                btn = tk.Button(
                    button_frame,
                    text=text,
                    font=("Arial", 16, "bold"),
                    bg=color,
                    fg="white" if color in ["#ff6b6b", "#ff9800", "#4caf50", "#2196f3"] else "#333333",
                    relief="flat",
                    bd=0,
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
    
    def style_buttons(self):
        # Add hover effects
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button):
                        child.bind("<Enter>", lambda e, btn=child: self.on_hover(btn, True))
                        child.bind("<Leave>", lambda e, btn=child: self.on_hover(btn, False))
    
    def on_hover(self, button, entering):
        if entering:
            # Darken the button
            current_bg = button.cget("bg")
            if current_bg == "#e0e0e0":
                button.configure(bg="#d0d0d0")
            elif current_bg == "#ff6b6b":
                button.configure(bg="#ff5252")
            elif current_bg == "#ff9800":
                button.configure(bg="#ff8c00")
            elif current_bg == "#4caf50":
                button.configure(bg="#45a049")
            elif current_bg == "#2196f3":
                button.configure(bg="#1976d2")
        else:
            # Restore original color
            button.configure(bg=button.master.children[button].cget("bg"))
    
    def button_click(self, value):
        if value.isdigit() or value == ".":
            self.handle_number(value)
        elif value in ["+", "-", "×", "÷"]:
            self.handle_operation(value)
        elif value == "=":
            self.calculate()
        elif value == "C":
            self.clear()
        elif value == "±":
            self.toggle_sign()
        elif value == "%":
            self.percentage()
        elif value == "√":
            self.square_root()
        elif value == "x²":
            self.square()
        elif value == "1/x":
            self.reciprocal()
        elif value == "⌫":
            self.backspace()
    
    def handle_number(self, number):
        if self.should_reset:
            self.current_number = ""
            self.should_reset = False
        
        if number == "." and "." in self.current_number:
            return
        
        self.current_number += number
        self.update_display()
    
    def handle_operation(self, op):
        if self.current_number:
            if self.operation and not self.should_reset:
                self.calculate()
            
            self.first_number = float(self.current_number)
            self.operation = op
            self.should_reset = True
        elif self.operation and not self.should_reset:
            self.operation = op
    
    def calculate(self):
        if not self.current_number or not self.operation:
            return
        
        second_number = float(self.current_number)
        result = 0
        
        try:
            if self.operation == "+":
                result = self.first_number + second_number
            elif self.operation == "-":
                result = self.first_number - second_number
            elif self.operation == "×":
                result = self.first_number * second_number
            elif self.operation == "÷":
                if second_number == 0:
                    messagebox.showerror("Error", "Tidak bisa membagi dengan nol!")
                    return
                result = self.first_number / second_number
            
            # Format result
            if result.is_integer():
                self.current_number = str(int(result))
            else:
                self.current_number = str(result)
            
            self.update_display()
            self.operation = ""
            self.should_reset = True
            
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    
    def clear(self):
        self.current_number = ""
        self.first_number = 0
        self.operation = ""
        self.should_reset = False
        self.display_var.set("0")
    
    def toggle_sign(self):
        if self.current_number:
            if self.current_number.startswith("-"):
                self.current_number = self.current_number[1:]
            else:
                self.current_number = "-" + self.current_number
            self.update_display()
    
    def percentage(self):
        if self.current_number:
            try:
                result = float(self.current_number) / 100
                if result.is_integer():
                    self.current_number = str(int(result))
                else:
                    self.current_number = str(result)
                self.update_display()
            except:
                messagebox.showerror("Error", "Input tidak valid!")
    
    def square_root(self):
        if self.current_number:
            try:
                number = float(self.current_number)
                if number < 0:
                    messagebox.showerror("Error", "Tidak bisa menghitung akar dari bilangan negatif!")
                    return
                
                result = math.sqrt(number)
                if result.is_integer():
                    self.current_number = str(int(result))
                else:
                    self.current_number = str(result)
                self.update_display()
            except:
                messagebox.showerror("Error", "Input tidak valid!")
    
    def square(self):
        if self.current_number:
            try:
                result = float(self.current_number) ** 2
                if result.is_integer():
                    self.current_number = str(int(result))
                else:
                    self.current_number = str(result)
                self.update_display()
            except:
                messagebox.showerror("Error", "Input tidak valid!")
    
    def reciprocal(self):
        if self.current_number:
            try:
                number = float(self.current_number)
                if number == 0:
                    messagebox.showerror("Error", "Tidak bisa menghitung 1/0!")
                    return
                
                result = 1 / number
                if result.is_integer():
                    self.current_number = str(int(result))
                else:
                    self.current_number = str(result)
                self.update_display()
            except:
                messagebox.showerror("Error", "Input tidak valid!")
    
    def backspace(self):
        if self.current_number:
            self.current_number = self.current_number[:-1]
            if not self.current_number:
                self.current_number = "0"
            self.update_display()
    
    def update_display(self):
        if not self.current_number:
            self.display_var.set("0")
        else:
            self.display_var.set(self.current_number)

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
