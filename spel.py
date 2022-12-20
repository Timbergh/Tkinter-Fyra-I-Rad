from tkinter import *
from tkinter import messagebox
import time

root = Tk()
root.title("Fyra I Rad")

bluesTurn = True

rundor = 0
vinst = False

clickTime = 0
cooldown = 0.4

filled = {}
canvasCirlce = {}

rows = 6
cols = 7

def restart_game():
    global bluesTurn
    global rundor
    global vinst
    global filled
    global canvasCirlce

    bluesTurn = True
    rundor = 0
    vinst = False
    filled = {(i, j): False for i in range(rows) for j in range(cols)}
    canvasCirlce = {(i, j): (canvasCirlce[(i, j)][0], canvasCirlce[(i, j)][0].create_oval(5, 5, 50, 50, fill="white")) for i in range(rows) for j in range(cols)}
    for (i, j) in canvasCirlce:
        canvasCirlce[(i, j)][0].tag_bind(canvasCirlce[(i, j)][1], "<Button-1>", lambda event, i=i, j=j: clickCircle(event, i, j, canvasCirlce))
   
for i in range(rows):
    for j in range(cols):
        canvas = Canvas(root, width=50, height=50, bg="SystemButtonFace")
        canvas.grid(row=i, column=j)

        circle = canvas.create_oval(5, 5, 50, 50, fill="white")
        filled[(i, j)] = False
        canvasCirlce[(i, j)] = (canvas, circle)
        canvas.tag_bind(circle, "<Button-1>", lambda event, i=i, j=j: clickCircle(event, i, j, canvasCirlce))

def update_dimensions(new_rows, new_cols):
    global rows
    global cols
    rows = new_rows
    cols = new_cols

def dimensions(rows, cols):
    global canvasCirlce
    global filled
    global rundor
    
    if rundor == 0:
        update_dimensions(rows, cols)
        # Destroy existing canvas objects
        for (i, j) in canvasCirlce:
            canvasCirlce[(i, j)][0].destroy()

        # Clear the canvasCirlce and filled dictionaries
        canvasCirlce.clear()
        filled.clear()
        
        # Create new widgets with the desired number of rows and columns
        for i in range(rows):
            for j in range(cols):
                canvas = Canvas(root, width=50, height=50, bg="SystemButtonFace")
                canvas.grid(row=i, column=j)

                circle = canvas.create_oval(5, 5, 50, 50, fill="white")
                filled[(i, j)] = False
                canvasCirlce[(i, j)] = (canvas, circle)
                canvas.tag_bind(circle, "<Button-1>", lambda event, i=i, j=j: clickCircle(event, i, j, canvasCirlce))

def check_win(color):
    global rows
    global cols
    # Check rows
    for i in range(rows):
        for j in range(cols - 3):
            if canvasCirlce[(i, j)][0].itemcget(canvasCirlce[(i, j)][1], "fill") == color and canvasCirlce[(i, j+1)][0].itemcget(canvasCirlce[(i, j+1)][1], "fill") == color and canvasCirlce[(i, j+2)][0].itemcget(canvasCirlce[(i, j+2)][1], "fill") == color and canvasCirlce[(i, j+3)][0].itemcget(canvasCirlce[(i, j+3)][1], "fill") == color:
                return True
    
    # Check columns
    for i in range(rows - 3):
        for j in range(cols):
            if canvasCirlce[(i, j)][0].itemcget(canvasCirlce[(i, j)][1], "fill") == color and canvasCirlce[(i+1, j)][0].itemcget(canvasCirlce[(i+1, j)][1], "fill") == color and canvasCirlce[(i+2, j)][0].itemcget(canvasCirlce[(i+2, j)][1], "fill") == color and canvasCirlce[(i+3, j)][0].itemcget(canvasCirlce[(i+3, j)][1], "fill") == color:
                return True
    
    # Check diagonal
    for i in range(rows - 3):
        for j in range(cols - 3):
            if canvasCirlce[(i, j)][0].itemcget(canvasCirlce[(i, j)][1], "fill") == color and canvasCirlce[(i+1, j+1)][0].itemcget(canvasCirlce[(i+1, j+1)][1], "fill") == color and canvasCirlce[(i+2, j+2)][0].itemcget(canvasCirlce[(i+2, j+2)][1], "fill") == color and canvasCirlce[(i+3, j+3)][0].itemcget(canvasCirlce[(i+3, j+3)][1], "fill") == color:
                return True
            if canvasCirlce[(i, j+3)][0].itemcget(canvasCirlce[(i, j+3)][1], "fill") == color and canvasCirlce[(i+1, j+2)][0].itemcget(canvasCirlce[(i+1, j+2)][1], "fill") == color and canvasCirlce[(i+2, j+2)][0].itemcget(canvasCirlce[(i+2, j+1)][1], "fill") == color and canvasCirlce[(i+3, j)][0].itemcget(canvasCirlce[(i+3, j)][1], "fill") == color:
                return True
    
    return False

def animate_circle(row, column, color):
    # Animera cirkeln
    for i in range(row):
        canvasCirlce[(i, column)][0].itemconfig(canvasCirlce[(i, column)][1], fill=color)
        root.update()
        time.sleep(0.01)
        canvasCirlce[(i, column)][0].itemconfig(canvasCirlce[(i, column)][1], fill="white")
        root.update()
        time.sleep(0.01)

def clickCircle(event, i, j, canvasCirlce):
    global vinst, color, bluesTurn, rundor, clickTime, cooldown, rows, cols

    # Väntar lite innan man kan göra nästa drag
    timeSinceLastClick = time.time() - clickTime

    if timeSinceLastClick < cooldown:
        return

    clickTime = time.time()
    
    # Hitta den första tomma cirkeln i collumnen du klickar på
    for i in range(rows-1, -1, -1):
        if not filled[(i, j)] and not vinst:
            # skapa en ny cirkel där
            if bluesTurn:
                color = "blue"
                bluesTurn = False
            else:
                color = "red"
                bluesTurn = True
            animate_circle(i, j, color)
            filled[(i, j)] = True
            new_circle = canvasCirlce[(i, j)][0].create_oval(5, 5, 50, 50, fill=color)
            rundor += 1
            canvasCirlce[(i, j)] = (canvasCirlce[(i, j)][0], new_circle)
            break
    if check_win(color) and not vinst:
        vinst = True
        messagebox.showinfo("Vinst", f"{color} vann!")
    elif rundor == rows*cols:
        messagebox.showinfo("Vinst?", "Lika!")
    
menu = Menu(root)
root.config(menu=menu)
gameMenu = Menu(menu)
menu.add_cascade(label="Game", menu=gameMenu)
gameMenu.add_separator()
gameMenu.add_command(label="Restart", command=restart_game)
gameMenu.add_command(label="Exit", command=root.quit)
dimMenu = Menu(menu)
menu.add_cascade(label="Dimensions", menu=dimMenu)
dimMenu.add_command(label="4x5", command=lambda: dimensions(4, 5))
dimMenu.add_command(label="5x6", command=lambda: dimensions(5, 6))
dimMenu.add_command(label="6x7 - Default", command=lambda: dimensions(6, 7))
dimMenu.add_command(label="7x8", command=lambda: dimensions(7, 8))
dimMenu.add_command(label="7x9", command=lambda: dimensions(7, 9))
dimMenu.add_command(label="8x8", command=lambda: dimensions(8, 8))
dimMenu.add_command(label="7x10", command=lambda: dimensions(7, 10))
root.mainloop()