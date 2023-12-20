import tkinter as tk
from tkinter import messagebox

from _cffi_backend import callback

class WumpusWorldApp:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback  # Callback function to handle button click
        master.title("Wumpus World")

        # Define custom fonts
        self.title_font = ("Arial", 16, "bold")
        self.button_font = ("Arial", 12)

        # Create and pack the title label
        self.title_label = tk.Label(master, text="Wumpus World", font=self.title_font)
        self.title_label.pack(pady=10)

        # Create buttons for each input
        for input in range(1, 5):
            button_text = f"{input}. Input {input}"
            input_button = tk.Button(master, text=button_text, command=lambda l=input: self.on_input_click(l),
                                     font=self.button_font)
            input_button.pack(pady=5)
        self.selected_input = None  # Initialize selected_input to None

    def on_input_click(self, input):
        self.selected_input = input
        self.callback(self.selected_input)

    def clearscreen(self):
        # Destroy all widgets in the first screen
        for widget in self.master.winfo_children():
            widget.destroy()