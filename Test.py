import queue
from Draw import WumpusWorldApp,KnowledgeBoard
import tkinter as tk
from tkinter import messagebox
from World import World
from Agent import Agent
import pygame

def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("scream.wav")  # Replace with the path to your sound file
    pygame.mixer.music.play()

def schedule_sound_playback():
    root.after(0, play_sound) 
def moveToward(agent,world,knowledge_board,min_x,max_x,min_y,max_y):
    move = 0
    newPos, path = agent.findUnvisitedCell(killWUmpus = False)
    if newPos is None:
        return False

    q = queue.LifoQueue()
    while newPos != agent.pos:
        q.put(newPos)
        newPos = path[newPos[0]][newPos[1]]

    while q.qsize() > 0:
        next = q.get()
        nextMove = (next[0] - agent.pos[0], next[1] - agent.pos[1])
        knowledge_board.update_knowledge(agent.knowledge,world,agent,move)
        agent.move(nextMove)
        for i in range(min_x, max_x):
                for j in range(min_y, max_y):
                    if i in range(0, 21) and j in range(0, 21):
                        print(agent.knowledge[i][j].content, end=' ')
                print()
        app.master.update()
        app.master.after(1000)
        print("Now at:", agent.pos, " Score:", agent.score)
        agent.world.printWorld()
        
        return True
def moveTowardShoot(agent,world,knowledge_board,min_x,max_x,min_y,max_y):
    move = 0
    newPos, path = agent.findUnvisitedCell(killWUmpus = True)
    if newPos is None:
        return False
        
    q = queue.LifoQueue()
    while newPos != agent.pos:
        q.put(newPos)
        newPos = path[newPos[0]][newPos[1]]
    while q.qsize() > 0:
        next = q.get()
        nextMove = (next[0] - agent.pos[0], next[1] - agent.pos[1])
        if q.qsize() == 0:
            move = 1
            print("Shoot at:", next)
            knowledge_board.update_knowledge(agent.knowledge,world,agent,move)
            play_sound()
            app.master.update()
            app.master.after(1000)
            agent.shoot(nextMove)
            move = 0
        knowledge_board.update_knowledge(agent.knowledge,world,agent,move)
        app.master.update()
        app.master.after(1000)
        agent.move(nextMove)
        
        print("Now at:", agent.pos, " Score:", agent.score)
        agent.world.printWorld()

    return True        
def exit(agent,world,knowledge_board,min_x,max_x,min_y,max_y):
    move = 0
    newPos, path = agent.findUnvisitedCell(killWUmpus = False, exit = True)
    if newPos is None:
        return False
        
    q = queue.LifoQueue()
    while newPos != agent.pos:
        q.put(newPos)
        newPos = path[newPos[0]][newPos[1]]
            
    while q.qsize() > 0:
        next = q.get()
        nextMove = (next[0] - agent.pos[0], next[1] - agent.pos[1])
        knowledge_board.update_knowledge(agent.knowledge,world,agent,move)
        agent.move(nextMove)
        app.master.update()
        app.master.after(1000)
        if agent.world.agent is not None:
            print("Now at:", agent.pos, " Score:", agent.score)
        else:
            tk.messagebox.showinfo("Exit the map", "Score: "+str(agent.score)+"\n"+"Exit the map")
            move = 2
            knowledge_board.update_knowledge(agent.knowledge,world,agent,move)
            app.master.update()
            app.master.after(1000)
            print("Exit!")
        agent.world.printWorld()
            
    print("Exited with score:", agent.score)

    return True
if __name__ == '__main__':
    def startworld(selected_input):
        app.clearscreen()
        world = World(f"input{selected_input}.txt")
        agent = Agent(world=world)

        # Create the Tkinter window
        min_x = 10-world.agent[0]
        min_y = 10-world.agent[1]
        max_x = 10-world.agent[0]+world.n
        max_y = 10-world.agent[1]+world.n
        # Create an instance of KnowledgeBoard
        knowledge_board = KnowledgeBoard(root, knowledge=agent.knowledge,world=world,agent=agent,min_x=min_x,max_x=max_x,min_y=min_y,max_y=max_y)
        root.geometry(f"{800}x{800}")
        world.printWorld()
        
        while world.agent is not None:
            # Print the knowledge board
            for i in range(min_x, max_x):
                for j in range(min_y, max_y):
                    if i in range(0, 21) and j in range(0, 21):
                        print(agent.knowledge[i][j].content, end=' ')
                print()
            if moveToward(agent,world, knowledge_board,min_x,max_x,min_y,max_y) == False:
                if moveTowardShoot(agent,world,knowledge_board,min_x,max_x,min_y,max_y) == False:
                    exit(agent,world,knowledge_board,min_x,max_x,min_y,max_y)

        # Start the Tkinter event loop
        root.mainloop()

    # Create the Tkinter window for the WumpusWorldApp
    root = tk.Tk()
    app = WumpusWorldApp(root, startworld)

    # Start the Tkinter event loop
    root.mainloop()
"""
world = World("input1.txt")
agent = Agent(world=world)

world.printWorld()

while world.agent is not None:
    agent.printXYKnowledge(12, 10)
    if agent.moveToward() == False:
        if agent.moveTowardShoot() == False:
            agent.exit()
"""    