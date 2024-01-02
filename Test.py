from Draw import WumpusWorldApp
import tkinter as tk
from tkinter import messagebox
from World import World
from Agent import Agent
# if __name__ == '__main__':
#     def startworld(selected_input):
#         world = World(f"input{selected_input}.txt")
        
#     root = tk.Tk()
#     app = WumpusWorldApp(root, startworld)
#     root.mainloop()

world = World("input1.txt")
agent = Agent(world=world)

world.printWorld()

while world.agent is not None:
    if agent.moveToward() == False:
        if agent.moveTowardShoot() == False:
            agent.exit()
    