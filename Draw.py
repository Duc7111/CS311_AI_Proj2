import tkinter as tk
from tkinter import PhotoImage, messagebox

from _cffi_backend import callback

class WumpusWorldApp:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback  # Callback function to handle button click
        master.title("Wumpus World")

        # Load the background image
        self.background_image = PhotoImage(file="theme.png")
        image_width = self.background_image.width()
        image_height = self.background_image.height()

        # Set the size of the main window based on the image size
        master.geometry(f"{image_width}x{image_height}")

        # Create a label to display the background image
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)  # Make the label cover the entire window

        # Create and pack the title label
        self.title_font = ("Arial", 16, "bold")
        self.title_label = tk.Label(master, text="Wumpus World", font=self.title_font, bg='white')  # Set background color if needed
        self.title_label.pack(pady=10)

        # Define custom fonts
        self.button_font = ("Arial", 12)

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