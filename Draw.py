import tkinter as tk
from tkinter import PhotoImage, messagebox

from _cffi_backend import callback

def getKnowledgeboard(knowledge,world,min_x,max_x,min_y,max_y):
    
    # Initialize the board as a list of lists
    board = [[None for _ in range(max_y - min_y)] for _ in range(max_x - min_x)]

    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            if i in range(0, 21) and j in range(0, 21):
                # Populate the board with values from the knowledge array
                board[i - min_x][j - min_y] = knowledge[i][j]

    return board
def convertKnowledge(KnowledgeCell):
    if KnowledgeCell.hasPit == True and KnowledgeCell.hasWumpus == True:
        return "Pit & Wumpus"
    elif KnowledgeCell.hasPit == True:
        return "Pit"
    elif KnowledgeCell.hasWumpus == True:
        return "Wump"
    elif KnowledgeCell.hasPit == None and KnowledgeCell.hasWumpus == None:
        return "?"
    elif KnowledgeCell.hasPit == False and KnowledgeCell.hasWumpus == False:
        return "Safe"
    elif KnowledgeCell.hasPit == False and KnowledgeCell.hasWumpus == None:
        return "Pit-"
    elif KnowledgeCell.hasPit == None and KnowledgeCell.hasWumpus == False:
        return "Wum-"
    elif KnowledgeCell.hasVisited == True: 
        return "Visited"
    else:
        return "-"

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
        master.geometry(f"{image_width}x{image_height*2}")

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
        for input in range(1, 6):
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

class KnowledgeBoard:
    def __init__(self, master, knowledge,world,agent,min_x,max_x,min_y,max_y, cell_size=60, offset_x=30, offset_y=30):
        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y  
        self.score_label = tk.Label(master, text="Score: 0", font=("Arial", 16))
        self.score_label.pack()
        self.action_label = tk.Label(master, text="Action: ", font=("Arial", 16))
        self.action_label.pack()
        self.move=0#0:move,1:shoot
        self.update_knowledge(knowledge,world,agent,self.move)
        
    def update_knowledge(self, knowledge,world,agent,move):
        self.move= move
        num_rows = world.n
        num_cols = world.n

        canvas_width = num_cols * self.cell_size + 2 * self.offset_x
        canvas_height = num_rows * self.cell_size + 2 * self.offset_y
        
        self.canvas.config(width=canvas_width, height=canvas_height)
        self.canvas.delete("all")
        board=getKnowledgeboard(knowledge,world,self.min_x,self.max_x,self.min_y,self.max_y)
        for i in range(len(board)):
            for j in range(len(board[i])):
                cell_x = self.offset_x + j * self.cell_size
                cell_y = self.offset_y + i * self.cell_size
                reversed_i = num_rows - 1 - i
                cell_content = board[reversed_i][j].visited
                cell_content_1 = convertKnowledge(board[reversed_i][j])
                self.canvas.create_rectangle(
                    cell_x, cell_y, cell_x + self.cell_size, cell_y + self.cell_size, outline="black"
                )
                if [reversed_i, j] == world.agent:
                    text = "A"
                    text_color = "red"
                elif cell_content == True:
                    if(board[reversed_i][j].content!=""):
                        text = str(board[reversed_i][j].content)
                    else:
                        text = str("")
                    text_color = "black"
                else:
                    text = str(cell_content_1)
                    text_color = "black"
                #text = "A" if [reversed_i, j] == world.agent else str(cell_content_1)
                self.canvas.create_text(
                    cell_x + self.cell_size // 2, cell_y + self.cell_size // 2,
                    text=text, font=("Arial", 13),fill=text_color
                )
        self.score_label.config(text=f"Score: {agent.score}")
        if move == 0:
            self.action_label.config(text=f"Action: Move")
        else:
            self.action_label.config(text=f"Action: Shoot")
